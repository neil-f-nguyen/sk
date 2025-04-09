# Copyright (c) Microsoft. All rights reserved.

import subprocess
from typing import Annotated

from semantic_kernel.functions import kernel_function


class TerraformExecutionPlugin:
    """A plugin that executes Terraform commands."""

    def __init__(self, base_path: str = "terraform"):
        self.base_path = base_path

    @kernel_function(description="Initialize a Terraform working directory.")
    def init(
        self
    ) -> Annotated[str, "Returns the output of the command."]:
        """Initialize a Terraform working directory."""
        try:
            result = subprocess.run(
                ["terraform", "init"],
                cwd=self.base_path,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    @kernel_function(description="Validate Terraform configuration files.")
    def validate(
        self
    ) -> Annotated[str, "Returns the output of the command."]:
        """Validate Terraform configuration files."""
        try:
            result = subprocess.run(
                ["terraform", "validate"],
                cwd=self.base_path,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    @kernel_function(description="Format Terraform configuration files.")
    def fmt(
        self
    ) -> Annotated[str, "Returns the output of the command."]:
        """Format Terraform configuration files."""
        try:
            result = subprocess.run(
                ["terraform", "fmt"],
                cwd=self.base_path,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}" 