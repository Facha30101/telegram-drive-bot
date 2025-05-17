import logging
import os
import tempfile
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID", None)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ✅ Autenticación Google Drive con Service Account
gauth = GoogleAuth()
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", ['https://www.googleapis.com/auth/drive']
)
drive = GoogleDrive(gauth)

user_temp_files = {}

@dp.message(lambda message: message.photo or message.video)
async def handle_media(message: types.Message):
    file = message.photo[-1] if message.photo else message.video
    file_info = await bot.get_file(file.file_id)
    file_path = file_info.file_path

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        await bot.download_file(file_path, tmp)
        user_temp_files[message.from_user.id] = tmp.name
        await message.reply("✅ Archivo recibido. Ahora enviá el nombre con el que querés guardarlo (sin extensión).")

@dp.message()
async def handle_filename(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_temp_files:
        await message.reply("⚠️ Primero tenés que enviar una foto o video.")
        return

    file_path = user_temp_files.pop(user_id)
    filename = message.text.strip() + os.path.splitext(file_path)[-1]

    file_drive = drive.CreateFile({
        'title': filename,
        'parents': [{'id': DRIVE_FOLDER_ID}] if DRIVE_FOLDER_ID else []
    })
    file_drive.SetContentFile(file_path)
    file_drive.Upload()

    os.remove(file_path)

    await message.reply(f"📤 Archivo subido a Google Drive como *{filename}*", parse_mode=ParseMode.MARKDOWN)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
