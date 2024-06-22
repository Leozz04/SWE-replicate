from openai import OpenAI
import os, yaml, time
from AI_AGent.secret_key import my_sk
from log import default_logger, get_logger
import Commands, Prompt

client = OpenAI(api_key=my_sk)


def add_message(role, content):
    conversation.append({"role": role, "content": content})

def environment_feedback():
    f=1


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
with open("temp_cmd.txt", "w+") as file:
    file.write(response_message)
add_message("assistant", response_message)



def get_response(prompt):
    add_message("user", prompt)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation
    )
    assistant_message = response.choices[0].message.content
    add_message("assistant", assistant_message)
    return assistant_message

