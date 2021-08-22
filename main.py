#Coder @sigaris
# module
from pyrogram import Client, filters, idle
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import requests, os, random

# config
from config import token, api_id, api_hash, sudo, id_bot, channel

# Client
tikTok = Client("Tiktok-bot", api_id=api_id, api_hash=api_hash, bot_token=token)

# join check
async def join_check(_, __, msg):
    try:
        await tikTok.get_chat_member(channel, msg.from_user.id)
        status = True
    except UserNotParticipant:
        await msg.reply_text(f"Para el uso gratuito del robot por favor únete\n{channel}")
        status = False

    return status

verify_filter = filters.create(join_check)

# download Tiktok
def downloader(video_url):
    req = requests.get(f"https://www.wirexteam.ga/tiktok/v1?url={video_url}").json()
    if req["result"] == False:
        return 404
    request = requests.Request(method='GET',url=req["tiktok"]["download"])
    prepared_request = request.prepare()
    session = requests.Session()
    response = session.send(request=prepared_request)
    response.raise_for_status()
    video = f"{random.choice('0123456789')}_TikTok.mp4"
    with open(os.path.abspath(video), 'wb') as output_file:
        output_file.write(response.content)
    return video, req["tiktok"]["music"]["download"], req["tiktok"]["user"]["author"],\
         req["tiktok"]["comments"], req["tiktok"]["likes"], req["tiktok"]["play"],\
              req["tiktok"]["shares"], req["tiktok"]["caption"],

#command start
@tikTok.on_message(filters.private & filters.command("start") & verify_filter)
async def start(client, update):
    await update.reply(" {update.from_user.mention} Bienvenido a TikTok Downloader Robot❤️\n Para continuar con tu enlace de publicación!**")


#command TikTok
@tikTok.on_message(filters.private & filters.regex('https://www.tiktok.com/(.*)') & verify_filter)
async def tiktok(client, update):
    msg = await update.reply("**Por favor, espere hasta que envíe una descarga...**")
    req = downloader(update.text)
    if req == 404:
        return await msg.edit("**Ha habido un problema !**")
    await client.send_video(update.chat.id, video=req[0], caption=f"**🗣 Cuenta : {req[2]}\n💬 Comentarios : {req[3]}\n❤️ Me gusta : {req[4]}\n👁 Visitas : {req[5]}\n👥 Compartidas: {req[6]}\n\n{req[7]}**")
    await client.send_audio(update.chat.id, audio=req[1], caption=f"Descarga: {id_bot}")
    await msg.delete()
    os.remove(req[0])
    return


tikTok.start()
idle()

