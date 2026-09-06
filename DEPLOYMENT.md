# HAMZAM deployment

Local: `python run.py`, then open `http://localhost:8000`.

Docker: `docker compose up --build`.

For public hosting, deploy the Docker service using `render.yaml` or another Docker host. Set the resulting HTTPS URL as the Android `HAMZAM_URL` build input.

Live market data uses Binance public klines. No trading orders are executed by HAMZAM.
