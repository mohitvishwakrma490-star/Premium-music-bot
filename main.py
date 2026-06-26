import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from pytgcalls.types.stream import StreamAudioQuality
import yt_dlp
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- DUMMY WEB SERVER FOR RENDER FREE TIER ---
# Render free tier ko port chahiye hota hai, isliye hum ek chota server background me chala rahe hain
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Phoenix Music Bot is Running 24/7!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyServer)
    server.serve_forever()

# --- CONFIGURATION ---
API_ID =   31453705            
API_HASH = "dfc61d0510f0b21df29770ad4a374b8a" 
BOT_TOKEN = "8986495273:AAH3rdE9sA-z8uXDg9CSCTP4geu68hoeCrk"   # <--- Apna token dalein
CHAT_ID = -1003793631090     # <--- Apne group ki id dalein

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
        stream = AudioPiped(audio_url, audio_parameters=StreamAudioQuality.HIGH)
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
    # Web server ko alag thread me start karenge Render ko khush rakhne ke liye
    threading.Thread(target=run_web_server, daemon=True).start()
    call_py.start()
    app.run()
    
