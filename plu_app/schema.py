## GENERATED CODE - DO NOT MODIFY BY HAND

import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import declarative_base, relationship


convention = {
    "ix": "Idx_%(column_0_label)s",
    "uq": "Idx_%(table_name)s_%(column_0_name)s",
    "fk": "FK_%(table_name)s_%(column_0_name)s",
}

metadata = sa.MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


class ItemHarga(Base):
    __tablename__ = 'titemhargah'

    IDItemHargaH = sa.Column(sa.Integer, primary_key=True)
    Kode = sa.Column(sa.String(30), nullable=False)
    Nama = sa.Column(sa.String(50), nullable=False)
    TanggalAwal = sa.Column(sa.Date, nullable=False)
    TanggalAkhir = sa.Column(sa.Date, nullable=False)
    Keterangan = sa.Column(sa.Text)
    Aktif = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Ya')
    InsertUser = sa.Column(sa.String(16))
    InsertTime = sa.Column(sa.DateTime)
    UpdateUser = sa.Column(sa.String(16))
    UpdateTime = sa.Column(sa.DateTime)

    sa.UniqueConstraint('Kode', name='Idx_Kode')
    sa.Index('Idx_Tanggal', 'TanggalAwal', 'TanggalAkhir')


class ItemTree(Base):
    __tablename__ = 'mitemtree'

    IDItemTree = sa.Column(sa.Integer, primary_key=True)
    TreePath = sa.Column(sa.String(255), nullable=False)
    Kode = sa.Column(sa.String(20), nullable=False)
    Nama = sa.Column(sa.String(50), nullable=False)
    FullPath = sa.Column(sa.String(255), nullable=False)
    marginlabapersen = sa.Column(sa.Float)
    # IDCoa = sa.Column(sa.Integer, sa.ForeignKey('mcoa.IDCOA', onupdate='CASCADE'))
    TipeKategori = sa.Column(sa.Enum('Obral', 'Normal'), server_default='Normal')
    Keterangan = sa.Column(sa.Text)
    Selectable = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Ya')
    Aktif = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Ya')
    KenaPPN = sa.Column(sa.Boolean, nullable=False, server_default='1')
    IkutDiskon = sa.Column(sa.Enum('Ya', 'Tidak'), server_default='Tidak')
    InsertUser = sa.Column(sa.String(16))
    InsertTime = sa.Column(sa.DateTime)
    UpdateUser = sa.Column(sa.String(16))
    UpdateTime = sa.Column(sa.DateTime)
    RefID = sa.Column(sa.Integer)
    Lokasi = sa.Column(sa.String(30))

    sa.UniqueConstraint('Kode', name='Idx_Kode')
    sa.UniqueConstraint('TreePath', name='Idx_TreePath')


class Item(Base):
    __tablename__ = 'mitem'

    IDItem = sa.Column(sa.Integer, primary_key=True)
    Kode = sa.Column(sa.String(20), nullable=False)
    Nama = sa.Column(sa.String(255))
    Singkatan = sa.Column(sa.String(20))
    Barcode = sa.Column(sa.String(20))
    JumlahDos = sa.Column(sa.Float, server_default='0')
    KodePabrik = sa.Column(sa.String(30))
    # IDTipeItem = sa.Column(sa.Integer, sa.ForeignKey('mitemtipe.IDTipeItem', onupdate='CASCADE'))
    IDItemTree = sa.Column(sa.Integer, sa.ForeignKey('mitemtree.IDItemTree', onupdate='CASCADE'))
    TipeStok = sa.Column(sa.Enum('Stok', 'Nonstok', 'Konsinyasi'), nullable=False, server_default='Stok')
    Brand = sa.Column(sa.String(50))
    Manufacturer = sa.Column(sa.String(50))
    # IDSupplier = sa.Column(sa.Integer)
    # IDWarehouse = sa.Column(sa.Integer, sa.ForeignKey('mwarehouse.IDWarehouse', ondelete='SET NULL', onupdate='CASCADE'))
    # IDLorong = sa.Column(mysql.INTEGER(unsigned=True), sa.ForeignKey('mlorong.IDLorong', onupdate='CASCADE'))
    UrutanProduksi = sa.Column(sa.Integer, nullable=False, server_default='0')
    Satuan = sa.Column(sa.String(10))
    HargaNormal = sa.Column(sa.Float, nullable=False, server_default='0')
    HargaJual = sa.Column(sa.Float)
    HargaJualMin = sa.Column(sa.Float, nullable=False, server_default='0')
    # HargaBeli = sa.Column(sa.Float)
    # PersenFranchise = sa.Column(sa.Float, server_default='0')
    # StokMin = sa.Column(sa.Float, nullable=False, server_default='0')
    # Dimensi = sa.Column(sa.Float, nullable=False, server_default='0')
    # IDItemParent = sa.Column(sa.Integer)
    # FaktorParent = sa.Column(sa.Float)
    # HargaDariFaktor = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Ya')
    # Refundable = sa.Column(sa.Enum('Ya', 'Tidak', 'Supplier', 'Customer'))
    # KenaPPN = sa.Column(sa.Boolean, nullable=False, server_default='1')
    # IsBarangBonus = sa.Column(sa.Boolean, nullable=False, server_default='0')
    # IkutDiskonMember = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Tidak')
    Keterangan = sa.Column(sa.Text)
    Aktif = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Ya')
    InsertUser = sa.Column(sa.String(16))
    InsertTime = sa.Column(sa.DateTime)
    UpdateUser = sa.Column(sa.String(16))
    UpdateTime = sa.Column(sa.DateTime)
    RefID = sa.Column(sa.Integer)
    Lokasi = sa.Column(sa.String(30))

    sa.Index('Idx_Kode', 'Kode')
    sa.Index('Idx_RefIDItem', 'RefID')
    sa.Index('Idx_UrutanProduksi', 'UrutanProduksi')

    ItemTree = relationship('ItemTree', backref='Items')


class ItemHargaGrosir(Base):
    __tablename__ = 'mitemhargagrosir'

    IDItemHargaGrosir = sa.Column(sa.Integer, primary_key=True)
    IDItem = sa.Column(sa.Integer, sa.ForeignKey('mitem.IDItem', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Jumlah = sa.Column(sa.Float, nullable=False, server_default='0')
    Harga = sa.Column(sa.Float, nullable=False, server_default='0')
    IsDos = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Tidak')
    IsTampilPrint = sa.Column(sa.Enum('Ya', 'Tidak'), server_default='Ya')
    Aktif = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Ya')

    Item = relationship('Item', backref='ItemHargaGrosirs')


class ItemHargaD(Base):
    __tablename__ = 'titemhargad'

    IDItemHargaD = sa.Column(sa.Integer, primary_key=True)
    IDItemHargaH = sa.Column(sa.Integer, sa.ForeignKey('titemhargah.IDItemHargaH', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    IDItem = sa.Column(sa.Integer, sa.ForeignKey('mitem.IDItem'), nullable=False)
    HargaJual = sa.Column(sa.Float, nullable=False, server_default='0')
    DiskonPersen = sa.Column(sa.Float, nullable=False, server_default='0')
    Diskon = sa.Column(sa.Float, server_default='0')
    Aktif = sa.Column(sa.Enum('Ya', 'Tidak'), nullable=False, server_default='Ya')

    ItemHarga = relationship('ItemHarga', backref='ItemHargaDs')
    Item = relationship('Item', backref='ItemHargaDs')
