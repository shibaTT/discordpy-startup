import discord
import time
import datetime
import asyncio
import random
import requests
from discord.ext import tasks  # taskというライブラリをdiscord.extという名前にしてる？
from discord.ext import commands
import os
import http.client  # 天気予報用（Open Weather Map）

bot = commands.Bot(command_prefix='/')
token = "NzgxODI2NDM1NzI3MjI4OTU5.X8DSmw.JytE2U5h4oEywPythu8A6oXHFNY"

## Global settings ##
# client = discord.Client()  # なぜかclientに情報が入ってないらしい。逆にbot(変数)にデータがすべて格納されてるっぽい？
channelID = 781878197465120808  # これ砂場のIDでした
vChannelID = 758983784963637252

## OpenWeatherMap API ##
w_api = "43835b975fd8940129162cb4fb64dafd"
we_api = ""

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

    # 月曜～金曜の間で
    if dt_now.weekday() >= 0 and dt_now.weekday() < 5:

        # 8:50になったら
        if dt_now.hour == 14:
           # if dt_now.minute == 50:
            voice = await discord.VoiceChannel.connect(bot.get_channel(vChannelID))
            audioSource = discord.FFmpegPCMAudio(
                source="E:\Documents\ようわからんデータ入れ場\discord.py\zihoo\\12zi.wav", executable="E:\Documents\ようわからんデータ入れ場\discord.py\zihoo\\ffmpeg.exe")
            voice.play(audioSource)
            time.sleep(10)
            await voice.disconnect()

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
    payload = {'city': '130010'}
    weather_data = requests.get(url, params=payload).json()
    w_date = weather_data['forecasts'][0]['date']
    w_telop = weather_data['forecasts'][0]['telop']
    # w_max = weather_data['forecasts'][0]['temperature']['max']['celsius']
    # w_min = weather_data['forecasts'][0]['temperature']['min']['celsius']

    if weather_data['forecasts'][0]['temperature']['max'] is None:
        w_max = "--"
    else:
        w_max = weather_data['forecasts'][0]['temperature']['max']['celsius']

    if weather_data['forecasts'][0]['temperature']['min'] is None:
        w_min = "--"
    else:
        w_min = weather_data['forecasts'][0]['temperature']['min']['celsius']

    await ctx.send("今日の東京の天気は" + w_telop + "です。\n最高気温は" + w_max + "度、最低気温は" + w_min + "度です。\n今日も1日ご安全に、ヨシ！")


@bot.command()
async def getget(ctx):
    w_lat = 18.55  # 緯度
    w_lon = 154.40  # 経度
    conn = http.client.HTTPSConnection(
        "community-open-weather-map.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "4944761566mshcf99993c914aa21p1db9d0jsn4589ecd92bae"
    }

    conn.request(
        "GET", "/forecast?q=tokyo%252Cjp&units=metric&lang=ja", headers=headers)

    response = conn.getresponse().read()

    w_telop = response["daily"][0]["weather"][0]["description"]
    w_max = response["daily"][0]["temp"]["max"]
    w_min = response["daily"][0]["temp"]["min"]
    w_pres = response["daily"][0]["pressure"]

    await ctx.send("今日の東京の天気は" + w_telop + "です。\n最高気温は" + str(w_max) + "度、最低気温は" + str(w_min) + "度です。\n今日も1日ご安全に、ヨシ！")

    await ctx.send(response)


@bot.command()
async def openweather(ctx):
    w_lat = 35.41  # 緯度
    w_lon = 139.45  # 経度
    api = "http://api.openweathermap.org/data/2.5/onecall?units=metric&lat={lat}&lon={lon}&APPID={key}&lang=ja"

    url = api.format(lat=w_lat, lon=w_lon, key=w_api)
    response = requests.get(url).json()
    """w_telop = response["daily"][0]["weather"][0]["description"]
    w_max = response["daily"][0]["temp"]["max"]
    w_min = response["daily"][0]["temp"]["min"]"""

    # await ctx.send("今日の東京の天気は" + w_telop + "です。\n最高気温は" + str(w_max) + "度、最低気温は" + str(w_min) + "度です。\n今日も1日ご安全に、ヨシ！")

    await ctx.send(response["daily"])


@bot.command(aliases=["bosyuu", "boshuu", "boshu"])
async def bosyu(ctx, *args):

    if args:
        if args[1]:
            if args[1].isdigit():
                number = int(args[1])
            else:
                await ctx.send("人数の指定方法が不正です。もう一度やり直してください")
            if type(number) is int:
                msg = await ctx.send("everyone 募集件名「{}」、人数は「{}人」で募集します。\n参加したい人は :poop: スタンプを押してください。\nバツのスタンプを押すと募集終了します。".format(
                    args[0], number))
                await msg.add_reaction("💩")
                await msg.add_reaction("✖")
                rec_members = []  # 参加者リスト

                while len(rec_members) < number:
                    target_reaction = await bot.wait_for('reaction_add')
                    # print(target_reaction)
                    print(target_reaction)
                    if target_reaction[1].name != msg.author.name:
                        if target_reaction[0].emoji == '💩':
                            if target_reaction[1] in rec_members:
                                await ctx.send("すでにリストに存在してるが？")
                            else:
                                rec_members.append(target_reaction[1])
                                # await ctx.send('(テスト用){}を追加'.format(target_reaction[1]))
                        elif target_reaction[0].emoji == '✖':
                            if len(rec_members) <= 0:
                                for_aho_msg = 'こいつ({})参加者いないから「{}」の募集終了しやがったｗ'.format(
                                    target_reaction[1].name, args[0])
                                await msg.edit(content=for_aho_msg)
                                break
                            else:
                                join_members = ""
                                mention_members = ""
                                for item in rec_members:
                                    join_members += item.name + '　'
                                    mention_members += "<@" + \
                                        str(item.id) + "> "
                                for_forced_msg = mention_members + f"「{args[0]}」の募集は強制終了されました。\n【参加者】\n" + \
                                    join_members
                                await msg.edit(content=for_forced_msg)
                                break
                else:
                    join_members = ""
                    mention_members = ""
                    for item in rec_members:
                        join_members += item.name + '　'
                        mention_members += "<@" + str(item.id) + "> "
                    for_end_msg = mention_members + f"「{args[0]}」の募集は定員に達したため終了しました。\n【参加者】\n" + \
                        join_members
                    await msg.edit(content=for_end_msg)
        else:
            await ctx.send("人数が入力されていません")
    else:
        await ctx.send("募集したいときは、「\/bosyu AmongUsやる 100」のように、コマンドのあとに半角スペースを開けて「件名」と「人数（整数）」を入力してください。")


on_timeSignal.start()
bot.run(token)
