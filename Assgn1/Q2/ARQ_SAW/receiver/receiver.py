# please do not use any library
def xor(a, b):
    assert(len(a) == len(b))
    ans = ""
    for i in range(len(b)):
        if a[i] == b[i]:
            ans += '0'
        else:
            ans += '1'
    return ans


def compute_rem(dividend_, divisor):

    k = len(divisor)
    n = len(dividend_)

    dividend = ['0'] * len(dividend_)
    for i in range(n):
        dividend[i] = dividend_[i]

    i = 0
    while i + k - 1 < n:
        dividend[i:i + k] = xor(dividend[i:i + k], divisor)
        while i < n and dividend[i] == '0':
            i += 1

    ans = ""
    for j in range(i, n):
        ans += dividend[j]

    while len(ans) < k-1:
        ans = '0' + ans

    return ans


def checkMSG(msg):
    length = len("10011")
    pad_msg = msg + '0'*(length-1)
    remainder = compute_rem(pad_msg, "10011")
    if(remainder == "0000"):
        return True
    return False


def receiveMSG():
    prev_line = ""
    prev_flag = '0'
    result = []
    with open("input.txt") as fp:
        for line in fp:
            line = line.strip()
            if(line == prev_line):
                result.append("duplicate")
                # print("duplicate", end=" ")
                continue
            elif(line[-1] == prev_flag or not(checkMSG(line[:-1]))):
                result.append("corrupt")
                #print("corrupt", end=" ")
                continue
            line_integer = int(line[:-5], 2)
            crc = line[-5:-1]
            ascii_msg = line_integer.to_bytes(
                (line_integer.bit_length() + 7) // 8, "big").decode()
            result.append(ascii_msg)
            #print(ascii_msg, end=" ")

            prev_flag = line[-1]
            prev_line = line
    print(" ".join(result))


receiveMSG()
