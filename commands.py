import nextcord
from nextcord.ext import commands
import config


# needed this not requierd to have

class CommandsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="test", description="Nur zum Testen")
    async def test(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="Test erfolgreich")
        embed.add_field(name="Message Author", value=interaction.user.mention)

        # Extract relevant details from the Guild object
        guild_name = interaction.guild.name  # You can also use guild.id or other properties as needed
        embed.add_field(name="Server", value=guild_name)

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="get-message-id", description="Message-ID")
    async def get_message_id(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("copy_message_id")

    @nextcord.slash_command(name="check-permissions", description="Überprüft die Berechtigungen des Bots.")
    async def check_permissions(self, interaction: nextcord.Interaction):
        permissions = interaction.guild.me.guild_permissions
        await interaction.response.send_message(f"Meine Berechtigungen:\n{permissions}",
                                                ephemeral=True)


def setup(client):
    client.add_cog(CommandsCog(client))