import discord
from discord.ext import commands
from mail import email
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

embed = discord.Embed(
    title="Última email de código da Disney",
    description="📩 **Recuperado último email enviado de código de acesso único para o Disney+**",
    color=discord.Color.red() 
)
file = discord.File("assets/images/baymax.jpg", filename="baymax.jpg")
embed.set_image(url="attachment://baymax.jpg")
embed.set_footer(text="BigHero Bot • Código recuperado com sucesso!")

@bot.command()
async def codigo(ctx):
    email_info = email.get_last_code()
    embed.add_field(name="📌 Código", value=f"```{email_info['código']}```", inline=False)
    await ctx.send(embed=embed, file=file)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(os.getenv('WELCOME_CHANNEL_ID'))
    if channel:
        embed = discord.Embed(
            title=f"👋 Bem-vindo(a), {member.name}!",
            description=(
                "🌟 Seja bem-vindo(a) ao **nosso servidor**! "
                "Aqui estão algumas regras importantes para seguir:\n\n"
                "📌 **Respeite todos os membros**\n"
                "📌 **Sem spam ou flood**\n"
                "📌 **Evite discussões desnecessárias**\n"
                "📌 **Use os canais corretamente**\n\n"
            ),
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else bot.user.avatar.url)
        embed.set_footer(text="BigHero Bot • Boas-vindas automáticas")
        
        await channel.send(embed=embed)