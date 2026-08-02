# Secure EPİAŞ Live Mode

This project keeps the public demo independent and enables official EPİAŞ data only when the app owner configures private Streamlit Secrets.

## Official data used

- Real-time consumption: `/v1/consumption/data/realtime-consumption`
- Real-time generation by resource: `/v1/generation/data/realtime-generation`
- Day-ahead market clearing price: `/v1/markets/dam/data/mcp`

EPİAŞ documents TGT authentication and states that real-time consumption is published with a delay.

## Registration

Create and activate a free Transparency Platform account through the official EPİAŞ registration page:

`https://kayit.epias.com.tr/epias-transparency-platform-registration-form`

Do not commit credentials to GitHub and do not send them to another person.

## Streamlit Community Cloud configuration

1. Open `https://share.streamlit.io/`.
2. Select the `enerjinabiz-ai` app.
3. Open **Manage app → Settings → Secrets**.
4. Paste the following TOML, replacing only the username and password:

```toml
[epias]
username = "your-email@example.com"
password = "your-epias-password"
base_url = "https://seffaflik.epias.com.tr/electricity-service"
auth_url = "https://giris.epias.com.tr/cas/v1/tickets"
```

5. Save and reboot the app.
6. Open the sidebar and select **Live EPİAŞ**.
7. Start with a one-day lookback and press **Refresh official data**.

## Security design

- Secrets are stored in Streamlit's server-side secret store.
- Credentials are never rendered in the user interface.
- Credentials are not written to CSV exports, logs, GitHub, or browser storage by this application.
- The app stores only the returned analytical dataframe in the current Streamlit session.
- Demo mode remains available if authentication or an endpoint fails.

## Operational limits

This is not an official grid-control, settlement, emergency-warning, or trading system. Data availability, delays, and field definitions remain controlled by EPİAŞ and the original data-owning institutions.
