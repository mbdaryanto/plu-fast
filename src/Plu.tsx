import { useState, useRef, useEffect } from 'react'
import { Input, Button, FormControl, FormErrorMessage, Center, Text,
  VStack, HStack, Box, Heading, Image, Spacer, CircularProgress } from '@chakra-ui/react'
import { Formik, Form, Field, FieldProps } from 'formik'
import { gql, useQuery } from '@apollo/client'
import { PluSchema } from './item'
import PluGraphql from './components/PluGraphql'
// import PluRest from './components/PluRest'
import companyLogo from './companyLogo.png'

export const GET_GLOBALS = gql`
  query getGlobals {
    globals {
      appSubtitle
      appTitle
      version
    }
  }
`

interface GlobalType {
  appTitle: string
  appSubtitle: string
  version: string
}

interface GetGlobalsResponse {
  globals: GlobalType
}

function PluPage() {
  const [barcode, setBarcode] = useState('')
  // const [plu, setPlu] = useState<PluResponseType>()
  const txtCodeRef = useRef<HTMLInputElement>(null)
  // const toast = useToast()
  const { loading, error, data } = useQuery<GetGlobalsResponse, {}>(GET_GLOBALS)

  useEffect(() => {
    // barcode reader sends ctrl+J after scanning barcode
    // prevent browser to open download dialog
    const cancelCtrlJ = (ev: KeyboardEvent) => {
      if (ev.ctrlKey && (ev.key === 'J' || ev.key === 'j')) {
        ev.preventDefault()
        ev.stopPropagation()
      }
    }
    // register keydown
    window.addEventListener('keydown', cancelCtrlJ)
    return () => {
      // unregister on page unmount
      window.removeEventListener('keydown', cancelCtrlJ)
    }
  }, [])

  if (loading) return <Center minH="100vh"><CircularProgress isIndeterminate/></Center>
  if (error) return <Center minH="100vh">Error loading globals</Center>

  return (
    <Center minH="100vh">
      <VStack spacing={8} w="100%" maxW="800px">
        <HStack w="100%" as="header" spacing={8} px={8}>
          <VStack align="flex-start" spacing="0">
            <Heading fontSize="xxx-large">{data?.globals.appTitle ?? 'Cek Harga'}</Heading>
            {data?.globals.appSubtitle && (<Text fontStyle="italic">{data?.globals.appSubtitle}</Text>)}
          </VStack>
          <Spacer flexGrow={1}/>
          <Image src={companyLogo} w="100px" />
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

          {/* <PluGraphql barcode={barcode}/> */}

          {!!barcode && <PluGraphql barcode={barcode}/>}
          {/* {!!barcode && <PluRest code={barcode}/>} */}

        </Box>
      </VStack>
    </Center>
  )
}

export default PluPage
