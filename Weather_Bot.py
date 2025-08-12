import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from discord.ext import commands, tasks
import datetime
import pytz

utc = datetime.timezone.utc

#cache to stop multiple requsts from rate limiting discord and flooding bot
weather_cache = {
    'timestamp' : 0,
    'weather_Data_Copy' : None
}

CACHE_TTL = 30

# this is on utc time so time is displaced by either 4 or 5 hours ahead from orlando time. 21:15 is 5:15 which is time I want to alert about practice.
alert_time = datetime.time(hour=21,minute=15,tzinfo=utc)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
 
async def scrape_weather():
       
            #run headless no visible browser
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://360.thormobile.net/ucf-rwc/tv/")

            #wait for JavaScript to load the page
    time.sleep(4)

    try:
                #get the element by ID
        time_element = driver.find_element(By.ID, 'wxtimeStampLabel')
        weather_element = driver.find_element(By.ID, "thorStatusLabel")
        temp_element = driver.find_element(By.ID, 'wxTempValueLabel')
        humidity_element = driver.find_element(By.ID, 'humidityValue')

        #Using a dictionary to get each piece of weather data, very cool!
        return {
            'printable_time' : time_element.text.strip(),
            'printable_weather' : weather_element.text.strip(),
            'printable_temp' : temp_element.text.strip(),
            'printable_humidity' : humidity_element.text.strip()
        }
                #print("\nWeather Status:", weather_element.text.strip())
           
    except Exception as e:
        print("Error:", e)

    driver.quit()      

#!weather command
@bot.command(name='weather')
async def weather(ctx):
    now = time.time()

    #checks if datas in cache or not and if time is still under 30 seconds 
    if weather_cache['weather_Data_Copy'] and (now - weather_cache['timestamp'] < CACHE_TTL):
        weather_copy = weather_cache["weather_Data_Copy"]
        await ctx.send('Too Many Requests Please Wait 30 Seconds')
    else:
        # Need fresh data 30 secs has expired so get new data
        weather_copy = await scrape_weather()
        weather_cache["weather_Data_Copy"] = weather_copy
        weather_cache["timestamp"] = now

        await ctx.send('Pulling Thorguards Current Weather Status...')
        #new data sent
        if weather_copy:
            await ctx.send(".......................................................................................")
            await ctx.send(weather_copy['printable_time'])
            await ctx.send('Current Temperature: ' + weather_copy['printable_temp'])
            await ctx.send('Current Humidity: ' + weather_copy['printable_humidity'] + '%')
            if weather_copy['printable_weather'] == "ALL CLEAR":
                await ctx.send(f"{weather_copy['printable_weather']} : Practice is on!")
                await ctx.send(".......................................................................................")
            else:
                await ctx.send(f"{weather_copy['printable_weather']} : Ask Officers if Practice is happening!")
                await ctx.send(".......................................................................................")
        else:
            await ctx.send('Failed to retrieve Thorguards Current Status')
#ADD HUMIDITY and test
#loops everyday to tell current weather
@tasks.loop(time=alert_time)
async def daily_weather():
    #channel id for bot you would enter that info here
    channel = bot.get_channel(...)
    #if we have correct channel then begin pulling data
    if channel:
        await channel.send(".......................................................................................")
        await channel.send("Daily weather update!")
        await channel.send("Pulling Thorguard's current weather status...")
        result = await scrape_weather()

        #if scrape is successful print weather out depending on outcome
        if result:
            await channel.send(result['printable_time'])
            await channel.send(f"Current Temperature: {result['printable_temp']}")
            await channel.send(f"Current Humidity: {result['printable_humidity']}%")
            
            if result['printable_weather'] == "ALL CLEAR":
                await channel.send(f"{result['printable_weather']} : Practice is on!")
                await channel.send(".......................................................................................")
            else:
                await channel.send(f"{result['printable_weather']} : Ask Officers if Practice is happening!")
                await channel.send(".......................................................................................")
        else:
            await channel.send("Failed to retrieve weather data.")


# Wait for bot to be ready before starting the loop
@daily_weather.before_loop
async def before_daily_weather():
    await bot.wait_until_ready()


# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    daily_weather.start()

    
#key to run bot in specific servers you would enter your code here to run bot.
bot.run('...')


