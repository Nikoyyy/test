from openai import OpenAI
import re
import time

# 初始化 OpenAI 客户端
client = OpenAI()
"""gpt-3.5-turbo     gpt-3.5-turbo-1106   gpt-3.5-turbo-0125 """
model = "gpt-3.5-turbo-0125"
response_tokens = 0
last_sentence = ""
last_translation = None


def append_to_log_file(text, first_call=False):
    # 检查是否为第一次调用，如果是，则清空文件内容
    mode = 'w' if first_call else 'a'
    
    with open("log.log", mode, encoding='utf-8') as file:
        file.write(text + "\n")

def translate_text(text):
    global last_sentence
    if text.startswith('(') and text.endswith(')'):
        return ''  # 如果是，返回空字符串
    else:
        if last_sentence != text:
            last_sentence = text
            """将文本翻译成目标语言（示例函数，需替换为实际的API调用）"""
            targetInput = f'Translate the following text into Chinese, Just show the translation text:\n{text}'
            print(targetInput)
            append_to_log_file(targetInput)
            retry_count = 0
            message_content = None
            while message_content is None :
                try:
                    completion = client.chat.completions.create(
                                    model=model,
                                    #response_format={ "type": "json_object" },
                                    messages=[
                                        {"role": "user", "content": targetInput}
                                    ],
                                    #max_tokens=100
                                )

                    # 获取回复中的消息
                    message_content = completion.choices[0].message.content if completion.choices[0].message else None
                except Exception as e:
                    print(f"Exception: {e}")
                    print(f"API 调用失败，正在进行第 {retry_count + 1} 次重试...")
                    retry_count += 1
                    time.sleep(1)  # 简单的延时，避免过快重试

            global response_tokens
            global last_translation
            response_tokens += completion.usage.prompt_tokens
            append_to_log_file(message_content + "\n")
            print(message_content)
            last_translation = message_content
            return message_content
        else:
            return last_translation


def process_srt_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    block_number = None
    time_code = None
    subtitle_block = []
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            #time.sleep(1)
            if line.strip().isdigit():
                # 如果当前行是数字，表示是新的字幕块的开始
                if subtitle_block:
                    # 如果subtitle_block非空，处理上一个字幕块
                    block_text = ''.join(subtitle_block)
                    translated_text = translate_text(block_text)
                    # 写入序号、时间码、原文和翻译文本
                    f.write(f'{block_number}{time_code}')
                    for original_line in subtitle_block:
                        f.write(original_line)
                    f.write(translated_text + '\n\n')
                    subtitle_block = []  # 清空字幕块缓存
                block_number = line  # 保存新字幕块的序号
            elif '-->' in line:
                time_code = line  # 保存时间码
            elif line.strip():
                # 将字幕文本添加到字幕块缓存中
                subtitle_block.append(line)
            else:
                continue  # 跳过空行
        
        # 处理文件末尾的最后一个字幕块
        if subtitle_block:
            block_text = ''.join(subtitle_block)
            translated_text = translate_text(block_text)
            f.write(f'{block_number}\n{time_code}\n')
            for original_line in subtitle_block:
                f.write(original_line)
            f.write('\n' + translated_text + '\n\n')
    
    print(f"双语字幕文件已生成：{output_file_path}")


append_to_log_file("",True)
# 请将以下函数调用替换为您的SRT文件路径和输出文件路径
process_srt_file('input.srt', 'output.srt')
