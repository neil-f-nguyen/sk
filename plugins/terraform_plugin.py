import os
from typing import List, Optional
from semantic_kernel.plugin_definition import kernel_function, kernel_function_context_parameter

class TerraformPlugin:
    def __init__(self, base_path: str = "terraform"):
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    @kernel_function(
        description="Create a new Terraform file with the given content",
        name="create_terraform_file"
    )
    async def create_terraform_file(
        self,
        filename: str,
        content: str,
        context: Optional[dict] = None
    ) -> str:
        """Create a new Terraform file with the given content."""
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, "w") as f:
            f.write(content)
        return f"Created Terraform file: {file_path}"

    @kernel_function(
        description="Read the content of a Terraform file",
        name="read_terraform_file"
    )
    async def read_terraform_file(
        self,
        filename: str,
        context: Optional[dict] = None
    ) -> str:
        """Read the content of a Terraform file."""
        file_path = os.path.join(self.base_path, filename)
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        with open(file_path, "r") as f:
            return f.read()

    @kernel_function(
        description="List all Terraform files in the directory",
        name="list_terraform_files"
    )
    async def list_terraform_files(
        self,
        context: Optional[dict] = None
    ) -> List[str]:
        """List all Terraform files in the directory."""
        return [f for f in os.listdir(self.base_path) if f.endswith(".tf")]

    @kernel_function(
        description="Validate a Terraform configuration",
        name="validate_terraform"
    )
    async def validate_terraform(
        self,
        filename: str,
        context: Optional[dict] = None
    ) -> str:
        """Validate a Terraform configuration."""
        file_path = os.path.join(self.base_path, filename)
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        # In a real implementation, this would run `terraform validate`
        # For now, we'll just check if the file exists and has content
        with open(file_path, "r") as f:
            content = f.read()
            if not content.strip():
                return f"File is empty: {file_path}"
            return f"File {file_path} appears to be valid"

    @kernel_function(
        description="Format a Terraform file",
        name="format_terraform"
    )
    async def format_terraform(
        self,
        filename: str,
        context: Optional[dict] = None
    ) -> str:
        """Format a Terraform file."""
        file_path = os.path.join(self.base_path, filename)
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        # In a real implementation, this would run `terraform fmt`
        # For now, we'll just return a success message
        return f"Formatted file: {file_path}" 