import os

import discord
from os import path

def error(content, channel, client):
    yield from client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description=content))

def get(server):
    f = "SETTINGS/" + server.id + "/autorole"
    if path.isfile(f):
        with open(f) as f:
            return discord.utils.get(server.roles, id=f.read())
    else:
        return None

def savefile(id,server):
    if not path.isdir("SETTINGS/" + server.id):
        os.makedirs("SETTINGS/" + server.id)
    with open("SETTINGS/" + server.id + "/autorole", "w") as f:
        f.write(id)
        f.close()


def ex(args, message, client, invoke):

    print(args)

    if len(args) > 0:
        rolename = args.__str__()[1:-1].replace(",", "").replace("'", "")
        print(rolename)
        role = discord.utils.get(message.server.roles, name=rolename)
        if role == None:
            yield from error("Please enter a vaild role existing on the server.", message.channel, client)
        else:
            try:
                savefile(role.id, message.server)
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("Succsessfully set autorole to role '%s'" % role.name)))
            except Exception:
                yield from error("Something went wrong while saving autorole.", message.channel, client)
                raise Exception