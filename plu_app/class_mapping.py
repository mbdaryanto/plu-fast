from typing import Optional, Dict

# defining class_mapping
# using dictionary str? -> str -> str
# for default schema use None: { 'table_name', 'OrmClassName' }
# for other schema use 'other_schema': { 'table_name', 'OrmClassName' }

class_mapping: Dict[Optional[str], Dict[str, str]] = {
    None: {
        'mitem': 'Item',
        'mitemtree': 'ItemTree',
        'titemhargah': 'ItemHarga',
        'titemhargad': 'ItemHargaD',
    },
}
