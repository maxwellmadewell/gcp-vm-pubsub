from google.cloud import storage
import os
from datetime import datetime as dt
import pandas as pd

##########PROGRAMMATIC###################
# Instantiates a client
#storage_client = storage.Client()
# The name for the new bucket
# bucket_name = "mxm-predeng-input2"
# Creates the new bucket
# bucket = storage_client.create_bucket(bucket_name)
# print("Bucket {} created.".format(bucket.name))


def save_output_data(df_obj, address):
    filename = dt.now().strftime("%Y%m%d-%H%M%S")
    if not os.path.exists(address):
        os.makedirs(address)
    print("Saving to GCS... \n \n")
    df_obj.to_csv(address + filename + ".csv")
    df_obj.to_csv(address + "_LATEST.csv")


if __name__ == "__main__":
    df_raw = pd.read_csv('input/raw/simple.csv', usecols=['date', 'value'])
    print(df_raw.to_string())
    save_output_data(df_raw, "output/")
