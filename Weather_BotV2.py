import discord
import time
from discord.ext import commands, tasks
from discord import app_commands
import datetime
import asyncio
import json
import requests


#works in any channel
utc = datetime.timezone.utc

GUILD_ID = discord.Object(id=1293001574217547816)

#cache to stop multiple requsts from rate limiting discord and flooding bot
weather_cache = {
    'timestamp' : 0,
    'weather_Data_Copy' : None
}

CACHE_TTL = 30

# this is on utc time so time is displaced by either 4 or 5 hours ahead from orlando time. 21 15 is 5 pm
alert_time = datetime.time(hour=21,minute=15,tzinfo=utc)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
 
 
async def Getapi_weather():
    #pull json data from api's
    thorguard_Json_weather = requests.get("https://360.thormobile.net/thorcloud/api/weatherpackets/GetBySystemID?ids=3338")
    thorguard_Json_lightningstatus = requests.get("https://360.thormobile.net/thorcloud/api/productionpackets/GetBySystemID?ids=3338&ms=1755887859790")     

    try:
        #convert json to python dict for easy access
        thorguard_Python_weather = json.loads(thorguard_Json_weather.text)
        thorguard_Python_lightningstatus = json.loads(thorguard_Json_lightningstatus.text)
        
        Api_CreatedTime = thorguard_Python_weather['23-08-30-010']['CreatedTime']
        Api_FriendlyAdvisoryLevel = thorguard_Python_lightningstatus['23-08-30-010']['FriendlyAdvisoryLevel']
        Api_Temperature = thorguard_Python_weather['23-08-30-010']['Temperature']
        Api_Humidity = thorguard_Python_weather['23-08-30-010']['Humidity']
        
        #Using a dictionary to get each piece of weather data, very cool!
        return {
            'printable_time' : Api_CreatedTime,
            'printable_weather' : Api_FriendlyAdvisoryLevel,
            'printable_temp' : Api_Temperature,
            'printable_humidity' : Api_Humidity
        }
     
    except Exception as e:
        print("Error:", e)

         

#loops everyday to tell current weather
@tasks.loop(time=alert_time)
async def daily_weather():

    maxhour_twelve = datetime.time(hour=12,minute=59,second=59)
    twelve_hour_delta = datetime.timedelta(hours=12)
    current_datetime = datetime.datetime.now()

    #channel id for bot
    channel = bot.get_channel(1400512264448114758)
    #if we have correct channel then begin pulling data
    if channel:
        result = await Getapi_weather()
        
        #if api call is successful print weather out depending on outcome
        if result:
            
            time_string = result['printable_time']
            date_time_obj = datetime.datetime.fromisoformat(time_string)
            date_part = date_time_obj.date()
            time_part = date_time_obj.time()

            #if statement for am or pm for clock
            if time_part > maxhour_twelve:
                date_time_obj = date_time_obj - twelve_hour_delta
                new_time_part = date_time_obj.time()
                
                embed = discord.Embed(title=f"Current Weather around UCF", url ="https://360.thormobile.net/ucf-rwc/tv/", description="Your daily weather report.", color=discord.Color.blue())
                embed.set_thumbnail(url="https://www.cbs42.com/wp-content/uploads/sites/81/2019/01/Weather20Alert20Web_1533812455093.png_51182794_ver1.0.png")
                embed.add_field(name=f"Current Time is: {current_datetime} UTC",value="",inline=False)
                embed.add_field(name=f"Last Time ThorGuard has been Updated {date_part} , {new_time_part} PM",value="",inline=False)
                embed.add_field(name=f"Current Temperature: {result['printable_temp']}°F",value="",inline=False)
                embed.add_field(name=f"Current Humidity:  {result['printable_humidity']}%",value="",inline=False)
                if result['printable_weather'] == "AllClear":
                    embed.add_field(name="All Clear : Practice is on!",value="",inline=False)
                else:
                    embed.add_field(name=f"{result['printable_weather']} : Ask Officers if Practice is happening!",value="",inline=False)
                await channel.send(embed=embed)
            else:
                embed = discord.Embed(title=f"Current Weather around UCF", url ="https://360.thormobile.net/ucf-rwc/tv/", description="Your daily weather report.", color=discord.Color.blue())
                embed.set_thumbnail(url="https://www.cbs42.com/wp-content/uploads/sites/81/2019/01/Weather20Alert20Web_1533812455093.png_51182794_ver1.0.png")
                embed.add_field(name=f"Current Time is: {current_datetime} UTC",value="",inline=False)
                embed.add_field(name=f"Last Time ThorGuard has been Updated {date_part} , {time_part} AM",value="",inline=False)
                embed.add_field(name=f"Current Temperature: {result['printable_temp']}°F",value="",inline=False)
                embed.add_field(name=f"Current Humidity:  {result['printable_humidity']}%",value="",inline=False)
                if result['printable_weather'] == "AllClear":
                    embed.add_field(name="All Clear : Practice is on!",value="",inline=False)
                else:
                    embed.add_field(name=f"{result['printable_weather']} : Ask Officers if Practice is happening!",value="",inline=False)
                await channel.send(embed=embed)
        else:
            await channel.send('Failed to retrieve Thorguards Current Status')


