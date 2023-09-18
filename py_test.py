import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

# ReliveHD
# api_id = 25149133
# api_hash = "a2532dd4b45ceda3815cc826daefdfef"
# bot_token = "6082546372:AAHM33fkvArJpe8wU5IQeg0L4jOGNpHJe2Q"

# app = Client("showWithBo", api_id, api_hash, bot_token)
app = Client("showWithBo", bot_token="6082546372:AAHM33fkvArJpe8wU5IQeg0L4jOGNpHJe2Q")


def all_message(app: Client, message: Message):
    message.reply(message.text, quote=True, reply_to_message_id=message.id)
    print(message.location)

app.add_handler(MessageHandler(all_message))

app.run()
# asyncio.run(main())
# app.run(main())




# @app.on_message()
# async def my_handler(client, message):
#     await message.forward("me")


# app.run()


# @app.on_message()
# async def echo(client, message):
#     await message.reply(message.text)
#
# app.run()

# async def main():
#     async with Client("showWithBo") as app:
#         await app.send_message("me", "Это сообщение отправлено **программой**")
#
#
# async def main():
#     async with app:
#         # "me" refers to your own chat (Saved Messages)
#         async for message in app.get_chat_history("me"):
#             print(message)

#
# @app.on_message(filters.text & filters.private)
# async def echo(client, message):
#     await message.reply(message.text)


# @app.on_message()
# async def my_handler(client, message):
#     await message.forward("me")

# async def main():
#     async with app:
#         async for dialog in app.get_dialogs():
#             print(dialog.chat.title or dialog.chat.first_name)


# @app.on_callback_query()
# async def answer(client, callback_query):
#     await callback_query.answer(
#         f"Button contains: '{callback_query.data}'",
#         show_alert=True)

