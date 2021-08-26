from PIL import Image
import sys


def LeftShiftRotate(oldstate):  								# please Don't Modified it :)

    leftbit = oldstate[0]

    for i in range(0, 14):
        oldstate[i] = oldstate[i+1]

    oldstate[14] = leftbit
    newstate = oldstate

    return newstate


def hamming_decode(bitstring):
    N = len(bitstring)
    n, k = 15, 11
    x = bitstring
    assert(len(x) == n)

    par = [0]*(n-k)

    out = ["Valid", "p1", "p2", "d3", "p4", "d5", "d6", "d7",
           "p8", "d9", "d10", "d11", "d12", "d13", "d14", "d15"]

    for i in range(n):
        for j in range(n - k):
            if ((i + 1) & (1 << j)) != 0:
                par[j] ^= int(x[i])

    corrupted_bit = 0

    for j in range(n - k):
        corrupted_bit += par[j] * (1 << j)

    y = out[corrupted_bit] + " "

    for i in range(n):
        flag = 0
        for j in range(n - k):
            if i + 1 == (1 << j):
                flag = 1
                break
        if flag:
            continue
        if i == corrupted_bit - 1:
            y += flip(x[i])
        else:
            y += x[i]

    return y


def hamming_encode(bitstring):
    x = bitstring
    n, k = 15, 11
    assert (len(x) == k)
    y = [0] * n
    cur = 0
    for i in range(n):
        flag = 0
        for j in range(n - k):
            if i + 1 == (1 << j):
                flag = 1
                break
        if flag:
            continue
        y[i] = int(x[cur])
        cur += 1
        for j in range(n - k):
            if ((i + 1) & (1 << j)) != 0:
                y[((1 << j) - 1)] ^= y[i]
    ret = ""
    for c in y:
        ret += str(c)
    return ret


def flip(c):
    if c == '0':
        return '1'
    return '0'


def ReadImage():

    image_name = sys.argv[1]  # read as command line argrument
    flip_bits = sys.argv[2].split(',')  # same as above

    image_ = Image.open(image_name)
    pixel_ = image_.load()
    width, height = image_.size
    sender = open("sender.txt", 'w')
    receiver = open("receiver.txt", 'w')

    for y in range(0, height):
        for x in range(0, width):
            print("{" + str(pixel_[x, y][0]), pixel_[x, y][1],
                  str(pixel_[x, y][2]) + "}", sep=',', end=' ', file=sender)
            
            a = [""] * 3
            for i in range(3):
                a[i] = hamming_encode(format(pixel_[x, y][i], "011b"))
            
            print("{" + a[0], a[1], a[2] + "}", sep=',', file=sender)
            
            for i in range(3):
                b = ""
                for j in range(len(flip_bits)):
                    if flip_bits[j] == '1':
                        b += flip(a[i][j])
                    else:
                        b += a[i][j]
                print(hamming_decode(b), end=' ', file=receiver)
            print(file=receiver)
            
            flip_bits = LeftShiftRotate(flip_bits)
    
    sender.close()
    receiver.close()


ReadImage()
