def main():
    N = int(input())
    set = SetHash()
    for _ in range(N):
        command = input().split()
        if command[0] == "contains":
            print(str(set.contains(int(command[1]))).lower())

        if command[0] == "insert":
            set.insert(int(command[1]))

        if command[0] == "remove":
            set.remove(int(command[1]))

        if command[0] == "size":
            print(set.size())


class SetHash:
    def __init__(self):
        pass

    def contains(self, x):
        return False

    def insert(self, x):
        pass

    def remove(self, x):
        pass

    def size(self):
        return 0

if __name__ == '__main__':
    main()
