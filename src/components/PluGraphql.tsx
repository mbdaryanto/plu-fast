import { gql, useQuery } from '@apollo/client'
import { Center, CircularProgress, Grid, GridItem, Text, VStack } from '@chakra-ui/react'
import { Fragment } from 'react'
import LabelValue from './LabelValue'


const nf = new Intl.NumberFormat('id')
const GET_PLU = gql`
  query getPlu($barcode: String!) {
    plu(barcode: $barcode) {
      id
      code
      barcode
      name
      normalPrice
      discountedPrice
      bulkPrices {
        id
        quantity
        unitPrice
      }
      promoPrices {
        id
        promoCode
        promoName
        start
        end
        discountPercent
        discount
        unitPrice
      }
    }
  }
`

interface PluArgsType {
  barcode: string
}

interface BulkPriceType {
  id: string
  quantity: number
  unitPrice: number
}

interface PromoPriceType {
  id: string
  promoCode: string
  promoName: string
  start: string
  end: string
  discountPercent: number
  discount: number
  unitPrice: number
}

interface ItemType {
  id: string
  code: string
  barcode: string
  name: string
  normalPrice: number
  discountedPrice: number
  bulkPrices: BulkPriceType[]
  promoPrices: PromoPriceType[]
}

interface PluType {
  plu: ItemType
}

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

function PluGraphql({ barcode }: {
  barcode: string
}) {
  const { data, error, loading, refetch } = useQuery<PluType, PluArgsType>(GET_PLU, {
    variables: { barcode },
    // using 1s pollInterval to refresh data
    // pollInterval: 1000,
    // read from cache first then update from network
    fetchPolicy: 'cache-and-network'
  })

  if (loading) return (
    <Center w="100%" minH="200px">
      <CircularProgress isIndeterminate/>
    </Center>
  )

  if (error) return (
    <Center w="100%" minH="200px">
      <Text>Error {error.message}</Text>
    </Center>
  )

  if (!data) return (
    <Center w="100%" minH="200px">
      <Text>Enter barcode</Text>
    </Center>
  )

  return (
    <VStack w="100%" marginTop={3} spacing={3}>
      <Grid w="100%" templateColumns="repeat(2, 1fr)" columnGap={2} rowGap={3}>
        <GridItem>
          <LabelValue label="Kode" value={data!.plu.code} {...normalTheme}/>
        </GridItem>
        <GridItem>
          <LabelValue label="Barcode" value={data!.plu.barcode} {...normalTheme}/>
        </GridItem>
        <GridItem colSpan={2}>
          <LabelValue label="Nama" value={data!.plu.name} fontSize="4xl" {...normalTheme}/>
        </GridItem>
        <GridItem colSpan={2}>
          <LabelValue
            label="Harga"
            fontSize="4xl"
            textAlign="center"
            {...normalTheme}
            value={(
              <Fragment>
                <Text as="span" textColor="red.200" fontSize="md">
                  <del>{`Rp `}{nf.format(data!.plu.normalPrice)}</del>
                </Text>
                {' Rp '}
                {nf.format(data!.plu.discountedPrice)}
              </Fragment>
            )}
          />
        </GridItem>
      </Grid>

      {data!.plu.bulkPrices.length !== 0 && (
        <Grid w="100%" templateColumns="1fr 2fr" columnGap={2} rowGap={3}>
          {data!.plu.bulkPrices.map((row) => (
            <Fragment key={row.id}>
              <GridItem>
                <LabelValue label="Jumlah" textAlign="right" value={nf.format(row.quantity)} {...grosirTheme}/>
              </GridItem>
              <GridItem>
                <LabelValue label="Harga Satuan" textAlign="right" value={`Rp ${nf.format(row.unitPrice)}`} {...grosirTheme}/>
              </GridItem>
            </Fragment>
          ))}
        </Grid>
      )}

      {data!.plu.promoPrices.length !== 0 && (
        <Grid w="100%" templateColumns="4fr 1fr 1fr 1fr" columnGap={2} rowGap={3}>
          {data!.plu.promoPrices.map((row) => (
            <Fragment key={row.id}>
              <GridItem>
                <LabelValue label="Promo" value={row.promoName} {...promoTheme}/>
              </GridItem>
              <GridItem>
                <LabelValue label="Kode" value={row.promoCode} {...promoTheme}/>
              </GridItem>
              {/* <GridItem>
                {nf.format(row.HargaJual)}
              </GridItem> */}
              <GridItem>
                <LabelValue label="Diskon %" textAlign="right" value={`${nf.format(row.discountPercent)} %`} {...promoTheme}/>
              </GridItem>
              <GridItem>
                <LabelValue label="Diskon Rp" textAlign="right" value={`${nf.format(row.discount)}`} {...promoTheme}/>
              </GridItem>
            </Fragment>
          ))}
        </Grid>
      )}
    </VStack>
  )
}

export default PluGraphql
