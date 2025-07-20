from pyrogram import Client, enums
import os
from dotenv import load_dotenv
import logging

from app.values import DATA_DANTIC, DATA_PATH
from app.utils import updateData


load_dotenv()

class Config:
    API_KEY  : str  = os.getenv("API_KEY")
    API_HASH : str  = os.getenv("API_HASH")
    API_ID   : int  = int(os.getenv("API_ID"))
    SUDO     : int  = int(os.getenv("SUDO"))

temp = {}
datas = {
    'status':False, 
    'app':None
}

os.makedirs("./.session", exist_ok=True)
os.makedirs("./data", exist_ok=True)
os.makedirs("./logo", exist_ok=True)

if not os.path.exists(DATA_PATH):
    updateData(DATA_DANTIC)


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("./log/raid.log", encoding="utf-8"), 
        # logging.StreamHandler()  
    ]
)

logger = logging.getLogger("pyrogram")  

app = Client(
    name="./.session/rad", 
    api_hash=Config.API_HASH, 
    api_id=Config.API_ID, 
    bot_token=Config.API_KEY, 
    plugins=dict(root="app"),
    parse_mode=enums.ParseMode.DEFAULT
)



