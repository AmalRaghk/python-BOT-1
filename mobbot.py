
import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv
import phonenumbers
from phonenumbers import geocoder ,carrier,timezone
import mechanize
from bs4 import BeautifulSoup
import pandas as pd
a='+'
load_dotenv()
TOKEN = os.getenv('DIS_TOKEN')
client = discord.Client()
bot=commands.Bot(command_prefix='?')
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('The phone no doesnt exist or it is in wrong format')    
@bot.command(name="phone",help="?mobile 124567891 finds details of International mobile numbers")
async def phone(ctx,*,arg):
    phone=str(arg)
    phone_number = phonenumbers.parse(a+phone) 
    country=geocoder.description_for_number(phone_number, 'en')
    carry=(carrier.name_for_number(phone_number, 
                                      'en')) 
    zone=str(timezone.time_zones_for_number(phone_number))
    embed=discord.Embed( color=0x00ff00)
    if country:
        embed.add_field(name="country", value=country, inline=True) 
    if carry:    
        embed.add_field(name="carry", value=carry, inline=True)
    if zone:    
        embed.add_field(name="zone", value=zone, inline=True)
    print("done") 
    await ctx.send(embed=embed)
@bot.command(name="mobile",help="?mobile 1234567812 finds country and network of Indian Numbers")                                                                                              
async def mobile(ctx,*,arg):
    phono=arg
    phonono=str(phono)
    mc = mechanize.Browser()
    mc.set_handle_robots(False)
    url = 'https://www.findandtrace.com/trace-mobile-number-location'
    mc.open(url)
    mc.select_form(name='trace')
    mc['mobilenumber'] = phonono# Enter a targeted mobile number
    res = mc.submit().read()
    soup = BeautifulSoup(res,'html.parser')
    tbl = soup.find_all('table',class_='shop_table')
    data = tbl[0].find('tfoot')
    c=0
    embed=discord.Embed( color=0x00ff00)
    for i in data:
        c+=1
        if c in (1,4,6,8,10,11,14):
            continue
        th = i.find('th')
        td = i.find('td')
        if td.text:
             embed.add_field(name=th.text, value=td.text, inline=True)
        if c>14:
            break
    data = tbl[1].find('tfoot')
    c=0
    for i in data:
        c+=1
        if c in (2,4,8,10,12,14,16,18,20,22,24,26,28): 
            th = i.find('th')
            td = i.find('td')
            if pd.isnull('td'):
                continue
            embed.add_field(name=th.text, value=td.text, inline=True) 
    await ctx.send(embed=embed)
    print("done")
           
bot.run(TOKEN)
