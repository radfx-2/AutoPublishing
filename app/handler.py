from pyrogram import Client , filters, types, enums
from pyrogram.errors import ListenerTimeout, SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid, ChannelInvalid
import asyncio

from app.helpers import MAIN_MESSAGE, Keyboards
from app.utils import getData, updateData, IS_SPLIT
from app.values import DATA_DANTIC
from config import Config, temp, datas



@Client.on_callback_query(filters.regex("^back$"))
@Client.on_message(filters.private & filters.regex("^/start$") & filters.user(Config.SUDO))
async def ON_START_BOT(app :Client, message: types.Message):
    if isinstance(message, types.CallbackQuery):
        await message.edit_message_text(
            text=MAIN_MESSAGE['MAIN'],
            reply_markup=Keyboards.MAIN_KEYBOARD())
        return 
    await message.reply(
        text=MAIN_MESSAGE['MAIN'],
        reply_markup=Keyboards.MAIN_KEYBOARD()
    )


@Client.on_callback_query(filters.regex("^SET_ACCOUNT$"))
async def ON_SET_ACCOUNT(app: Client, query: types.CallbackQuery):
    Password = None
    await query.edit_message_text(
        text="⌔︙ꜱᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ .", 
        reply_markup=Keyboards.BACK_MAIN()
    )

    try:
        data : types.Message = await app.listen(
            chat_id=query.message.chat.id,
            filters=filters.private & filters.text, 
            timeout=120
        )
    except ListenerTimeout as e:
        return 0
    
    PHONE = data.text
    if not PHONE.strip("+").replace(' ', '').isdigit():
        await data.reply(
            text="⌔︙ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴏɴʟʏ ɴᴜᴍʙᴇʀꜱ. .", 
            reply_markup=Keyboards.BACK_MAIN()

        )
        return
    
    await asyncio.sleep(0.3)
    tempClient = Client(
        name=":memory:", 
        api_hash=Config.API_HASH,
        api_id=Config.API_ID, 
        in_memory=True,
        workers=2, 
        no_updates=True)
    
    await tempClient.connect()
    try:
        verCodeData = await tempClient.send_code(phone_number=PHONE)
    except Exception as e:
        await data.reply(
            text="⌔︙ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ .",
            reply_markup=Keyboards.BACK_MAIN()

        )
        return
    
    await data.reply(
        text="⌔︙ ꜱᴇɴᴅ ᴍᴇ ᴛʜᴇ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴄᴏᴅᴇ ."
    )

    try:
        data : types.Message = await app.listen(
            chat_id=query.message.chat.id,
            filters=filters.private & filters.text, 
            timeout=120
        )
    except ListenerTimeout as e:
        return 0
    
    verCode = data.text
    if not verCode.isdigit():
        await data.reply(
            text="⌔︙ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴏɴʟʏ ɴᴜᴍʙᴇʀꜱ. .", 
            reply_markup=Keyboards.BACK_MAIN()

        )
        return
    
    try:
        signIn = await tempClient.sign_in(
            phone_code=verCode, 
            phone_number=PHONE, 
            phone_code_hash=verCodeData.phone_code_hash
        )
    except PhoneCodeInvalid as e:
        await data.reply(
            text="⌔︙ɪɴᴠᴀʟɪᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴄᴏᴅᴇ .", 
            reply_markup=Keyboards.BACK_MAIN()

        )
        return
    except SessionPasswordNeeded as e:
        await data.reply(
            text="⌔︙ꜱᴇɴᴅ ᴍᴇ ʏᴏᴜʀ 2-ꜱᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴘᴀꜱꜱᴡᴏʀᴅ ."

        )

        try:
            data : types.Message = await app.listen(
                chat_id=query.message.chat.id,
                filters=filters.private & filters.text, 
                timeout=120
            )
        except ListenerTimeout as e:
            await tempClient.disconnect()
            return 0

        Password = data.text
        try:
            await tempClient.check_password(Password)
        except PasswordHashInvalid as e:
            await data.reply(
                text="⌔︙ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀꜱꜱᴡᴏʀᴅ.", 
                reply_markup=Keyboards.BACK_MAIN()

            )
            await tempClient.disconnect()
            return
        except Exception as e:
            print(e)
            await data.reply(
                text="⌔︙ᴜɴᴋɴᴏᴡɴ ᴇʀʀᴏʀ .",
                reply_markup=Keyboards.BACK_MAIN()

            )
            await tempClient.disconnect()
            return
    
    except Exception as e:
        await data.reply(
            text="⌔︙ᴜɴᴋɴᴏᴡɴ ᴇʀʀᴏʀ .", 
            reply_markup=Keyboards.BACK_MAIN()

        )
        print(e)
        await tempClient.disconnect()
        return
    
    sessionData = await tempClient.get_me()
    session = await tempClient.export_session_string()

    botData = getData()
    botData['session']['id'] = sessionData.id
    botData['session']['first_name'] = sessionData.first_name
    botData['session']['username'] = sessionData.username
    botData['session']['password'] = Password
    botData['session']['session'] = session
    updateData(botData)
    await tempClient.disconnect()
    await data.reply(
        text="⌔︙ᴀᴄᴄᴏᴜɴᴛ ꜱᴇᴛ ᴜᴘ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ", reply_markup=Keyboards.BACK_MAIN()
    )


