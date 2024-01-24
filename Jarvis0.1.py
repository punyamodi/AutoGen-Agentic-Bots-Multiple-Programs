import autogen

from autogen import UserProxyAgent

from dotenv import load_dotenv

load_dotenv()

# ----------------- #
config_list=[
        {
            "model": "chatglm2-6b",
            "base_url": "http://localhost:1234/v1",
            "api_type": "open_ai",
            "api_key": "NULL",
        }
    ]

llm_config={
  "seed": 42,
  "config_list": config_list,
  "temperature": 0
}

PythonCoder = autogen.AssistantAgent(
    name="PythonCoder",
    llm_config=llm_config,
    system_message="You are an expert Python Coder, write efficeient code. Also Always consider all edge cases.",
    description=" You are the best coder in the company, you will write code in multiple languages"
)
Friend = autogen.AssistantAgent(
    name="Friend",
    llm_config=llm_config,
    system_message="You are a great friend. You can do normal conversation with him  and talk about general things",
    description=" You are a friend, you will generally converse with the person"
)
Critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="You will analyze the code and then determine if it is Good, or needs to be modified. You will also check if the code is running correctly or not. You will also consider all edge cases and then guide other agents to build better codet",
    description=" You are supposed to criticaly analyze the code and suggest improvments "

)
CTO = autogen.AssistantAgent(
    name="CTO",
    llm_config=llm_config,
    system_message="You are the head of the coding department. You have to make sure the work is good and correct.",
    description=" You are the head of the technical coding department"
)

Jarvis = UserProxyAgent(name="Jarvis",
                        human_input_mode="NEVER",
                        max_consecutive_auto_reply=10,
                        system_message="""Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
                        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
                        )
Coding = autogen.GroupChat(agents=[Critic,PythonCoder,CTO], messages=[], max_round=50, speaker_selection_method="auto",allow_repeat_speaker=False)
Coding_manager = autogen.GroupChatManager(groupchat=Coding, llm_config = llm_config)
Hello = autogen.GroupChat(agents=[CTO,Jarvis,Friend,Critic,PythonCoder], messages=[], max_round=50, speaker_selection_method="auto",allow_repeat_speaker=False)
Hello_manager = autogen.GroupChatManager(groupchat=Hello, llm_config = llm_config)

while True:
    query=input("Enter task:")
    Jarvis.initiate_chat(Hello_manager,  message=query)
