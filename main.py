import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from pytgcalls.types.stream import StreamAudioQuality
import yt_dlp

# --- CONFIGURATION (YAHAN APNI DETAILS DALEIN) ---
API_ID =      31453705         # <--- Apna API ID yahan dalein (bina quotes ke)
API_HASH = "dfc61d0510f0b21df29770ad4a374b8a" # <--- Aapka API Hash
BOT_TOKEN = "8986495273:AAH3rdE9sA-z8uXDg9CSCTP4geu68hoeCrk"   # <--- BotFather se mila token yahan dalein
CHAT_ID = -1003793631090      # <--- YAHAN APNE GROUP KI ID DALEIN (Bina quotes ke, -100 ke sath)

# Clients Initialize karein
app = Client("PhoenixMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

def get_premium_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url'], info.get('title', 'Unknown Track')

@app.on_message(filters.command("play") & filters.group)
async def play_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ **Usage:** `/play [YouTube Link]`")

    url = message.text.split(None, 1)[1]
    status = await message.reply_text("💎 **Analyzing Audio Stream for Best Quality...**")

    try:
        audio_url, title = get_premium_audio(url)
        
        stream = AudioPiped(
            audio_url,
            audio_parameters=StreamAudioQuality.HIGH
        )

        # Aapke specified CHAT_ID ke group voice chat me bot join karega
        await call_py.join_group_call(CHAT_ID, stream)
        await status.edit_text(f"🎧 **Now Playing in HD Quality:**\n🎵 `{title}`")

    except Exception as e:
        await status.edit_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command("stop") & filters.group)
async def stop_handler(client, message):
    try:
        await call_py.leave_group_call(CHAT_ID)
        await message.reply_text("🛑 **Stream stopped successfully.**")
    except Exception:
        await message.reply_text("❌ **Bot is not in voice chat.**")

if __name__ == "__main__":
    call_py.start()
    app.run()
  
