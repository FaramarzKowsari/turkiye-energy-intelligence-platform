class EnergyPlatformError(Exception):
    """Base exception for the project."""


class ProviderConfigurationError(EnergyPlatformError):
    """Raised when a provider is not configured correctly."""


class ProviderResponseError(EnergyPlatformError):
    """Raised when a provider returns an invalid response."""
