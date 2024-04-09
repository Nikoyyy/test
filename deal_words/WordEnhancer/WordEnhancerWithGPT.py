####      读取  textFile/input.txt  文件里所有单词丢给gpt进行格式化处理，增加音标，中文释义与造句

from openai import OpenAI
import time
import json
import tiktoken
import re
from datetime import datetime
import shutil #文件操作

# 初始化 OpenAI 客户端
client = OpenAI()
"""gpt-3.5-turbo     gpt-3.5-turbo-1106   gpt-3.5-turbo-0125 """
model = "gpt-3.5-turbo-0125"
#encoding = tiktoken.get_encoding("cl100k_base")
#token_encoding = tiktoken.encoding_for_model(model)
expected_tokens = 0
readLineOnce = 100
excute_count = 0
input_file = "textFile/inputOpt.txt"
output_file = 'textFile/output.txt'
log_file = "textFile/log.log"

stringtest = """将以上每个单词翻译成中文，并用英文造个句子,展示英文与中文，参照下面的例子
late - /leɪt/ - 迟到 - The train arrived late at the station due to a technical issue.
interrupt - /ɪntəˈrʌpt/ - 打断 - We had to interrupt our picnic because of the sudden rainstorm.
wander - /ˈwɒndər/ - 漫步 - They decided to wander through the city and explore its hidden gems."""

def append_to_log_file(text):
    # 打开或创建log.log文件，以追加模式写入
    with open(log_file, 'a', encoding='utf-8') as file:
        # 将文本追加到文件中
        file.write(text + "\n")

def num_tokens_from_string(string: str, model: str) -> int:
    """Returns the number of tokens in a text string."""
    #encoding = tiktoken.get_encoding(encoding_name)
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def remove_empty_lines_and_count(s):
    # 分割字符串到行
    lines = s.split('\n')
    # 使用正则表达式移除空白行
    non_empty_lines = [line for line in lines if line.strip() != ""]
    # 将剩余的行重新组合成一个字符串
    result = "\n".join(non_empty_lines)
    # 计算行数
    line_count = len(non_empty_lines)
    return result, line_count

def replace_lines(input_string, filename=output_file):
    # 将输入字符串分割成行
    input_lines = input_string.strip().split('\n')

    # 读取文件内容
    with open(filename, 'r', encoding='utf-8') as file:
        file_lines = file.readlines()

    # 创建一个字典来存储输入字符串的每一行，键是每行的第一个单词
    input_dict = {line.split()[0]: line for line in input_lines if line.split() and line.split()[0].isalpha()}

    # 遍历文件的每一行
    for i, line in enumerate(file_lines):
        words = line.split()
        if words and words[0] in input_dict:
            # 如果找到匹配，替换该行
            file_lines[i] = input_dict[words[0]] + '\n'

    # 将更新后的内容写回文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(file_lines)



with open('UniqueWordsExtractor.py',encoding='utf-8') as file:
    exec(file.read())

with open(log_file, 'w', encoding='utf-8') as file:
    pass


# 复制文件
shutil.copyfile(input_file, output_file)

while True:

    excute_count = excute_count + 1
    append_to_log_file(str(excute_count) + " time :")

    with open(output_file, 'r', encoding='utf-8') as file:
        file_lines = file.readlines()

    remain_lines = [line for line in file_lines if len(line.split()) == 1]
    append_to_log_file("remain lines : " + str(len(remain_lines)))

    if len(remain_lines) == 0 :
        break

    # 读取下一批行
    lines_batch = remain_lines[:readLineOnce]
    batch_text = ''.join(lines_batch)

    # 初始化回复内容和重试计数
    message_content = None
    retry_count = 0

    targetInput = batch_text + stringtest
    append_to_log_file(targetInput)

    tokens = num_tokens_from_string(targetInput, model)
    print("\ninput tokens = " + str(tokens))

    # 尝试发送请求直到成功获取回复或达到重试次数上限
    while message_content is None : #and retry_count < max_retries:
        try:
            # 记录开始时间
            start_time = datetime.now()
            print("start request !")
            completion = client.chat.completions.create(
                model=model,
                #response_format={ "type": "json_object" },
                messages=[
                    {"role": "user", "content": targetInput}
                ],
                #max_tokens=100
            )

            """
                    {"role": "system", s"content": "You are a helpful assistant."},
                    {"role": "user", "content": "Who won the world series in 2020?"},
                    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                    {"role": "user", "content": "Where was it played?"}
            """

            # 记录结束时间
            end_time = datetime.now()
            # 计算时间差
            time_diff = end_time - start_time
            print(f"耗时: {time_diff.seconds}s {time_diff.microseconds // 1000}ms")

            # 获取回复中的消息
            message_content = completion.choices[0].message.content if completion.choices[0].message else None
            
            print(f"finish_reason = {completion.choices[0].finish_reason}")

            if message_content:
                #print(json.dumps(json.loads(completion.model_dump_json()), indent=4))
                append_to_log_file("\n耗时: " + str(time_diff.seconds) + "s " + str(time_diff.microseconds // 1000) + "ms")
                append_to_log_file(json.dumps(json.loads(completion.model_dump_json()), indent=4) )
                append_to_log_file("\n" +"origin output:\n" +  message_content )
                break  # 如果成功获取回复，退出循环

        except Exception as e:
            print(f"Exception: {e}")
            print(f"API 调用失败，正在进行第 {retry_count + 1} 次重试...")
            retry_count += 1
            time.sleep(1)  # 简单的延时，避免过快重试
        

    # 检查消息是否成功接收
    if message_content:
        tokens = num_tokens_from_string(message_content, model)
        print("接受到的 tokens = " + str(tokens))

        target_text, target_text_line_count = remove_empty_lines_and_count(message_content)

        print("优化后行数 = " + str(target_text_line_count))
        append_to_log_file("\n" + "优化后行数 = " + str(target_text_line_count) + "\n")
        append_to_log_file(target_text + "\n")
        
        #检查收到的tokens数量是否符合预期
        if tokens > expected_tokens:
            replace_lines(target_text,output_file)
        else:
            print("tokens数量不符合预期")
    else:
        print("未能成功接收到消息")