import os
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# -------------------------------
# Configuration
# -------------------------------

# Set your OpenAI API key here
from dotenv import load_dotenv
load_dotenv() # 🔑 REPLACE THIS

llm_config = {
    "model": "gpt-4.1-nano",
    "api_key": os.environ["OPENAI_API_KEY"],
    "max_tokens": 1024,      # Critical: limits response length
    "temperature": 0,     
}

# -------------------------------
# Define Specialized Agents
# -------------------------------

# 1. Minute-Taking Agent
minute_taker = AssistantAgent(
    name="Minute_Taker",
    system_message="""
    You are the Minute-Taking Agent.
    Your job is to summarize discussions in clear, professional English.
    After the meeting, produce a structured summary including:
    - Topic
    - Key decisions
    - Action items (with owner and deadline if mentioned)
    - Next meeting time (if decided)
    Do not add opinions. Be concise and factual.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# 2. Management Agent
management_agent = AssistantAgent(
    name="Management_Agent",
    system_message="""
    You are the Management Agent.
    Focus on project goals, timelines, scope, and stakeholder needs.
    Speak in English only.
    Suggest deadlines, flag risks, and keep discussion aligned with business value.
    Keep responses under 80 words.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# 3. Technical Agent
technical_agent = AssistantAgent(
    name="Technical_Agent",
    system_message="""
    You are the Technical Agent.
    Discuss architecture, implementation, and technology choices.
    Use English only.
    Recommend tools (e.g., React, Node, OAuth2, Docker) and explain trade-offs.
    Stay practical and concise.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# 4. Quality Agent
quality_agent = AssistantAgent(
    name="Quality_Agent",
    system_message="""
    You are the Quality Assurance Agent.
    Focus on testing, reliability, edge cases, and security.
    Ask about test coverage, failure modes, and monitoring.
    Respond in clear English.
    Suggest QA practices and automation.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# 5. User Proxy (Meeting Moderator)
user_proxy = UserProxyAgent(
    name="Moderator",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    code_execution_config=False,
    system_message="""
    You are the Meeting Moderator.
    Start the meeting with the agenda.
    Invite agents in order: Management_Agent, Technical_Agent, Quality_Agent.
    Then ask Minute_Taker to summarize.
    End by saying 'TERMINATE'.
    Conduct the entire meeting in English.
    """
)

# -------------------------------
# Start the Meeting in Terminal
# -------------------------------

if __name__ == "__main__":
    print("\n" + "═" * 70)
    print("🚀 AI MEETING AGENTS FOR SOFTWARE DEVELOPMENT")
    print("│")
    print("│  Agents: Management • Technical • Quality • Minute-Taker")
    print("│  Language: English only | Token limit: 1024 per request")
    print("│  Powered by AutoGen + OpenAI")
    print("═" * 70)

    # Get agenda from user input
    print("\n📋 Enter the meeting agenda (e.g., 'Design a login system with 2FA'):")
    agenda = input("👉 ").strip()

    if not agenda:
        print("❌ No agenda provided. Exiting.")
        exit()

    print("\n🔄 Starting meeting simulation...\n")
    print(f"📌 Agenda: {agenda}\n")

    # Build group chat
    agents = [user_proxy, minute_taker, management_agent, technical_agent, quality_agent]
    groupchat = GroupChat(
        agents=agents,
        messages=[],
        max_round=6,
        speaker_selection_method="round_robin"  # Ensures fair turn-taking
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start the meeting
    try:
        user_proxy.initiate_chat(
            manager,
            message=f"Let's start the meeting.\n"
                    f"Agenda: {agenda}\n"
                    "Please discuss:\n"
                    "1. Scope and timeline (Management_Agent)\n"
                    "2. Technical design (Technical_Agent)\n"
                    "3. Testing and risks (Quality_Agent)\n"
                    "4. Summarize key outcomes (Minute_Taker)\n"
                    "After summary, say 'TERMINATE'."
        )

        # Extract and display final summary
        print("\n" + "🔐" + "=" * 68)
        print("                   FINAL MEETING SUMMARY")
        print("🔐" + "=" * 68)
        summary_found = False
        for msg in reversed(groupchat.messages):
            if msg["name"] == "Minute_Taker":
                print(msg["content"])
                summary_found = True
                break
        if not summary_found:
            print("No summary was generated by the Minute-Taker.")
        print("🔐" + "=" * 68)

    except Exception as e:
        print(f"\n❌ An error occurred during the meeting: {e}")

    print("\n✅ Meeting simulation complete.\n")