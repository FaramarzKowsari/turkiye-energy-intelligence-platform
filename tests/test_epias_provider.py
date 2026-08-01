from datetime import datetime

from enerjinabiz.providers.epias import EpiasProvider


def test_epias_provider_normalizes_documented_responses(monkeypatch):
    provider = EpiasProvider("user@example.com", "secret")
    monkeypatch.setattr(provider, "_get_tgt", lambda: "TGT-test")

    responses = {
        "/v1/consumption/data/realtime-consumption": {
            "items": [
                {"date": "2026-07-01T00:00:00+03:00", "consumption": 41000.0},
                {"date": "2026-07-01T01:00:00+03:00", "consumption": 40500.0},
            ]
        },
        "/v1/generation/data/realtime-generation": {
            "items": [
                {
                    "date": "2026-07-01T00:00:00+03:00",
                    "naturalGas": 8000.0,
                    "blackCoal": 3000.0,
                    "wind": 5000.0,
                    "sun": 0.0,
                    "total": 42000.0,
                },
                {
                    "date": "2026-07-01T01:00:00+03:00",
                    "naturalGas": 7600.0,
                    "blackCoal": 2900.0,
                    "wind": 5200.0,
                    "sun": 0.0,
                    "total": 41500.0,
                },
            ]
        },
        "/v1/markets/dam/data/mcp": {
            "items": [
                {"date": "2026-07-01T00:00:00+03:00", "price": 2200.0},
                {"date": "2026-07-01T01:00:00+03:00", "price": 2100.0},
            ]
        },
    }
    monkeypatch.setattr(provider, "_post", lambda path, payload: responses[path])

    result = provider.fetch(datetime(2026, 7, 1), datetime(2026, 7, 1, 2))
    assert len(result) == 2
    assert result.loc[0, "consumption_mwh"] == 41000.0
    assert result.loc[0, "hard_coal_mwh"] == 3000.0
    assert result.loc[0, "market_price_try_mwh"] == 2200.0
    assert result["source"].eq("epias").all()
    assert not result["is_synthetic"].any()


def test_epias_items_tolerates_response_envelope():
    payload = {"body": {"items": [{"date": "2026-01-01T00:00:00+03:00"}]}}
    assert len(EpiasProvider._items(payload)) == 1
