import { ReactNode, useState } from 'react'
import { Input, Button, FormControl, FormErrorMessage,
  VStack, HStack, Box, Heading, Text, useToast, Grid, GridItem, CSSObject } from '@chakra-ui/react'
import axios from 'axios'
import { Formik, Form, Field, FieldProps } from 'formik'
import { PluSchema, getItem, ItemType } from './item'


interface ErrorResponse {
  detail: string
  [key: string]: any
}

const nf = new Intl.NumberFormat('id')

function PluPage() {
  const [item, setItem] = useState<ItemType>()
  const toast = useToast()

  return (
    <VStack spacing={8} w="100%" minH="100vh" py={20}>
      <Box as="header">
        <Heading>Cek Harga</Heading>
      </Box>
      <main>
        <Formik
          initialValues={{ code: '' }}
          validationSchema={PluSchema}
          onSubmit={async (values, { setSubmitting }) => {
            try {
              const item = await getItem({ axios, code: values.code })
              setItem(item)
            } catch (ex) {
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
              setSubmitting(true)
            }
          }}
        >
          {({ isSubmitting }) => (
            <Form>
              <HStack spacing={8} align="start">
                <Field name="code">
                  {({ field, meta }: FieldProps<string>) => (
                    <FormControl isRequired>
                      {/* <FormLabel htmlFor="txtCode">Barcode</FormLabel> */}
                      <Input id="txtCode" {...field}/>
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

        {!!item && <ItemView2 item={item}/>}

      </main>
    </VStack>
  )
}

const labelStyle: CSSObject = { fontSize: "sm" }
const valueStyle: CSSObject = { fontSize: "lg" }

const ItemView = ({ item }: {
  item: ItemType
}) => (
  <Grid templateColumns="100px 1fr">
    <GridItem sx={labelStyle}>
      Kode
    </GridItem>
    <GridItem sx={valueStyle}>
      {item.Kode}
    </GridItem>
    <GridItem sx={labelStyle}>
      Barcode
    </GridItem>
    <GridItem sx={valueStyle}>
      <Text>{item.Barcode}</Text>
    </GridItem>
    <GridItem sx={labelStyle}>
      Nama
    </GridItem>
    <GridItem sx={valueStyle}>
      <Text>{item.Nama}</Text>
    </GridItem>
    {/* <GridItem sx={labelStyle}>
      Satuan
    </GridItem>
    <GridItem sx={valueStyle}>
      <Text>{item.Satuan}</Text>
    </GridItem> */}
    <GridItem sx={labelStyle}>
      Harga
    </GridItem>
    <GridItem sx={valueStyle}>
      <Text>
        <del>{nf.format(item.HargaNormal)}</del>
        {nf.format(item.HargaJual)}
      </Text>
    </GridItem>

  </Grid>
)

const ItemView2 = ({ item }: {
  item: ItemType
}) => (
  <Grid templateColumns="repeat(2, 1fr)" columnGap={2} rowGap={4}>
    <GridItem>
      <LabelValue label="Kode" value={item.Kode}/>
    </GridItem>
    <GridItem>
      <LabelValue label="Barcode" value={item.Barcode}/>
    </GridItem>
    <GridItem colSpan={2}>
      <LabelValue label="Nama" value={item.Nama}/>
    </GridItem>
    <GridItem colSpan={2}>
      <LabelValue label="Harga" value={(
        <Text fontSize="xx-large">
          <del>{nf.format(item.HargaNormal)}</del>
          {' '}
          {nf.format(item.HargaJual)}
        </Text>
      )}/>
    </GridItem>
  </Grid>
)

const LabelValue = ({ label, value }: {
  label: string
  value: string | ReactNode
}) => (
  <VStack align="left" spacing="0">
    <Text textColor="green.800" sx={{ fontSize: "sm" }}>
      {label}
    </Text>
    <Box w="100%" bgColor="green.100" borderRadius="4px" p={2}>
      <Text sx={{ fontSize: "lg" }}>
        {value}
      </Text>
    </Box>
  </VStack>
)


export default PluPage
