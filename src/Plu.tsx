import { ReactNode, useState, useRef, Fragment, ComponentProps } from 'react'
import { Input, Button, FormControl, FormErrorMessage, Grid, GridItem, Center,
  VStack, HStack, Box, Heading, Text, useToast, CircularProgress } from '@chakra-ui/react'
import axios from 'axios'
import { Formik, Form, Field, FieldProps } from 'formik'
import { PluSchema, getItem, PluResponseType } from './item'
import { FaBox } from 'react-icons/fa'
import LabelValue from './components/LabelValue'
import PluGraphql from './PluGraphql'


interface ErrorResponse {
  detail: string
  [key: string]: any
}

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

function PluPage() {
  const [barcode, setBarcode] = useState('')
  // const [plu, setPlu] = useState<PluResponseType>()
  const txtCodeRef = useRef<HTMLInputElement>(null)
  const toast = useToast()

  return (
    <Center minH="100vh">
      <VStack spacing={8} w="100%" maxW="800px">
        <Box as="header">
          <Heading>Cek Harga</Heading>
        </Box>
        <Box as="main" w="100%" px={8}>
          <Formik
            initialValues={{ code: '' }}
            validationSchema={PluSchema}
            onSubmit={async (values, { setSubmitting }) => {
              setBarcode(values.code)
              // try {
              //   const item = await getItem({ axios, code: values.code })
              //   setPlu(item)
              // } catch (ex) {
              //   if (axios.isAxiosError(ex)) {
              //     console.log('Axios Error', ex.response!.data)
              //     const errorResponse = ex.response!.data as ErrorResponse
              //     toast({
              //       title: 'Kesalahan',
              //       status: 'error',
              //       description: errorResponse.detail
              //     })
              //   } else {
              //     console.log('Unknown Error', ex)
              //   }
              // } finally {
              //   setSubmitting(true)
              //   if (!!txtCodeRef.current) {
              //     txtCodeRef.current.focus()
              //     txtCodeRef.current.select()
              //   }
              // }
            }}
          >
            {({ isSubmitting }) => (
              <Form>
                <HStack spacing={1} align="start">
                  <Field name="code">
                    {({ field, meta }: FieldProps<string>) => (
                      <FormControl isRequired>
                        {/* <FormLabel htmlFor="txtCode">Barcode</FormLabel> */}
                        <Input id="txtCode" ref={txtCodeRef} {...field}/>
                        {meta.touched && !!meta.error && (
                          <FormErrorMessage className="errors">{meta.error}</FormErrorMessage>
                        )}
                      </FormControl>
                    )}
                  </Field>
                  <Button type="submit" disabled={isSubmitting}>Search</Button>
                </HStack>
              </Form>
            )}
          </Formik>

          {!!barcode && <PluGraphql barcode={barcode}/>}
          {/* {!!plu && <PluView plu={plu}/>} */}

        </Box>
      </VStack>
    </Center>
  )
}

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

export default PluPage
