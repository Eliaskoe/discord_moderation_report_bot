import os
import discord
from discord.ext import commands
import logging
from utils.config_loader import load_config
from utils.logger import setup_logger

# Setup logging
logger = setup_logger()

# Load configuration
config = load_config()

# Initialize bot with all required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True  # For server info
intents.guild_messages = True  # For message events
intents.message_content = True  # For message content

bot = commands.Bot(command_prefix=config['prefix'], intents=intents, help_command=None)  # Disable default help command

@bot.event
async def on_ready():
    logger.info(f'Bot ist bereit! Eingeloggt als {bot.user.name}')

    # Load cogs
    await bot.load_extension('cogs.moderation')
    await bot.load_extension('cogs.message_commands')
    await bot.load_extension('cogs.help_commands')

    # Sync application commands
    try:
        synced = await bot.tree.sync()
        logger.info(f"{len(synced)} Befehle synchronisiert")
    except Exception as e:
        logger.error(f"Fehler beim Synchronisieren der Befehle: {e}")

    # Set activity to "Made by Elias"
    await bot.change_presence(activity=discord.Game(name="Made by Elias"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("❌ Du hast keine Berechtigung für diesen Befehl!")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(f"❌ Unbekannter Befehl. Nutze {config['prefix']}help für eine Liste aller Befehle.")
    else:
        logger.error(f"Fehler beim Ausführen des Befehls: {error}")
        await ctx.send("❌ Ein Fehler ist aufgetreten.")

def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("Kein Discord-Token in den Umgebungsvariablen gefunden!")
        return

    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"Fehler beim Starten des Bots: {e}")

if __name__ == "__main__":
    main()