import { Box, Text, VStack } from '@chakra-ui/react'
import { ComponentProps, ReactNode } from 'react'


const LabelValue = ({ label, value, fontSize, textAlign, labeltextColor,valueBgColor }: {
  label: string
  value: ReactNode
  fontSize?: ComponentProps<typeof Text>['fontSize']
  textAlign?: ComponentProps<typeof Text>['textAlign']
  labeltextColor?: ComponentProps<typeof Text>['textColor']
  valueBgColor?: ComponentProps<typeof Box>['bgColor']
}) => (
  <VStack align="left" spacing="0">
    <Text fontSize="sm" textColor={labeltextColor ?? "green.800"}>
      {label}
    </Text>
    <Box w="100%" bgColor={valueBgColor ?? "green.100"} borderRadius="4px" p={2}>
      <Text fontSize={fontSize ?? 'lg'} textAlign={textAlign}>
        {value}
      </Text>
    </Box>
  </VStack>
)

export default LabelValue
