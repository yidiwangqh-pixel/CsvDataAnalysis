import openai
import yaml
import json
import io
import sys
import pandas as pd

config_file_path = 'config.yaml'

message_history = []

with open(config_file_path, 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
file_path = config.get('file_path')
my_api_key = config.get('api_key')
my_system_prompt = config.get('system_prompt')
client = openai.OpenAI(api_key=my_api_key, base_url="https://api.deepseek.com")

csv_data = pd.read_csv(file_path)
csv_data_info = {
    "行数": len(csv_data),
    "列数": len(csv_data.columns),
    "列名": list(csv_data.columns),
    "数据类型": csv_data.dtypes.to_dict(),
    "前十行数据": csv_data.head(10).to_dict('records')
}

user_content = "这是CSV文件概略信息：{csv_data_info}。".format(csv_data_info=csv_data_info)

message_history.append({"role": "system", "content": my_system_prompt})
message_history.append({"role": "user", "content": user_content})

response = client.chat.completions.create(
    # DeepSeek-V3.1 thinking model
    model='deepseek-reasoner', 
    messages=message_history,
    # json output
    response_format={"type": "json_object"},
    temperature=0.1,
    stream=False
)

message_history.append({"role": "assistant", "content": response.choices[0].message.content})
print(f"\nAssistant's response: {response.choices[0].message.content}")

# wait for user question
while True:
    user_content = input("\nPlease enter your question (or 'quit' to exit): ")
    if user_content.lower() == 'quit':
        break
        
    message_history.append({"role": "user", "content": user_content})
    # print(message_history)

    response = client.chat.completions.create(
        model='deepseek-reasoner',
        messages=message_history,
        response_format={"type": "json_object"},
        temperature=0.1,
        stream=False,
    )
    
    message_history.append({"role": "assistant", "content": response.choices[0].message.content})
    # print(f"\nAssistant's response: {response.choices[0].message.content}")

    while True:
        python_code = json.loads(response.choices[0].message.content)
        python_code_str = python_code.get("Python代码", "")
        # print python code
        print(f"\nPython代码:\n[\n{python_code_str}\n]")
        try:
            output = io.StringIO()
            sys.stdout = output

            exec(python_code_str)

            sys.stdout = sys.__stdout__
            break
        except Exception as e:
            sys.stdout = sys.__stdout__
            error_message = f"Error executing Python code: {e}"
            # print error message
            print(f"\n错误信息:\n{error_message}")
            message_history.append({"role": "user", "content": "你上一次返回的代码报错, 报错信息为{error_message}, 请据此重新修改代码".format(error_message=error_message)})
            response = client.chat.completions.create(
                model='deepseek-reasoner',
                messages=message_history,
                response_format={"type": "json_object"},
                temperature=0.1,
                stream=False,
            )
            message_history.append({"role": "assistant", "content": response.choices[0].message.content})
            # print(f"Assistant's response: {response.choices[0].message.content}")

    # run code result
    code_result = output.getvalue()
    print(f"\n执行结果:\n{code_result}")
    message_history.append({"role": "user", "content": "这是代码运行时各变量的值：{code_result}, 请你综合之前的历史以及代码信息从这些变量中找出最终结果，对结果进行分析从而回答我提出的上一个与代码无关的问题".format(code_result=code_result)})
    response = client.chat.completions.create(
        model='deepseek-reasoner',
        messages=message_history,
        response_format={"type": "json_object"},
        temperature=0.1,
        stream=False,
    )
    message_history.append({"role": "assistant", "content": response.choices[0].message.content})
    #print(f"Assistant's response: {response.choices[0].message.content}")
    analysis_result = json.loads(response.choices[0].message.content)
    print("\n最终解释:\n")
    print(analysis_result.get("思考过程", ""))
