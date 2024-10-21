#!/usr/bin/env python3
"""
This module defines the configuration settings for the GoPlan application,
including database configurations and other global settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the GoPlan app."""

    # Database configurations from .env
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.getenv('GO_PLAN_USER')}:"
        f"{os.getenv('GO_PLAN_MYSQL_PWD')}@{os.getenv('GO_PLAN_MYSQL_HOST')}/"
        f"{os.getenv('GO_PLAN_MYSQL_DB')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event system


config = Config()