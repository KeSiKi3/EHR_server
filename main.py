from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict
import time

app = FastAPI()

# In-memory store for connected devices
connected_clients: Dict[str, float] = {}

# Request body model for emergency data
class EmergencyData(BaseModel):
    device_id: str
    heart_rate: int
    gps_location: str
    symptoms: str

# Register or update device status
@app.get("/ping/{device_id}")
def ping(device_id: str):
    connected_clients[device_id] = time.time()
    return {
        "device_id": device_id,
        "active": True,
        "all_clients": list(connected_clients)
    }

# Receive emergency alert from device or app
@app.post("/emergency")
def handle_emergency(data: EmergencyData):
    print(f"[EMERGENCY RECEIVED] From: {data.device_id}")
    print(f"Heart Rate: {data.heart_rate}")
    print(f"Location: {data.gps_location}")
    print(f"Symptoms: {data.symptoms}")

    # ⛑️ This is where you could trigger SMS sending
    # send_sms(data.device_id, data.heart_rate, data.gps_location, data.symptoms)

    return {
        "status": "ok",
        "message": "Emergency data received successfully.",
        "received_data": data.dict()
    }

# Optional placeholder for SMS function
def send_sms(device_id, heart_rate, location, symptoms):
    print(f"Sending SMS alert for {device_id}: HR={heart_rate}, Loc={location}, Symptoms={symptoms}")
    # Integrate Twilio or other API here
