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
    code_execution_config={"work_dir": "web","use_docker": False},
)
Friend = autogen.AssistantAgent(
    name="Friend",
    llm_config=llm_config,
    system_message="You are a great friend. You can do normal conversation with him  and talk about general things",
)
Ccoder = autogen.AssistantAgent(
    name="Ccoder",
    llm_config=llm_config,
    system_message="You are an expert C++ coder. Write Expert C++ code considering all edge cases.",
    code_execution_config={"work_dir": "web","use_docker": False},
)
Coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    system_message="You are a general expert coder and can write code in any language",
    code_execution_config={"work_dir": "web","use_docker": False},
)
Critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="You will analyze the code and then determine if it is Good, or needs to be modified. You will also check if the code is running correctly or not. You will also consider all edge cases and then guide other agents to build better codet",
    code_execution_config={"work_dir": "web","use_docker": False},
)
Chat = autogen.AssistantAgent(
    name="Chat",
    llm_config=llm_config,
    system_message="You will collect all the data from various agents and then generate a good conversation result"
)
CTO = autogen.AssistantAgent(
    name="CTO",
    llm_config=llm_config,
    system_message="You are the head of the coding department. You have to make sure the work is good and correct."
)
Advisor = autogen.AssistantAgent(
    name="Advisor",
    llm_config=llm_config,
    system_message="You are wise, you shall guide him whenever he is confused. Give him the correct advice."
)

Jarvis = UserProxyAgent(
    name="Jarvis",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web", "use_docker": False},
    llm_config=llm_config,
    system_message="""Reply 'TERMINATE' if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)
Coding = autogen.GroupChat(agents=[Critic,PythonCoder,Ccoder,Coder,CTO,Friend,Chat,CTO,Chat,Advisor,Jarvis], messages=[], max_round=50, speaker_selection_method="auto")

Coding_manager = autogen.GroupChatManager(groupchat=Coding, llm_config = llm_config)

Conversation = autogen.GroupChat(agents=[Critic,PythonCoder,Ccoder,Coder,CTO,Friend,Chat,CTO,Chat,Advisor,Jarvis], messages=[], max_round=50, speaker_selection_method="auto")

Conversation_manager = autogen.GroupChatManager(groupchat=Conversation, llm_config = llm_config)

Central_Processing_unit = autogen.GroupChat(agents=[Critic,PythonCoder,Ccoder,Coder,CTO,Friend,Chat,CTO,Chat,Advisor,Jarvis], messages=[], max_round=50, speaker_selection_method="auto")

Central_Processing_unit_manager = autogen.GroupChatManager(groupchat=Central_Processing_unit, llm_config = llm_config)

while True:
    Query=input("Enter Query:")
    Jarvis.initiate_chat(Central_Processing_unit_manager,  message=Query)