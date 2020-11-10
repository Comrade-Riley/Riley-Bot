from discord.utils import get
from discord import FFmpegPCMAudio
from PIL import Image
from datetime import datetime
from youtube_dl import YoutubeDL
import wikipedia,json,praw,os,sys,discord,random,requests,subprocess,sys,json,youtube_dl,operator
os.system('chmod +777 ./ffmpeg')
os.system('./ffmpeg')
os.system('python3 -m pip install -U discord.py[voice]')
os.system('python3 -m pip install -U youtube_dl')
import GetLinkMetaData as glmd
import urllib.request as ur
import Search_Google as google
from bs4 import BeautifulSoup
from webserver import keep_alive
from discord.ext import commands
from better_profanity import profanity
from io import BytesIO
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip3", "install", package])
os.system('pip install youtube-search-python')
from youtubesearchpython import SearchVideos
#set up
levels = json.loads(open('levels.json','r').read())

reddit = praw.Reddit(client_id=os.environ.get("CLIENT_ID"),
                     client_secret=os.environ.get("SECRET"),
                     password=os.environ.get("PASSWORD"),
                     user_agent="testscript by /u/Riley bot",
                     username="Comrade-Riley") 

b = {1:'Ace Of Hearts (Friendship, new relationships, and happiness)',2:'Two Of Hearts (Fortune in love, success, and prosperity)',3:'Three Of Hearts (Be cautious about what you are saying and to whom)',4:'Four Of Hearts (Represent change and travel, possibly taking the next step in the relationship)',5:'Five Of Hearts (Jealousy and deceit surround the questioner)',6:'Six Of Hearts (A pleasant surprise will occur soon)',7:'Seven Of Hearts (Someone close to you will break a promise)',8:'Eight Of Hearts (Invitation or a surprise visit)',9:'Nine Of Hearts (Serves as “the wish” card any wish may come true)',10:'Ten Of Hearts (Good fortune is around the corner)',11:'Jack Of Hearts (Can represent a blonde younger person or information about a close friend)',12:"Queen Of Hearts (Represents a good-natured blonde woman)",13:"King Of Hearts (Represents a blonde man or gentle, good advice giving male)",14:'Ace Of Diamonds (A gift of jewelry, or news about money)',15:'Two Of Diamonds (Disagreements in business or people not approving of a current relationship)',16:'Three Of Diamonds (Legal issues and family issues)',17:'Four Of Diamonds (Improvement in financial position and inheritance)',18:'Five Of Diamonds (Happiness at home and successful business ventures)',19:'Six Of Diamonds (Issues in a second marriage should one exist)',20:'Seven Of Diamonds (Problems at work)',21:'Eight Of Diamonds (Marriage later in life, traveling in the winter)',22:'Nine Of Diamonds (Restless of changes and a new business opportunity may arise)',23:'Ten Of Diamonds (Positive change and good luck are ahead of you)',24:'Jack Of Diamonds(Can represent a family member, a light blonde youth, or a dishonest person)',25:"Queen Of Diamonds (A fair-haired woman, a flirty person, or someone who enjoys partying and gossiping)",26:"King Of Diamonds (A fair-haired man who is stubborn and holds a position of authority)",27:'Ace Of Spades (Insight, understanding, and change)',28:'Two Of Spades (Though choices, deceit and communication issues)',29:'Three Of Spades (Issues with a romantic partner)',30:'Four Of Spades (Broken promises and illness)',31:'Five Of Spades (Indicates anger and loss)',32:'Six Of Spades (Small victories, and turning a new leaf)',33:'Seven Of Spades (Loss of a friend and unexpected burdens)',34:'Eight Of Spades (Know as a card of disappointment, illness, and a loss of social balance)',35:'Nine Of Spades (Bad luck in all aspects of life)',36:'Ten Of Spades (Unwelcome news, and imprisonment)',37:'Jack Of Spades (Dark haired youth who is means well but is unreliable and immature)',38:"Queen Of Spades (A dark-haired woman or a widow)",39:"King Of Spades (A dark-haired man who is ambitious and an authoritative presence)",40:'Ace Of Clubs (Represents happiness, wealth, and the potential for a new business opportunity)',41:'Two Of Clubs (Represents individuals who oppose you or deceive you)',42:'Three Of Clubs (Money coming from a wealthy partner’s family)', 43:'Four Of Clubs (Change for the worse, betrayal from a trusted friend)',44:'Five Of Clubs (Success in current marriage, and assistance from friends)',45:'Six Of Clubs (Financial support obtained)',46:'Seven Of Clubs (Success that may be undermined by people of the opposite gender)',47:'Eight Of Clubs (Trouble in business ventures, personal relationships, and love)',48:'Nine Of Clubs ( A warning against stubbornness)',49:'Ten Of Clubs (Good fortune or money from an unexpected source)',50:'Jack Of Clubs (A dark-haired and young person who is reliable to a fault)',51:"Queen Of Clubs (A dark-haired woman who is charming and confident)",52:"King Of Clubs (A dark-haired man who is honest and affectionate)"}

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='r.', case_insensitive=False,owner_id=754534064618340422,intents=intents)


