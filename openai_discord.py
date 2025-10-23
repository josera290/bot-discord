import discord
import os
from dotenv import load_dotenv
import openai

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

if not DISCORD_TOKEN:
    raise ValueError("No se encontró DISCORD_TOKEN en las variables de entorno. Verifica tu archivo .env.")
if not OPENAI_API_KEY:
    raise ValueError("No se encontró OPENAI_API_KEY en las variables de entorno. Verifica tu archivo .env.")
if not ASSISTANT_ID:
    raise ValueError("No se encontró ASSISTANT_ID en las variables de entorno. Verifica tu archivo .env.")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def get_assistant_response(assistant_id, user_content, api_key):
    openai.api_key = api_key
    # Crear thread
    thread = openai.beta.threads.create()
    # Crear mensaje en el thread
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_content
    )
    # Ejecutar el assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    # Esperar a que termine
    import asyncio
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        await asyncio.sleep(1)
    # Obtener la respuesta
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            return msg.content[0].text.value
    return "No se obtuvo respuesta del assistant."

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$question"):
        prompt = message.content.split("$question", 1)[1].strip()
        if prompt:
            try:
                reply = await get_assistant_response(ASSISTANT_ID, prompt, OPENAI_API_KEY)
            except Exception as e:
                reply = f"Error al consultar el Assistant: {e}"
            await message.channel.send(reply)

client.run(DISCORD_TOKEN)