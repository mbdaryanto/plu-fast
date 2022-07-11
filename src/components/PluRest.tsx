import { Fragment, useEffect, useState } from 'react'
import axios from 'axios'
import { getItem, PluResponseType } from '../item'
import { Center, CircularProgress, Grid, GridItem, Text, useToast, VStack } from '@chakra-ui/react'
import LabelValue from './LabelValue'

// const labelStyle: CSSObject = { fontSize: "sm" }
// const valueStyle: CSSObject = { fontSize: "lg" }

// const PluViewX = ({ item }: {
//   item: PluResponseType
// }) => (
//   <Grid templateColumns="100px 1fr">
//     <GridItem sx={labelStyle}>
//       Kode
//     </GridItem>
//     <GridItem sx={valueStyle}>
//       {item.item.Kode}
//     </GridItem>
//     <GridItem sx={labelStyle}>
//       Barcode
//     </GridItem>
//     <GridItem sx={valueStyle}>
//       <Text>{item.Barcode}</Text>
//     </GridItem>
//     <GridItem sx={labelStyle}>
//       Nama
//     </GridItem>
//     <GridItem sx={valueStyle}>
//       <Text>{item.Nama}</Text>
//     </GridItem>
//     {/* <GridItem sx={labelStyle}>
//       Satuan
//     </GridItem>
//     <GridItem sx={valueStyle}>
//       <Text>{item.Satuan}</Text>
//     </GridItem> */}
//     <GridItem sx={labelStyle}>
//       Harga
//     </GridItem>
//     <GridItem sx={valueStyle}>
//       <Text>
//         <del>{nf.format(item.HargaNormal)}</del>
//         {nf.format(item.HargaJual)}
//       </Text>
//     </GridItem>

//   </Grid>
// )

const nf = new Intl.NumberFormat('id')

const normalTheme = {
  labeltextColor: "green.800",
  valueBgColor: "green.100",
}

const grosirTheme = {
  labeltextColor: "blue.800",
  valueBgColor: "blue.100",
}

const promoTheme = {
  labeltextColor: "red.800",
  valueBgColor: "red.100",
}

interface ErrorResponse {
  detail: string
  [key: string]: any
}

const PluRest = ({ code }: {
  code: string
}) => {
  const [plu, setPlu] = useState<PluResponseType>()
  const [loading, setLoading] = useState(false)
  const toast = useToast()

  useEffect(() => {
    let isMounted = true;
    (async () => {
      try {
        setLoading(true)
        const item = await getItem({ axios, code })
        if (!isMounted) return
        setPlu(item)
      } catch (ex) {
        if (!isMounted) return
        if (axios.isAxiosError(ex)) {
          console.log('Axios Error', ex.response!.data)
          const errorResponse = ex.response!.data as ErrorResponse
          toast({
            title: 'Kesalahan',
            status: 'error',
            description: errorResponse.detail
          })
        } else {
          console.log('Unknown Error', ex)
        }
      } finally {
        setLoading(false)
      }
    })();
    return () => {
      isMounted = false;
    }
  }, [code])

  if (loading) return (
    <Center w="100%" minH="200px">
      <CircularProgress isIndeterminate/>
    </Center>
  )
  if (!!plu) return <PluView plu={plu}/>
  return <Text>Enter barcode</Text>
}

const PluView = ({ plu }: {
  plu: PluResponseType
}) => (
  <VStack w="100%" marginTop={3} spacing={3}>
    <Grid w="100%" templateColumns="repeat(2, 1fr)" columnGap={2} rowGap={3}>
      <GridItem>
        <LabelValue label="Kode" value={plu.item.Kode} {...normalTheme}/>
      </GridItem>
      <GridItem>
        <LabelValue label="Barcode" value={plu.item.Barcode} {...normalTheme}/>
      </GridItem>
      <GridItem colSpan={2}>
        <LabelValue label="Nama" value={plu.item.Nama} {...normalTheme}/>
      </GridItem>
      <GridItem colSpan={2}>
        <LabelValue
          label="Harga"
          fontSize="xx-large"
          textAlign="center"
          {...normalTheme}
          value={(
            <Fragment>
              <Text as="span" textColor="red.200">
                <del>{nf.format(plu.item.HargaNormal)}</del>
              </Text>
              {' '}
              {nf.format(plu.item.HargaJual)}
            </Fragment>
          )}
        />
      </GridItem>
    </Grid>

    {plu.hargaGrosir.length !== 0 && (
      <Grid w="100%" templateColumns="1fr 2fr" columnGap={2} rowGap={3}>
        {plu.hargaGrosir.map((row) => (
          <Fragment key={row.IDItemHargaGrosir}>
            <GridItem>
              <LabelValue label="Jumlah" textAlign="right" value={nf.format(row.Jumlah)} {...grosirTheme}/>
            </GridItem>
            <GridItem>
              <LabelValue label="Harga Satuan" textAlign="right" value={nf.format(row.Harga)} {...grosirTheme}/>
            </GridItem>
            {/* if you want to show IsDos field use 60px at the end of templateColumns */}
            {/* <GridItem pt="21px" display="flex" alignItems="center" justifyContent="center">
              {row.IsDos === 'Ya' && (<FaBox/>)}
            </GridItem> */}
          </Fragment>
        ))}
      </Grid>
    )}

    {plu.hargaPromo.length !== 0 && (
      <Grid w="100%" templateColumns="4fr 1fr 1fr 1fr" columnGap={2} rowGap={3}>
        {plu.hargaPromo.map((row) => (
          <Fragment key={row.IDItemHargaD}>
            <GridItem>
              <LabelValue label="Promo" value={row.Nama} {...promoTheme}/>
            </GridItem>
            <GridItem>
              <LabelValue label="Kode" value={row.Kode} {...promoTheme}/>
            </GridItem>
            {/* <GridItem>
              {nf.format(row.HargaJual)}
            </GridItem> */}
            <GridItem>
              <LabelValue label="Diskon %" textAlign="right" value={`${nf.format(row.DiskonPersen)} %`} {...promoTheme}/>
            </GridItem>
            <GridItem>
              <LabelValue label="Diskon Rp" textAlign="right" value={`${nf.format(row.Diskon || 0.0)}`} {...promoTheme}/>
            </GridItem>
          </Fragment>
        ))}
      </Grid>
    )}
  </VStack>
)

export default PluRest