#Welcome/goodbye
@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        embed = discord.Embed(title=f"{member} has joined the server",description=f'There are now {channel.guild.member_count} members in the server',colour=random.randint(0, 0xFFFFFF))
        embed.set_thumbnail(url=member.avatar_url) 
        embed.timestamp = datetime.now()
        if str(channel) == "general":    
          await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        embed = discord.Embed(title=f"{member} has left the server",description=f'There are now {channel.guild.member_count} members in the server',colour=random.randint(0, 0xFFFFFF))
        embed.set_thumbnail(url=member.avatar_url) 
        embed.timestamp = datetime.now()
        if str(channel) == "general":    
          await channel.send(embed=embed)
        del levels[channel.guild.id][member.id]
        json.dump(levels,open('levels.json','w'))


SortedRanks = []
@bot.event
async def on_message(message):
  global SortedRanks
  #debug
  if message.guild == None:
    await message.channel.send("The bot isn't supported in dms yet.")
    return

  #level system
  guild = str(message.guild.id)
  author = str(message.author.id)
  if guild not in levels:
    levels[guild] = {}

  if author not in levels[guild]:
    levels[guild][author] = {'Level':0,'XP':0,'Rank':"N/A"}

  rando = random.randint(1,25)
  levels[guild][author]['XP'] += rando
  if levels[guild][author]['XP'] >= 2500:
    levels[guild][author]['Level'] += 1
    levels[guild][author]['XP'] = 0
    await message.channel.send("GG, <@{}> you just leveled up to level {}".format(author,levels[guild][author]['Level']))
  ranks = {}
  for member in levels[guild]:
    ranks[member] = levels[guild][member]['Level']+ (levels[guild][member]['XP']/1000)
  SortedRanks = sorted(ranks.items(), key = lambda x: x[1],reverse=True)
  i = 0
  

  levels[guild][author]['Rank'] = SortedRanks.index((author,ranks[author]))+1
  json.dump(levels,open('levels.json','w'),indent=4)
  await bot.process_commands(message)



