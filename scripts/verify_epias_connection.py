from __future__ import annotations

from datetime import datetime, timedelta

from enerjinabiz.config import settings
from enerjinabiz.pipeline import clean_energy_data
from enerjinabiz.providers.epias import EpiasProvider

if __name__ == "__main__":
    provider = EpiasProvider(
        settings.epias_username,
        settings.epias_password,
        settings.epias_base_url,
        settings.epias_auth_url,
    )
    end = datetime.now() - timedelta(hours=3)
    start = end - timedelta(days=2)
    frame = clean_energy_data(provider.fetch(start, end))
    print("Authentication: successful")
    print(f"Records received: {len(frame)}")
    print(f"Start: {frame['timestamp'].min()}")
    print(f"End: {frame['timestamp'].max()}")
    print("Credentials stored: no")
