# Copyright (c) Microsoft. All rights reserved.

import os
from typing import Annotated

from semantic_kernel.functions import kernel_function


class TerraformFilePlugin:
    """A plugin that manages Terraform files."""

    def __init__(self, base_path: str = "terraform"):
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    @kernel_function(description="Create a new Terraform file with the given content.")
    def create_file(
        self, 
        filename: Annotated[str, "The name of the file to create."],
        content: Annotated[str, "The content of the file."]
    ) -> Annotated[str, "Returns the path of the created file."]:
        """Create a new Terraform file with the given content."""
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, "w") as f:
            f.write(content)
        return f"Created Terraform file: {file_path}"

    @kernel_function(description="Read the content of a Terraform file.")
    def read_file(
        self, 
        filename: Annotated[str, "The name of the file to read."]
    ) -> Annotated[str, "Returns the content of the file."]:
        """Read the content of a Terraform file."""
        file_path = os.path.join(self.base_path, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")
        with open(file_path, "r") as f:
            return f.read()

    @kernel_function(description="List all Terraform files in the directory.")
    def list_files(
        self
    ) -> Annotated[str, "Returns a list of Terraform files."]:
        """List all Terraform files in the directory."""
        files = [f for f in os.listdir(self.base_path) if f.endswith(".tf")]
        return "\n".join(files) if files else "No Terraform files found." 