@bot.command()
async def rank(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author
  try:
    embed = discord.Embed(title=str(member),description="{} : \n level: {} \n XP: {}/2500 \n rank {}".format(member.mention,levels[str(ctx.guild.id)][str(member.id)]['Level'],levels[str(ctx.guild.id)][str(member.id)]['XP'],levels[str(ctx.guild.id)][str(member.id)]['Rank']),colour=random.randint(0, 0xFFFFFF))
    embed.set_thumbnail(url=member.avatar_url) 
    embed.timestamp = datetime.now()
    await ctx.send(embed=embed)
  except:
    await ctx.send("That user hasn't sent any messages yet")


@bot.command()
async def ranks(ctx):
  rs = {}
  for user in levels[str(ctx.guild.id)]:
    rs[levels[str(ctx.guild.id)][user]["Rank"]+(levels[str(ctx.guild.id)][user]['XP']/1000)] = user
  ras = "```java\n"
  for i in range(5):
    try:
      ras += f'{i+1}. {bot.get_user(int(rs[min(rs)]))}:{int(min(rs))}\n'
      del rs[min(rs)]
    except:
      pass
  await ctx.send(ras+"```")


#fun 
@bot.command()
async def howsus(ctx, User : discord.Member = None):
  if User == None:
    User = ctx.author
  im = Image.open('./imgs/sus.jpeg')
  r = requests.get(User.avatar_url)
  user = Image.open(BytesIO(r.content))
  user = user.resize((33, 35), Image.ANTIALIAS)  
  user = user.copy()
  im.paste(user,(125, 65))
  with BytesIO() as image_binary:
    im.save(image_binary, 'PNG')
    image_binary.seek(0)
    file=discord.File(fp=image_binary, filename='image.png')
  sus = random.randint(0,100)
  embed = discord.Embed(title=f"How sus is {str(User)}?",description=f"{User.mention} is {sus}% sus",colour=random.randint(0, 0xFFFFFF))
  embed.set_thumbnail(url="attachment://image.png")
  await ctx.send(file=file, embed=embed)


#lib commands
@bot.command()
async def wiki(ctx, *, search):  
  try:
    search += ' +'
    wiki = wikipedia.summary(search,5)
    if profanity.contains_profanity(wiki):
      if ctx.channel.is_nsfw():
        embed = discord.Embed(title=search.replace(' +',''),url=google.search(wiki,"link",0,True),description=wiki,colour=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=embed) 
      else:
        await ctx.send('you need to be in a nsfw channel to seartch this')
    else:
      embed = discord.Embed(title=search.replace(' +',''),url=google.search(wiki,"link",0,True),description=wiki,colour=random.randint(0, 0xFFFFFF))
      await ctx.send(embed=embed)
  except:
    await ctx.send(f"Unable to find anything about {search.replace(' +','')} on wikipedia")

@bot.command()
async def search(ctx,*,query):
  if not ctx.channel.is_nsfw():
    link = list(google.search(query,"link",5,True).split('\n'))[random.randint(1,5)]
    metadata = glmd.scrape_page_metadata(link)
    try:
      embed = discord.Embed(title=metadata['title'],type='rich',url=link,description=metadata['description'],colour=random.randint(0, 0xFFFFFF))
      embed.set_image(url=metadata['image'])
      await ctx.send(embed=embed)
    except:
      await ctx.send(embed = discord.Embed(title=link,type='rich',url=link,description='Metadata failed to load for this page',colour=random.randint(0, 0xFFFFFF)))
  else:
    aslist = list(google.search(query,"link",5,False).split('\n'))
    await ctx.send('The top five results are...')
    i = 0
    for link in aslist:
      if i < 5:
        await ctx.send(embed = discord.Embed(title='result',type='rich',url=link,colour=random.randint(0, 0xFFFFFF)))
      i+=1

@bot.command()
async def video(ctx,*,query):
    search = SearchVideos(query, offset = 1, mode = "json", max_results = 20)
    results = json.loads(search.result())
    l = []
    t = []
    tn = []
    v = []
    c = []
    r = random.randint(0,4)
    for result in results["search_result"]:
      l.append(result['link'])
      t.append(result['title'])
      tn.append(result['thumbnails'][0])
      v.append(result['views'])
      c.append(result['channel'])
    embed = discord.Embed(title=t[r],type='rich',url=l[r],colour=random.randint(0, 0xFFFFFF))
    embed.set_footer(text=f"Views: {v[r]} | Made by {c[r]}.")
    embed.set_thumbnail(url=tn[r])
    if not ctx.channel.is_nsfw() and profanity.contains_profanity(t[r]) or not ctx.channel.is_nsfw() and profanity.contains_profanity(query):
      await ctx.send('you need to be in a nsfw channel to seartch this')
    else:
      await ctx.send(embed=embed)

@bot.command()
async def img(ctx,*,query):
    if not ctx.channel.is_nsfw():  
      r = requests.get("https://api.qwant.com/api/search/images",
      params={
        'count': 20,
        'q': query,
        't': 'images',
        'safesearch': True, 
        'locale': 'en_US',
        'uiv': 4
      },
      headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
      response = r.json().get('data').get('result').get('items')
      r = random.randint(0,4)
      embed = discord.Embed(title='result for "{}"'.format(query),type='rich',url=[r.get ('media') for r in response][r],colour=random.randint(0, 0xFFFFFF))
      embed.set_image(url=[r.get ('media') for r in response][r])
      if profanity.contains_profanity(query):
        await ctx.send('you need to be in a nsfw channel to seartch this')
      else:
        await ctx.send(embed=embed)
    else:
      r = requests.get("https://api.qwant.com/api/search/images",
      params={
        'count': 20,
        'q': query,
        't': 'images',
        'safesearch': False, 
        'locale': 'en_US',
        'uiv': 4 
      },
      headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
      response = r.json().get('data').get('result').get('items')
      r = random.randint(0,4)
      embed = discord.Embed(title='result for "{}"'.format(query),type='rich',url=[r.get ('media') for r in response][r],colour=random.randint(0, 0xFFFFFF))
      embed.set_image(url=[r.get ('media') for r in response][r])
      await ctx.send(embed=embed)     
#help
bot.remove_command('help')
@bot.command()
async def help(ctx):
  if ctx.message.content == 'r.help':
    await ctx.send(open('txt/help.txt','r').read())
  search = ctx.message.content.replace('r.help ','')
  if search == 'nsfw':
    await ctx.send(open('txt/helpNSFW.txt','r').read())
  if search == 'pagan':
    await ctx.send(open('txt/helpPagan.txt','r').read())

#pegan
@bot.command()
async def cards(ctx,*, cards):
  d = int(cards)
  e = []
  while d != 0:
    rando = random.randint(1,52)
    d-=1
    e.append(rando)
    e.append('\n')
    c = ''
    for index in e:
      if index != '\n':
        c += b[index] + '\n'
        c= c[:-2]    
    await ctx.send('```'+c+'```')
    if rando <= 16:
      await ctx.send(':hearts:')
    if rando <= 26 and rando < 16:
      await ctx.send(':diamonds:')
    if rando <= 42 and rando < 16 and rando < 26:
      await ctx.send(':clubs:')
    else:
      await ctx.send(':spades:')

@bot.command()
async def pendulum(ctx,*,question):
  a = random.randint(0,2)
  if not a:
    await ctx.send(embed=discord.Embed(title='yes',description=open('txt/yes.txt','r').read()))  
  elif a==1: 
    await ctx.send(embed=discord.Embed(title='no',description=open('txt/no.txt','r').read()) )   
  else:
    await ctx.send(embed=discord.Embed(title='maybe',description=open('txt/maybe.txt','r').read()) )

#reddit commands
@bot.command()
async def wholesome(ctx):
  reddit_submissions = reddit.subreddit("wholesomememes").hot()
  post_to_pick = random.randint(1, 100)
  for i in range(1, post_to_pick):
    submission = next(x for x in reddit_submissions)
  embed = discord.Embed(title=submission.title, url=f"https://www.reddit.com/r/dankmemes/comments/{submission.id}/{submission.name}/", colour=random.randint(0, 0xFFFFFF))
  embed.set_footer(text=f"👍{submission.ups} | Made by u/{submission.author}.")
  embed.set_author(name=ctx.author
  ,icon_url=ctx.author.avatar_url)
  embed.set_image(url=submission.url)
  await ctx.send(embed=embed)

@bot.command()
async def meme(ctx):
  reddit_submissions = reddit.subreddit("dankmemes").hot()
  post_to_pick = random.randint(1, 100)
  for i in range(1, post_to_pick):
    submission = next(x for x in reddit_submissions)
  embed = discord.Embed(title=submission.title, url=f"https://www.reddit.com/r/dankmemes/comments/{submission.id}/{submission.name}/", colour=random.randint(0, 0xFFFFFF))
  embed.set_footer(text=f"👍{submission.ups} | Made by u/{submission.author}.")
  embed.set_author(name=ctx.author
  ,icon_url=ctx.author.avatar_url)
  embed.set_image(url=submission.url)
  await ctx.send(embed=embed)

#Nsfw reddit commands
@bot.command
async def pornpics(ctx):
  if ctx.channel.is_nsfw():
    reddit_submissions = reddit.subreddit("pornpics").hot()
    post_to_pick = random.randint(1, 100)
    for i in range(1, post_to_pick):
      submission = next(x for x in reddit_submissions)
    embed = discord.Embed(title=submission.title, url=f"https://www.reddit.com/r/dankmemes/comments/{submission.id}/{submission.name}/", colour=random.randint(0, 0xFFFFFF))
    embed.set_footer(text=f"👍{submission.ups} | Made by u/{submission.author}.")
    embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
    embed.set_image(url=submission.url)
    await ctx.send(embed=embed)  
  else:
    ctx.send('You need to be in a nsfw channel to use this command.')

@bot.command
async def pornvids(ctx):
  if ctx.channel.is_nsfw():
    reddit_submissions = reddit.subreddit("porn").hot()
    post_to_pick = random.randint(1, 100)
    for i in range(1, post_to_pick):
      submission = next(x for x in reddit_submissions)
    embed = discord.Embed(title=submission.title, url=f"https://www.reddit.com/r/dankmemes/comments/{submission.id}/{submission.name}/", colour=random.randint(0, 0xFFFFFF))
    embed.set_footer(text=f"👍{submission.ups} | Made by u/{submission.author}.")
    embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
    embed.set_image(url=submission.url)
    await ctx.send(embed=embed)  
  else:
    ctx.send('You need to be in a nsfw channel to use this command.')

@bot.command
async def hentai(ctx):
  if ctx.channel.is_nsfw():
    reddit_submissions = reddit.subreddit("hentai").hot()
    post_to_pick = random.randint(1, 100)
    for i in range(1, post_to_pick):
      submission = next(x for x in reddit_submissions)
    embed = discord.Embed(title=submission.title, url=f"https://www.reddit.com/r/dankmemes/comments/{submission.id}/{submission.name}/", colour=random.randint(0, 0xFFFFFF))
    embed.set_footer(text=f"👍{submission.ups} | Made by u/{submission.author}.")
    embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
    embed.set_image(url=submission.url)
    await ctx.send(embed=embed)  
  else:
    await ctx.send('You need to be in a nsfw channel to use this command.')

#Mod commands
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx,*,amount):
    try:
      await ctx.message.channel.purge(limit=int(amount)+1)
    except:
      await ctx.send("There was an error. the amoung of messages you want to purge might not exist.")

#run everything
keep_alive()
TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)