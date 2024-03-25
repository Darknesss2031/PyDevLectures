import socket
import cmd
from threading import Thread
import readline
import shlex

class cmdLine(cmd.Cmd):
    prompt = '> '

    def __init__(self, socketfd: socket.socket):
        super().__init__()
        self.socket = socketfd

    def do_login(self, arg):
        self.socket.sendall(f"login {arg.split()[0]}\n".encode())

    def do_who(self, arg):
        self.socket.sendall(b"who\n")

    def do_cows(self, arg):
        self.socket.sendall(b"cows\n")

    def do_say(self, arg):
        args = shlex.split(arg)
        self.socket.sendall(f"say {shlex.join(args[:2])}\n".encode())

    def do_yield(self, arg):
        args = shlex.split(arg)
        self.socket.sendall(f"yield {shlex.join(args[:1])}\n".encode())

    def do_EOF(self, args):
        return True

    def do_quit(self, args):
        return True

def targetFunction(cmdline: cmdLine):
    while cmdline.socket is not None:
        data = b''
        while len(new := cmdline.socket.recv(1024)) == 1024:
            data += new
        data += new
        print(f"\n{data.decode().rstrip()}",
              f"\n{cmdline.prompt}{readline.get_line_buffer()}",
              sep='', end='', flush=True)

HOST = 'localhost'
PORT = 1337

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
    sockfd.connect((HOST, PORT))
    cmdline = cmdLine(sockfd)
    Thread(target=targetFunction, args=(cmdline,)).start()
    cmdLine.cmdloop()