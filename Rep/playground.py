import time
import io
import subprocess
proc = subprocess.Popen(['python','-u', 'fake_utility.py '],stdout=subprocess.PIPE)
i = 0
while True:
        print(hex(i)*512)
        i += 1
        time.sleep(0.5)

        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            with open("temp_feedback.txt", "w") as file:
                file.write(line)


