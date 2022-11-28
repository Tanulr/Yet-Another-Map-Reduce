from flask import Flask, jsonify, request
import requests
import json
import os
#Taking input from user 
while(True):
    oper = int(input("Enter the operation number that needs to be performed:\n 1. WRITE \n 2. READ \n 3. MAP REDUCE\n 4. EXIT\n "))
    if oper==1:
        filename=input("Enter the name of the file to be written: ")
        response=requests.get(f'http://127.0.0.1:5000/write')
        if response.status_code==200:
            network=response.json()['network']
            num_partitions=len(network)
            f=open(filename,'r') 
            stats = os.stat(filename)
            file_size = stats.st_size
            if(file_size>=num_partitions):
                partition_size = file_size//num_partitions
                remaining_bytes = file_size-partition_size*num_partitions
                for node in network:
                    if(node==network[-1]):
                        data = f.read(partition_size+remaining_bytes)
                    else:
                        data = f.read(partition_size)
                    myobj={"data":data,"filename":filename,"node":node}
                    url=f'http://127.0.0.1:{node}/write'
                    x = requests.post(url, json = myobj)
                    if x.status_code==201:
                        msg=x.json()
                        print(msg['message'])

            elif(file_size<num_partitions):
                for node in network:
                    if(node==network[0]):
                        data = f.read(file_size)
                    else:
                        #Some partitions be empty data
                        data = ""
                    myobj={"data":data,"filename":filename,"node":node}
                    url=f'http://127.0.0.1:{node}/write'
                    x = requests.post(url, json = myobj)
                    if x.status_code==201:
                        msg=x.json()
                        print(msg['message'])

            
                
    elif oper==2:
        filename=input("Enter the name of the file to be read: ")
        response=requests.get(f'http://127.0.0.1:5000/read')
        if response.status_code==200:
            network=response.json()['network']
            #print(network)
        for node in network:
            partition_file_name = f'partition_{filename[:-4]}_node_{node}.txt'
            myobj={'partition_file_name':partition_file_name}
            #print(partition_file_name)
            response = requests.post(f'http://127.0.0.1:{node}/read',json=myobj)
            if response.status_code==201:
                data=response.json()
                print(data['data'],end="")
        print()

    elif oper==3:
        filename=input("Enter the name of the input file: ")
        filename=input("Enter the name of the mapper file: ")
        filename=input("Enter the name of the reducer file: ")

    elif oper==4:
        exit()
    else:
        print("Invalid operation!")
            


        


