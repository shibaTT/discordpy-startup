import discord
import time
import datetime
import asyncio
import random
import requests
from discord.ext import tasks  # taskというライブラリをdiscord.extという名前にしてる？
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

## Global settings ##
client = discord.Client()  # なぜかclientに情報が入ってないらしい。逆にbot(変数)にデータがすべて格納されてるっぽい？
channelID = 758983784963637251
vChannelID = 758983784963637252

# if not discord.opus.is_loaded():
# もし未ロードだったら
# discord.opus.load_opus("heroku-buildpack-libopus")

## 初期設定 ##
@bot.event
async def on_ready():
    # channel = bot.get_channel(channelID)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = discord.Game("時報です")
    await bot.change_presence(activity=game)


@tasks.loop(seconds=60)
async def on_timeSignal():
    dt_now = datetime.datetime.now()
    await bot.wait_until_ready()  # on_ready内でget_channelしないとエラー出るので、その対策
    channel = bot.get_channel(channelID)  # チャンネルの対象IDからチャンネル情報を取得
    # ボイスチャンネルにジョイン、部屋情報をvoiceに格納
    # await channel.send("on_timeSignalのループ始動")
    # ボイスチャンネルの参考元:https://qiita.com/sizumita/items/cafd00fe3e114d834ce3
    # ↑情報古いので関数名とクラス名変わってますです

    ## 天気情報の処理 ##
    url = 'https://weather.tsukumijima.net/api/forecast'
    payload = {'city': '471010'}
    weather_data = requests.get(url, params=payload).json()

    # 月曜～金曜の間で
    if dt_now.weekday() >= 0 and dt_now.weekday() < 5:

        # 8:50になったら
        if dt_now.hour == 8:
            if dt_now.minute == 50:
                await channel.send("8時50分になりました！「出社」をお忘れなく！")
                await channel.send("今日の那覇の天気は" + weather_data['telop'] + "です。\n最高気温は" + weather_data['temperature']['max']['celsius'] + "度です。最低気温は" + weather_data['temperature']['min']['celsius'] + "度です。\nお気をつけて、行ってらっしゃい！")

        elif dt_now.hour == 12:
            if dt_now.minute == 0:
                await channel.send("12時です！お昼ごはんを食べましょう")
                voice = await discord.VoiceChannel.connect(bot.get_channel(vChannelID))
                audioSource = discord.FFmpegPCMAudio("12zi.wav")
                voice.play(audioSource)
                time.sleep(10)
                await voice.disconnect()

        elif dt_now.hour == 13:
            if dt_now.minute == 0:
                await channel.send("13時です！早く仕事に戻ってください！")
                voice = await discord.VoiceChannel.connect(bot.get_channel(vChannelID))
                audioSource = discord.FFmpegPCMAudio("13zi.mp3")
                voice.play(audioSource)
                time.sleep(30)
                await voice.disconnect()

        elif dt_now.hour == 15:
            if dt_now.minute == 0:
                await channel.send("おやつの時間ですね。一度休憩しませんか？")
                voice = await discord.VoiceChannel.connect(bot.get_channel(vChannelID))
                audioSource = discord.FFmpegPCMAudio("15zi.wav")
                voice.play(audioSource)
                time.sleep(10)
                await voice.disconnect()

        elif dt_now.hour == 16:
            if dt_now.minute == 50:
                await channel.send("まもなく夕会のお時間です。日報の提出をお願いします。")
                voice = await discord.VoiceChannel.connect(bot.get_channel(vChannelID))
                audioSource = discord.FFmpegPCMAudio("17zi.wav")
                voice.play(audioSource)
                time.sleep(20)
                await voice.disconnect()

        elif dt_now.hour == 18:
            if dt_now.minute == 0:
                voice = await discord.VoiceChannel.connect(bot.get_channel(vChannelID))
                audioSource = discord.FFmpegPCMAudio("18zi.wav")
                voice.play(audioSource)
                time.sleep(10)
                await voice.disconnect()

                await channel.send("退勤ァ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！")


@bot.command(aliases=["un", "unsei"])
async def luck(ctx):
    fortune_list = ['大吉', '中吉', '吉', '小吉',
                    '末吉', '凶', '大凶', '判断が遅い', 'SSR', 'UR']
    fortune_length = len(fortune_list)

    await ctx.send(
        "今日の運勢は【" + fortune_list[random.randint(0, fortune_length - 1)] + "】だよ！")


@bot.command()
async def gacha(ctx):
    reality = ['☆☆☆☆☆(UR)', '☆☆☆☆(SSR)', '☆☆☆(SR)', '☆☆(R)', '☆(N)']
    prob = [0.06, 0.1, 0.175, 0.3, 0.7]

    n = random.choices(reality, weights=prob, k=10)  # 乱数で抽選。引数は「抽選対象」「確率」「総数」
    n = '\n'.join(n)

    await ctx.send("今回の10連の結果は以下になります。\n" + n)


@bot.command()
async def get_wea(ctx):
    ## 天気情報の処理 ##
    url = 'https://weather.tsukumijima.net/api/forecast'
    payload = {'city': '471010'}
    weather_data = requests.get(url, params=payload).json()

    # await ctx.send("今日の那覇の天気は" + weather_data['forecasts'][0]['telop'] + "です。\n最高気温は" + weather_data['forecasts'][0]['temperature']['max']['celsius'] + "度です。最低気温は" + weather_data['forecasts'][0]['temperature']['min']['celsius'] + "度です。\nお気をつけて、行ってらっしゃい！")
    ctx.send(weather_data)


on_timeSignal.start()
bot.run(token)
