from datetime import date
from typing import Optional, List
import strawberry
from strawberry.types import Info
from sqlalchemy import select, desc, and_, or_

from ..db import Session
from ..schema import Item, ItemHarga, ItemHargaD, ItemHargaGrosir


@strawberry.type
class BulkPrice:
    id: strawberry.ID
    quantity: int
    unit_price: float


@strawberry.type
class PromoPrice:
    id: strawberry.ID
    promo_code: str
    promo_name: str
    start: date
    end: date
    discount_percent: float
    discount: float
    unit_price: float


@strawberry.type(name='Item')
class ItemType:
    id: strawberry.ID
    code: str
    barcode: Optional[str]
    name: str
    normal_price: float
    discounted_price: float

    @strawberry.field
    def bulk_prices(self, info: Info) -> List[BulkPrice]:
        item_id = int(self.id)
        session: Session = info.context['session']
        rows: List[ItemHargaGrosir] = session.execute(
            select(ItemHargaGrosir).where(
                and_(
                    ItemHargaGrosir.IDItem == item_id,
                    ItemHargaGrosir.Aktif == 'Ya',
                )
            ).order_by(
                ItemHargaGrosir.Jumlah
            )
        ).scalars().all()

        return [
            BulkPrice(
                id=strawberry.ID(row.IDItemHargaGrosir),
                quantity=int(row.Jumlah),
                unit_price=row.Harga,
            )
            for row in rows
        ]

    @strawberry.field
    def promo_prices(self, info: Info) -> List[PromoPrice]:
        item_id = int(self.id)
        session: Session = info.context['session']
        rows = session.execute(
            select(
                ItemHargaD.IDItemHargaD,
                ItemHarga.Kode,
                ItemHarga.Nama,
                ItemHarga.TanggalAwal,
                ItemHarga.TanggalAkhir,
                ItemHargaD.DiskonPersen,
                ItemHargaD.Diskon,
                ItemHargaD.HargaJual,
            ).join_from(
                ItemHarga,
                ItemHargaD,
                ItemHarga.IDItemHargaH == ItemHargaD.IDItemHargaH,
            ).where(
                and_(
                    ItemHargaD.IDItem == item_id,
                    ItemHarga.Aktif == 'Ya',
                    ItemHarga.TanggalAwal <= date.today(),
                    ItemHarga.TanggalAkhir >= date.today(),
                )
            )
        ).all()

        return [
            PromoPrice(
                id=strawberry.ID(row.IDItemHargaD),
                promo_code=row.Kode,
                promo_name=row.Nama,
                start=row.TanggalAwal,
                end=row.TanggalAkhir,
                discount_percent=row.DiskonPersen,
                discount=row.Diskon,
                unit_price=row.HargaJual,
            )
            for row in rows
        ]


@strawberry.type
class Query():
    @strawberry.field
    def plu(self, barcode: str, info: Info) -> ItemType:
        session: Session = info.context['session']
        item: Optional[Item] = session.execute(
            select(Item).where(
                or_(
                    Item.Kode == barcode,
                    Item.Barcode == barcode,
                ),
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

    @strawberry.field
    def item(self, id: strawberry.ID, info: Info) -> ItemType:
        session: Session = info.context['session']
        item: Optional[Item] = session.execute(
            select(Item).where(
                Item.IDItem == int(id),
            )
        ).scalar_one_or_none()

        if item is None:
            raise ValueError(
                "Item with id {!r} not found".format(id)
            )

        if item.Aktif == 'Tidak':
            raise ValueError(
                "Item with id {!r} is inactive".format(id)
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
