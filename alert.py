import os
import requests
from twilio.rest import Client
import webbrowser
import http.server
import socketserver
import threading
from urllib.parse import parse_qs, urlparse
import time

# Load environment variables safely
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
PERSONAL_PHONE_NUMBER = os.getenv("PERSONAL_PHONE_NUMBER")

location_data = {}

class LocationHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/location":
            query_components = parse_qs(parsed_path.query)

            try:
                location_data["lat"] = float(query_components.get("lat", [0])[0])
                location_data["lon"] = float(query_components.get("lon", [0])[0])

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Location received. You may close this tab.")

            except Exception:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Failed to parse location.")
        else:
            super().do_GET()


def start_location_server():
    handler = LocationHandler
    httpd = socketserver.TCPServer(("", 8081), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        response = requests.get(url, headers={"User-Agent": "SafeMuster-App"})
        data = response.json()

        city = data.get("address", {}).get("city", "Unknown")
        address = data.get("display_name", "Unknown Location")

        return city, address

    except Exception as e:
        print("⚠ Reverse geocoding error:", e)
        return "Unknown", "Unknown Location"


def get_current_location():
    try:
        start_location_server()

        html = """
        <html>
        <body>
        <script>
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            fetch("http://localhost:8081/location?lat=" + lat + "&lon=" + lon);
        });
        </script>
        <h2>Requesting your location...</h2>
        </body>
        </html>
        """

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)

        webbrowser.open("http://localhost:8081/index.html")

        for _ in range(60):

            if "lat" in location_data and "lon" in location_data:

                lat = location_data["lat"]
                lon = location_data["lon"]

                city, address = reverse_geocode(lat, lon)

                return lat, lon, city, address

            time.sleep(1)

        raise TimeoutError("Location not received in time.")

    except Exception as e:
        print("⚠ Failed to get location:", e)
        return None, None, None, None


def get_nearest_police_station(lat, lon):

    try:
        overpass_url = "https://overpass-api.de/api/interpreter"

        query = f"""
        [out:json];
        (
          node["amenity"="police"](around:3000,{lat},{lon});
          way["amenity"="police"](around:3000,{lat},{lon});
          relation["amenity"="police"](around:3000,{lat},{lon});
        );
        out center 1;
        """

        response = requests.post(overpass_url, data=query.encode("utf-8"))
        data = response.json()

        if data["elements"]:
            element = data["elements"][0]
            return element.get("tags", {}).get("name", "Unnamed Police Station")

        return "No police station found nearby"

    except Exception as e:
        print("⚠ Overpass API error:", e)
        return "Unknown Police Station"


def send_alert():

    # Check environment variables
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, PERSONAL_PHONE_NUMBER]):
        print("⚠ Twilio environment variables not set.")
        return

    lat, lon, city, address = get_current_location()

    if not lat or not lon:
        print("❌ Location not available.")
        return

    police_station = get_nearest_police_station(lat, lon)

    message_text = (
        f"🚨 Emergency Alert!\n"
        f"Location: {address}\n"
        f"City: {city}\n"
        f"Nearest Police Station: {police_station}\n"
        f"Stay alert and take immediate action."
    )

    try:

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        print("📤 Sending SMS...")

        message = client.messages.create(
            body=message_text,
            from_=TWILIO_PHONE_NUMBER,
            to=PERSONAL_PHONE_NUMBER
        )

        print("✅ SMS Sent:", message.sid)

        print("📞 Placing Call...")

        call = client.calls.create(
            twiml=f"<Response><Say>{message_text}</Say></Response>",
            from_=TWILIO_PHONE_NUMBER,
            to=PERSONAL_PHONE_NUMBER
        )

        print("✅ Call Placed:", call.sid)

    except Exception as e:
        print("⚠ Twilio error:", e)


if __name__ == "__main__":
    send_alert()