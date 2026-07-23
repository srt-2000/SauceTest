"""Application settings loaded from environment / ``.env``."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from constants import Messages, Fields


_ENV_PATH = Path(__file__).resolve().parent / ".env"


def _to_check_variable_is_exist(name: str) -> str:
    """Return a required environment variable value.

    Args:
        name: Environment variable name to read.

    Returns:
        Stripped non-empty value of the variable.

    Raises:
        ValueError: If the variable is missing or blank.
    """
    value: str | None = os.getenv(name)

    if value is None or not value.strip():
        raise ValueError(f"{Messages.MISSING_REQUIRES_VAR}: {name}")
    return value.strip()


@dataclass(frozen=True, slots=True)
class ProjectSettings:
    """SauceDemo credentials and target URL from ``.env``.

    Attributes:
        STANDARD_USER: Login username.
        PASSWORD: Login password.
        RESOURCE_URL: Base URL of the SauceDemo site.
    """

    STANDARD_USER: str
    PASSWORD: str
    RESOURCE_URL: str

    @classmethod
    def get_from_env_and_check(
        cls,
        *,
        env_file_path: Path = _ENV_PATH,
    ) -> ProjectSettings:
        """Build settings from process env after optional ``.env`` load.

        Args:
            env_file_path: Path to the ``.env`` file. Defaults to project root
                ``.env``.

        Returns:
            Validated immutable settings instance.
        """
        load_dotenv(env_file_path, override=False)
        settings_from_env: ProjectSettings = cls(
            STANDARD_USER=_to_check_variable_is_exist(Fields.STANDARD_USER),
            PASSWORD=_to_check_variable_is_exist(Fields.PASSWORD),
            RESOURCE_URL=_to_check_variable_is_exist(Fields.RESOURCE_URL),
        )

        return settings_from_env


def get_settings() -> ProjectSettings:
    """Initialize and return application settings.

    Returns:
        Loaded ``ProjectSettings`` instance.

    Raises:
        ValueError: If a required environment variable is missing or blank.
    """
    try:
        settings_data: ProjectSettings = ProjectSettings.get_from_env_and_check()
        return settings_data
    except ValueError as error:
        logger.error(f"{Messages.CONFIG_VALUE_ERROR}: {error}")
        raise


settings = get_settings()
