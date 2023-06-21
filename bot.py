import discord
from discord.ext import commands
from discord.utils import get
from scraper import *
import datetime


def run_discord_bot():
    TOKEN = 'MTA0NTQxMjY4NzA2NjE3NzY0OA.G5Wh-w.ZElpoLzO4Hbmg7rj985clMCxVy0-RDVKgVPhFk'
    SERVER_ID = 1045395445163241563

    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running', flush=True)
        global TEST_CHANNEL
        TEST_CHANNEL = client.get_channel(1066412436850221056)
        await TEST_CHANNEL.send('BOT IS ONLINE')

    @client.command()
    async def start(ctx):
        date = datetime.datetime.now()
        time = str(date)[0: 16]
        embed = discord.Embed(title='ROUTE PROGRESS', description=f'{time}',
                              colour=discord.Colour.blue())
        data = new_format()
        datacopy = new_format()
        driver_names = []
        driver_stops = []
        driver_percent = []
        name_str = ''
        stop_str = ''
        percent_str = ''
        # Sort by % Completed
        sorted = []
        sort(data, sorted)
        for member in sorted:
            for driver in datacopy:
                if driver['name'] == member:
                    total = driver['total']
                    completed = driver['completed']
                    stops_str = f'{completed} / {total}'
                    driver_names.append(driver['name'])
                    driver_stops.append(stops_str)
                    sph = driver['sph']
                    sph = round(sph, 1)
                    per = driver['percent_complete']
                    per_full = str(per) + '%'
                    stat_str = f'{sph} SPH -- {per_full}'
                    driver_percent.append(stat_str)

        for name in driver_names:
            name_str += name + '\n'
        for stop in driver_stops:
            stop_str += stop + '\n'
        for status in driver_percent:
            percent_str += status + '\n'

        embed.set_author(
            name=f'|-----------------------------------------------------------------------|')
        embed.add_field(
            name='DRIVER | STOPS | SPH | PERCENT COMPLETE', value='AHEAD', inline=False)
        embed.add_field(name='DRIVER', value=name_str, inline=True)
        embed.add_field(name='STOPS', value=stop_str, inline=True)
        embed.add_field(name='STATS', value=percent_str, inline=True)
        await TEST_CHANNEL.send(embed=embed)

    @client.command()
    async def driverid(ctx):
        time_stamp = str(datetime.datetime.now())
        date = time_stamp[0:16]
        data = new_format()
        driver_name_str = ''
        driver_id_str = ''
        for driver in data:
            driver_name_str += str(driver['name']) + '\n'
            driver_id_str += str(driver['id']) + '\n'

        embed = discord.Embed(title=f'DRIVER ID\'S', description=f'{date}',
                              colour=discord.Colour.blue())
        embed.set_author(
            name=f'|---------------------------------------------------|')
        embed.add_field(name='DRIVER', value=driver_name_str, inline=True)
        embed.add_field(name='ID', value=driver_id_str, inline=True)
        await TEST_CHANNEL.send(embed=embed)

    @client.command()
    async def driverinfo(ctx):
        time_stamp = str(datetime.datetime.now())
        date = time_stamp[0:16]
        data = new_format()
        driver_name_str = ''
        driver_phone_str = ''
        for driver in data:
            driver_name_str += str(driver['name']) + '\n'
            if len(driver['phone']) == 12:
                num = driver['phone']
                area_code = num[2:5]
                p2 = num[5:8]
                p3 = num[8:12]
                temp_str = f'1-({area_code})-{p2}-{p3}'
                driver_phone_str += temp_str + '\n'
            else:
                driver_phone_str += str(driver['phone']) + '\n'

        embed = discord.Embed(title=f'DRIVER PHONE NUMBER', description=f'{date}',
                              colour=discord.Colour.blue())
        embed.set_author(
            name=f'|------------------------------------------------|')
        embed.add_field(name='DRIVER', value=driver_name_str, inline=True)
        embed.add_field(name='PHONE', value=driver_phone_str, inline=True)
        await TEST_CHANNEL.send(embed=embed)

    client.run(TOKEN)
