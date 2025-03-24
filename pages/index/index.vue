<template>
  <view class="container">
    <!-- 顶部选择区 -->
    <view class="header">
      <u-tabs :list="sceneList" @click="onSceneChange"></u-tabs>
    </view>
    
    <!-- 主要内容区 -->
    <view class="content">
      <u-form :model="form">
        <!-- 添加文案输入框 -->
        <u-form-item label="原始文案">
          <u-textarea
            v-model="form.originalText"
            placeholder="请输入您想要改写的文案"
            :height="120"
          ></u-textarea>
        </u-form-item>

        <!-- 添加场景选择 -->
        <u-form-item label="场景选择">
          <u-select
            v-model="form.scene"
            :list="sceneOptions"
            placeholder="请选择场景"
          ></u-select>
        </u-form-item>

        <!-- 添加心情选择 -->
        <u-form-item label="心情选择">
          <u-select
            v-model="form.mood"
            :list="moodOptions"
            placeholder="请选择心情"
          ></u-select>
        </u-form-item>

        <!-- 添加角色选择 -->
        <u-form-item label="角色选择">
          <u-select
            v-model="form.role"
            :list="roleOptions"
            placeholder="请选择角色"
          ></u-select>
        </u-form-item>
        
        <u-form-item label="文案风格">
          <u-radio-group v-model="form.style">
            <u-radio v-for="item in styleList" :key="item.value" :label="item.name"></u-radio>
          </u-radio-group>
        </u-form-item>
        
        <u-form-item label="文案长度">
          <u-radio-group v-model="form.lengthType" @change="handleLengthChange">
            <u-radio 
              v-for="item in lengthOptions" 
              :key="item.value" 
              :label="item.label"
              :name="item.value"
            ></u-radio>
          </u-radio-group>
          
          <!-- 自定义长度滑块，当选择"自定义"时显示 -->
          <template v-if="form.lengthType === 'custom'">
            <view class="custom-length">
              <u-slider 
                v-model="form.length" 
                :min="50" 
                :max="500"
                :step="10"
                showValue
              ></u-slider>
              <text class="length-hint">当前长度：{{form.length}}字</text>
            </view>
          </template>
        </u-form-item>

        <!-- 在表单中添加模板选择 -->
        <u-form-item label="文案模板">
          <u-select
            v-model="form.template"
            :list="templateOptions"
            placeholder="选择模板（可选）"
          ></u-select>
        </u-form-item>

        <!-- 如果选择了模板，显示示例 -->
        <view class="template-examples" v-if="currentTemplate">
          <text class="title">模板示例：</text>
          <view class="example" v-for="(example, index) in currentTemplate.examples" :key="index">
            {{example}}
          </view>
        </view>
      </u-form>

      <!-- 添加生成按钮 -->
      <view class="btn-wrapper">
        <u-button 
          type="primary" 
          @click="generateContent" 
          :loading="loading"
          :disabled="loading || !form.originalText"
        >
          {{ loading ? '生成中...' : '生成文案' }}
        </u-button>
      </view>

      <!-- 添加结果展示区 -->
      <view class="result-wrapper" v-if="generatedContent">
        <u-card title="生成结果">
          <text>{{generatedContent}}</text>
          <view class="action-buttons">
            <u-button size="mini" @click="copyContent">复制文案</u-button>
            <u-button size="mini" @click="saveToHistory">保存到历史</u-button>
          </view>
        </u-card>
      </view>

      <!-- 添加错误提示 -->
      <u-toast ref="uToast" />
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      form: {
        originalText: '',
        scene: '',
        mood: '',
        role: '',
        style: '',
        lengthType: 'medium',
        length: 100,
        template: ''
      },
      sceneOptions: [
        { label: '职场', value: 'work' },
        { label: '生活', value: 'life' },
        { label: '社交', value: 'social' },
        { label: '情感', value: 'emotion' }
      ],
      moodOptions: [
        { label: '开心', value: 'happy' },
        { label: '悲伤', value: 'sad' },
        { label: '愤怒', value: 'angry' },
        { label: '平静', value: 'calm' }
      ],
      roleOptions: [
        { label: '朋友', value: 'friend' },
        { label: '同事', value: 'colleague' },
        { label: '家人', value: 'family' },
        { label: '恋人', value: 'lover' }
      ],
      generatedContent: '',
      loading: false,
      templateOptions: [
        { label: '会议发言', value: 'work.meeting' },
        { label: '工作邮件', value: 'work.email' },
        { label: '社交问候', value: 'social.greeting' }
      ],
      lengthOptions: [
        { label: '短文案(50字)', value: 'short' },
        { label: '中等(100字)', value: 'medium' },
        { label: '长文案(200字)', value: 'long' },
        { label: '自定义', value: 'custom' }
      ],
      lengthPresets: {
        short: 50,
        medium: 100,
        long: 200,
        custom: null
      }
    }
  },
  computed: {
    currentTemplate() {
      if (!this.form.template) return null
      const [scene, subScene] = this.form.template.split('.')
      return this.templates[scene]?.[subScene] || null
    }
  },
  methods: {
    handleLengthChange(value) {
      if (value !== 'custom') {
        this.form.length = this.lengthPresets[value]
      }
    },

    async generateContent() {
      if (!this.form.originalText) {
        this.$refs.uToast.show({
          type: 'warning',
          message: '请输入原始文案'
        })
        return
      }

      this.loading = true
      try {
        const template = this.currentTemplate
        if (template) {
          // 使用模板生成内容
          this.form.template = template.prompt
        }

        const result = await this.$api.generateContent({
          originalText: this.form.originalText,
          scene: this.form.scene,
          mood: this.form.mood,
          role: this.form.role,
          style: this.form.style,
          length: this.form.length,
          lengthType: this.form.lengthType
        })
        
        if (result.success) {
          this.generatedContent = result.content
          this.$refs.uToast.show({
            type: 'success',
            message: '生成成功'
          })
        } else {
          throw new Error(result.error)
        }
      } catch (error) {
        this.$refs.uToast.show({
          type: 'error',
          message: error.message || '生成失败，请重试'
        })
      } finally {
        this.loading = false
      }
    },

    // 复制文案
    copyContent() {
      uni.setClipboardData({
        data: this.generatedContent,
        success: () => {
          this.$refs.uToast.show({
            type: 'success',
            message: '复制成功'
          })
        }
      })
    },

    // 保存到历史记录
    async saveToHistory() {
      try {
        await this.$api.saveHistory({
          originalText: this.form.originalText,
          generatedContent: this.generatedContent,
          scene: this.form.scene,
          mood: this.form.mood,
          role: this.form.role
        })
        
        this.$refs.uToast.show({
          type: 'success',
          message: '保存成功'
        })
      } catch (error) {
        this.$refs.uToast.show({
          type: 'error',
          message: '保存失败'
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  padding: 20rpx;
}

.btn-wrapper {
  margin: 30rpx 0;
}

.result-wrapper {
  margin-top: 30rpx;
  
  .action-buttons {
    margin-top: 20rpx;
    display: flex;
    gap: 20rpx;
    justify-content: flex-end;
  }
}

// 添加加载状态样式
.loading {
  opacity: 0.7;
  cursor: not-allowed;
}

.template-examples {
  margin: 20rpx 0;
  padding: 20rpx;
  background: #f5f5f5;
  border-radius: 8rpx;
  
  .title {
    font-weight: bold;
    margin-bottom: 10rpx;
  }
  
  .example {
    color: #666;
    margin: 10rpx 0;
    font-size: 28rpx;
  }
}

.custom-length {
  margin-top: 20rpx;
  padding: 20rpx;
  background: #f8f8f8;
  border-radius: 8rpx;
  
  .length-hint {
    font-size: 24rpx;
    color: #666;
    margin-top: 10rpx;
    display: block;
    text-align: right;
  }
}

// 优化单选按钮组的样式
.u-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
  
  .u-radio {
    margin-right: 30rpx;
    
    &:last-child {
      margin-right: 0;
    }
  }
}
</style> 