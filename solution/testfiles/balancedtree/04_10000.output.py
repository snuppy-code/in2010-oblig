from check import check
from os import path
path = path.abspath(__file__)
check({int(n) for n in open(path.removesuffix("output.py") + "input.txt")})
