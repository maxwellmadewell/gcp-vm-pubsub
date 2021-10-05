from google.cloud import storage
# import pandas as pd
from datetime import datetime as dt
import base64
import os

from flask import Flask, request

BUCKET_IN = "mxm-predeng-input"
BUCKET_OUT = "mxm-predeng-output"

app = Flask(__name__)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def download_blob(bucket_name, source_blob_name, destination_file_name):
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "/app/output/raw.csv"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)
    return str(blobs)
#    for blob in blobs:
#        print(blob.name)


@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]
    name = "pub message had no data value"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

    print(f"Running engine {name}...")

    # gs_bucket = "gs://" + BUCKET_IN + "/input/raw/simple.csv"
    # df_raw = pd.read_csv(gs_bucket, usecols=['date', 'value'])
    download_blob(BUCKET_IN, "input/raw/simple.csv", "/app/output/raw.csv")
    filename = dt.now().strftime("%Y%m%d-%H%M%S")
    # df_csv = df_raw.to_csv(filename)
    # print(df_raw.to_string())
    upload_blob(BUCKET_OUT, "/app/output/raw.csv", filename)

    print(f"Completed engine {name}.")

    return ("", 204)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # app.run for local hosting
    # Gunicorn entrypoint will be set in dockerfile
    app.run(host="127.0.0.1", port=PORT, debug=True)
