from disnake.ext import commands
from disnake import Embed
from disnake.ui import View, Button
import disnake
import infoServer

from pathlib import Path
import dotenv
import os

env_path = Path('.') / '.env'
dotenv.load_dotenv(dotenv_path=env_path)

bot = commands.InteractionBot(test_guilds=[int(os.getenv('ID'))])

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n")

@bot.event
async def on_button_click(interaction: disnake.Interaction):
    print(interaction)
    user = interaction.author
    guild = interaction.guild

    if interaction.data.custom_id == "ticket-suport":  # Verifica se o botão clicado é o esperado
        user = interaction.author
        guild = interaction.guild

        channel_suport = await guild.create_text_channel(name=f"Suporte - {user.name}")

        await channel_suport.set_permissions(guild.default_role, read_messages=False)
        await channel_suport.set_permissions(user, read_messages=True)

        embed = Embed(description="Olá!\nO pessoal do suporte já foram alertados, assim que possivel entrarão em contato por este canal.\n\nA Evocloud agradece o contato!", title=f"Suporte - {user.name}")
        embed.add_field(name='Horários de atendimento', value='Segunda a sexta das 13h as 18h')
        embed.add_field(name='Encerramento de atendimento', value='Clique no botão a baixo para encerrar o atendimento.')
        embed.set_author(name="Desenvolvido por Pedro", url="https://github.com/kepe150", icon_url="https://avatars.githubusercontent.com/u/95188379?v=4")
        embed.set_default_colour(value=disnake.Colour.from_rgb(255,156,0))

        view = View()       
        view.add_item(Button(label="Encerrar chamado", style=disnake.ButtonStyle.red, custom_id='close-suport'))

        await channel_suport.send(content=f"<@{user.id}> @everyone", embed=embed, view=view)
        await interaction.response.send_message(content=f"O canal de {channel_suport.jump_url} foi criado!"  , ephemeral=True)
    if interaction.data.custom_id == "close-suport":
        channel_suport = interaction.channel
        await channel_suport.set_permissions(guild.default_role, read_messages=False)
        await channel_suport.edit(name=channel_suport.name + '-arquivado')
@bot.slash_command(description="ping")
async def ping(inter):
    print('pong')
    await inter.response.is_done()

@bot.slash_command(description="info")
async def info(inter):
    info = infoServer.getInfo()
    embed = Embed(title='Informações do servidor', description='Veja em tempo real o uso dos recursos dos nossos servidores')
    embed.add_field(name='CPU:', value=str(info['cpu']) + '%')
    embed.add_field(name='RAM:', value=str(info['mem']) + ' Gb')
    embed.add_field(name='Temperatura CPU:', value=str(info['temp-cpu']) + ' C')
    await inter.response.send_message(embed=embed)

@bot.slash_command(description="suporte")
async def ticket_message(inter):
    embed = Embed(title='Suporte - Evocloud', description='Seja bem-vindo ao canal de suporte da Evocloud, aqui você poderá obter o suporte necessário para a manutenção do seu plano ou mesmo a assinatura de um plano')
    embed.add_field(name='Horários de atendimento', value='Segunda a sexta das 13h as 18h')
    embed.set_author(name="Desenvolvido por Pedro", url="https://github.com/kepe150", icon_url="https://avatars.githubusercontent.com/u/95188379?v=4")
    embed.set_default_colour(value=disnake.Colour.from_rgb(255,156,0))
    view = View()       
    view.add_item(Button(label="Abrir chamado suporte", style=disnake.ButtonStyle.green, custom_id='ticket-suport'))

    await inter.send(view = view, embed=embed)

bot.run(os.getenv('TOKEN'))

# Isso é apenas para dizer para a hospedagem que o bot iniciou.
print("PROGRAMA INICIADO")