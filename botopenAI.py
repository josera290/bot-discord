from dotenv import load_dotenv
from openai import OpenAI
import discord
import asyncio
import os

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

openai_client = OpenAI(api_key=OPENAI_KEY)

async def send_message(assistant_id, content):
    try:
        # Crear thread
        thread = openai_client.beta.threads.create()
        # Crear mensaje en el thread
        openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=content
        )
        # Ejecutar el assistant
        run = openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        # Esperar a que termine
        while True:
            run_status = openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            await asyncio.sleep(1)
        # Obtener la respuesta
        messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                return msg.content[0].text.value
        return "No se obtuvo respuesta del assistant."
    except Exception as e:
        return f"Error procesando mensaje: {e}"

# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord_client))

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.startswith('$hello'):
        try:
            await message.channel.send('Hello!')
        except Exception as e:
            await message.channel.send(f"Error enviando saludo: {e}")

    if message.content.startswith('$question'):
        message_content = message.content.split("$question", 1)[1].strip()
        if message_content:
            try:
                response = await send_message(ASSISTANT_ID, message_content)
            except Exception as e:
                response = f"Error procesando pregunta: {e}"
            await message.channel.send(response)

@discord_client.event
async def on_error(event, *args, **kwargs):
    import traceback
    error_msg = traceback.format_exc()
    print(f"Error en evento {event}:\n{error_msg}")
    # Enviar error al primer canal de texto disponible
    for guild in discord_client.guilds:
        for channel in guild.text_channels:
            try:
                await channel.send(f"⚠️ Error en evento `{event}`:\n```{error_msg}```")
                return
            except Exception:
                continue
    # Si no se pudo enviar, solo imprime

discord_client.run(DISCORD_TOKEN)