# Wait for bot to be ready before starting the loop
@daily_weather.before_loop
async def before_daily_weather():
    print("here")
    await bot.wait_until_ready()


# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        guild = discord.Object(id=1293001574217547816)
        synced = await bot.tree.sync(guild=guild)
        print(f'Synced {len(synced)} commands to guild {guild.id}')

    except Exception as e:
        print(f'Error syncing commands: {e}')
    await bot.tree.sync(guild=GUILD_ID)
    daily_weather.start()

    
@bot.tree.command(name="weather", description="Pulls Thorguard's Weather", guild = GUILD_ID)
@commands.has_any_role("Officers")
async def Slash_weather(interaction: discord.Interaction):
    #did this to have a 12 hour clock to show last time thorguard updated more clearly
    maxhour_twelve = datetime.time(hour=12,minute=59,second=59)
    twelve_hour_delta = datetime.timedelta(hours=12)
    channel = bot.get_channel(1400512264448114758)
    now = time.time()
    current_datetime = datetime.datetime.now()
    #checks if datas in cache or not and if time is still under 30 seconds, sleep for 4 seconds so message foesn't display in data
    if weather_cache['weather_Data_Copy'] and (now - weather_cache['timestamp'] < CACHE_TTL):
        #runs concurently so don't need to multithread
        await asyncio.sleep(3)                 
        weather_copy = weather_cache["weather_Data_Copy"]
        await channel.send('Too Many Requests Please Wait 30 Seconds')
    else:
        try:
        # Need fresh data 30 secs has expired so get new data
            await interaction.response.defer()
            weather_copy = await Getapi_weather()
            weather_cache["weather_Data_Copy"] = weather_copy
            weather_cache["timestamp"] = now
            #new data sent
            if weather_copy:
                time_string = weather_copy['printable_time']
                date_time_obj = datetime.datetime.fromisoformat(time_string)
                date_part = date_time_obj.date()
                time_part = date_time_obj.time()

                #if statement for am or pm for clock
                if time_part > maxhour_twelve:
                    date_time_obj = date_time_obj - twelve_hour_delta
                    new_time_part = date_time_obj.time()

                    embed = discord.Embed(title=f"Current Weather around UCF", url ="https://360.thormobile.net/ucf-rwc/tv/", description="Your daily weather report.", color=discord.Color.blue())
                    embed.set_thumbnail(url="https://www.cbs42.com/wp-content/uploads/sites/81/2019/01/Weather20Alert20Web_1533812455093.png_51182794_ver1.0.png")
                    embed.add_field(name=f"Current Time is: {current_datetime} UTC",value="",inline=False)
                    embed.add_field(name=f"Last Time ThorGuard has been Updated {date_part} , {new_time_part} PM",value="",inline=False)
                    embed.add_field(name=f"Current Temperature: {weather_copy['printable_temp']}°F",value="",inline=False)
                    embed.add_field(name=f"Current Humidity:  {weather_copy['printable_humidity']}%",value="",inline=False)
                    if weather_copy['printable_weather'] == "AllClear":
                        embed.add_field(name="All Clear : Practice is on!",value="",inline=False)
                    else:
                        embed.add_field(name=f"{weather_copy['printable_weather']} : Ask Officers if Practice is happening!",value="",inline=False)
                else:
                    embed = discord.Embed(title=f"Current Weather around UCF", url ="https://360.thormobile.net/ucf-rwc/tv/", description="Your daily weather report.", color=discord.Color.blue())
                    embed.set_thumbnail(url="https://www.cbs42.com/wp-content/uploads/sites/81/2019/01/Weather20Alert20Web_1533812455093.png_51182794_ver1.0.png")
                    embed.add_field(name=f"Current Time is: {current_datetime} UTC",value="",inline=False)
                    embed.add_field(name=f"Last Time ThorGuard has been Updated {date_part} , {time_part} AM",value="",inline=False)
                    embed.add_field(name=f"Current Temperature: {weather_copy['printable_temp']}°F",value="",inline=False)
                    embed.add_field(name=f"Current Humidity:  {weather_copy['printable_humidity']}%",value="",inline=False)
                    if weather_copy['printable_weather'] == "AllClear":
                        embed.add_field(name="All Clear : Practice is on!",value="",inline=False)
                    else:
                        embed.add_field(name=f"{weather_copy['printable_weather']} : Ask Officers if Practice is happening!",value="",inline=False)
    
                #confirm to discord command ran succesfully
                await interaction.followup.send(embed=embed)
            else:
                await channel.send('Failed to retrieve Thorguards Current Status')
        #handle errors if slash command fails 
        except Exception as e:
            print(f"An error occurred in the weather command: {e}")
            await interaction.followup.send("An error occurred while getting the weather. Please try again later.")

#key to run bot in specific servers
bot.run(...)

