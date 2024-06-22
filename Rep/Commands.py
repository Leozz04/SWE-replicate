import os
from log import default_logger

Command_lib = """
read_file(arg:<file_path>):
    return the code file content with line number start with 
locate_line(arg:<line_num>):
    return the line located at line_num
"""


def msg_record(message):
    with open("msg_record.txt", "a") as file:
        file.write(f"{message} \n")


def locate_command(conversation, command):
    if contains_command(conversation, command):
        with open("temp_cmd.txt", "w+") as file:
            command_line = file.readline()
            command_line.strip(" ")
    else:
        print("No command found")
        return

            


def contains_command(message, command):
    return command in message
def read_file(file_path):
    if not os.path.isfile(file_path):
        return f"Error: The file {file_path} does not exist."
    numbered_lines = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                numbered_line = f"{i}: {line}"
                numbered_lines.append(numbered_line)
                default_logger.info(numbered_line)
    except Exception as e:
        default_logger.error(f"Failed to read file {file_path}: {e}")
        return f"Error: Could not read the file {file_path}."
    return "\n".join(numbered_lines)

def locate_line(line_num, file_path):
    with open(file_path, 'r') as file:
        line = file.readline(line_num)
    return line

def fix_line(og_line):
    f=1

def replace_line(line):
    f=1



