import re
# 假设tiktoken库已经安装并可以导入
from openai import OpenAI
import tiktoken


def read_file_content(file_path: str) -> str:
    """读取并返回文件的内容。"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def count_chinese_characters(text: str) -> int:
    """计算文本中中文汉字的数量。"""
    return len(re.findall(r'[\u4e00-\u9fff]+', text))

def count_chinese_characters_2(str):
    hans_total = 0
    for s in str:
        # 中文字符其实还有很多，但几乎都用不到，这个范围已经足够了
        if '\u4e00' <= s <= '\u9fff':
            hans_total += 1
    return hans_total

def count_words(str):
    return len(re.findall(r'\b[a-zA-Z]+\b', str))


def num_tokens_from_string(string: str, model: str) -> int:
    """返回文本字符串中的token数量。"""
    token_encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(token_encoding.encode(string))
    return num_tokens



# 设置文件路径和模型
file_path = "token_cal.txt"
model = "gpt-3.5-turbo-0125"

# 读取文件内容
content = read_file_content(file_path)

# 计算所有字符数
total_chars = len(content)

# 计算所有中文汉字数
#total_chinese_characters = count_chinese_characters(content)
total_chinese_characters = count_chinese_characters_2(content)

total_words = count_words(content)

# 计算token数
total_tokens = num_tokens_from_string(content, model)

print(f"\n所有字符数: {total_chars}")
print(f"所有单词数: {total_words}")
print(f"所有中文汉字数: {total_chinese_characters}")
print(f"Token计数: {total_tokens}")