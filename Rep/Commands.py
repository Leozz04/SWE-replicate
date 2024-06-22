import os,re
from log import default_logger

Command_lib = """
read_file(arg:<file_path>):
    return the code file content with line number start with 
locate_line(arg:<line_num>):
    return the line located at line_num
"""


class Command(object):
    def __init__(self):
        self.name = '1'

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

    def command_realize(command):
        with open("temp_cmd.txt", "r") as file:
            conversation = file.readlines()
            for i, line in enumerate(conversation):
                if Command.contains_command(conversation[i], "command"):
                    if Command.contains_command(conversation[i + 1], command):
                        return getattr(Command, command)

    @staticmethod
    def locate_command():
        with open("temp_cmd.txt", "r") as file:
            conversation = file.readlines()
            for i, line in enumerate(conversation):
                if Command.contains_command(conversation[i], "command"):
                    temp_cmd = conversation[i + 1].split("(")[0]
                    parameter = str(re.findall(r"\((.*?)\)", conversation[i + 1])[0])
                    return temp_cmd, parameter

    def contains_command(message, command):
        return command in message

    def msg_record(message):
        with open("msg_record.txt", "a") as file:
            file.write(f"{message} \n")

    def environment_feedback(self):
        with open("temp_feedback.txt", "w") as file:
            file.write()


