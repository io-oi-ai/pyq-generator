import { View } from '@tarojs/components'
import { AtForm, AtButton } from 'taro-ui'

const Index = () => {
  return (
    <View className='index'>
      <AtForm>
        <AtButton type='primary' onClick={generateContent}>
          生成文案
        </AtButton>
      </AtForm>
    </View>
  )
} 