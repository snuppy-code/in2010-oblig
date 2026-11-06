import sys

def main():
    array = []
    for line in sys.stdin:
        array.append(int(line))
    print_balanced(array)

def print_balanced(array):
    if len(array) == 1:
        print(array[0])
        return
    elif len(array) == 0:
        return

    index = (0 + len(array)) // 2
    print(array[index])
    print_balanced(array[index:])
    print_balanced(array[:index])

if __name__ == '__main__':
    main()

