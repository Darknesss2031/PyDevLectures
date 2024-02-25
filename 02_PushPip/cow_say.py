import argparse
from cowsay import cowsay, list_cows

parser = argparse.ArgumentParser(prog="cowsay", description="Cowsay program")

parser.add_argument('message', nargs='?', default='', help='cow help message')
parser.add_argument('-e', default='oo', dest='eye_string')
parser.add_argument('-f', dest='cowfile')
parser.add_argument('-l', action='store_true')
parser.add_argument('-n', action='store_false')
parser.add_argument('-T', dest='tongue_string')
parser.add_argument('-W', dest='column', type=int, default=40)

parser.add_argument('-b', action='store_true')
parser.add_argument('-d', action='store_true')
parser.add_argument('-g', action='store_true')
parser.add_argument('-p', action='store_true')
parser.add_argument('-s', action='store_true')
parser.add_argument('-t', action='store_true')
parser.add_argument('-w', action='store_true')
parser.add_argument('-y', action='store_true')

args = parser.parse_args()
opts = 'bdgpstwy'
options = ''
for opt in opts:
    if getattr(args, opt): options += str(opt)

if args.l:
    print(*list_cows())
else:
    print(cowsay(args.message, preset=options, eyes=args.e, tongue=args.T, wigth=args.W, wrap_text=args.n, cowfile=args.f))