from openai import OpenAI
import os, yaml, time
from AI_AGent.secret_key import my_sk
import Prompt
from Commands import Command

client = OpenAI(api_key=my_sk)


def add_message(role, content):
    conversation.append({"role": role, "content": content})


def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            log_content = file.read()
        return log_content
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None


def get_record_response(prompt):
    add_message("user", prompt)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation,
        max_tokens=300,
    )
    assistant_message = response.choices[0].message.content
    with open("temp_cmd.txt", "w+") as file:
        file.write(assistant_message)
    Command.msg_record(assistant_message)
    return assistant_message


log_file_path = "Info.log"
log_content = read_log_file(log_file_path)
conversation = [
    {"role": "system", "content": Prompt.System_Prompt},
]
with open("msg_record.txt", "w+") as file:
    file.write(" ")
response_message1 = get_record_response(Prompt.Instance_Prompt)
add_message("assistant", response_message1)
cmd, par = Command.locate_command()
Command.command_realize(cmd, par)
for i in range(0, 4):
    response_message = get_record_response(log_content)
    add_message("assistant", response_message)
    cmd, par = Command.locate_command()
    Command.command_realize(cmd, par)

