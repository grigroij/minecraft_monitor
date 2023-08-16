import asyncio
from mcstatus import JavaServer
import time
import telegram
import json
from config import *

async def error_to_tg(server,status):
    if tg_alerts:
        print("tg alert initiated for " + str(server))
        bot = telegram.Bot(bot_token)
        async with bot:
            await bot.send_message(text=f"server {server} went to {status}!", chat_id=chat_id)


def main():
    print("getting status in loop...")
    servers_ponline = {}
    for i in servers:
        servers_ponline[i] = {"tg_alert_sended" : "undefined"}

    while True:
        for i in servers:
            try:
                server = JavaServer.lookup(servers[i])
                status = server.status()
                servers_ponline[i]["online"] = 'online'
                servers_ponline[i]["name"] = i
                servers_ponline[i]["motd"] = status.motd.raw.lstrip()
                servers_ponline[i]["players_online"] = status.players.online
                servers_ponline[i]["players_max"] = status.players.max
                servers_ponline[i]["players_percentage"] = round(status.players.online / status.players.max * 100, 1)
                servers_ponline[i]["latency"] = round(status.latency)
                #servers_ponline[i]["tg_alert_sended"] = 'online'
                if tg_alerts:
                    if servers_ponline[i]["tg_alert_sended"] != servers_ponline[i]["online"]:
                        asyncio.run(error_to_tg(i,servers_ponline[i]["online"]))
                        servers_ponline[i]["tg_alert_sended"] = servers_ponline[i]["online"]
            except:
                servers_ponline[i]["online"] = 'offline'
                if tg_alerts:
                    if servers_ponline[i]["tg_alert_sended"] != servers_ponline[i]["online"]:
                        asyncio.run(error_to_tg(i,servers_ponline[i]["online"]))
                        servers_ponline[i]["tg_alert_sended"] = servers_ponline[i]["online"]

        print(servers_ponline)
        json_object = json.dumps(servers_ponline, indent=4)
        try:
            file = open(json_path, "w")
            file.write(json_object)
            file.close()
        except:
            print("Error while creating file! Change the json_path")

        # print(json_object)
        time.sleep(10)


if __name__ == '__main__':
    main()
