from openai import OpenAI
import os, yaml, time
from AI_AGent.secret_key import my_sk
from log import default_logger, get_logger
import Prompt
from Commands import Command

client = OpenAI(api_key=my_sk)


def add_message(role, content):
    conversation.append({"role": role, "content": content})


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


conversation = [
    {"role": "system", "content": Prompt.System_Prompt},
]
response_message1 = get_record_response(Prompt.Instance_Prompt)
add_message("assistant", response_message1)
cmd, par = Command.locate_command()
temp_cmd = Command.command_realize(cmd)(par)
response_message2 = get_record_response(temp_cmd)
print(response_message2)

