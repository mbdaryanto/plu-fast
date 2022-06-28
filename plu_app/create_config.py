from rich.prompt import IntPrompt, Prompt, Confirm
from rich.console import Console
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import OperationalError
from .settings import Settings


def create_config():
    console = Console()
    settings = Settings()
    console.print('Change Settings [old values], blank = keep old values')

    if not settings.secret_key:
        settings.generate_secret_key()

    console.print('Setting database connection')

    settings.db_host = Prompt.ask('host', console=console, default=settings.db_host)
    settings.db_port = IntPrompt.ask('port', console=console, default=settings.db_port)
    settings.db_database = Prompt.ask('database', console=console, default=settings.db_database)
    settings.db_user = Prompt.ask('user', console=console, default=settings.db_user)
    settings.set_password(
        Prompt.ask(
            'password',
            console=console,
            default='' if not settings.db_password else settings.get_password(),
            show_default=False,
            password=True,
        )
    )

    if Confirm.ask('Test connection', console=console, default=True):
        db_url = settings.get_db_url()
        engine = create_engine(db_url)
        try:
            try_con = engine.connect()
            print('Connection success!')
            try_con.close()
        except OperationalError:
            print('Connection failed!')

    console.print('Create settings and save to: {}'.format(settings.Config.env_file))
    settings.save()


if __name__ == '__main__':
    create_config()
