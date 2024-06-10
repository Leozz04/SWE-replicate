from openai import OpenAI
import os, yaml
from AI_AGent.secret_key import my_sk
from log import default_logger, get_logger
import Commands
client = OpenAI(api_key=my_sk)
with open("Prompt.yaml") as stream:
    try:
        P = yaml.safe_load(stream)
        system_prompt = P['system_template']
    except yaml.YAMLError as exc:
        print(exc)

def chat_with_openai(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300,
        model="gpt-4o"
    )
    return response.choices[0].message.content.strip()


# Main function to read file and interact with OpenAI
def openai_file_assistant(file_path):
    file_content = Commands.read_local_file(file_path)
    if "Error" in file_content:
        return file_content

    prompt = f"The following is the content of the file {file_path}:\n\n{file_content}\n\n. Identifie which line cause the error."
    response = chat_with_openai(prompt)
    return response


# Example usage
if __name__ == "__main__":
    file_path = '/Users/Leo/Documents/AI_Agent/SWE-replicate/Rep/file_inter.py'
    assistant_response = openai_file_assistant(file_path)
    print(assistant_response)
