conversation = "hi"


def msg_record(message):
    with open("msg_record.txt", "a") as file:
        file.write(f"{message} \n")



msg_record(conversation)