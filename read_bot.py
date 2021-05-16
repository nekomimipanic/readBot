#!/usr/bin/env python3
import discord
from discord.ext import commands
import asyncio
import os
import subprocess
import ffmpeg
from voice_generator import creat_WAV
import tempfile
import os
import time

client = commands.Bot(command_prefix='!')
voice_client = None


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command()
async def join(ctx):
    print('#join')
    print('#voicechannelを取得')
    vc = ctx.author.voice.channel
    print('#voicechannelに接続')
    await vc.connect()
    await ctx.send('`読み替えは「!reg 名前　読み方」で登録します。読上終了は!byeで、\n別のチャンネルに呼ぶときは、そのチャンネルで!joinしてください`')

@client.command()
async def bye(ctx):
    print('#bye')
    print('#切断')
    await ctx.voice_client.disconnect()

@client.command()
async def reg(ctx, arg1, arg2):
    with open('/opt/readBot-master/dic.txt', mode='a') as f:
        f.write('\n'+ arg1 + ',' + arg2)
        print('dic.txtに書き込み：''\n'+ arg1 + ',' + arg2)
    await ctx.send('`' + arg1+'` を `'+arg2+'` として登録しました')

@client.event
async def on_voice_state_update(member, before, after):
    server_id_test = "サーバーID"
    text_id_test = "通知させたいテキストチャンネルID"


    if member.guild.id == server_id_test:   # サーバーid
        text_ch = client.get_channel(text_id_test)   # 通知させたいTEXTチャンネルid
        if before.channel is None:
            msg = f'【VC参加ログ】{member.name} が {after.channel.name} に参加しました。'
            await text_ch.send(msg)

@client.event
async def on_message(message):
    print('---on_message_start---')
    msgclient = message.guild.voice_client
    print(msgclient)
    if message.content.startswith('!'):
        pass
    elif message.content.startswith('`'):
        pass
    elif message.content.startswith('<'):
        pass
    else:
        while (message.guild.voice_client.is_playing()):
            await asyncio.sleep(1)
        if message.guild.voice_client:
            vt_fd, voice_tmp = tempfile.mkstemp()
            print('#message.content:'+ message.author.name + ':' + message.content)
            creat_WAV(message.author.name + '  ' + message.content, voice_tmp)
            source = discord.FFmpegPCMAudio(voice_tmp)
            message.guild.voice_client.play(source)
            await asyncio.sleep(0.5)
            os.remove(voice_tmp)
        else:
            pass
    await client.process_commands(message)
    print('---on_message_end---')

client.run("でぃすこーどのえーぴーあいきー")
