# Terraform Generator POC

This is a POC using Semantic Kernel to automatically generate Terraform configurations for AWS.

## Project Structure

```
poc/
├── agents/
│   ├── terraform_creation_agent.py
│   ├── terraform_validation_agent.py
│   └── user_agent.py
├── plugins/
│   └── terraform_plugin.py
├── custom_selection_strategy.py
├── custom_termination_strategy.py
├── main.py
├── requirements.txt
└── README.md
```

## Main Components

1. **TerraformCreationAgent**: Agent responsible for creating Terraform configuration
2. **TerraformValidationAgent**: Agent responsible for validating Terraform configuration
3. **UserAgent**: Agent representing the user to provide feedback
4. **CustomSelectionStrategy**: Strategy for selecting the next agent
5. **CustomTerminationStrategy**: Strategy for deciding when to end the process
6. **TerraformPlugin**: Plugin for managing Terraform files

## Terraform Plugin

The Terraform Plugin provides the following functions:

1. `create_terraform_file`: Create a new Terraform file with the given content
2. `read_terraform_file`: Read the content of a Terraform file
3. `list_terraform_files`: List all Terraform files in the directory
4. `validate_terraform`: Validate a Terraform configuration
5. `format_terraform`: Format a Terraform file

## Prerequisites

1. Azure OpenAI Service
2. Azure App Insights (for logging and tracing)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following environment variables:

```
AZURE_APP_INSIGHTS_CONNECTION_STRING=your_connection_string
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

3. Run the program:

```bash
python main.py
```

## Workflow

1. TerraformCreationAgent creates the initial Terraform configuration
2. TerraformValidationAgent validates the configuration
3. UserAgent provides feedback on the configuration
4. The process repeats until:
   - UserAgent does not request changes
   - Or maximum number of cycles is reached

## Requirements

- Python 3.8+
- Semantic Kernel
- Azure OpenAI Service
- Azure App Insights
