from openai import OpenAI
from AI_AGent.secret_key import my_sk
import Prompt
client = OpenAI(api_key=my_sk)
Execute_assistant = client.beta.assistants.create(
    instructions=Prompt.Executor_Prompt,
    name="SWE-Executor",
    model="gpt-4o",
)
Exe_id = Execute_assistant.id
Feedback_assistant = client.beta.assistants.create(
    instructions=Prompt.Feedbacker_Prompt,
    name="SWE-Feedbacker",
    model="gpt-4o",
)
Feed_id = Feedback_assistant.id