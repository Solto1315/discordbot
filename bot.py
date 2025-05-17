import discord
from discord import app_commands
import config
import google.generativeai as genai

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

genai.configure(api_key=config.GEMINI_API_KEY)

with open("prompt_q.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

def ask_gemini(user_question: str) -> str:
    try:
        full_prompt = f"{base_prompt}\n\n質問: {user_question}\n答え:"
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

@client.event
async def on_ready():
    print(f"ログイン完了: {client.user}")
    await tree.sync()

@tree.command(name="q", description="質問に答えます")
async def question(interaction: discord.Interaction, *, prompt: str):
    await interaction.response.defer()
    response = ask_gemini(prompt)

    message = f"**質問:** {prompt}\n**回答:** {response}"
    await interaction.followup.send(message)

client.run(config.TOKEN_DISCORD)
