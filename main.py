import asyncio
from mcstatus import JavaServer
import time
import telegram
import json

servers = {
    "server": "1dedic.stankcraft.ru:25565",
    "hub": "10.8.0.2:25570",
    "surv_1": "10.8.0.2:25571"
}

json_path = "/var/www/html/monitoring.json"

tg_alerts = True
chat_id = ""
bot_token = ""


async def error_to_tg(server):
    bot = telegram.Bot(bot_token)
    async with bot:
        await bot.send_message(text=f"server {server} went to offline!", chat_id=chat_id)


def main():
    print("getting status in loop...")
    servers_ponline = {}
    for i in servers:
        servers_ponline[i] = {}

    while True:
        for i in servers:
            try:

                server = JavaServer.lookup(servers[i])
                status = server.status()

                servers_ponline[i]["online"] = True
                servers_ponline[i]["tg_alert_sended"] = False
                servers_ponline[i]["players_online"] = status.players.online
                servers_ponline[i]["players_max"] = status.players.max
                servers_ponline[i]["players_percentage"] = status.players.online / status.players.max * 100
            except:

                if not "tg_alert_sended" in servers_ponline[i] or servers_ponline[i]["tg_alert_sended"] == False:
                    print("tg alert initiated for " + str(i))
                    asyncio.run(error_to_tg(i))
                    servers_ponline[i]["tg_alert_sended"] = True
                servers_ponline[i]["online"] = False

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
