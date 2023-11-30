from dotenv import load_dotenv
import os

DEV = True
if DEV:
    load_dotenv()
    ACCESS_TOKEN=os.getenv("API_NEWSI_LBOT")
else:
    ACCESS_TOKEN=os.getenv("API_NEWSI_LBOT")

CHANNEL_ID = -1002099984327