@Client.on_callback_query(filters.regex("^DELETE_ACCOUNT$"))
async def ON_DELETE_ACCOUNT(app: Client, query: types.CallbackQuery):
    botData = getData()
    botData['session'] = DATA_DANTIC['session']
    updateData(botData)
    await query.edit_message_text(
        text="⌔︙ᴍʏ ᴀᴄᴄᴏᴜɴᴛ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.", reply_markup=Keyboards.BACK_MAIN()
    )


@Client.on_callback_query(filters.regex("^ADD_CHAT$"))
async def ON_ADD_CHAT(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text="⌔︙ᴄʜᴏᴏꜱᴇ ʜᴏᴡ ᴛᴏ ᴀᴅᴅ ᴛʜᴇ ɢʀᴏᴜᴘ", 
        reply_markup=Keyboards.SELECT_ADD_CHAT_TYPE()
    )

@Client.on_callback_query(filters.regex("^ADD_CHAT_USERNAME$"))
async def ON_ADD_CHAT_USERNAME(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text="⌔︙send chat username", 
        reply_markup=Keyboards.BACK_MAIN()
    )
    try:
        data : types.Message = await app.listen(
            chat_id=query.message.chat.id,
            filters=filters.private & filters.text, 
            timeout=120
        )
    except ListenerTimeout as e:
        return 0
    


    ChatUsername = data.text
    try:
        Chatdata = await app.get_chat(ChatUsername)
    except Exception as e:
        await data.reply(
            text="⌔︙Chat ID is invalid .", 
            reply_markup=Keyboards.BACK_MAIN()
        )
        return
    
    if Chatdata.type not in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
        await data.reply(
            text="⌔︙Only groups and supergroups can be added.", 
            reply_markup=Keyboards.BACK_MAIN()
        )
        return
    
    botData = getData()
    botData['chats'].update({Chatdata.id:{
        'id':Chatdata.id, 
        'username':Chatdata.username, 
        'title':Chatdata.title,
        'type':str(Chatdata.type)
    }})
    updateData(botData)

    await data.reply(
        text="⌔︙done add chat",
        reply_markup=Keyboards.BACK_MAIN()
    )


@Client.on_callback_query(filters.regex("^ADD_CHAT_INVETE$"))
async def ON_ADD_CHAT_INVETE(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text="⌔︙ꜱᴇɴᴅ ᴍᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ", 
        reply_markup=Keyboards.BACK_MAIN()
    )
    try:
        data : types.Message = await app.listen(
            chat_id=query.message.chat.id,
            filters=filters.private & filters.text, 
            timeout=120
        )
    except ListenerTimeout as e:
        return 0
    
    botData = getData()
    LINK = data.text
    # Start App 
    if datas['app'] is None:
        datas['app'] = Client(
            name="RAID", 
            no_updates=True,
            session_string=botData['session']['session']
        )
        try:
            await datas['app'].connect()
            datas['app'].me = await datas['app'].get_me()
        except Exception as e:
            print(e)
            await query.edit_message_text(
                text="⌔︙There is a problem with the account..", 
                reply_markup=Keyboards.BACK_MAIN()
            )
            return
    chatdata = await datas['app'].get_chat(LINK)



