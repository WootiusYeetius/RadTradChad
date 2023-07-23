from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
import datetime

dateArray = []
date = datetime.datetime.now()
for i in str(date.year):
    dateArray.append(i)
dateArray.pop(0)
dateArray.pop(0)
year = "".join(dateArray)
dateArray.clear()
month = str(date.month)
day = str(date.day)

#It won't always have the 0 in front so you got to change that
if (len(month) == 1) and (len(day) == 1):
    finalDate = "/0" + month + "0" + day + year
elif (len(month) == 2) and (len(day) == 1):
    finalDate = "/" + month + "0" + day + year
elif (len(month) == 1) and (len(day) == 2):
    finalDate = "/0" + month + day + year
elif (len(month) == 2) and (len(day) == 2):
    finalDate = "/" + month + day + year

url = "https://bible.usccb.org/bible/readings{}.cfm".format(finalDate)
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

rawReadings = soup.find_all("div", class_="content-body")
refinedReadings = []

def refineFound(unrefined, refined):
    for k in unrefined:
        refined.append(k.text)
    return refined

refineFound(rawReadings, refinedReadings)

everyFreakingIntegerUntil175BecauseOfCourse = [0]
for p in range(175):
    everyFreakingIntegerUntil175BecauseOfCourse.append(p)

TOKEN = "Bot token"
GENERAL_CHANNEL = "Put a channel id here if you want"
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("The bot is ready")

@bot.command()
async def greet(ctx):
    await ctx.send("Hello, everyone")

#Correct code below, just can't send long enough messages w/out nitro
'''
@bot.command()
async def dailyreadings(ctx):
    print(rawReadings)
    for k in refinedReadings:
        await ctx.send(k)
'''

@bot.command()
async def dailyreadings(ctx):
    for k in refinedReadings:
        embed = discord.Embed(title="Daily Readings", description=k)
        await ctx.send(embed=embed)

@bot.command()
async def versions(ctx):
    vurl = "https://www.biblegateway.com/versions"
    vpage = requests.get(vurl)
    vsoup = BeautifulSoup(vpage.content, "html.parser")
    list = vsoup.find_all("tr", class_="info-row language-row en collapse in")
    print(list)
    textList = []
    for x in list:
        textList.append(x.text)
    rList = []
    for z in textList:
        rList.append(z)

    embed = discord.Embed(title="Here's a list of options", description=rList)
    await ctx.send(embed=embed)

