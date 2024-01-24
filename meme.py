import os
os.environ["AUTOGEN_USE_DOCKER"] = "False"

import autogen

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

assistant = autogen.AssistantAgent(
  name="CTO",
  llm_config=llm_config,
  system_message="Chief technical officer of a tech company"
)

user_proxy = autogen.UserProxyAgent(
  name="user_proxy",
  human_input_mode="NEVER",
  max_consecutive_auto_reply=10,
  is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
  code_execution_config={"work_dir": "web","use_docker": False},
  llm_config=llm_config,
  system_message="""Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)


task=input("Enter task:")
user_proxy.initiate_chat(assistant, message=task)

