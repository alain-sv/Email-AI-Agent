# This is the basic  supervaizer controller for the Email-AI-Agent.
# Use it as an example to experiment with the Email-AI-Agent with supervaize.com


from supervaizer import (
    Agent,
    AgentMethod,
    AgentMethods,
    Parameter,
    ParametersSetup,
    Server,
)

from rich.console import Console


# Public url of your hosted agent  (including port if needed)
# Use loca.lt or ngrok to get a public url during development.
DEV_PUBLIC_URL = "https://myagent-dev.loca.lt"
# Public url of your hosted agent
PROD_PUBLIC_URL = "https://myagent.cloud-hosting.net:8001"


# Create a console with default style set to yellow
console = Console(style="yellow")

# Define the parameters and secrets expected by the agent
agent_parameters = ParametersSetup.from_list([
    Parameter(
        name="IMAP_USERNAME",
        description="IMAP username for email access",
        is_environment=True,
        is_secret=False,
    ),
    Parameter(
        name="IMAP_PASSWORD",
        description="IMAP password for email access",
        is_environment=True,
        is_secret=True,
    ),
    Parameter(
        name="IMAP_SERVER",
        description="IMAP server address",
        is_environment=True,
        is_secret=False,
    ),
    Parameter(
        name="IMAP_PORT",
        description="IMAP port for email access",
        is_environment=True,
        is_secret=False,
    ),
    Parameter(
        name="EMAIL_SERVER",
        description="Email server address",
        is_environment=True,
        is_secret=False,
    ),
    Parameter(
        name="EMAIL_USERNAME",
        description="Email username for email access",
        is_environment=True,
        is_secret=False,
    ),
    Parameter(
        name="EMAIL_PASSWORD",
        description="Email password for email access",
        is_environment=True,
        is_secret=True,
    ),
    Parameter(
        name="EMAIL_PORT",
        description="Email port for email access",
        is_environment=True,
        is_secret=False,
    ),
    Parameter(
        name="DEEPSEEK_API_KEY",
        description="DeepSeek API Key for AI processing",
        is_environment=True,
        is_secret=True,
    ),
])

# Define the main email processing method
process_email_method = AgentMethod(
    name="start",
    method="sv_main.process_email_workflow",  # This will be the main workflow function
    is_async=False,
    params={},
    fields=[
        {
            "name": "your_name",
            "type": str,
            "field_type": "CharField",
            "max_length": 100,
            "required": True,
            "description": "Your name for email signature",
        },
        {
            "name": "recipient_name",
            "type": str,
            "field_type": "CharField",
            "max_length": 100,
            "required": True,
            "description": "Recipient's name",
        },
        {
            "name": "email_choice",
            "type": int,
            "field_type": "IntegerField",
            "required": True,
            "description": "Email selection (1-5 for latest emails)",
        },
        {
            "name": "action_type",
            "type": str,
            "field_type": "ChoiceField",
            "choices": [("send", "Send Email"), ("draft", "Draft to Gmail")],
            "required": True,
            "description": "Action type: 'send' or 'draft'",
        },
        {
            "name": "gmail_address",
            "type": str,
            "field_type": "CharField",
            "max_length": 200,
            "required": False,
            "description": "Gmail address for drafts (required if action_type is 'draft')",
        },
    ],
)

# Define email action method
email_action_method = AgentMethod(
    name="email_action",
    method="sv_main.process_email_action",
    is_async=False,
    params={"action": "email_action"},
    fields=[
        {
            "name": "email_data",
            "type": dict,
            "field_type": "JSONField",
            "required": True,
            "description": "Email data with response",
        },
        {
            "name": "your_name",
            "type": str,
            "field_type": "CharField",
            "max_length": 100,
            "required": True,
            "description": "Your name for signature",
        },
        {
            "name": "action_type",
            "type": str,
            "field_type": "ChoiceField",
            "choices": [("send", "Send Email"), ("draft", "Draft to Gmail")],
            "required": True,
            "description": "Action type: 'send' or 'draft'",
        },
        {
            "name": "gmail_address",
            "type": str,
            "field_type": "CharField",
            "max_length": 200,
            "required": False,
            "description": "Gmail address for drafts",
        },
    ],
)

# Define status check method
status_method = AgentMethod(
    name="check_status",
    method="sv_main.check_email_status",
    is_async=False,
    params={"action": "check_status"},
    fields=[
        {
            "name": "email_id",
            "type": str,
            "field_type": "CharField",
            "max_length": 100,
            "required": True,
            "description": "Email ID to check status",
        }
    ],
)

# Define agent parameters
agent_parameters = ParametersSetup.from_list([
    Parameter(
        name="OPENAI_API_KEY",
        description="OpenAI API Key for AI processing",
        is_environment=True,
    ),
    Parameter(
        name="IMAP_USERNAME",
        description="IMAP username for email access",
        is_environment=True,
    ),
    Parameter(
        name="IMAP_PASSWORD",
        description="IMAP password for email access",
        is_environment=True,
    ),
    Parameter(
        name="IMAP_SERVER",
        description="IMAP server address",
        is_environment=True,
    ),
])

# Define the email AI agent
email_ai_agent = Agent(
    name="Email AI Agent",
    id="email_ai_agent",
    author="Email AI Team",
    developer="AI Developer",
    maintainer="AI Maintainer",
    editor="AI Editor",
    version="1.0.0",
    description="AI-powered email processing agent that can fetch, analyze, generate responses, and send/draft emails",
    urls={"dev": "http://host.docker.internal:8001", "prod": ""},
    active_environment="dev",
    tags=["email", "ai", "automation", "communication"],
    methods=AgentMethods(
        job_start=process_email_method,
        job_stop=status_method,
        job_status=status_method,
        chat=None,
        custom=None,
    ),
    parameters_setup=agent_parameters,
)

# Initialize a connection to the SUPERVAIZE server
server = Server(
    agents=[email_ai_agent],
    acp_endpoints=True,  # Enable ACP protocol support
    a2a_endpoints=True,  # Enable A2A protocol support
    admin_interface=True,  # Enable web admin interface (requires api_key)
    api_key=os.getenv("SUPERVAIZE_API_KEY"),  # Required for admin interface
    supervisor_account=None,
)

# Start the server
server.launch(log_level="DEBUG")
