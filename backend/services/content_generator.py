from pathlib import Path
import re
import random
import jieba
from .openai_service import OpenAIService

# Initialize content generator service
class ContentGenerator:
    def __init__(self):
        try:
            # 初始化OpenAI服务
            self.openai_service = OpenAIService()
        except Exception as e:
            print(f"OpenAI service initialization error: {str(e)}")
            raise

    def generate_content(self, input_text='', platform='微信朋友圈', style='轻松', trend='无', length=100):
        """
        使用GPT-4o-mini生成内容
        """
        try:
            if not input_text:
                return "请提供初始文案"

            # 调用OpenAI服务生成内容
            content = self.openai_service.generate_content(
                input_text=input_text,
                platform=platform,
                style=style,
                length=length
            )
            
            # 如果有热梗且生成成功，添加到内容中
            if trend and trend != '无' and content and not content.startswith("系统") and not content.startswith("内容"):
                content += f" #{trend}"
            
            return content

        except Exception as e:
            print(f"Content generation error: {str(e)}")  # 记录错误但不暴露给用户
            return "内容生成遇到问题，请重试"