from openai import OpenAI
import os, yaml, time
from AI_AGent.secret_key import my_sk
from log import default_logger, get_logger
import Prompt
from Commands import Command

client = OpenAI(api_key=my_sk)


def add_message(role, content):
    conversation.append({"role": role, "content": content})




conversation = [
    {"role": "system", "content": Prompt.System_Prompt},
    {"role": "user", "content": Prompt.Instance_Prompt},
]
response = client.chat.completions.create(
    model="gpt-4o",
    messages=conversation,
    max_tokens=300,
)
response_message = response.choices[0].message.content
print(response_message)
with open("temp_cmd.txt", "w+") as file:
    file.write(response_message)

Command.msg_record(response_message)
add_message("assistant", response_message)
cmd, par = Command.locate_command()
print(par)
temp_cmd = Command.command_realize(cmd)(par)
