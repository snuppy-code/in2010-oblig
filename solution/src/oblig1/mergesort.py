# Implementert både i python og java.
# De burde være ganske like.
# Gi gjerne tilbakemelding på begge :)


import sys


def main():
    # Read input
    A = [int(line) for line in sys.stdin]

    A = mergesort(A)
    # Print result
    for num in A:
        print(num)


def mergesort(A):
    if len(A) > 1:
        a = mergesort(A[len(A)//2:])
        a_min = 0
        b = mergesort(A[:len(A)//2])
        b_min = 0

        # merge
        out = []
        while a_min < len(a) and b_min < len(b):
            if a[a_min] < b[b_min]:
                out.append(a[a_min])
                a_min+=1
            else:
                out.append(b[b_min])
                b_min+=1

        # merge remaining
        entered_a = False
        while a_min < len(a):
            entered_a = True
            out.append(a[a_min])
            a_min+=1
        while b_min < len(b):
            assert not entered_a, "unreachable!"
            out.append(b[b_min])
            b_min+=1

        return out
    else:
        return A



if __name__ == "__main__":
    main()
