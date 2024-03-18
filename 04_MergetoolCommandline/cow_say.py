import cmd
import cowsay
import shlex

def parseInput(string):
    args = shlex.split(string)
    if len(string) % 2 == 0:
        return dict(zip(args[::2], args[1::2]))
    return None

cow = cowsay.list_cows()
eyes = ["OO", "oO", "Oo", "oo", "..", "0O", "xx", "--", "TT", "==", "++", "$$", "::", "()", "~~"]
tongue = [" U", "U ", "# ", " #", "| ", " |", " /", "/ ", "\ "]
params = ["message", "cow", "eyes", "tongue"]

def complete(text, line, begidx, endidx):
    if begidx == endidx :
        key = shlex.split(line)[-1]
    else:
        key = shlex.split(line)[-2]
    match key:
        case "cow":
            return [i for i in cow if i.startswith(text)]
        case "eyes":
            return [i for i in eyes if i.startswith(text)]
        case "tongue":
            return [i for i in tongue if i.startswith(text)]
        case _:
            return [i for i in params if i.startswith(text)]

class Cowsay(cmd.Cmd):
    prompt = ">"

    def do_list_cows(self, _):
        """
        Print all cows
        """
        print(cowsay.list_cows())

    def do_exit(self, _):
        """
        Exit from cows
        """
        return True

    def do_make_bubble(self, args):
        """
        Print a bubble with text.
        Usage: make_bubble text TEXT
        """
        print(cowsay.make_bubble(parseInput(args)))

    def do_cowsay(self, args):
        """
        Print a cow with its message.
        Usage: cowsay message MESSAGE [cow COW] [eyes EYES] [tongue TONGUE]
        """
        print(cowsay.cowsay(parseInput(args)))

    def do_cowthink(self, args):
        """
        Print a cow with its message in a bubble.
        Usage: cowthink message MESSAGE [cow COW] [eyes EYES] [tongue TONGUE]
        """
        print(cowsay.cowthink(args))

    def complete_make_bubble(self, text, line, begidx, endidx):
        if "text".startswith(text):
            return ["text"]

    def complete_cowsay(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def complete_cowthink(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

if __name__ == '__main__':
    Cowsay().cmdloop()