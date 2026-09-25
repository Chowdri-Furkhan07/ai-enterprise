from autogen.agents import assistant, user, researcher, retriever, reporter, group_chat, manager
import json

def chat(query, use_multi_agent=False):
    """
    Start a chat with the AI assistant.
    
    Args:
        query: The user's question
        use_multi_agent: If True, use multi-agent group chat
    
    Returns:
        The AI's response
    """
    if use_multi_agent:
        # Use group chat for complex queries
        user.initiate_chat(manager, message=query)
        return group_chat.messages
    else:
        # Use single assistant agent
        user.initiate_chat(assistant, message=query)
        return assistant.last_message()["content"]


def chat_with_specialist(query, specialist="researcher"):
    """
    Chat with a specific specialist agent.
    
    Args:
        query: The user's question
        specialist: One of 'researcher', 'retriever', or 'reporter'
    
    Returns:
        The specialist's response
    """
    specialist_agents = {
        "researcher": researcher,
        "retriever": retriever,
        "reporter": reporter
    }
    
    agent = specialist_agents.get(specialist.lower())
    if not agent:
        return {"error": f"Unknown specialist: {specialist}"}
    
    user.initiate_chat(agent, message=query)
    return agent.last_message()["content"]


def multi_agent_research(query):
    """
    Use the full multi-agent team for complex queries.
    
    Args:
        query: The user's complex question requiring multiple specialists
    
    Returns:
        Combined response from all specialists
    """
    # Start group chat
    group_chat.reset()
    user.initiate_chat(manager, message=query)
    
    # Collect all responses
    responses = []
    for msg in group_chat.messages:
        responses.append({
            "agent": msg.get("name"),
            "content": msg.get("content")
        })
    
    return {"responses": responses}


# Convenience functions
def research_chat(query):
    """Chat with the research specialist"""
    return chat_with_specialist(query, "researcher")


def retrieve_chat(query):
    """Chat with the document retriever specialist"""
    return chat_with_specialist(query, "retriever")


def report_chat(query):
    """Chat with the report generator specialist"""
    return chat_with_specialist(query, "reporter")

