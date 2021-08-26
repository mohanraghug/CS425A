#!/bin/bash

python3 hamming_code.py tests/input1/example1.jpg 1,0,0,0,0,0,0,1,0,0,0,0,0,0,1
if ! cmp -s sender.txt tests/input1/sender.txt
then
    echo 'Test 1 Failing, sender.txt doesnot match !'
    exit 0
fi
if ! cmp -s receiver.txt tests/input1/reciever.txt
then
    echo 'Test 1 Failing,receiver.txt doesnot match !'
    exit 0
fi

python3 hamming_code.py tests/input2/example1.jpg 0,0,0,0,0,0,0,1,0,0,0,0,0,0,1
if ! cmp -s sender.txt tests/input2/sender.txt
then
    echo 'Test 2 Failing,sender.txt doesnot match !!'
    exit 0
fi
if ! cmp -s receiver.txt tests/input2/reciever.txt
then
    echo 'Test 2 Failing,receiver.txt doesnot match !'
    exit 0
fi


python3 hamming_code.py tests/input3/example1.jpg 0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
if ! cmp -s sender.txt tests/input3/sender.txt
then
    echo 'Test 3 Failing,sender.txt doesnot match!'
    exit 0
fi
if ! cmp -s receiver.txt tests/input3/reciever.txt
then
    echo 'Test 3 Failing,receiver.txt doesnot match!'
    exit 0
fi

echo 'All tests Passed!!'


