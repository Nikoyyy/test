####      读取input文件里所有单词丢给gpt进行格式化处理，增加音标，中文释义与造句

from openai import OpenAI
import time
import json
import tiktoken
import re


# 初始化 OpenAI 客户端
client = OpenAI()
"""gpt-3.5-turbo      """
model = "gpt-3.5-turbo"
encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model(model)
expected_tokens = 0
readLineOnce = 30
expected_output_lines = 30
stringtest = """将以上每个单词翻译成中文，并用英文造个句子,展示英文与中文，参照下面的例子
late - /leɪt/ - 迟到 - The train arrived late at the station due to a technical issue.
interrupt - /ɪntəˈrʌpt/ - 打断 - We had to interrupt our picnic because of the sudden rainstorm.
wander - /ˈwɒndər/ - 漫步 - They decided to wander through the city and explore its hidden gems."""


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
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



# 打开 input.txt 文件以读取内容
with open('input.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 获取文件的总行数
total_lines = len(lines)

# 初始化读取的行数索引
start_line = 0

while start_line < total_lines:
    # 计算剩余行数
    remaining_lines = total_lines - start_line

    # 确定这次读取的行数
    read_lines = min(readLineOnce, remaining_lines)

    # 读取下一批行
    lines_batch = lines[start_line:start_line + read_lines]
    batch_text = ''.join(lines_batch)

    #print("error:" + lines_batch)

    print(f"正在处理从行 {start_line + 1} 到行 {start_line + read_lines} 的内容...")  # 调试信息

    # 初始化回复内容和重试计数
    message_content = None
    retry_count = 0

    targetStr = batch_text +stringtest

    tokens = num_tokens_from_string(targetStr, "cl100k_base")
    print("input tokens = " + str(tokens))
    print("input content = "+ targetStr)


    # 尝试发送请求直到成功获取回复或达到重试次数上限
    while message_content is None : #and retry_count < max_retries:
        try:
            print("-----1\n")
            completion = client.chat.completions.create(
                model=model,
                #response_format={ "type": "json_object" },
                messages=[
                    {"role": "user", "content": targetStr}
                ],
                #max_tokens=100
            )

            print("-----2\n")

            # 获取回复中的消息
            message_content = completion.choices[0].message.content if completion.choices[0].message else None

            print(json.dumps(json.loads(completion.model_dump_json()), indent=4))
            
            print("-----3\n")

            if message_content:
                break  # 如果成功获取回复，退出循环

        except Exception as e:
            print(f"Exception: {e}")
            print(f"API 调用失败，正在进行第 {retry_count + 1} 次重试...")
            retry_count += 1
            time.sleep(1)  # 简单的延时，避免过快重试
        

    # 检查消息是否成功接收
    if message_content:
        tokens = num_tokens_from_string(message_content, "cl100k_base")
        print("接受到的 tokens = " + str(tokens))

        #test code
        with open('test.txt', 'a', encoding='utf-8') as output_file:
            output_file.write("input:\n" + targetStr + "\n\n")
            output_file.write("output:\n" + message_content + "\n\n\n\n")

        target_text, target_text_line_count = remove_empty_lines_and_count(message_content)

        print("优化后行数 = " + str(target_text_line_count))
        
        #检查收到的tokens数量是否符合预期
        if tokens > expected_tokens:

            if(target_text_line_count == expected_output_lines):
                # 追加信息到文件
                with open('words.txt', 'a', encoding='utf-8') as output_file:
                    output_file.write(target_text + "\n")  # 确保追加内容后有换行符

                # 读取文件内容并移除空行
                with open('words.txt', 'r', encoding='utf-8') as file:
                    output_lines = file.readlines()
                    output_lines = [output_line for output_line in output_lines if output_line.strip()]

                # 重写文件，不包含空行
                with open('words.txt', 'w', encoding='utf-8') as file:
                    file.writelines(output_lines)

                print("回复已成功追加到 'words.txt' 并清除了所有空行")  # 调试信息

                # 更新读取的行数索引
                start_line += read_lines
            else:
                print("lines != " + str(expected_output_lines))
        else:
            print("tokens数量不符合预期")
    else:
        print("未能成功接收到消息")

    # 如果已处理所有行，则结束循环
    if start_line >= total_lines:
        print("所有行已处理完毕")  # 调试信息
        break



