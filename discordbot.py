import discord
import time
import datetime
import asyncio
from discord.ext import tasks  # taskというライブラリをdiscord.extという名前にしてる？
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

## Global settings ##
client = discord.Client()
channelID = 758983784963637251
vChannelID = 758983784963637252

if not discord.opus.is_loaded(): 
    #もし未ロードだったら
    discord.opus.load_opus("heroku-buildpack-libopus")

## 初期設定 ##
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    game = discord.Game("時報")
    await client.change_presence(activity=game)


@tasks.loop(seconds=60)
async def on_timeSignal():
    dt_now = datetime.datetime.now()
    await client.wait_until_ready()  # on_ready内でget_channelしないとエラー出るので、その対策
    channel = client.get_channel(channelID)  # チャンネルの対象IDからチャンネル情報を取得
    # ボイスチャンネルにジョイン、部屋情報をvoiceに格納
    # await channel.send("on_timeSignalのループ始動")
    # ボイスチャンネルの参考元:https://qiita.com/sizumita/items/cafd00fe3e114d834ce3
    # ↑情報古いので関数名とクラス名変わってますです

    # 月曜～金曜の間で
    if dt_now.weekday() >= 0 and dt_now.weekday() < 5:

        # 8:50になったら
        if dt_now.hour == 8:
            if dt_now.minute == 50:
                await channel.send("8時50分になりました！「出社」をお忘れなく！")

        elif dt_now.hour == 12:
            if dt_now.minute == 0:
                await channel.send("12時です！お昼ごはんを食べましょう")

        elif dt_now.hour == 13:
            if dt_now.minute == 0:
                await channel.send("13時です！早く仕事に戻ってください！")

        elif dt_now.hour == 16:
            if dt_now.minute == 50:
                voice = await discord.VoiceChannel.connect(client.get_channel(vChannelID))
                await channel.send("退勤！！！！！！！！！！！！！")
                audioSource = discord.FFmpegPCMAudio("18zi.wav")
                voice.play(audioSource)
                time.sleep(10)
                
                await voice.disconnect()
                # await channel.send("まもなく夕会のお時間です。日報の提出をお願いします。")

        elif dt_now.hour == 18:
            if dt_now.minute == 0:
                voice = await discord.VoiceChannel.connect(client.get_channel(vChannelID))
                await channel.send("退勤！！！！！！！！！！！！！")
                audioSource = discord.FFmpegPCMAudio("18zi.wav")
                voice.play(audioSource)
                time.sleep(10)
                
                await voice.disconnect()

on_timeSignal.start()
bot.run(token)
