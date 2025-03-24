"""
Project structure:

PYQ/
├── backend/
│   ├── app.py
│   └── services/
│       ├── __init__.py
│       └── content_generator.py
├── requirements.txt
└── .env
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ContentGenerator:
    def __init__(self):
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL")
        )
        
        # 初始化平台风格提示词
        self.platform_prompts = {
            '微信朋友圈': {
                '轻松': "请以轻松愉快的语气，生成一条朋友圈文案。要求：1. 语气要轻松自然 2. 可以适当使用表情符号 3. 长度适中",
                '正式': "请以正式的语气，生成一条朋友圈文案。要求：1. 语气要正式得体 2. 避免使用表情符号 3. 表达要清晰",
                '幽默': "请以幽默诙谐的语气，生成一条朋友圈文案。要求：1. 语气要幽默有趣 2. 可以适当使用表情符号 3. 要有趣味性",
                '文艺': "请以文艺清新的语气，生成一条朋友圈文案。要求：1. 语气要文艺优雅 2. 可以适当使用表情符号 3. 要有诗意"
            }
        }

    def generate_content(self, input_text='', platform='微信朋友圈', style='轻松', trend='无', length=100):
        """
        根据给定的参数生成内容
        
        Args:
            input_text (str): 用户输入的初始文案
            platform (str): 目标平台 (微信朋友圈, 微博, 小红书, B站)
            style (str): 语言风格 (轻松, 正式, 幽默, 文艺)
            trend (str): 网络热梗
            length (int): 期望的文本长度
            
        Returns:
            str: 生成的文案内容
        """
        # 如果平台或风格不存在，返回空字符串
        if platform not in self.platform_prompts or style not in self.platform_prompts[platform]:
            return ""
            
        # 构建系统提示词
        system_prompt = self.platform_prompts[platform][style]
        
        # 构建用户提示词
        user_prompt = f"请根据以下要求生成一条文案：\n"
        if input_text:
            user_prompt += f"参考文案：{input_text}\n"
        user_prompt += f"目标平台：{platform}\n"
        user_prompt += f"语言风格：{style}\n"
        if trend and trend != '无':
            user_prompt += f"需要融入的热梗：{trend}\n"
        user_prompt += f"期望长度：{length}字左右"
        
        try:
            # 调用DeepSeek API
            completion = self.client.chat.completions.create(
                model=os.getenv("DEEPSEEK_MODEL"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 获取生成的文案
            generated_content = completion.choices[0].message.content
            
            # 如果有热梗且不为"无"，添加到内容中
            if trend and trend != '无':
                generated_content += f" #{trend}"
                
            return generated_content
            
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return ""