@Client.on_callback_query(IS_SPLIT("SHOW_MESSAGE_CHAT"))
async def ON_SHOW_MESSAGE_CHAT(app: Client, query: types.CallbackQuery):
    botData = getData()
    ID =  query.data.split("|")[1]
    message = ""
    for i in botData['messages'][int(ID)]['chat']:
        message+=f"{botData['chats'][i]['title']}\n{botData['chats'][i]['id']}\n" + "="*10 + '\n'

    await query.answer(message , show_alert=True)



@Client.on_callback_query(filters.regex("^ADD_CHAT_JOINGROUP$"))
async def ON_ADD_CHAT_JOINGROUP(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text="⌔︙ʟᴏᴀᴅɪɴɢ ᴛʜᴇ ɢʀᴏᴜᴘꜱ ᴛʜᴀᴛ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ ɪᴛ."
    )
    botData = getData()
    if datas['app'] is None:
        datas['app'] = Client(
            name="RAID", 
            no_updates=True,
            session_string=botData['session']['session']
        )
        try:
            await datas['app'].connect()
            datas['app'].me = await datas['app'].get_me()
        except Exception as e:
            print(e)
            await query.edit_message_text(
                text="⌔︙There is a problem with the account..", 
                reply_markup=Keyboards.BACK_MAIN()
            )
            return
        
    chats = {}
    async for i in datas['app'].get_dialogs():
        if i.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP] and i.chat.members_count > 3 and str(i.chat.id) not in botData['chats']:
            chats.update({i.chat.id:{
                'title':i.chat.title or i.chat.name, 
                'username':i.chat.username, 
                'id':i.chat.id, 
                'type':str(i.chat.type) 
            }})
    if not chats:
        return await query.edit_message_text(
            text="⌔︙ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ɢʀᴏᴜᴘꜱ ɪɴ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴏʀ ᴀʟʟ ɢʀᴏᴜᴘꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ", 
            reply_markup=Keyboards.BACK_MAIN()
        )
    temp['chatsJoing'] = chats
    await query.edit_message_text(
        text="⌔︙ʟɪꜱᴛ ᴏꜰ ɢʀᴏᴜᴘꜱ ɪ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ", 
        reply_markup=Keyboards.SELECT_JOING_CHAT(chats)
    )





@Client.on_callback_query(IS_SPLIT("ADD_GROUP"))
async def ON_ADD_GROUP(app: Client, query: types.CallbackQuery):
    chatData = getData()
    chatID = int(query.data.split("|")[1])
    if chatID in chatData['chats']:
        return await query.answer(text="ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴘʀᴇᴠɪᴏᴜꜱʟʏ.", show_alert=True)
    
    chat = temp['chatsJoing'][chatID]
    chatData['chats'].update({chatID:chat})
    updateData(chatData)
    
    temp['chatsJoing'].pop(chatID)
    await query.answer(text="ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ.", show_alert=True)

    await query.edit_message_text(
        text="⌔︙ʟɪꜱᴛ ᴏꜰ ɢʀᴏᴜᴘꜱ ɪ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ", 
        reply_markup=Keyboards.SELECT_JOING_CHAT(temp['chatsJoing'])
    )


@Client.on_callback_query(filters.regex("^SHOW_CHAT$"))
async def ON_SHOW_CHATS(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text="⌔︙List of groups", 
        reply_markup=Keyboards.SHOW_CHAT()
    )


