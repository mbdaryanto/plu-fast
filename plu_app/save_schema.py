import re
import keyword
import logging
from pathlib import Path
from typing import Optional, Dict
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Float, Numeric, Enum, DateTime, Date, Time, Text, Index, inspect
from sqlalchemy.types import _Binary
from sqlalchemy.dialects import mysql
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.sql.schema import DefaultClause
from rich.progress import Progress, BarColumn
from .settings import get_settings
from .class_mapping import class_mapping


INDENTATION = ' ' * 4
OUTPUT_SCHEMA_FILENAME = 'schema.py'
# put the python keyword in here as it is an invalid identifier
# every generated identifier in this set will be appended with _
INVALID_IDENTIFIER = set(keyword.kwlist)

logger = logging.getLogger('save_schema')
logging.basicConfig(level=logging.NOTSET)
string_pattern = re.compile(r"^'[^']*'$")


def main():
    # output_filename = join(dirname(dirname(abspath(__file__))), OUTPUT_SCHEMA_FILENAME)
    output_file = Path(__file__).parent / OUTPUT_SCHEMA_FILENAME

    with Progress(
        '{task.description}',
        BarColumn(),
        '{task.completed} of {task.total}',
    ) as progress, output_file.open('wt') as output:
        table_task = progress.add_task('Generate Schema', start=False)
        engine = create_engine(get_settings().get_db_url())
        metadata = MetaData()
        insp = inspect(engine)
        # use this line
        # metadata.reflect(bind=engine)
        # controlled reflection
        # list ORM class names, table names, schema

        for schema_name, tables in class_mapping.items():
            for table_name, class_name in tables.items():
                if insp.has_table(table_name, schema_name):
                    Table(table_name, metadata, schema=schema_name, autoload_with=engine)
                else:
                    progress.console.print(
                        '[red]Table [bold]{}[/bold] not found.[/red]'.format(
                            table_name if schema_name is None else '.'.join([schema_name, table_name])
                        )
                    )

        tables = list(metadata.sorted_tables)

        # schema headers
        output.write(
            '## GENERATED CODE - DO NOT MODIFY BY HAND\n'
            '\n'
            'import sqlalchemy as sa\n'
            # 'import sqlalchemy.schema as sas\n'
            'from sqlalchemy.dialects import mysql\n'
            'from sqlalchemy.orm import declarative_base\n'
            '\n'
            '\n'
            'convention = {\n'
            '    "ix": "Idx_%(column_0_label)s",\n'
            '    "uq": "Idx_%(table_name)s_%(column_0_name)s",\n'
            '    "fk": "FK_%(table_name)s_%(column_0_name)s",\n'
            '}\n'
            '\n'
            'metadata = sa.MetaData(naming_convention=convention)\n'
            'Base = declarative_base(metadata=metadata)\n'
        )

        progress.update(table_task, total=len(tables))
        progress.start_task(table_task)

        for table in tables:
            progress.console.print('Reflecting [bold]{}[/bold]...'.format(table.name))
            progress.advance(table_task)
            write_schema(output, table, class_mapping, progress.console)

        progress.stop_task(table_task)


