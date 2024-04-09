import re
import time
import os

"""
deelp:

import deepl

auth_key = os.getenv("DEEPL_AUTH_KEY")
translator = deepl.Translator(auth_key)

result = translator.translate_text("Hello, world!", target_lang="ZH")
print(result.text)  # "Bonjour, le monde !"
"""

# if deelp    else openai
is_deepl = True
is_translate = False

if is_translate:
    if is_deepl:
        import deepl
        # 初始化 Deepl
        auth_key = os.getenv("DEEPL_AUTH_KEY")
        translator = deepl.Translator(auth_key)
    else:
        from openai import OpenAI
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

def translate_text_by_deepl(text, target_language='zh'):
    result = translator.translate_text(text, target_lang="ZH")
    print(result.text)
    return result.text

def translate_text_by_openai(text):
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

            #translated_sentences = [message_content for _ in re.split(r'(?<=[。.!！?？;；])', text) if _]
            return message_content
        else:
            return last_translation


def is_sentence_complete(text):
    # 这是一个简化的例子，实际应用中可能需要更复杂的逻辑来判断句子是否完整
    # 例如，检查是否以句号、问号或感叹号等结尾
    return text.strip().endswith(('。', '.', '!','！', '?','？', '；', ';'))

def split_sentences(text):
    # 使用正则表达式分割句子，保留句末标点
    sentences = [sentence.strip() for sentence in re.split(r'(?<=[。.!！?？;；])', text) if sentence.strip()]
    return sentences

def process_srt_file(input_file_path, output_file_path, output_file_path2):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    block_number = 1
    start_time = ''
    end_time = ''
    accumulated_text = ''

    with open(output_file_path, 'w', encoding='utf-8') as f,\
         open(output_file_path2, 'w', encoding='utf-8') as f2:
        for i, line in enumerate(lines):
            if line.strip().isdigit():
                continue  # 跳过序号行
            elif '-->' in line:
                if not start_time:  # 记录第一个字幕块的开始时间
                    start_time = line.split(' --> ')[0]
                end_time = line.split(' --> ')[1]  # 更新结束时间
            elif not line.strip():
                if accumulated_text and is_sentence_complete(accumulated_text):
                    # 形成一个完整句子的字幕块
                    sentences = split_sentences(accumulated_text)
                    if is_translate:
                        if is_deepl:
                            translated_sentences = [translate_text_by_deepl(sentence) for sentence in sentences]
                        else:
                            translated_sentences = [translate_text_by_openai(sentence) for sentence in sentences]
                    else:
                        translated_sentences = ""
                    f.write(f"{block_number}\n{start_time} --> {end_time.strip()}\n")
                    for original in sentences:
                        f.write(f"{original}\n")
                        f2.write(f"{original} ")
                    #f.write("\n")  # 原文与译文之间添加一个空行分隔
                    # 再写入所有翻译文本句子
                    if translated_sentences:
                        for translated in translated_sentences:
                            f.write(f"{translated}\n")
                    f.write("\n")
                    block_number += 1
                    start_time = ''
                    accumulated_text = ''
                    end_time = ''
            else:
                accumulated_text += line.strip() + ' '
        
        # 处理文件末尾可能的未处理字幕块
        if accumulated_text and is_sentence_complete(accumulated_text):
            sentences = split_sentences(accumulated_text)
            if is_translate:
                if is_deepl:
                    translated_sentences = [translate_text_by_deepl(sentence) for sentence in sentences]
                else:
                    translated_sentences = [translate_text_by_openai(sentence) for sentence in sentences]
            else:
                translated_sentences = ""
            f.write(f"{block_number}\n{start_time} --> {end_time.strip()}\n")
            for original in sentences:
                f.write(f"{original}\n")
            #f.write("\n")  # 原文与译文之间添加一个空行分隔
            # 再写入所有翻译文本句子
            if translated_sentences:
                for translated in translated_sentences:
                    f.write(f"{translated}\n")
            f.write("\n")

    print(f"字幕文件已生成：{output_file_path}")



append_to_log_file("",True)
# 请将以下函数调用替换为您的SRT文件路径和输出文件路径
process_srt_file('input.srt', 'output.srt', 'output.txt')
"""
https://chat.openai.com/g/g-cKXjWStaE-python/c/cbc275b1-6a28-4188-8b9f-b2d8f369378d
"""