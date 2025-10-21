import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == "$hola":
        usuario = message.author.mention  # Obtiene el nombre del usuario que envió el mensaje
        #await message.channel.send("Hola , es una prueba exitosa de mi bot en Discord!")
        #await bot.process_commands(message)
        await message.channel.send(f"Hola {usuario},gracias por ayudarme a una prueba exitosa de mi bot en Discord!")

# Obtener el token desde las variables de entorno
token = os.getenv("DISCORD_TOKEN")

if not token:
    print("Error: No se encontró el token de Discord. Asegúrate de que DISCORD_TOKEN esté en el archivo .env")
    exit(1)

bot.run(token)
