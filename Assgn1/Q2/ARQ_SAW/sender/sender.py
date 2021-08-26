from threading import Thread
import time
import socket

# Please do not change the socket configration
# socket used are blocking in nature

#####################################
##########code here##################
#####################################

poly = '10011'  # polynomial
to = 2  # timeout


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


def checkMsg(msg):
    # this is a Receiver side helper function
    # you can change the name of the function if you want
    # checks weather the message is correctly received or not
    # i.e detect error using CRC, return True if no error,else Flase
    #####################################
    #####################################
    # TO DO
    length = len("10011")
    pad_msg = msg[:-1] + '0'*(length-1)
    remainder = compute_rem(pad_msg, "10011")
    # print(msg,remainder)
    if(remainder == "0000"):
        return True
    return False


def encodeMsg(msg):
    # TO DO
    length = len("10011")
    pad_msg = msg + '0'*(length-1)
    remainder = compute_rem(pad_msg, "10011")
    # print(msg,remainder)
    msg = msg + remainder
    return msg


def sender():
    s = socket.socket()
    # print("Socket successfully created")
    port = 12345
    s.bind(('', port))
    # print("socket binded to %s" % (port))
    s.listen(1)
    # print("socket is listening")
    c, addr = s.accept()
    c.settimeout(to)
    ack1 = "10011000"
    ack0 = "10001011"

    #####################################
    ##########code here##################
    #####################################
    # take input from input.txt line by line and make sure you send all the messages
    # to the receiver
    flag = '0'
    f = open("input.txt", 'r')
    msg_list = []
    for i in f.readlines():
        msg_list.append(i.strip())
    msg_no = 0

    while msg_no < len(msg_list):
        msg = msg_list[msg_no]
        flag = '1' if flag == '0' else '0'
        msg = encodeMsg(msg) + flag

        c.sendall(bytes(msg, 'utf-8'))
#         time.sleep(to) ????

        try:
            msg = c.recv(1024)
            msg = msg.decode('utf-8')
            # print(msg)
            if (flag == '0' and msg == ack0) or (flag == '1' and msg == ack1):
                print("message sent")
                msg_no += 1
            else:
                print("wrong ack")
        except:
            print("no ack")
    #####################################
    #####################################
    c.close()


def receiver():
    s = socket.socket()
    port = 12345
    s.connect(('127.0.0.1', port))
    #####################################
    ##########read here##################
    #####################################
    # the receiver function seems to be long however it is just same thing repeated
    # over and over again, so understanding a part will be
    ack1 = "10011000"
    ack0 = "10001011"

    # 1
    #####################################
    msg = s.recv(1024)  # receiving msg from sender
    msg = msg.decode('utf-8')  # converting into string
    # checking if the msg is valid(i.e detect error using CRC)
    check = checkMsg(msg)
    flag = msg[-1]
    ack = ''
    if check:
        if flag == '0':
            ack = ack0
        else:
            ack = ack1
        s.sendall(bytes(ack, 'utf-8'))  # sending ACK to sender
    else:  # idealy we should never get in this else, since students should send the message correctly
        print('message is encode wrongly')
        time.sleep(to)

    # 2.1  corrupt ACK
    #####################################
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    check = checkMsg(msg)
    flag = msg[-1]
    ack = ''
    if check:
        if flag == '0':
            ack = ack0
        else:
            ack = ack1
        # courrupting ack
        ack += '1'  # appending '1' will lead to ack being corrupt, test case will be
        # made in such a way that this is guranteed
        s.sendall(bytes(ack, 'utf-8'))
    else:
        print('message is encode wrongly')
        # this will make sender think that, user didn't receive the message
        time.sleep(to)
        # i.e we waited for timeout and didn't send ACK

    # 2.2  since above msg had corrupt ACK, therefore this is response for the resent message form sender
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    check = checkMsg(msg)
    flag = msg[-1]
    ack = ''
    if check:
        if flag == '0':
            ack = ack0
        else:
            ack = ack1
        s.sendall(bytes(ack, 'utf-8'))
    else:
        print('message is encode wrongly')
        time.sleep(to)

    # 3.1 ACK lost
    #####################################
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    check = checkMsg(msg)
    flag = msg[-1]
    ack = ''
    if check:
        if flag == '0':
            ack = ack0
        else:
            ack = ack1
        # ack lost then resending ack
        # .5 added so that we can safely assume that the sender has resent
        time.sleep(to+.5)
        # the msg before we try to receive it again
    else:
        print('message is encode wrongly')
        time.sleep(to)

    # 3.2  receiving the resent msg again since previous ACK was lost
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    check = checkMsg(msg)
    flag = msg[-1]
    ack = ''
    if check:
        if flag == '0':
            ack = ack0
        else:
            ack = ack1
        s.sendall(bytes(ack, 'utf-8'))
    else:
        print('message is encode wrongly')
        time.sleep(to)
    # 4
    #####################################
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    check = checkMsg(msg)
    flag = msg[-1]
    ack = ''
    if check:
        if flag == '0':
            ack = ack0
        else:
            ack = ack1
        s.sendall(bytes(ack, 'utf-8'))
    else:
        print('message is encode wrongly')
        time.sleep(to)
    # 5
    #####################################
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    check = checkMsg(msg)
    flag = msg[-1]
    ack = ''
    if check:
        if flag == '0':
            ack = ack0
        else:
            ack = ack1
        s.sendall(bytes(ack, 'utf-8'))
    else:
        print('message is encode wrongly')
        time.sleep(to)

    #####################################
    #####################################
    s.close()


def main():
    # making both functions run on different thread
    t1 = Thread(target=sender, args=[])
    t2 = Thread(target=receiver, args=[])

    t1.start()
    t2.start()


main()
