"""
Unique Words Extractor

This Python script reads all words from 'input.txt', filters out any word that contains numbers or special characters, and removes duplicates. It retains only alphabetically composed words. The resulting unique words are then written to 'inputOpt.txt', one word per line. This process ensures that the output file contains a clean list of unique, purely alphabetical words from the input file, suitable for applications requiring such filtered datasets.
"""
import re

# 读取input.txt文件并使用正则表达式匹配只包含字母的单词
with open('textFile/input.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    words = re.findall(r'\b[a-zA-Z]+\b', text)

# 使用集合去除重复单词，同时保留原有顺序
unique_words = []
seen = set()
for word in words:
    if word not in seen:
        unique_words.append(word)
        seen.add(word)

# 将去重后的单词列表写入inputOpt.txt文件，每个单词一行
with open('textFile/inputOpt.txt', 'w', encoding='utf-8') as file:
    for word in unique_words:
        file.write(word + '\n')
