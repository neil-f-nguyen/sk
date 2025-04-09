import asyncio
import logging
import os

from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

from .agents import TerraformValidationAgent, TerraformCreationAgent, UserAgent
from .custom_selection_strategy import CustomSelectionStrategy
from .custom_termination_strategy import CustomTerminationStrategy
from .plugins import TerraformFilePlugin, TerraformExecutionPlugin, UserPlugin
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.contents import AuthorRole, ChatMessageContent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.kernel import Kernel

TASK = """
Create a Terraform file to deploy a simple web application on AWS.
The Terraform file should include the following components:
1. VPC with public and private subnets
2. Security groups allowing HTTP/HTTPS access
3. EC2 instance running the web application
4. Load Balancer for traffic distribution
5. Auto Scaling Group for automatic scaling based on load

Requirements:
- Use Terraform best practices
- Include comprehensive comments explaining each part
- Include output variables for important information
- Include proper tags and metadata
"""

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_APP_INSIGHTS_CONNECTION_STRING = os.getenv("AZURE_APP_INSIGHTS_CONNECTION_STRING")

resource = Resource.create({ResourceAttributes.SERVICE_NAME: "Terraform Generator"})


def set_up_tracing():
    if not AZURE_APP_INSIGHTS_CONNECTION_STRING:
        return

    from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.trace import set_tracer_provider

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            AzureMonitorTraceExporter(
                connection_string=AZURE_APP_INSIGHTS_CONNECTION_STRING
            )
        )
    )
    set_tracer_provider(tracer_provider)


def set_up_logging():
    if not AZURE_APP_INSIGHTS_CONNECTION_STRING:
        return

    from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
    from opentelemetry._logs import set_logger_provider
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(
            AzureMonitorLogExporter(
                connection_string=AZURE_APP_INSIGHTS_CONNECTION_STRING
            )
        )
    )
    set_logger_provider(logger_provider)

    handler = LoggingHandler()
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


async def main():
    if AZURE_APP_INSIGHTS_CONNECTION_STRING:
        set_up_tracing()
        set_up_logging()

    # Initialize the kernel with Azure OpenAI
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            service_id="azure_openai",
            deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
            endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
        )
    )

    # Add plugins
    terraform_file_plugin = TerraformFilePlugin()
    terraform_execution_plugin = TerraformExecutionPlugin()
    user_plugin = UserPlugin()

    kernel.add_plugin(terraform_file_plugin, "terraform_file")
    kernel.add_plugin(terraform_execution_plugin, "terraform_execution")
    kernel.add_plugin(user_plugin, "user")

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("main"):
        agents = [
            TerraformCreationAgent(),
            UserAgent(),
            TerraformValidationAgent(),
        ]

        # Initialize agents with the kernel
        for agent in agents:
            agent._chat_completion_service = kernel.get_service("azure_openai")
            agent._kernel = kernel  # Pass the kernel to agents

        group_chat = AgentGroupChat(
            agents=agents,
            termination_strategy=CustomTerminationStrategy(agents=agents),
            selection_strategy=CustomSelectionStrategy(),
        )
        await group_chat.add_chat_message(
            ChatMessageContent(
                role=AuthorRole.USER,
                content=TASK.strip(),
            )
        )

        async for response in group_chat.invoke():
            print(f"==== {response.name} just responded ====")

        content_history: list[ChatMessageContent] = []
        async for message in group_chat.get_chat_messages(agent=agents[0]):
            if message.name == agents[0].name:
                content_history.append(message)

        print("Final Terraform configuration:")
        print(content_history[0].content)


if __name__ == "__main__":
    asyncio.run(main())
