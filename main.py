import asyncio
import discord
from discord import Game, Embed, Color

import SECRETS
import STATICS
from commands import cmd_ping, cmd_autorole

client = discord.Client()

commands = {

    "ping": cmd_ping,
    "autorole": cmd_autorole,
}

@client.event
@asyncio.coroutine
def on_ready():
    print('Eingelogt als')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    for s in client.servers:
        print("  - %s (%s)" % (s.name, s.id))
        yield from client.change_presence(game=Game(name="Ich spiele nichts!!!"))

@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith(STATICS.PREFIX):
        invoke = message.content[len(STATICS.PREFIX):].split(" ")[0]
        args = message.content.split(" ")[1:]
        print("Invoke: %s\nArgs:%s" % (invoke, args.__str__()))
        if commands.__contains__(invoke):
            yield from commands.get(invoke).ex(args, message, client, invoke)
        else:
            yield from client.send_message(message.channel, embed=Embed(color=Color.red(), description="The commend '%s' is not vaild" % invoke))

@client.event
@asyncio.coroutine
def on_member_join(member):
    yield from client.send_message(member, "**Hey %s**\n\nWelcome on the official nice supercool %s discord server from %s\n\nNow have a nice day!" % (member.name, member.server.name, member.server.owner.mention))
    with cmd_autorole(member.server) as role:
        if not cmd_autorole.get(role) == None:
            yield from client.add_roles(member, role)
            yield from client.send_message(member, "You got automatically assigned the role" + role.mention + "!")



client.run(SECRETS.TOKEN)