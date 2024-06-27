import logging
import os, re, subprocess
from log import log

# Command lib for agent to read
Command_lib = """
read_file(<file_path>)
    Rule: return the code file content with line number start with 0
          argument need to be formatted as readfile(<file_path>) rather than readfile("<file_path>") 
create_file(<file_path>)
    Rule: Create a file in the <file_path> inputted
write_file(<file_path>, <message>)
    Rule: This method contains two argument. Input the <file_path> containing the file you want to edit, and the message you want to write to the file.
run_py(<file_path>)
    Rule: Run the specific python file inputted as <file_path>
          Will return "Run complete, No error" If the file can successfully compile and run
          Will return error message begin with "Error: " if error occur
search_dir(<dir_path>)
    Rule: Return a list containing all file inside the requested <dir_path>
          Directories inside the directory is listed as name only: 'Example', Example as ['Test.py', 'Example_directory']
          Example of <dir_path>: "/Users/Leo/Documents/AI_Agent/SWE-replicate/Rep"
          
"""


# object class Command containing all the commands agent needed to call
class Command(object):
    def __init__(self):
        self.name = 'Command Lib'

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
                    log.info(numbered_line)
        except Exception as e:
            log.error(f"Failed to read file {file_path}: {e}")
            return f"Error: Could not read the file {file_path}."
        return "\n".join(numbered_lines)


    def command_realize(command, parameters):
        log.info(f"Start command {command}")
        with open("temp_cmd.txt", "r") as file:
            conversation = file.readlines()
            for i, line in enumerate(conversation):
                if Command.contains_command(conversation[i], "cmd"):
                    if Command.contains_command(conversation[i + 1], command):
                        cmd = getattr(Command, command)
                        i = parameters[0].count(',')
                        parameter = parameters[0].split(',', i)
                        cmd(*parameter)
                        log.info(f"End command {command}")

    @staticmethod
    def locate_command():
        with open("temp_cmd.txt", "r") as file:
            conversation = file.readlines()
            for i, line in enumerate(conversation):
                if Command.contains_command(conversation[i], "cmd"):
                    temp_cmd = conversation[i + 1].split("(")[0]
                    parameters = re.findall(r"\((.*?)\)", conversation[i + 1])
                    return temp_cmd, parameters

    def contains_command(message, command):
        return command in message

    def create_file(file_path):
        file = open(f"{file_path}", "w")
        return file

    def write_file(file_path, message):
        with open(f"{file_path}", "w+") as file:
            file.write(message)

    def msg_record(message):
        with open("msg_record.txt", "a") as file:
            file.write(f"{message} \n")

    def search_dir(dir_path):
        return os.listdir(dir_path)

    def run_py(file_path):
        log.info(f"Start running {file_path}")
        try:
            process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                log.error(stderr.decode())

        except Exception:
            log.exception("Exception")


