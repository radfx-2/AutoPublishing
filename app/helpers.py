from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.utils import getData
from config import datas, temp

MAIN_MESSAGE = {
    "MAIN":
        u"⌔︙ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴜᴛᴏ ᴘᴜʙʟɪꜱʜ ʙᴏᴛ \n"
        u"⌔︙ᴛʜᴇ ʙᴏᴛ ᴄᴀɴ ᴘᴏꜱᴛ ɪɴ ɢʀᴏᴜᴘꜱ ᴀɴᴅ ꜱᴜᴘᴇʀɢʀᴏᴜᴘꜱ."
        u""
}



class Keyboards:

    def MAIN_KEYBOARD():
        botData = getData()
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text=f"ᴀᴄᴄᴏᴜɴᴛ : {botData['session']['username']}", 
                    url=("t.me/radfx2" if botData['session']['username'] is None 
                    else f"t.me/{botData['session']['username'] }")), 
                InlineKeyboardButton(text="ꜱᴛᴀʀᴛ" if not datas['status'] else "ꜱᴛᴏᴘ", callback_data="START_PUBLISH")
            ],

            [
                InlineKeyboardButton(text="⌔ ꜱᴇᴛ ᴀᴄᴄᴏᴜɴᴛ", callback_data="SET_ACCOUNT"), 
                InlineKeyboardButton(text="⌔ ᴅᴇʟᴇᴛᴇ ᴀᴄᴄᴏᴜɴᴛ", callback_data="DELETE_ACCOUNT")
            ], 
            [
                InlineKeyboardButton(text="⌔ ᴀᴅᴅ ᴍᴇꜱꜱᴀɢᴇ", callback_data="ADD_MESSAGE"),
                InlineKeyboardButton(text="⌔ ꜱʜᴏᴡ ᴍᴇꜱꜱᴀɢᴇ", callback_data="SHOW_MESSAGE")
            ], 
            [
                InlineKeyboardButton(text="⌔ ᴀᴅᴅ ɢʀᴏᴜᴘ", callback_data="ADD_CHAT"),
                InlineKeyboardButton(text="⌔ ꜱʜᴏᴡ ɢʀᴏᴜᴘ", callback_data="SHOW_CHAT"),
            ],
            [
                InlineKeyboardButton(text="⌔ ᴄʟᴇᴀʀ ᴅᴀᴛᴀʙᴀꜱᴇ", callback_data="CLEAER_DATABASE")
            ]

        ])
    
    def BACK_MAIN():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="ＢＡＣＫ", callback_data="back")
            ]
        ]) 
    
    def BACK_MENU(menu: str):
            return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="ＢＡＣＫ", callback_data=menu)
            ]
        ]) 
    
    def SELECT_ADD_CHAT_TYPE():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="ᴜꜱᴇʀɴᴀᴍᴇ", callback_data="ADD_CHAT_USERNAME"),
                InlineKeyboardButton(text="ɪɴᴠɪᴛᴇ ʟɪɴᴋ", callback_data="ADD_CHAT_INVETE"),
            ],
            [
                InlineKeyboardButton(text="ᴊᴏɪɴ ɢʀᴏᴜᴘꜱ", callback_data="ADD_CHAT_JOINGROUP")
            ] ,
            [
                InlineKeyboardButton(text="ＢＡＣＫ", callback_data="back")
            ]
        ])



    def SHOW_CHAT():
        botData = getData()
        keybaord = [
            [
                InlineKeyboardButton(text="ɪᴅ", callback_data="NONE"), 
                InlineKeyboardButton(text="ᴄʜᴀᴛ" , callback_data="NN"), 
                InlineKeyboardButton(text="ᴅᴇʟᴇᴛᴇ ɢʀᴏᴜᴘ", callback_data="DE")
            ]
        ]

        for chatID, chatData in botData['chats'].items():
            keybaord.append([
                InlineKeyboardButton(text=chatID, callback_data="NJ"), 
                InlineKeyboardButton(text=chatData['title'], url=f"t.me/{'radfx2' if not chatData['username'] else chatData['username']}"), 
                InlineKeyboardButton(text="ᴅᴇʟᴇᴛᴇ", callback_data=f"DELETE_CHAT|{chatID}")
            ])
        if not botData['chats']:
            keybaord.append([InlineKeyboardButton(text="ɴᴏ ɢʀᴏᴜᴘ", callback_data="a")])      
        keybaord.append([InlineKeyboardButton(text="ＢＡＣＫ", callback_data="back")])
        return InlineKeyboardMarkup(keybaord)
    
    def SELECT_CHAT():
        botData = getData()
        keybaord = []
        for chatID, chatData in botData['chats'].items():
            keybaord.append([
                InlineKeyboardButton(text=chatData['title'], url=f"t.me/{'radfx2' if not chatData['username'] else chatData['username']}"), 
                InlineKeyboardButton(text="✅" if temp['addMessageChatSelect'][chatID] else "☑️", callback_data=f"SELECT_CHAT|{chatID}"), 
            ])
        keybaord.append([InlineKeyboardButton(text="ᴅᴏɴᴇ ꜱᴇʟᴇᴄᴛ", callback_data="DONE_SELECT_MESSAGE_CHAT")])
        return InlineKeyboardMarkup(keybaord)
    

    def SHOW_MESSAGES():

        keybaord = [
            [
                InlineKeyboardButton(text="ᴍᴇꜱꜱᴀɢᴇ", callback_data='nn'),
                InlineKeyboardButton(text="ɢʀᴏᴜᴘ", callback_data='nSn'),
                InlineKeyboardButton(text="ꜱʟᴇᴇᴘ", callback_data='S'),
                InlineKeyboardButton(text="ᴅᴇʟᴇᴛᴇ", callback_data='S4'),
            ]
        ]

        botData = getData()
        for ID, msg in enumerate(botData['messages']):
            keybaord.append([
                InlineKeyboardButton(text="ꜱʜᴏᴡ", callback_data=f"SHOW_MESSAGE|{ID}"), 
                InlineKeyboardButton(text="ꜱʜᴏᴡ", callback_data=f"SHOW_MESSAGE_CHAT|{ID}"), 
                InlineKeyboardButton(text=msg['sleeps'], callback_data="SS"), 
                InlineKeyboardButton(text="ᴅᴇʟᴇᴛᴇ", callback_data=f"DELETE_MESSAGE|{ID}")
            ])

        if not botData['messages']:
            keybaord.append([InlineKeyboardButton(text="ɴᴏ ᴍᴇꜱꜱᴀɢᴇ", callback_data="NNE")])
    

        keybaord.append([InlineKeyboardButton(text="ＢＡＣＫ", callback_data="back")])
        return InlineKeyboardMarkup(keybaord)
    
    def MAKE_MESSAGE_KEYBOARD(keyboardsList: list):        
        keybaord = []
        for i in keyboardsList:
            keybaord.append([InlineKeyboardButton(text=i['text'], url=i['url'])])
        return InlineKeyboardMarkup(keybaord)
    
    def CHECK_CLEAER_DATABASE():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="ᴄʟᴇᴀʀ", callback_data="START_CLAER"), 
                InlineKeyboardButton(text="ＢＡＣＫ", callback_data="back")
            ]
        ])    

    def SELECT_JOING_CHAT(chats: dict):
        keyboard = []
        for _, i in chats.items():
            keyboard.append([
                InlineKeyboardButton(text=i['title'], callback_data="NN"),
                InlineKeyboardButton(text=f"@{i['username']}", callback_data="NNM"),
                InlineKeyboardButton(text="ᴀᴅᴅ ɢʀᴏᴜᴘ", callback_data=f"ADD_GROUP|{i['id']}")
            ])     
        keyboard.append([InlineKeyboardButton(text="ＢＡＣＫ", callback_data="back")])
        return InlineKeyboardMarkup(keyboard)