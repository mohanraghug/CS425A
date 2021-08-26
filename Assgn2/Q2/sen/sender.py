import socket
import time
import os
import hashlib
import random

host = ""
port = 9999


def check_sum(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest()


class Sender:

    def __init__(self, window_size, timeout):
        self.w = window_size  # sender's window size
        self.t = timeout
        self.filename = "FileToTransfer.txt"  # file to be transferred
        self.cur_seq = 0  # current sequence
        self.active_spaces = self.w  # free space in window
        self.window = window_size * [None]  # buffer
        self.soc = socket.socket()
        self.last_sent_seqnum = -1  # last sent sequence number
        self.last_ack_seqnum = -1  # last acknowledged sequence number

    def canAdd(self):  # check if a packet can be added to the send window
        if self.active_spaces == 0:
            return False
        else:
            return True

    def addAndSend(self, pack):  # add a packet to the send window
        self.last_sent_seqnum = self.cur_seq
        self.cur_seq += 1
        self.window[self.w - self.active_spaces] = pack
        self.active_spaces -= 1
        time.sleep(1.5)
        data = pack
        conn.send(data.encode('utf-8'))
        time.sleep(2)
        print("Sending packet: ", pack)

    def resend(self):  # function to resend packet if lost
        print('resending packets in the window....')
        print('self.active_spaces='+str(self.active_spaces))
        print('self.window=' + str(self.window))
        # For all packets in the current window
        for i in range(self.w - self.active_spaces):
            data = self.window[i]
            data2 = data.split('/////')
            # Recalculated the probability
            data2[-1] = str(random.randint(0, 100))
            data = '/////'.join(data2)
            self.window[i] = data
            # Resend the current packet
            time.sleep(1.5)
            conn.send(data.encode('utf-8'))
            time.sleep(2)
            self.last_sent_seqnum = int(data2[1])
            # print(data)
            print("Resending packet: ", data.split('/////'))

    def separateChunks(self, message):
        splitted = message.split('/////')
        received = []
        NumberOfItems = int((len(splitted)-1)/2)
        print(NumberOfItems)
        j = 1
        k = 2
        received.append('')
        if NumberOfItems != 1:
            print('separating packet collected from pipe')
            for i in range(0, NumberOfItems):
                if i == 0:
                    x = splitted[0]
                else:
                    received.append('')
                y = splitted[j]
                j = j+2
                mergedTexted = splitted[k]
                k = k+2
                z = mergedTexted[0:3]
                received[i] = x+'/////'+y+'/////'+z
                x = mergedTexted[3:len(mergedTexted)]
                print(received[i])
        else:
            received[0] = message
        print(received)
        return received

    def makePack(self, num, pac):  # Create a packet

        checksum = check_sum(pac.encode('utf-8'))
        length = len(pac)
        # probability_that_the_packet_will_reach
        probability = random.randint(0, 100)
        packet = checksum + "/////" + str(num) + "/////" + str(
            length) + "/////" + str(pac) + "/////" + str(probability)            # Creating Packet in format

        return packet

    def divide(self, data, num):  # create list of chunks from datas
        lis = []
        while data:
            lis.append(data[:num])
            data = data[num:]
        return lis

    def acc_Acks(self):  # check if all the sent packets have been ACKed
        print('checking if all the sent packets have been ACKed')
        print('receiving the packets....')
        try:
            data = conn.recv(1024)  # receive message from receiver
        except:  # if the message does not arrive within time bound print on console "'Connection lost due to timeout!'" and return 0
            print('Connection lost due to timeout!')
            self.resend()      # Resend window frame packets in case of a time out
            return 0

        packet = data.decode('utf-8')
        received = self.separateChunks(packet)
        for pack in received:
            if pack.split("/////")[-1] == "ACK":
                if(received.index(pack) == len(received)-1):
                    print("---------------Before ACK-----------")
                    print("The received packet from receiver is: " + pack)
                    print("self.last_ack_seqnum= " + str(self.last_ack_seqnum))
                    print("self.active_spaces= " + str(self.active_spaces))
                    print("self.window= ", self.window)
                remove_till = pack.split("/////")[1]
                self.last_ack_seqnum = int(remove_till)
                for i in range(self.w - self.active_spaces):
                    if self.window[i].split("/////")[1] == remove_till:
                        # Shift forward non-Acked elements of the window
                        for j in range(i + 1, self.w - self.active_spaces):
                            self.window[j - i - 1] = self.window[j]
                        # Fill the window with Nones till window size
                        for j in range(self.w-self.active_spaces-i-1, self.w - self.active_spaces):
                            self.window[j] = None
                        # Update active spaces in the window
                        self.active_spaces += (i+1)
                        break
                if(received.index(pack) == len(received)-1):
                    print("---------------After ACK-----------")
                    print("The received packet from receiver is: " + pack)
                    print("self.last_ack_seqnum= " + str(self.last_ack_seqnum))
                    print("self.active_spaces= " + str(self.active_spaces))
                    print("self.window= ", self.window)

            else:
                if(received.index(pack) == len(received)-1):
                    print("The received packet from receiver is: " + pack)
                self.resend()               # Resend the window packets in case of an NAK
                return 0
        return int(self.active_spaces == self.w)

        """
        # Testcase for points (3) and (4) in section 2.3:

        received_packet='c81e728d9d4c2f636f067f89cc14862c/////2/////NAK'
        self.window=["f861c77c48e93c3221f61d/////0/////10/////b'Go-Back-N '/////57",\
                     "fdbeff054b0c917df19343c/////1/////10/////b'ARQ is a s'/////30",\
                     "b6e2213c855aa95dfd97732/////2/////10/////b'pecific in'/////62", \
                     "dc7fd4698c43bea0469e76/////3/////7/////b'stance.'/////52"]
        self.w = 4
        self.active_spaces=0
        self.last_ack_seqnum = 0
        """

    def SendMessage(self, pack_list):  # send the messages till all packets are sent
        for chunk in pack_list:
            packet = self.makePack(self.cur_seq, chunk)   # Makes packet
            # print(packet)
            # check for Acks whilst the canAdd function returns a true value
            while(not self.canAdd()):
                self.acc_Acks()
            # Waits for the canAdd function to indicate empty space in the window
            self.addAndSend(packet)
        # Ensures the last chunk is sent properly
        while not self.acc_Acks():
            time.sleep(1)

        print("END")
        time.sleep(1)
        data = "$$$$$$$"
        conn.send(data.encode('utf-8'))
        time.sleep(1)

    def SendPacketsFromFile(self):  # to send packets from the file
        try:
            fil = open(self.filename, 'r')
            data = fil.read()
            pack_list = self.divide(data, 25)
            fil.close()
        except IOError:
            print("No such file exists")
        l = len(pack_list)
        self.SendMessage(pack_list)


win = input("Enter window size: ")
tim = input("Enter the timeout: ")

server = Sender(int(win), float(tim))

server.soc.bind((host, port))
server.soc.listen(5)
conn, addr = server.soc.accept()
data = conn.recv(1024)
print("received connection")
response = str(win) + "/////" + str(tim) + "/////" + "FileToTransfer.txt"
conn.send(response.encode('utf-8'))
conn.close()

server.soc.settimeout(float(tim))
conn, addr=server.soc.accept()
data=conn.recv(1024)
server.SendPacketsFromFile()
conn.close()