def write_schema(output, table: Table, class_mapping: Dict[Optional[str], Dict[str, str]], console):
    """
    create an sqlalchemy declarative table source code by using reflect/inspect
    :param output: file-like output source
    :param table: table to reflect
    :param console: for progress
    :return: None
    """
    if table.name in class_mapping[table.schema]:
        class_name = class_mapping[table.schema][table.name]
    else:
        class_name = table.name.title()

    output.write('\n\nclass {}(Base):\n'.format(class_name))
    output.write('{}__tablename__ = \'{}\'\n\n'.format(INDENTATION, table.name))

    for column in table.columns:
        assert isinstance(column, Column)
        output.write('{}{}\n'.format(INDENTATION, column_schema(column, console)))

    has_constraints: bool = False
    has_table_args: bool = False
    # indentation: str = INDENTATION
    foreign_keys_name = set()

    def constraints_separator():
        nonlocal has_constraints
        # nonlocal indentation
        if not has_constraints:
            has_constraints = True
            output.write('\n')

    # for FK constraints of composed columns
    # put it in __table_args__ tuple
    for fk in table.foreign_key_constraints:
        foreign_keys_name.add(fk.name)
        if len(fk.column_keys) > 1:
            if fk.ondelete and fk.ondelete != 'RESTRICT':
                ondelete = ', ondelete={!r}'.format(fk.ondelete)
            else:
                ondelete = ''

            if fk.onupdate and fk.onupdate != 'RESTRICT':
                onupdate = ', onupdate={!r}'.format(fk.ondelete)
            else:
                onupdate = ''

            col_targets = [
                (col.name, get_target(col.foreign_keys, fk.name),)
                for col in fk.columns
            ]

            constraints_separator()

            if not has_table_args:
                output.write('{}__table_args__ = (\n'.format(INDENTATION))
                has_table_args = True

            # if prefered with name
            output.write('{}sa.ForeignKeyConstraint([{}], [{}], name={!r}{}{}),\n'.format(
                INDENTATION * 2,
                ', '.join([repr(col) for col, target in col_targets]),
                ', '.join([repr(target) for col, target in col_targets]),
                fk.name,
                onupdate,
                ondelete,
            ))

    # other args such as schema
    if table.schema is not None:
        constraints_separator()
        if not has_table_args:
            output.write('{}__table_args__ = (\n'.format(INDENTATION))
            has_table_args = True
        output.write('{}{{\'schema\': \'{}\'}}\n'.format(
            INDENTATION * 2,
            table.schema
        ))

    # closing table_args
    if has_table_args:
        output.write('{})\n'.format(INDENTATION))

    for idx in table.indexes:
        if isinstance(idx, Index):
            if idx.unique:
                constraints_separator()
                output.write('{}sa.UniqueConstraint({}, name={!r})\n'.format(
                    INDENTATION,
                    ', '.join([repr(col.name) for col in idx.columns]),
                    idx.name,
                ))
            # if it's not foreign key index
            elif idx.name not in foreign_keys_name:
                if idx.name.startswith('FK_'):
                    logger.debug('index %s not in (%s)', idx.name, ','.join(foreign_keys_name))
                constraints_separator()
                output.write('{}sa.Index({!r}, {})\n'.format(
                    INDENTATION,
                    idx.name,
                    ', '.join([repr(col.name) for col in idx.columns]),
                ))
        else:
            raise Exception('Unexpected type {!r}'.format(idx))


