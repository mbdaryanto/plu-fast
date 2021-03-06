import { ChakraProvider } from '@chakra-ui/react'
import { ApolloProvider, ApolloClient, InMemoryCache } from '@apollo/client'
import Plu from './Plu'
import ErrorBoundary from './components/ErrorBoundary'


const client = new ApolloClient({
  uri: () => {
    const url = new URL('/graphql', window.location.href)
    return url.href
    // return 'http://localhost:8000/graphql'
  },
  cache: new InMemoryCache(),
})

function App() {
  return (
    <ErrorBoundary>
      <ChakraProvider>
        <ApolloProvider client={client}>
          <Plu/>
        </ApolloProvider>
      </ChakraProvider>
    </ErrorBoundary>
  )
}

export default App
