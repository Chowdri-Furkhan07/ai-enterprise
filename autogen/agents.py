import os
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from core.llm import LLM

# Initialize LLM
llm = LLM()

# Create assistant agent (AI assistant)
assistant = AssistantAgent(
    name="AI_Assistant",
    llm=llm.generate,
    system_message="""
    You are an Enterprise AI Assistant. You help users with:
    - Research and analysis
    - Document retrieval
    - Database queries
    - Report generation
    
    Use the provided tools and context to answer user questions accurately.
    """
)

# Create user proxy agent (human-in-the-loop)
user = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=3,
    code_execution_config={"work_dir": "coding"}
)

# Create additional specialist agents
researcher = AssistantAgent(
    name="Researcher",
    llm=llm.generate,
    system_message="""
    You are a Research Specialist. Your role is to:
    - Research topics thoroughly
    - Provide detailed insights and analysis
    - Stay current with best practices
    
    Always provide comprehensive, well-researched answers.
    """
)

retriever = AssistantAgent(
    name="Retriever",
    llm=llm.generate,
    system_message="""
    You are a Document Retrieval Specialist. Your role is to:
    - Find relevant documents from the knowledge base
    - Extract relevant information
    - Present findings clearly
    
    Help users find the information they need.
    """
)

reporter = AssistantAgent(
    name="Reporter",
    llm=llm.generate,
    system_message="""
    You are a Report Generation Specialist. Your role is to:
    - Create well-structured reports
    - Tailor content to different roles (admin, analyst, viewer)
    - Present data clearly and professionally
    
    Generate accurate and professional reports.
    """
)

# Create group chat for multi-agent collaboration
group_chat = GroupChat(
    agents=[user, assistant, researcher, retriever, reporter],
    speaker_selection_method="round_robin",
    max_round=10
)

# Create group chat manager
manager = GroupChatManager(
    groupchat=group_chat,
    llm=llm.generate
)

