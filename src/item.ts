import { number, string, object, Asserts } from 'yup'
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

export type ItemType = Asserts<typeof ItemSchema>

export async function getItem({
    axios, code
}: {
    axios: AxiosInstance
    code: string
}): Promise<ItemType> {
    const response = await axios.get('/item', { params: { 'code': code } })
    return await ItemSchema.validate(response.data)
}
