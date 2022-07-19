import { ComponentProps, ReactNode } from 'react'
import { Text } from '@chakra-ui/react'


function ValueView({ value, fontSize, textAlign}: {
  value: ReactNode
  fontSize?: ComponentProps<typeof Text>['fontSize']
  textAlign?: ComponentProps<typeof Text>['textAlign']
}) {
  if (!value) return null

  return (
    <Text w="100%" fontSize={fontSize ?? 'xx-large'} textAlign={textAlign}>
      {value}
    </Text>
  )
}

export default ValueView
