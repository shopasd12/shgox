import os
import discord
from discord.ext import commands
import mimetypes
from flask import Flask
from threading import Thread

# กรอกโทเค็นบอทและ ID ของห้องที่ต้องการให้แสดงข้อความต้อนรับและลาก่อน
WELCOME_CHANNEL_ID = 1320391859322753080  # ใส่ ID ของห้องที่ต้องการให้แสดงข้อความต้อนรับที่นี่
GOODBYE_CHANNEL_ID = 1324706160644849697  # ใส่ ID ของห้องที่ต้องการให้แสดงข้อความลาก่อนที่นี่

# สร้างตัวแปรสำหรับบอท
intents = discord.Intents.default()
intents.members = True  # ให้บอทสามารถฟังการเข้าหรือออกของสมาชิกได้
bot = commands.Bot(command_prefix='!', intents=intents)

# ฟังก์ชัน server_no() ที่แสดงชื่อเซิร์ฟเวอร์
def server_no():
    print("ฟังก์ชัน server_no ถูกเรียกใช้งานแล้ว!")
    print(f"ชื่อเซิร์ฟเวอร์: {bot.guilds[0].name}")

# Flask Web Server
app = Flask('')

@app.route('/')
def home():
    return "Server is running!"

# ฟังก์ชันที่ใช้ในการเริ่มต้นเซิร์ฟเวอร์
def run_flask_server():
    app.run(host='0.0.0.0', port=8080)

# ฟังก์ชัน start_server ที่ใช้รันฟังก์ชัน run_flask_server ใน Thread
def start_server():
    t = Thread(target=run_flask_server)  # ใช้ target=run_flask_server แทน
    t.start()

# คำสั่งที่เมื่อบอทพร้อมทำงาน
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    server_no()  # เรียกใช้ฟังก์ชัน server_no เมื่อบอทออนไลน์
    start_server()  # เริ่มต้น Flask server หลังจากบอทออนไลน์

# การแสดงข้อความต้อนรับเมื่อมีคนเข้ามาในเซิร์ฟเวอร์
@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if welcome_channel:
        embed = discord.Embed(
            title=f'ยินดีต้อนรับ {member.name}!',
            description=f'🎉 ขอต้อนรับ {member.mention} เข้าสู่เซิร์ฟเวอร์ของเรา! 🎉\n\nID เซิร์ฟเวอร์: {member.guild.id}',
            color=discord.Color.green()
        )
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.set_thumbnail(url="https://f.ptcdn.info/065/072/000/qlxe2bdivctMDMB51ad-o.gif")  # GIF ด้านบนขวามือ
        embed.set_image(url="https://i.pinimg.com/originals/b0/bd/ab/b0bdabdb366b66f6840405500b1b5d82.gif")  # GIF ด้านล่าง
        await welcome_channel.send(embed=embed)

# การแสดงข้อความลาก่อนเมื่อมีคนออกจากเซิร์ฟเวอร์
@bot.event
async def on_member_remove(member):
    goodbye_channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if goodbye_channel:
        embed = discord.Embed(
            title=f'ลาก่อน {member.name}!',
            description=f'💔 ขอให้โชคดี {member.mention} ในการเดินทางของคุณ! 💔\n\nID เซิร์ฟเวอร์: {member.guild.id}',
            color=discord.Color.red()
        )
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.set_thumbnail(url="https://f.ptcdn.info/065/072/000/qlxe2bdivctMDMB51ad-o.gif")  # GIF ด้านบนขวามือ
        embed.set_image(url="https://i.pinimg.com/originals/b0/bd/ab/b0bdabdb366b66f6840405500b1b5d82.gif")  # GIF ด้านล่าง
        await goodbye_channel.send(embed=embed)

# การทำงานของบอท
bot.run(os.getenv('TOKEN'))