@bot.command()
async def searchverse(ctx, book, chapter, verse, version="NABRE"):
    bDict = {
        "Genesis" : "Gen",
        "Exodus" : "Exod",
        "Leviticus" : "Lev",
        "Numbers" : "Num",
        "Deuteronomy" : "Deut",
        "Joshua" : "Josh",
        "Judges" : "Judg",
        "Ruth" : "Ruth",
        "1Samuel" : "1Sam",
        "2Samuel" : "2Sam",
        "1Kings" : "1Kgs",
        "2Kings" : "2Kgs",
        "1Chronicles" : "1Chr",
        "2Chronicles" : "2Chr",
        "Ezra" : "Ezra",
        "Nehemiah" : "Neh",
        "Tobit" : "Tob",
        "Judith" : "Jdt",
        "Esther" : "Esth",
        "1Maccabees" : "1Macc",
        "2Maccabees" : "2Macc",
        "Job" : "Job",
        "Psalms" : "Ps",
        "Proverbs" : "Prov",
        "Ecclesiastes" : "Eccl",
        "Song of Songs" : "Song",
        "Wisdom" : "Wis",
        "Sirach" : "Sir",
        "Isaiah" : "Isa",
        "Jeremiah" : "Jer",
        "Lamentations" : "Lam",
        "Baruch" : "Bar",
        "Ezekiel" : "Ezek",
        "Daniel" : "Dan",
        "Hosea" : "Hos",
        "Joel" : "Joel",
        "Amos" : "Amos",
        "Obadiah" : "Obad",
        "Jonah" : "Jonah",
        "Micah" : "Mic",
        "Nahum" : "Nah",
        "Habakkuk" : "Hab",
        "Zephaniah" : "Zeph",
        "Haggai" : "Hag",
        "Zech" : "Zech",
        "Malachi" : "Mal",
        "Matthew" : "Matt",
        "Mark" : "Mark",
        "Luke" : "Luke",
        "John" : "John",
        "Acts" : "Acts",
        "Romans" : "Rom",
        "1Corinthians" : "1Cor",
        "2Corinthians" : "2Cor",
        "Galatians" : "Gal",
        "Ephesians" : "Eph",
        "Philippians" : "Phil",
        "Colossians" : "Col",
        "1Thessalonians" : "1Thess",
        "2Thessalonians" : "2Thess",
        "1Timothy" : "1Tim",
        "2Timothy" : "2Tim",
        "Titus" : "Titus",
        "Philemon" : "Phlm",
        "Hebrews" : "Heb",
        "James" : "Jas",
        "1Peter" : "1Pet",
        "2Peter" : "2Pet",
        "1John" : "1John",
        "2John" : "2John",
        "3John" : "3John",
        "Jude" : "Jude",
        "Revelation" : "Rev"
    }
    svurl = "https://www.biblegateway.com/passage/?search={}%20{}&version={}".format(book, chapter, version)
    svpage = requests.get(svurl)
    svsoup = BeautifulSoup(svpage.content, "html.parser")
    verseArrayZero = []
    verseArrayOne = []
    verseArrayTwo = []
    verseArrayFour = []

    if ("-" not in verse):
        svVerse = svsoup.find_all("span", class_="text {}-{}-{}".format(bDict[book], chapter, verse))
        verseFinal = []
        for s in svVerse:
            verseFinal.append(s.text)

    elif ("-" in verse):
        verseFinal = []
        for m in verse:
            verseArrayZero.append(m)
        for o in range(len(verseArrayZero)):
            if (o < verseArrayZero.index("-")):
                verseArrayOne.append(verseArrayZero[o])
            elif (o > verseArrayZero.index("-")):
                verseArrayTwo.append(verseArrayZero[o])

        startVerse = "".join(verseArrayOne)
        endVerse = "".join(verseArrayTwo)
        print(verseArrayTwo)

        for q in everyFreakingIntegerUntil175BecauseOfCourse:
            if (q > int(startVerse)) and (q <= int(endVerse)):
                verseArrayFour.append(q)

        svVerse = []
        svVerse.append(svsoup.find("span", class_="text {}-{}-{}".format(bDict[book], chapter, startVerse)))
        
        for sv in verseArrayFour:
            svVerse.append(svsoup.find("span", class_="text {}-{}-{}".format(bDict[book], chapter, sv)))

        for e in svVerse:
            verseFinal.append(e.text)

    embed = discord.Embed(title="{} {}:{}".format(book, chapter, verse), description=verseFinal)
    await ctx.send(embed=embed)

@bot.command()
async def dailygospel(ctx):
    gurl = "https://bible.usccb.org/bible/readings{}.cfm".format(finalDate)
    gpage = requests.get(gurl)
    gsoup = BeautifulSoup(gpage.content, "html.parser")
    grawReadings = gsoup.find_all("div", class_="content-body")
    grefinedReadings = []
    grefinedReadings.append(grawReadings[len(grawReadings) - 1].text)
    embed = discord.Embed(title="Here's a list of options", description=grefinedReadings)
    await ctx.send(embed=embed)

#Below is my draft for the og searchverse that didn't work because usccb has some web scraping prevention
#I deleted a bunch of the variables that were defined above
'''
@bot.command()
async def searchverse(ctx, book, chapter, verse):
    svurl = "https://bible.usccb.org/bible/{}/{}".format(book, chapter)
    try:
        svpage = requests.get(svurl)
        svsoup = BeautifulSoup(svpage.content, "html.parser")
    except Exception as e:
        print("An error occurred:", e)
    print(svurl)

    if ("-" not in verse):
        svholders = svsoup.find_all("span", class_="txt")
        print(svholders)
        for s in svholders:
            rawVerse.append(s)
        refinedVerse = rawVerse[int(verse) - 1].text
    elif ("-" in verse):
        for m in verse:
                verseArrayZero.append(m)
        for n in range(len(verseArrayZero) - 1):
            if (verseArrayZero[n] == "-"):
                dashLocation = n

        for o in verseArrayZero:
            if (o < dashLocation):
                verseArrayOne.append(o)
            elif (o > dashLocation):
                verseArrayTwo.append(o)

        startVerse = "".join(verseArrayOne)
        endVerse = "".join(verseArrayTwo)

        for q in everyFreakingIntegerUntil175BecauseOfCourse:
            if (q > startVerse) and (q < endVerse):
                verseArrayFour.append(q)

        svholders = svsoup.find_all("span", class_="txt")
        for holder in svholders:
            rawVerse.append(holder)
        for r in rawVerse:
            if (r in rawVerse):
                verseArrayFive.append(r.text)
        
        refinedVerse = "".join(verseArrayFive)

    embed = discord.Embed(title="Searched Verse", description=refinedVerse)
    await ctx.send(embed=embed)
    rawVerse.clear()
    svholders.clear()
'''
    
bot.run(TOKEN)
