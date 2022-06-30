from datetime import date
from typing import Optional, List
from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, constr, parse_obj_as
from sqlalchemy import and_, select, or_, desc
from ..db import Session, get_session
from ..schema import Item, ItemHarga, ItemHargaD, ItemHargaGrosir


router = APIRouter(
    prefix='/item',
    tags=['item']
)

class YaTidakEnum(str, Enum):
    ya = 'Ya'
    tidak = 'Tidak'


class ItemModel(BaseModel):
    IDItem: int
    Kode: constr(max_length=20)
    Nama: Optional[constr(max_length=255)] = None
    Singkatan: Optional[constr(max_length=20)] = None
    Barcode: Optional[constr(max_length=20)] = None
    KodePabrik: Optional[constr(max_length=30)] = None
    JumlahDos: Optional[float] = 0.0
    Satuan: Optional[constr(max_length=10)] = None
    HargaNormal: float = 0.0
    HargaJual: Optional[float] = 0.0

    class Config:
        orm_mode = True


class ItemHargaGrosirModel(BaseModel):
    IDItemHargaGrosir: int
    IDItem: int
    Jumlah: float = 0.0
    Harga: float = 0.0
    IsDos: YaTidakEnum

    class Config:
        orm_mode = True


class ItemHargaPromoModel(BaseModel):
    IDItemHargaD: int
    IDItemHargaH: int
    IDItem: int
    Kode: constr(max_length=30)
    Nama: constr(max_length=50)
    TanggalAwal: date
    TanggalAkhir: date
    Keterangan: Optional[str] = None
    HargaJual: float = 0.0
    DiskonPersen: float = 0.0
    Diskon: float = 0.0

    class Config:
        orm_mode = True


class PluModel(BaseModel):
    item: ItemModel
    hargaGrosir: List[ItemHargaGrosirModel] = []
    hargaPromo: List[ItemHargaPromoModel] = []


@router.get('', response_model=PluModel)
async def get_item(
    code: constr(max_length=20),
    session: Session = Depends(get_session),
):
    """
    Get Item by Kode/Barcode, returning Item information and price
    """
    item: Optional[Item] = session.execute(
        select(Item).where(
            or_(
                Item.Kode == code,
                Item.Barcode == code,
            )
        ).order_by(
            # diprioritaskan yang barcode-nya sama
            desc(Item.Barcode == code)
        ).limit(1)
    ).scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Barang dengan kode/barcode {!r} tidak ditemukan".format(code)
        )

    if item.Aktif == 'Tidak':
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Barang dengan kode/barcode {!r} tidak aktif".format(code)
        )

    # mencari harga grosir untuk item ini
    hargaGrosirs: List[ItemHargaGrosir] = session.execute(
        select(ItemHargaGrosir).where(
            and_(
                ItemHargaGrosir.IDItem == item.IDItem,
                ItemHargaGrosir.Aktif == 'Ya'
            )
        ).order_by(
            ItemHargaGrosir.Jumlah
        )
    ).scalars().all()

    today = date.today()
    # mencari harga promo yang aktif antara tanggal hari ini
    hargaPromos = session.execute(
        select(
            ItemHargaD.IDItemHargaD,
            ItemHargaD.IDItemHargaH,
            ItemHargaD.IDItem,
            ItemHarga.Kode,
            ItemHarga.Nama,
            ItemHarga.TanggalAwal,
            ItemHarga.TanggalAkhir,
            ItemHarga.Keterangan,
            ItemHargaD.HargaJual,
            ItemHargaD.DiskonPersen,
            ItemHargaD.Diskon,
        ).join_from(
            ItemHarga,
            ItemHargaD,
            ItemHarga.IDItemHargaH == ItemHargaD.IDItemHargaH,
        ).where(
            and_(
                ItemHargaD.IDItem == item.IDItem,
                ItemHarga.Aktif == 'Ya',
                ItemHarga.TanggalAwal <= today,
                ItemHarga.TanggalAkhir >= today,
            )
        ).order_by(
            ItemHarga.Kode
        )
    ).all()

    return PluModel(
        item=ItemModel.from_orm(item),
        hargaGrosir=parse_obj_as(List[ItemHargaGrosirModel], hargaGrosirs),
        hargaPromo=parse_obj_as(List[ItemHargaPromoModel], hargaPromos),
    )
