import subprocess


def execute_shell_command(command, *args):
    cmd = ["bash", "file_operations.sh", command] + list(args)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        return {"error": result.stderr.decode('utf-8')}
    return {"output": result.stdout.decode('utf-8')}
