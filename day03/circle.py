import argparse

parser=argparse.ArgumentParser(description="Calculate circle area")
parser.add_argument("--radius",help="Input radius",required=True)
args=parser.parse_args()

print(3.14*int(args.radius)**2)


