from openai import OpenAI
from AI_AGent.secret_key import my_sk

client = OpenAI(api_key=my_sk)

def openai_assistant(prompt, command, args):
    response = OpenAI.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        functions=[
            {
                "name": command,
                "description": f"Executes the command {command} with arguments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "args": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["args"],
                },
            }
        ],
        function_call={"name": command, "arguments": {"args": args}}
    )

    return response.choices[0].message['function_call']

def assistant_command_handler(command, args):
    result = execute_shell_command(command, *args)
    return result

def main():
    prompt = "Find file example.txt in /home/user/documents"
    command = "find_file"
    args = ["example.txt", "/home/user/documents"]

    api_response = openai_assistant(prompt, command, args)
    result = assistant_command_handler(command, api_response['arguments']['args'])
    print(result)

if __name__ == '__main__':
    main()
