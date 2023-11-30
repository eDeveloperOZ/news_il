from dotenv import load_dotenv
import os

DEV = False
if DEV:
    load_dotenv()
    ACCESS_TOKEN=os.getenv("API_NEWSI_LBOT")
else:
    print('prod')
    ACCESS_TOKEN=os.getenv("API_NEWSI_LBOT")

CHANNEL_ID = -1002099984327