@Client.on_callback_query(IS_SPLIT("DELETE_CHAT"))
async def ON_DELETE_CHAT(app: Client, query: types.CallbackQuery):
    chatID = query.data.split("|")[1]
    botData = getData()
    botData['chats'].pop(chatID)
    for e ,i in enumerate(botData['messages']):
        if chatID in i['chat']:
            if len(i['chat']) == 1:
                botData['messages'].pop(e)
            else:
                botData['messages'][e]['chat'].remove(chatID)
                
    updateData(botData)
    await query.answer(text="Done Delete Group", show_alert=True)
    await query.edit_message_text(
        text="⌔︙List of groups", 
        reply_markup=Keyboards.SHOW_CHAT()
    )





@Client.on_callback_query(filters.regex("^ADD_MESSAGE$"))
async def ON_ADD_MESSAGE(app: Client, query: types.CallbackQuery):
    botData = getData()
    if not botData['chats']:
        await query.edit_message_text(
            text="⌔︙Add groups first.", 
            reply_markup=Keyboards.BACK_MAIN()
            )
        return
    await query.edit_message_text(
        text="⌔︙ꜱᴇɴᴅ ᴍᴇ ᴍᴇꜱꜱᴀɢᴇ", 
        reply_markup=Keyboards.BACK_MAIN()
    )
    try:
        data : types.Message = await app.listen(
            chat_id=query.message.chat.id,
            filters=filters.private & filters.text, 
            timeout=120
        )
    except ListenerTimeout as e:
        return 0

    MESSAGE = data.text
    temp['message_data'] = {'text':MESSAGE}

    temp['addMessageChatSelect'] = {ID: False for ID in botData['chats']}
    await data.reply(
        text="⌔︙ꜱᴇʟᴇᴄᴛ ᴛʜᴇ ɢʀᴏᴜᴘ ᴛᴏ ᴡʜɪᴄʜ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ꜱᴇɴᴛ.", 
        reply_markup=Keyboards.SELECT_CHAT()
    )


@Client.on_callback_query(IS_SPLIT("SELECT_CHAT"))
async def ON_SELECT_CHAT(app : Client, query: types.CallbackQuery):
    chatID = query.data.split("|")[1]
    temp['addMessageChatSelect'][chatID] = not temp['addMessageChatSelect'][chatID]
    await query.edit_message_text(
        text="⌔︙ꜱᴇʟᴇᴄᴛ ᴛʜᴇ ɢʀᴏᴜᴘ ᴛᴏ ᴡʜɪᴄʜ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ꜱᴇɴᴛ.", 
        reply_markup=Keyboards.SELECT_CHAT()
    )



@Client.on_callback_query(filters.regex("^DONE_SELECT_MESSAGE_CHAT$"))
async def DONE_SELECT_MESSAGE_CHAT(app: Client, query: types.CallbackQuery):
    if all(i == False for i in temp['addMessageChatSelect'].values()):     
        return await query.answer(text="⌔︙ᴘʟᴇᴀꜱᴇ ꜱᴇʟᴇᴄᴛ ɢʀᴏᴜᴘꜱ ꜰɪʀꜱᴛ.", show_alert=True)

    groups = [i for i in temp['addMessageChatSelect'] if temp['addMessageChatSelect'][i]]
    await query.edit_message_text(
        text="⌔︙Send the number of seconds between each message.",
    )
    try:
        data : types.Message = await app.listen(
            chat_id=query.message.chat.id,
            filters=filters.private & filters.text, 
            timeout=120
        )
    except ListenerTimeout as e:
            return 0
    

    if not data.text.isdigit():
        await data.reply(
            text="⌔︙ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴏɴʟʏ ɴᴜᴍʙᴇʀꜱ.", 
            reply_markup=Keyboards.BACK_MAIN()
        )
        return
    
    botData = getData()
    sleeps = int(data.text)
    botData['messages'].append(
        {
            'text':temp['message_data']['text'],
            'chat':groups, 
            'sleeps':sleeps
        }
    )

    updateData(botData)        
    temp.clear()
    await data.reply(
        text=f"⌔︙ ᴍᴇꜱꜱᴀɢᴇ ᴀᴅᴅᴇᴅ. ɴᴜᴍʙᴇʀ ᴏꜰ ᴍᴇꜱꜱᴀɢᴇꜱ ɴᴏᴡ {len(botData['messages'])}.", 
        reply_markup=Keyboards.BACK_MAIN()
    )



