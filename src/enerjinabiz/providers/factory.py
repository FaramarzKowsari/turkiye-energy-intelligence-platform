from __future__ import annotations

from enerjinabiz.config import Settings, settings

from .base import EnergyDataProvider
from .demo import DemoProvider
from .epias import EpiasProvider
from .local import LocalFileProvider
from .teias import TeiasCatalogProvider


def get_provider(config: Settings = settings) -> EnergyDataProvider:
    if config.provider == "demo":
        return DemoProvider(config.local_data_path)
    if config.provider == "local":
        return LocalFileProvider(config.local_data_path)
    if config.provider == "epias":
        return EpiasProvider(
            config.epias_username,
            config.epias_password,
            config.epias_base_url,
            config.epias_auth_url,
        )
    if config.provider in {"teias", "teias-catalog"}:
        return TeiasCatalogProvider()
    raise ValueError(f"Unknown ENERGY_DATA_PROVIDER: {config.provider}")
