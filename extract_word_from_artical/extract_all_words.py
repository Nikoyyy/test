import re

is_repeat = True
#is_repeat = False

if 0:
    # 定义需要过滤的字符列表
    filter_chars = ['】', '[']

    # 打开原始文件并读取内容
    with open('input.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 筛选出不包含特定字符的行
    filtered_lines = [line for line in lines if not any(char in line for char in filter_chars)]

    # 使用相同的文件名打开文件，并在写入模式下覆盖原文件
    with open('input.txt', 'w', encoding='utf-8') as file:
        file.writelines(filtered_lines)

#以上为过滤原始文本，删除有问题的行
#=============================================================================================
        
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

# 打开input.txt文件并读取内容
with open('input.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 将文本分割为句子，这里简单地使用句号、问号和感叹号作为句子的分界
#sentences = re.split(r'\."|[.!?>()]', content)   # 正则表达式
#sentences = re.split(r'(?<=\.")|(?<=\?")|(?<=\?”)|(?<=[.!??>])', content)
#sentences = re.split(r'(?<=[.。!！?？>]["“”])|(?<=[.。!！?？>])', content)
#print(sentences)
    
regex_pattern = r'[.。!！?？>]\*+["“”]|[.。!！?？>]\*+|[.。!！?？>]["“”]|[.。!！?？>]'
sentences = split_text_by_regex(content, regex_pattern)

# 调整正则表达式以匹配紧邻的以星号(*)开头的单词作为一个词组
# 使用正则表达式 \*[\w+]+(?:\s+\*[\w+]+)* 来匹配一个或多个紧邻的以星号(*)开头的单词
#pattern_word = r'\*\w+(?:\s+\*\w+)*'
#pattern_word = r'\*\w+\*|\*(?:\w+\s+)+\w+\*'
#pattern_word = r'\*\w+\W?\*|\*(?:\w+\s+)+\w+\W?\*'
#pattern_word = r'\*\w+(?:[,.?!])?\*|\*(?:\w+\s+)+\w+(?:[,.?!])?\*'
#pattern_word = r'\*(?:\w+\s+)+\w+\*|\*(?:\w+\s+)+\w+(?:[,.?!]\*)|\*\w+\*|\*\w+(?:[,.?!]\*)'
pattern_word = r'\*(?:\w+\s+)+\w+(?:[,.?!])?\*|\*\w+(?:[,.?!])?\*'
#pattern_word = r'\*(?:\w+\s+)+\w+(?:[,.?!])?\*?|\*\w+\*|\*\w+(?:[,.?!])'

# 准备输出
output_lines = []

# 用于跟踪已处理单词，避免重复
processed_words = set()

for sentence in sentences:
    #print(sentence)
    # 查找当前句子中所有符合条件的词组
    matched_word_groups = re.findall(pattern_word, sentence)
    if matched_word_groups:
        
        print(matched_word_groups)
    # 对于找到的每个词组，记录词组（去除星号(*)）和句子
    for word_group in matched_word_groups:
        #clean_word_group = word_group.replace('*', '')  # 清理词组，去除"*"
        clean_word_group = re.sub(r'[^a-zA-Z\s]', '', word_group)
        if is_repeat:
            clean_sentence = sentence.replace('*', '').strip()  # 清理句子中的"*"并去除首尾空格
            # 将清理后的词组标记加粗显示
            highlighted_sentence = re.sub(re.escape(clean_word_group), f'***{clean_word_group}***', clean_sentence)
            output_lines.append(f"【{clean_word_group}】 -----> {highlighted_sentence}")
        else:
            if clean_word_group not in processed_words:
                processed_words.add(clean_word_group)  # 添加到已处理单词集合中
                clean_sentence = sentence.replace('*', '').strip()  # 清理句子中的"*"并去除首尾空格
                # 将清理后的词组标记加粗显示
                highlighted_sentence = re.sub(re.escape(clean_word_group), f'***{clean_word_group}***', clean_sentence)
                output_lines.append(f"【{clean_word_group}】 -----> {highlighted_sentence}")


# 写入到output.txt文件
with open('output.txt', 'w', encoding='utf-8') as file:
    for line in output_lines:
        file.write(line + '\n\n')
