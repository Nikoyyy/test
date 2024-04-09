import re
with open('input.txt', 'r', encoding='utf-8') as file:
    text = file.read()
def split_text_by_regex(text, regex_pattern):
    """
    根据给定的正则表达式分割文本，并保留分隔符。
    
    :param text: 要分割的文本
    :param regex_pattern: 用于分割文本的正则表达式，可以匹配一个或多个分隔符
    :return: 分割后的文本列表
    """
    # 匹配正则表达式，同时保留分隔符
    parts = re.split(f'({regex_pattern})', text)
    print(parts)
    # 过滤空字符串并合并分隔符及其后的文本
    parts = [part for part in parts if part]  # 移除空字符串
    result = []
    # 合并分隔符及其紧跟的文本片段
    for i in range(0, len(parts), 2):
        # 因为分隔符与文本是分开的，所以需要合并
        result.append(parts[i] if i + 1 == len(parts) else parts[i] + parts[i + 1])
    return result

# 使用正则表达式来分割文本，这个正则表达式匹配".*"或"."
regex_pattern = r'[.。!！?？>]\*["“”]|[.。!！?？>]\*|[.。!！?？>]["“”]|[.。!！?？>]'
split_by_regex = split_text_by_regex(text, regex_pattern)
print(split_by_regex)

