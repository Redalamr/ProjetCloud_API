import os
from flask import Flask, jsonify
from azure.storage.blob import BlobServiceClient
import time

app = Flask(__name__)

CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "content"

cache = {"data": None, "timestamp": 0}
TTL = 60 

def get_blob_data(blob_name):
    now = time.time()
    if cache["data"] and (now - cache["timestamp"] < TTL):
        return cache["data"]
    
    service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = service.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    data = blob_client.download_blob().readall()
    
    cache["data"] = data
    cache["timestamp"] = now
    return data

@app.route('/api/events', methods=['GET'])
def get_events():
    return get_blob_data("events.json")

@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200 

@app.route('/readyz', methods=['GET'])
def ready_check():
    return jsonify({"status": "ready"}), 200 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
