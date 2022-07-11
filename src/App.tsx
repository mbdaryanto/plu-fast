import { ChakraProvider } from '@chakra-ui/react'
import { ApolloProvider, ApolloClient, InMemoryCache } from '@apollo/client'
import Plu from './Plu'


const client = new ApolloClient({
  uri: () => {
    // const url = new URL('/', window.location.href)
    // return url.href
    return 'http://localhost:8000/graphql'
  },
  cache: new InMemoryCache(),
})

function App() {
  return (
    <ChakraProvider>
      <ApolloProvider client={client}>
        <Plu/>
      </ApolloProvider>
    </ChakraProvider>
  )
}

export default App
