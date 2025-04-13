import discord
import deepl
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio #auto delete messages

DEEPL_AUTH_KEY = os.getenv("DEEPL_API_KEY")

translator = deepl.Translator(DEEPL_AUTH_KEY)
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

FLAG_LANG_MAP = {
    "🇫🇷": "FR",
    "🇪🇸": "ES",
    "🇯🇵": "JA",
    "🇩🇪": "DE",
    "🇨🇳": "ZH",
    "🇷🇺": "RU",
    "🇮🇹": "IT",
    "🇰🇷": "KO",
    "🇺🇸": "EN-US",
    "🇬🇧": "EN-GB",
    "🇬🇷": "EL",
    "🇸🇦": "AR",
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_raw_reaction_add(payload):
    emoji = str(payload.emoji)
    if emoji not in FLAG_LANG_MAP:
        return

    lang = FLAG_LANG_MAP[emoji]
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author.bot:
        return

    try:
        translated = translator.translate_text(message.content, target_lang=lang.upper())
    except Exception as e:
        await channel.send(f"Translation failed: {e}")
        return

    embed = discord.Embed(
        title=f"Translation ({lang.upper()})",
        description=f"**Original Message:**\n{message.content}\n\n**Translated Message:**\n{translated.text}",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Original by {message.author.display_name}")

    # Send the embed as a response
    translated_message = await channel.send(embed=embed)

    # Auto-delete the translated message after 30 seconds
    await asyncio.sleep(30)
    await translated_message.delete()


bot.run(os.getenv("BOT_TOKEN"))
