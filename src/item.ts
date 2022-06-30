import { number, string, object, Asserts, array, date } from 'yup'
import type { AxiosInstance } from 'axios'


export const PluSchema = object({
  code: string().max(20).required(),
})

export const ItemSchema = object({
  IDItem: number().integer().required(),
  Kode: string().max(20).required(),
  Nama: string().max(255).default(''),
  Singkatan: string().max(20).default(''),
  Barcode: string().max(20).default(''),
  KodePabrik: string().max(30).default(''),
  JumlahDos: number().default(0),
  Satuan: string().max(10).default(''),
  HargaNormal: number().required(),
  HargaJual: number().required(),
})

export const ItemHargaGrosirSchema = object({
  IDItemHargaGrosir: number().integer().required(),
  Jumlah: number().required(),
  Harga: number().required(),
  IsDos: string().required().oneOf(['Ya', 'Tidak']),
})

export const ItemHargaPromoSchema = object({
  IDItemHargaD: number().integer().required(),
  IDItemHargaH: number().integer().required(),
  Kode: string().required().max(30),
  Nama: string().required().max(50),
  TanggalAwal: date(),
  TanggalAkhir: date(),
  Keterangan: string(),
  HargaJual: number().required(),
  DiskonPersen: number().required(),
  Diskon: number(),
})

export const PluResponseSchema = object({
  item: ItemSchema,
  hargaGrosir: array().of(ItemHargaGrosirSchema).ensure(),
  hargaPromo: array().of(ItemHargaPromoSchema).ensure(),
})

export type PluResponseType = Asserts<typeof PluResponseSchema>

export async function getItem({
  axios, code
}: {
  axios: AxiosInstance
  code: string
}): Promise<PluResponseType> {
  const response = await axios.get('/item', { params: { 'code': code } })
  return await PluResponseSchema.validate(response.data)
}
