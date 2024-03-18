import asyncio
import shlex
import cowsay

available_users = {}

def login(command, writer):
    if len(command) != 2:
        writer.write("Invalid arguments.\n".encode())
    elif command[1] not in cowsay.list_cows():
        writer.write("Error: use 'cows' to see existing login name.\n".encode())
    elif command[1] in available_users.keys():
        writer.write("Error: this login is already in use, choose another one.\n".encode())
    else: return True
    return False

def who(command, writer):
    if len(command) != 1:
        writer.write("Invalid arguments.\n".encode())
    else: return True
    return False

def cows(command, writer):
    if len(command) != 1:
        writer.write("Invalid arguments.\n".encode())
    else: return True
    return False

def say(me, id, command, writer):
    if id is None:
        print(me + ": trying to use say command without login")
        writer.write(("You have no rights here, please login.\n").encode())
    elif len(command) != 3:
        writer.write("Invalid arguments.\n".encode())
    elif command[1] not in available_users.keys():
        writer.write("There is no user with this name here.\n".encode())
    else: return True
    return False

def yield_check(me, id, command, writer):
    if id is None:
        print(me + ": trying to use yield command without login")
        writer.write(("You have no rights here, please login.\n").encode())
    elif len(command) != 2:
        writer.write("Invalid arguments.\n".encode())
    else: return True
    return False

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    id = None
    queue = asyncio.Queue()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

        for q in done:

            if q is send:
                send = asyncio.create_task(reader.readline())
                commands = shlex.split(q.result().decode())
                match commands[0]:
                    case "login":
                        if login(commands, writer):
                            id = commands[1]
                            available_users[id] = queue
                            print(me + ": my id is" + id)
                            writer.write(f"Your id - {id}.\n".encode())
                        else: continue

                    case "who":
                        if who(commands, writer):
                            print(me + ": using who command")
                            writer.write(("Online users:\n" + " ".join(available_users.keys()) + "\n").encode())
                        else: continue

                    case "cows":
                        if who(commands, writer):
                            print(me + ": using cows command")
                            writer.write(("Available logins:\n" + " ".join(list(set(cowsay.list_cows()) - set(available_users.keys()))) + "\n").encode())
                        else: continue

                    case "say":
                        if say(me, id, commands, writer):
                            print(me + ": saying to", commands[1])
                            await available_users[commands[1]].put(f"\n{cowsay.cowsay(commands[2], cow=id)}\n")
                        else: continue

                    case "yield":
                        if yield_check(me, id, commands, writer):
                            print(me + ": yielding")
                            for out in available_users.values():
                                if out is not available_users[id]:
                                    await out.put(f"\n{cowsay.cowsay(commands[1], cow=id)}\n")
                        else: continue

                    case "quit":
                        if len(commands) != 1:
                            writer.write(("Too much parameters\nLeaving the system...\n").encode())
                        print(me + ": logs out")
                        writer.write(("Logged out\n").encode())
                        del available_users[id]
                        id = None

                    case _:
                        continue

            elif q is receive:
                receive = asyncio.create_task(queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print(id, "DONE")
    del available_users[id]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())