from key import personal_openai_key
from openai import OpenAI

client = OpenAI(api_key=personal_openai_key)
openai_api_key = personal_openai_key

conversation = [
    {"role": "system", "content": "You are a helpful assistant. You can read programming files line by line as well as information from IDE. After careful thinking, you only need to tell me which line should be replaced with what."}
]


def add_message(role, content):
    conversation.append({"role": role, "content": content})


def get_response(prompt):
    add_message("user", prompt)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation
    )
    assistant_message = response.choices[0].message.content
    add_message("assistant", assistant_message)
    return assistant_message


file1 = open(r"C:\Python_OpenAI_API\SWE_Replica\TestFile\AnimalList.java", 'r')
input_file = file1.readlines()
user_first_prompt = input("The file was uploaded, please tell me what's wrong with it: ")
input_file.append(user_first_prompt)
input_file_content = "\n".join(input_file)
response = get_response(input_file_content)
print(response)

counter = 0
condition = True

while condition:
    user_prompt = input("Please keep going: ")
    response = get_response(user_prompt)
    print(response)
    counter += 1
    if counter >= 50:
        condition = False

