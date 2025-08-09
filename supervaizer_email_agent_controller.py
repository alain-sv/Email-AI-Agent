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
            "name": "Your Name",
            "type": str,
            "field_type": "CharField",
            "max_length": 100,
            "required": True,
            "description": "Your name for email signature",
        },
        {
            "name": "Recipient Name",
            "type": str,
            "field_type": "CharField",
            "max_length": 100,
            "required": True,
            "description": "Recipient's name",
        },
        {
            "name": "Number of emails (1 to 10)",
            "type": int,
            "field_type": "IntegerField",
            "required": True,
            "description": "Number of emails to process (1-10)",
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
job_stop = AgentMethod(
    name="stop",  # Must be present
    method="sv_main.stop",  # Initial deployment does not require this method to do anything
    is_async=False,
)

job_status = AgentMethod(
    name="status",  # Must be present
    method="sv_main.check_status",  # Initial deployment does not require this method to do anything
    is_async=False,
)

# Define the email AI agent
email_ai_agent = Agent(
    name="Email AI Agent",
    author="@parthshr370",  # Author of the agent
    developer="@alain_sv",  # Developer of the controller
    maintainer="@aintainer",
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
