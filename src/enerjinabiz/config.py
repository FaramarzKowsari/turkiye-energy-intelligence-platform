from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    provider: str = os.getenv("ENERGY_DATA_PROVIDER", "demo").lower()
    epias_username: str | None = os.getenv("EPIAS_USERNAME") or None
    epias_password: str | None = os.getenv("EPIAS_PASSWORD") or None
    epias_base_url: str = os.getenv(
        "EPIAS_BASE_URL", "https://seffaflik.epias.com.tr/electricity-service"
    ).rstrip("/")
    epias_auth_url: str = os.getenv(
        "EPIAS_AUTH_URL", "https://giris.epias.com.tr/cas/v1/tickets"
    )
    local_data_path: Path = Path(
        os.getenv("LOCAL_DATA_PATH", "data/samples/energy_hourly_demo.csv")
    )
    timezone: str = os.getenv("ENERGY_TIMEZONE", "Europe/Istanbul")


settings = Settings()
