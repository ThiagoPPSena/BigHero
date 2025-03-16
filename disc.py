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

@bot.event
async def on_member_join(member):
    welcome_channel_id = int(os.getenv('WELCOME_CHANNEL_ID'))
    welcome_channel = bot.get_channel(welcome_channel_id)
    
    if welcome_channel:

        await welcome_channel.send(f"👋 Bem-vindo(a), {member.mention}!")

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
        
        await welcome_channel.send(embed=embed)

@bot.tree.command(name="codigo", description="Recupera o último código de acesso único enviado por e-mail da Disney+.")
async def codigo(interaction: discord.Interaction):
    await interaction.response.defer() 
    email_info = email.get_last_code()
    if email_info and email_info['código']:
        embed = discord.Embed(
            title="Última email de código da Disney",
            description="📩 **Recuperado último email enviado de código de acesso único para o Disney+**",
            color=discord.Color.red() 
        )
        
        file = discord.File("assets/images/baymax.jpg", filename="baymax.jpg")
        embed.set_image(url="attachment://baymax.jpg")
        embed.set_footer(text="BigHero Bot • Código recuperado com sucesso!")

        embed.add_field(name="📌 Código", value=f"```{email_info['código']}```", inline=False)

        await interaction.followup.send(embed=embed, file=file)
    else:
        await interaction.followup.send("Nenhum código de acesso único encontrado.")

@bot.event
async def on_ready():
    await bot.tree.sync()