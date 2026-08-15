import discord
from discord.ext import commands
import google.generativeai as genai
import asyncio
from flask import Flask
from threading import Thread

# === TẠO WEB SERVER ĐỂ ĐÁP ỨNG GÓI FREE CỦA RENDER ===
app = Flask('')
@app.route('/')
def home():
    return "Bot đang chạy ngon lành cành đào!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# === CẤU HÌNH THÔNG SỐ CỦA BẠN ===
TOKEN = "MTQ3NjU5ODU0Mjg1MTExNzIxNw.GkEYwX.o7pon81hAmZYZFteLEtGE68pOAkO3BbrqKQtOU"
VOICE_CHANNEL_ID = 1522697019393577163  # ID phòng voice
GEMINI_API_KEY = "AQ.Ab8RN6JzuSb2oxna_5zE6xIjtDwuNDeu6G6AbW6G0nxurVSOfQ"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Bạn là một GenZ cọc cằn, thích khịa, nói chuyện hơi mất dạy, thô nhưng thật, hay dùng từ lóng GenZ Việt Nam (ví dụ: vô tri, chê, ét ô ét, cứu con tim, lụy, xu cà na, đỉnh nóc kịch trần, keo lì...). Trả lời thật ngắn gọn, cục súc nhưng hài hước. Không bao giờ xưng 'tôi với tư cách là AI', hãy đóng vai một đứa bạn toxic trong nhóm chat."
)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 {bot.user.name} online rồi chiến thần ơi!')
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print(f'✅ Đã treo voice tại: {channel.name}')
        except Exception as e:
            print(f'❌ Lỗi vào voice: {e}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    import random
    if bot.user.mentioned_in(message) or random.random() < 0.3:
        clean_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if not clean_text: clean_text = "Nói gì đi chứ gõ cái gì đấy?"
        try:
            async with message.channel.typing():
                response = model.generate_content(clean_text)
                await message.reply(response.text)
        except Exception as e:
            print(f"Lỗi AI: {e}")
    await bot.process_commands(message)

# Chạy web server ở luồng phụ, bot ở luồng chính
def keep_alive():
    t = Thread(target=run_web)
    t.start()

keep_alive()
bot.run(TOKEN)