def column_schema(column: Column, console) -> str:
    """
    Convert column schema to sqlalchemy declarative column
    :param column: the column
    :param console: console for output
    :return: string python source for declarative column
    """
    col_type_format = "{} = sa.Column({})"

    col_name = column.name

    col_types = []

    if col_name in INVALID_IDENTIFIER:
        col_types.append(repr(col_name))
        col_name = col_name + '_'

    if isinstance(column.type, Enum):
        col_types.append('sa.Enum({})'.format(', '.join(map(repr, column.type.enums))))
    elif isinstance(column.type, mysql.SET):
        col_types.append('mysql.SET({})'.format(', '.join(map(repr, column.type.values))))
    elif isinstance(column.type, Text):
        col_types.append('sa.Text')
    elif isinstance(column.type, String):
        if hasattr(column.type, 'length'):
            col_types.append('sa.String({})'.format(column.type.length))
        else:
            col_types.append('sa.String')
    elif isinstance(column.type, Integer):
        if isinstance(column.type, mysql.TINYINT) or isinstance(column.type, mysql.BIT):
            col_types.append('sa.Boolean')
        elif isinstance(column.type, mysql.INTEGER) and column.type.unsigned:
            col_types.append('mysql.INTEGER(unsigned=True)')
        else:
            col_types.append('sa.Integer')
    elif isinstance(column.type, Boolean) or isinstance(column.type, mysql.BIT):
        col_types.append('sa.Boolean')
    elif isinstance(column.type, Date):
        col_types.append('sa.Date')
    elif isinstance(column.type, DateTime):
        col_types.append('sa.DateTime')
    elif isinstance(column.type, Time):
        col_types.append('sa.Time')
    elif isinstance(column.type, Float):
        col_types.append('sa.Float')
    elif isinstance(column.type, Numeric):
        col_types.append('sa.Numeric({}, {})'.format(column.type.precision, column.type.scale))
    elif isinstance(column.type, mysql.MEDIUMBLOB):
        col_types.append('mysql.MEDIUMBLOB')
    elif isinstance(column.type, _Binary):
        col_types.append('sa.LargeBinary({})'.format(column.type.length))
    else:
        col_types.append(str(column.type))

    if isinstance(column.foreign_keys, set):
        # if the column is a composite/compound keys
        for fk in column.foreign_keys:
            if len(fk.constraint.column_keys) == 1:
                if isinstance(fk.column, str):
                    target = fk.column
                elif isinstance(fk.column, Column):
                    if fk.column.table.schema is None:
                        target = '{}.{}'.format(fk.column.table.name, fk.column.name)
                    else:
                        target = '{}.{}.{}'.format(fk.column.table.schema, fk.column.table.name, fk.column.name)
                else:
                    raise ValueError('No target on foreign key {!s}'.format(fk))

                if fk.ondelete is not None and fk.ondelete != 'RESTRICT':
                    ondelete = ', ondelete={!r}'.format(fk.ondelete)
                else:
                    ondelete = ''

                if fk.onupdate is not None and fk.onupdate != 'RESTRICT':
                    onupdate = ', onupdate={!r}'.format(fk.onupdate)
                else:
                    onupdate = ''

                # if prefered without name
                col_types.append(
                    'sa.ForeignKey({!r}{}{})'.format(
                        target, ondelete, onupdate
                    )
                )

    if column.primary_key:
        col_types.append('primary_key=True')
    elif not column.nullable:
        col_types.append('nullable=False')

    if isinstance(column.server_default, DefaultClause):
        if isinstance(column.server_default.arg, str):
            col_types.append('server_default={!r}'.format(column.server_default.arg))
        if isinstance(column.server_default.arg, TextClause):
            if string_pattern.match(column.server_default.arg.text):
                col_types.append('server_default={}'.format(column.server_default.arg.text))
            else:
                col_types.append('server_default=sa.text({!r})'.format(column.server_default.arg.text))
        else:
            console.print('Unknown column.server_default.arg in column {} {!r}'.format(column.name, column.server_default.arg))

        # if column.server_default.for_update:
        #     if isinstance(column.server_default.for_update.arg, str):
        #         col_types.append('server_onupdate={!r}'.format(column.server_default.arg))
        #     elif isinstance(column.server_default.for_update.arg, TextClause):
        #         col_types.append('server_default=sa.text({!r})'.format(column.server_default.arg.text))
        #     else:
        #         console.print('Unknown column.server_default.for_update in column {} {!r}'.format(
        #             column.name,
        #             column.server_default.for_update
        #         ))

    return col_type_format.format(
        col_name,
        ', '.join(col_types),
    )


def get_target(foreign_keys, fk_name) -> str:
    """
    find the target column in foreign key, to map composite FK
    :param foreign_keys: foreign key object
    :param fk_name: foreign key identifier
    :return: reference column name
    """
    fk = next(filter(lambda item: item.name == fk_name, foreign_keys))
    if isinstance(fk.column, str):
        return fk.column
    elif isinstance(fk.column, Column):
        return '{}.{}'.format(fk.column.table.name, fk.column.name)
    raise Exception('confused figuring FK {}'.format(fk_name))


if __name__ == '__main__':
    main()
