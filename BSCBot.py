import discord
from discord.ext import commands, tasks
import requests
import pprint
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from decouple import config
PATH = "C:\chromedriver.exe"
driver = webdriver.Chrome(PATH)
client = commands.Bot(command_prefix = '.')
token = config('token')
discordtoken = config('discordtoken')
burnaddress = config('burnaddress')

@client.event #Posts somewhere that the bot has joined the party
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event #Sends message when command is recieved
async def on_message(message):
    id = client.get_guild(830869440718438400)
    if message.content.find("!price") != -1:
        await message.channel.send("Current price is $" + update_price() + "\nCurrent market cap " + getmarketcap() + "\nTotal coins burnt " + getburn())
    elif message.content.find("!marketcap") != -1:
        await message.channel.send(getmarketcap())
    elif message.content.find("!burn") != -1:
        await message.channel.send(getburn())
        
def getburn():
    driver.get("https://bscscan.com/token/" + token + "?a=" + burnaddress)
    time.sleep(2)
    burn = driver.find_element_by_xpath('/html/body/div[1]/main/div[4]/div[3]/div/div/div[2]').get_attribute('innerText')
    burn = (burn.lstrip("ABCDEFGHIJKLMNOP \n"))
    print(burn)
    return(burn)

def update_price():
    r = requests.get('https://api.dex.guru/v1/tokens/' + token + '?sort_by=id&sort_by2=address&asc=false&from_num=0&size=15')
    current_price = ((r.json()["priceUSD"]))
    current_price_string = str(current_price)
    print("%0.11f" % float(current_price_string))
    return("%0.11f" % float(current_price_string))

def getmarketcap():
    driver.get("https://poocoin.app/tokens/" + token)
    time.sleep(2)
    marketcap = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]').get_attribute('innerText')
    market_cap_value = marketcap.split()
    print(market_cap_value[5])
    return(market_cap_value[5])

client.run(discordtoken)
