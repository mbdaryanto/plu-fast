from typing import Optional
import strawberry
from strawberry.types import Info
from sqlalchemy import select, desc, and_, or_

from ..db import Session
from ..schema import Item


@strawberry.type(name='Item')
class ItemType:
    id: strawberry.ID
    code: str
    barcode: Optional[str]
    name: str
    normal_price: str
    discounted_price: str


@strawberry.type
class Query():
    @strawberry.field
    def plu(self, barcode: str, info: Info) -> ItemType:

        session: Session = info.context['session']
        item: Optional[Item] = session.execute(
            select(Item).where(
                and_(
                    Item.Aktif == 'Ya',
                    or_(
                        Item.Kode == barcode,
                        Item.Barcode == barcode,
                    ),
                )
            ).order_by(
                # diprioritaskan yang barcode-nya sama
                desc(Item.Barcode == barcode)
            ).limit(1)
        ).scalar_one_or_none()

        if item is None:
            raise ValueError(
                "Barang dengan kode/barcode {!r} tidak ditemukan".format(barcode)
            )

        if item.Aktif == 'Tidak':
            raise ValueError(
                "Barang dengan kode/barcode {!r} tidak aktif".format(barcode)
            )

        return ItemType(
            id=strawberry.ID(str(item.IDItem)),
            code=item.Kode,
            barcode=item.Barcode,
            name=item.Nama,
            normal_price=item.HargaNormal,
            discounted_price=item.HargaJual,
        )

schema = strawberry.Schema(query=Query)
