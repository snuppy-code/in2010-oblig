import sys


def main():
    # Read input
    A = [int(line) for line in sys.stdin]

    insertionsort(A)

    # Print result
    for num in A:
        print(num)


def insertionsort(A):
    for i in range(1, len(A)):
        j = i
        while j > 0 and A[j - 1] > A[j]:
           A[j - 1], A[j] = A[j], A[j - 1]
           j -= 1


if __name__ == "__main__":
    main()
