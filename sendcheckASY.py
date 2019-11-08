import asyncio


def sendmsg(users, msg):
    msg_len = str(len(msg))
    while len(msg_len) < 5:
        msg_len = msg_len + "+"
    for user in users:
        user.write((msg_len+msg).encode())


def senduser(user, msg):
    msg_len = str(len(msg))
    while len(msg_len) < 5:
        msg_len = msg_len + "+"
    user.write((msg_len+msg).encode())
         

async def checkmsg(reader):
    msg_len =(await reader.read(5)).decode()
    msg_len = int(msg_len.replace('+', ''))
    msg = (await reader.read(msg_len*2)).decode()
    return msg