@Client.on_callback_query(filters.regex("^SHOW_MESSAGE$"))
async def ON_SHOW_MESSAGES(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text="⌔︙Message list", 
        reply_markup=Keyboards.SHOW_MESSAGES()
    )

@Client.on_callback_query(IS_SPLIT("SHOW_MESSAGE"))
async def ON_SHOW_MESSAGE(app: Client, query: types.CallbackQuery):
    ID = int(query.data.split("|")[1])
    botData = getData()
    await query.edit_message_text(
        text=botData['messages'][ID]['text'], 
        reply_markup=Keyboards.BACK_MENU("SHOW_MESSAGE")
    )


@Client.on_callback_query(IS_SPLIT("DELETE_MESSAGE"))
async def ON_DELETE_MESSAGES(app: Client, query: types.CallbackQuery):
    ID = int(query.data.split("|")[1])
    botData = getData()
    botData['messages'].pop(ID)
    updateData(botData)

    await query.answer(text="⌔︙Done Delete Message", show_alert=True)
    await query.edit_message_text(
        text="⌔︙Message list", 
        reply_markup=Keyboards.SHOW_MESSAGES()
    )




async def autoMessageProcess(message: dict, chatData: dict):
    while True:
        if not datas['status']:
            break
        for i in message['chat']:
            try:
                await datas['app'].send_message(
                    chat_id=int(i), 
                    text=message['text'], 
                )
            except ChannelInvalid as e:
                await datas['app'].join_chat(chatData[i]['username'])
            except Exception as e:
                print(e)
        await asyncio.sleep(message['sleeps'])



@Client.on_callback_query(filters.regex("^START_PUBLISH$"))
async def ON_START_PUBLISH(app: Client, query: types.CallbackQuery):
    if datas['status']:
        datas['status'] = False
        await query.edit_message_text(
            text="⌔︙Done Stop Auto Send", 
            reply_markup=Keyboards.BACK_MAIN()
        )
        return
    botData = getData()
    if not botData['session']['id']:
        await query.edit_message_text(
            text="⌔︙Add an account first.", 
            reply_markup=Keyboards.BACK_MAIN()
        )
        return
    if not botData['chats']:
        await query.edit_message_text(
            text="⌔︙Add groups first.", 
            reply_markup=Keyboards.BACK_MAIN()
            )
        return
    
    datas['status'] = True
    if datas['app'] is None:
        datas['app'] = Client(
            name="RAID", 
            no_updates=True,
            session_string=botData['session']['session']
        )
        try:
            await datas['app'].connect()
            datas['app'].me = await datas['app'].get_me()
        except Exception as e:
            print(e)
            await query.edit_message_text(
                text="⌔︙There is a problem with the account..", 
                reply_markup=Keyboards.BACK_MAIN()
            )
            return
        
    tasks = []
    for msg in botData['messages']:
        tasks.append(asyncio.create_task(autoMessageProcess(msg, botData['chats'])))
    
    asyncio.gather(*tasks)

    await query.edit_message_text(
        text="⌔︙Automatic publishing is turned on.", 
        reply_markup=Keyboards.BACK_MAIN()
    )

    

@Client.on_callback_query(filters.regex("^CLEAER_DATABASE$"))
async def ON_CLEAER_DATABASE(app: Client, query: types.CallbackQuery):
    await query.edit_message_text(
        text="⌔︙Are you sure you want to delete all data?", 
        reply_markup=Keyboards.CHECK_CLEAER_DATABASE()
    )


@Client.on_callback_query(filters.regex("^START_CLAER$"))
async def ON_START_CLAER(app: Client, query: types.CallbackQuery):
    updateData(DATA_DANTIC)
    await query.edit_message_text(
        text="⌔︙All data has been deleted.", 
        reply_markup=Keyboards.BACK_MAIN()
    )
