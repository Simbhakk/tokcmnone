import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import UsernameNotOccupied, FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, Message
from time import time
from uuid import uuid4
from pyrogram.errors import UserIsBlocked, InputUserDeactivated
from database import add_user, del_user, full_userbase, present_user
from short import short_url
import logging
import time
import os
import threading
import json

user=[]
user_data = {}
WAIT_MSG = """"<b>Processing ...</b>"""
REPLY_ERROR = 'error found'
START_TEXT = 'Hi👋, I am Save Restricted Content Bot.\n\n**•FROM PUBLIC CHANNELS**\n-Send direct message/video link to clone it here.\ne.g:- `https://t.me/rajz_bots/72`\n\n🚨`NOTE:-` Our bot does not support \nPRIVATE CHANNEL/GROUP.\n\nJoin for update:- @Save_Restricted_contentz'
#config
def getenv(var): return os.environ.get(var) or DATA.get(var, None)

bot_token = getenv("TOKEN") 
api_hash = getenv("HASH") 
api_id = getenv("ID")
CHANNEL = getenv("CHANNEL")
TOKEN_TIMEOUT = getenv("TOKEN_TIMEOUT")
bot_name = getenv("BOT_NAME")

bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
#shorthandler
def checking_access(message):
    user_id = message.from_user.id
    if TOKEN_TIMEOUT:
        user_data.setdefault(user_id, {})
        data = user_data[user_id]
        expire = data.get('time')
        is_expired = expire is None or (time.time() - float(expire)) > float(TOKEN_TIMEOUT)
        if is_expired:
            token = data.get('token') or str(uuid4())
            if expire is not None:
                del data['time']
            data['token'] = token
            user_data[user_id].update(data)             
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Click here to verify", url=short_url(f"https://telegram.me/{bot_name}?start={token}"))]
                ]
            )
   # Send a message with the keyboard
            message.reply_text('**Generate New token to use me**\n\nHow to verify:- <a href="https://youtube.com/shorts/-RrEXn9dXXM">Click For video</a>.',disable_web_page_preview = True, reply_markup=keyboard)
	
            return False
    return True, None
#close
@bot.on_callback_query(filters.regex("cancel"))
def cancel(client, callback_query):
    callback_query.message.delete()
#help
@bot.on_message(filters.command("help"))
def help(_, message):
    message.reply_text(START_TEXT,
                       reply_markup=InlineKeyboardMarkup(
                           [
                               [InlineKeyboardButton('👁️ Close', callback_data='cancel')]
                           ]
                       ))
#users
@bot.on_message(filters.command('users'))
def get_users(client, message):
    msg = client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = full_userbase()
    msg.edit(f"{len(users)} users are using this bot",
    reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('👁️ Close', callback_data='cancel')]
        ]
    ))
#broadcast
@bot.on_message(filters.command('broadcastingi'))
def send_text(client, message):
    if message.reply_to_message:
        query = full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                asyncio.sleep(e.x)
                broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return pls_wait.edit(status)

    else:
        msg = message.reply('REPLY_ERROR')
        asyncio.sleep(8)
        msg.delete()
# start command
@bot.on_message(filters.command("start"))
def start(client, message):
    id = message.from_user.id
    if not present_user(id):
        try:
            add_user(id)
        except Exception as e:
            pass
    text = message.text
    if len(message.command) > 1:
        userid = message.from_user.id
        input_token = message.command[1]
        if userid not in user_data:
            return message.reply_text('**Who are you?**')
        data = user_data[userid]
        if 'token' not in data or data['token'] != input_token:
            return message.reply_text('**This token is already expired. Generate new to use me.**')
        data['token'] = str(uuid4())
        data['time'] = time.time()
        user_data[userid].update(data)
        # Assuming TOKEN_TIMEOUT is in seconds
        token_refresh_minutes = int(TOKEN_TIMEOUT) // 60  # Convert seconds to minutes
        return bot.send_message(message.chat.id, f'**Token refresh successfully for {token_refresh_minutes} min.**\nSend link to use me.')
    else:
        message.reply_text(
            text=START_TEXT.format(message.from_user.first_name),
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('📍 Update Channel', url='https://t.me/Rajz_bots'),
                ],
                [
                    InlineKeyboardButton('👩‍💻 SOURCE', url='https://t.me/Save_Restricted_contentz/19'),
                    InlineKeyboardButton('🍻 Support Group', url='https://t.me/Save_Restricted_contentz'),
                ],
                [
                    InlineKeyboardButton('👁️ Close', callback_data='cancel')
                ]
            ]
        ))
#save
@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    print(message.text)
    id = message.from_user.id
    if not present_user(id):
        try:
            add_user(id)
        except:
            pass
    if CHANNEL:
        fsub = handle_force_subscribe(client, message)
        if fsub == 400:
            return

    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text or "https://t.me/c/" in message.text or "https://t.me/b/" in message.text:
        bot.send_message(message.chat.id, "Bot supports only public restricted channel.")
        return

    if not checking_access(message):
        return

    # getting message
    elif "https://t.me/" in message.text:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        for msgid in range(fromID, toID+1):
            username = datas[3]
            try:
                msg = bot.get_messages(username, msgid)
            except FloodWait as fw:
                hours, remainder = divmod(fw.value, 3600)
                minutes, seconds = divmod(remainder, 60)
                bot.send_message(message.chat.id, f"Try again after {hours} hours, {minutes} minutes, and {seconds} seconds due to floodwait from telegram.\n Or use our second bot:- @Save_Restricted_contentx_Bot 🤭", reply_to_message_id=message.id)
            except UsernameNotOccupied:
                bot.send_message(message.chat.id, "The username is not occupied by anyone", reply_to_message_id=message.id)
                return

            try:
                bot.copy_message(message.chat.id, msg.chat.id, msg.id)
            except Exception as e:
                bot.send_message(message.chat.id,f"**Error** : __{e}__")
            time.sleep(3)

    else:
        bot.send_message(message.chat.id, "**Send a Valid link. Bro, press /help for more info.**")

#forcesub
def handle_force_subscribe(bot, message):
    try:
        invite_link = bot.create_chat_invite_link(int(CHANNEL))
    except FloodWait as e:
        asyncio.sleep(e.x)
        return 400
    try:
        user = bot.get_chat_member(int(CHANNEL), message.from_user.id)
        if user.status == "kicked":
            bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry Sir, You are Banned. Contact My [Support Group](https://t.me/+Xvc0oHwMwjU3ZDJl).",
                disable_web_page_preview=True,
            )
            return 400
    except UserNotParticipant:
        bot.send_message(
            chat_id=message.from_user.id,
            text="You have to join  @Save_Restricted_contentz to use me.\n First join this channel then use me."
	)
        return 400
    except Exception:
        bot.send_message(
            chat_id=message.from_user.id,
            text="Something Went Wrong. Contact My [Support Group](https://t.me/NT_BOTS_SUPPORT).",
            disable_web_page_preview=True,
        )
        return 400
# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
	try:
		msg.document.file_id
		return "Document"
	except: pass

	try:
		msg.video.file_id
		return "Video"
	except: pass

	try:
		msg.animation.file_id
		return "Animation"
	except: pass

	try:
		msg.sticker.file_id
		return "Sticker"
	except: pass

	try:
		msg.voice.file_id
		return "Voice"
	except: pass

	try:
		msg.audio.file_id
		return "Audio"
	except: pass

	try:
		msg.photo.file_id
		return "Photo"
	except: pass

	try:
		msg.text
		return "Text"
	except: pass
# infinty polling
bot.run()
