from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, constr
from sqlalchemy import select, or_, desc
from ..db import Session, get_session
from ..schema import Item


router = APIRouter(
    prefix='/item',
    tags=['item']
)

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


@router.get('', response_model=ItemModel)
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

    return ItemModel.from_orm(item)
