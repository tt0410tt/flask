import os

from flask import Flask, render_template
import asyncio
import datetime
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


from discord.ext import commands, tasks
app = Flask(__name__)
discord_intents = discord.Intents.default()
discord_intents.message_content = True
discord_intents.members = True
discord_token= os.getenv("discord")
client = commands.Bot(intents=discord_intents, status=discord.Status.online, command_prefix='!')

is_striming_on = False
strimg_name = ""

@app.route("/")
def index():
    client.run(discord_token)
    return render_template('./index.html')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))  # 봇이 실행되면 콘솔창에 표시
    client.loop.create_task(Get_Info(client))


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:  # 봇 자신이 보내는 메세지는 무시
        return

    if message.content == "!안뇽":
        await client.get_channel(1145229472333844511).send("@everyone " + message.content)
        return


async def Get_Info(client: discord.ext.commands.Bot):
    strimg_name = ""
    while True:
        now = datetime.datetime.now()
        if 0 == now.minute % 5:
            url = 'https://play.afreecatv.com/jymin2174'
            response = requests.post(url)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                a = soup.find_all("meta")
                for i in range(len(a)):
                    if "og:title" in str(a[i]):
                        print("확인용\t\t" + str(a[i])[15:-23])
                        if strimg_name == str(a[i])[15:-23]:
                            print(now)
                            print("2")
                            break
                            pass
                        else:
                            if "방송중이지 않습니다." == str(a[i])[15:-23]:
                                is_striming_on = False
                                await client.get_channel(1145229621764313138).send("방송off")
                            elif not is_striming_on:
                                is_striming_on = True
                                await client.get_channel(1145229621764313138).send("방송on")
                            print(now)
                            print("1")
                            strimg_name = str(a[i])[15:-23]
                            await client.get_channel(1145229472333844511).send(str(a[i])[15:-23])
                            await client.get_channel(1145229472333844511).send(now)
                            break
        else:
            pass
        await asyncio.sleep(60)

