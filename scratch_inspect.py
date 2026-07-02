import urllib.request
import json

url = "https://gnozgzqehlwzphtvtaau.supabase.co/rest/v1/"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdub3pnenFlaGx3enBodHZ0YWF1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjcyODcwNSwiZXhwIjoyMDk4MzA0NzA1fQ.u21ncyKLRj4CezoAZvHhtLktawmQmxNTbTK6uusvz_E",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdub3pnenFlaGx3enBodHZ0YWF1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjcyODcwNSwiZXhwIjoyMDk4MzA0NzA1fQ.u21ncyKLRj4CezoAZvHhtLktawmQmxNTbTK6uusvz_E",
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        spec = json.loads(response.read().decode())
        definitions = list(spec.get("definitions", {}).keys())
        if "requests" in definitions:
            print("Table 'requests' already exists.")
        else:
            print("Table 'requests' does NOT exist.")
except Exception as e:
    print("Error:", e)
