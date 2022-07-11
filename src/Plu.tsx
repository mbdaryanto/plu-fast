import { useState, useRef } from 'react'
import { Input, Button, FormControl, FormErrorMessage, Center,
  VStack, HStack, Box, Heading, Image } from '@chakra-ui/react'
import { Formik, Form, Field, FieldProps } from 'formik'
import { PluSchema } from './item'
import PluGraphql from './components/PluGraphql'
// import PluRest from './components/PluRest'
import companyLogo from './companyLogo.png'


function PluPage() {
  const [barcode, setBarcode] = useState('')
  // const [plu, setPlu] = useState<PluResponseType>()
  const txtCodeRef = useRef<HTMLInputElement>(null)
  // const toast = useToast()

  return (
    <Center minH="100vh">
      <VStack spacing={8} w="100%" maxW="800px">
        <HStack as="header" spacing={8}>
          <Image src={companyLogo} w="100px" />
          <Heading>Cek Harga</Heading>
        </HStack>
        <Box as="main" w="100%" px={8}>
          <Formik
            initialValues={{ code: '' }}
            validationSchema={PluSchema}
            onSubmit={async (values, { setSubmitting }) => {
              setBarcode(values.code)
              setSubmitting(false)
              if (!!txtCodeRef.current) {
                txtCodeRef.current.focus()
                txtCodeRef.current.select()
              }
            }}
          >
            {({ isSubmitting }) => (
              <Form>
                <HStack spacing={1} align="start">
                  <Field name="code">
                    {({ field, meta }: FieldProps<string>) => (
                      <FormControl isRequired>
                        {/* <FormLabel htmlFor="txtCode">Barcode</FormLabel> */}
                        <Input id="txtCode" ref={txtCodeRef} {...field} autoFocus/>
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
          {/* {!!barcode && <PluRest code={barcode}/>} */}

        </Box>
      </VStack>
    </Center>
  )
}

export default PluPage
