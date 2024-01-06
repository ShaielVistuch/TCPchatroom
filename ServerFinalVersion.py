import threading
import socket
host = '127.0.0.2'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
ids = []
idsinitial = []
passwords =[]


def broadcast(message,c): #This function is responsible for sending client messages to everyone in their chat
    #c is the client that wants to send a messegae, message is the actual message
    index2 = clients.index(c) #finding the index of the client
    tempo = ids[index2] #finding the ID of the client
    for client in clients: #looping over all of the connected clients
        index3 = clients.index(client) #saving the current client index
        temp = ids[index3] #finding its ID
        if tempo == temp: #checking if the IDs match
            print(message)#printing on the screen of the server for supervising the code
            client.send(message) #sending messege if the IDs match




def handle_client(client): #This function handles clients'connections

    while True:
        try:
            message = client.recv(1024)
            broadcast(message,client) #broadcasting the message that the client send in the chat
        except: #closing the connection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'), client)
            aliases.remove(alias)
            break



def receive(): # Main function to receive the clients connection
    count = 1
    while True:

        print('Server is listening') #printing on the screen of the server for supervising the code
        client, address = server.accept()
        print(f'connection is established with {str(address)}')#printing on the screen of the server for supervising the code

        # defining keywords:

        client.send('enter group chat id:'.encode('utf-8'))
        ide = client.recv(1024).decode('utf-8')
        print(ide)#printing on the screen of the server for supervising the code
        idsinitial.append(ide)

        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)

        password = 'initial'
        client.send('password?'.encode('utf-8'))
        password = client.recv(1024).decode('utf-8')

        print(password)
        client.send('option?'.encode('utf-8'))
        option = client.recv(1024).decode('utf-8')


        # CLIENT CHOOSES TO CREATE A NEW CHAT GROUP
        if option=='2':

            passwords.append(password) #putting password in passwords list
            print("inside if")#printing on the screen of the server for supervising the code
            ide = str(idsinitial[-1])
            count = count + 1
            ide = str(count) #we are setting the group chat IDs to be 2, 3, 4, ...
            print(ide)#printing on the screen of the server for supervising the code
            ids.append(ide)
            broadcast(f'THE NEWLY CREATED CHAT ID IS {count} '.encode('utf-8'), client)
            print(f'The alias of this client is {alias}'.encode('utf-8'))
            Name=alias.decode('utf-8')
            broadcast(f'{Name} has connected to the chat room'.encode('utf-8'), client)
            client.send('YOU ARE NOW CONNECTED TO THE CHAT'.encode('utf-8'))
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        # CLIENT CHOOSES TO CONNECT TO AN EXISTING CHAT GROUP
        elif option == '1': #if true, it means that the client choose to connect to an existing group
            #CHEKING THAT THE PASSWORD IS CORRECT

            result = passwords.count(password)
            # Result would be greater than 0 if there exist a group chat with that password
            print("result\n") #printing on the screen of the server for supervising the code
            print(result)
            if result>0: #If true, the password exist in the passwords list, which means that there is a group chat with that password.
                passwords.append(password) #we will put the password in password list
                try:
                    index5 = ids.index(ide) #we will get the index of the the group ID in the idsinitial list
                    print("index5\n")
                    print(index5)
                    passoriginal=passwords[index5] #we will save the password of the ID in index number index5 to the variable passoriginal
                    print("passoriginal\n")
                    print(passoriginal)
                    print("current password\n")
                    print(password)
                    if password == passoriginal: #checking that the password is correct and maches the required password
                        print("matching password")
                        print("flag")
                        print(ide)
                        result2 = ids.count(ide)
                        print("result2 is:\n")
                        print(result2)
                        if result2 > 0: #If true, the ID exist in the ids list, which means that there is a group chat with that ID.
                            ids.append(ide) #Add the current id to tha last place in the ids list
                            print(f'The alias of this client is {alias}'.encode('utf-8'))
                            Name = alias.decode('utf-8') #decoding the client name to make it easy to read for the client
                            broadcast(f'{Name} has connected to the chat room'.encode('utf-8'), client)
                            client.send('YOU ARE NOW CONNECTED TO THE CHAT'.encode('utf-8'))
                            thread = threading.Thread(target=handle_client, args=(client,))
                            thread.start()
                    else: #password doesn't equal passoriginal, which means that there is a chat with that password but the
                        # password and ID don't mach
                        print("unmatching password")
                        client.send('disconnect'.encode('utf-8'))
                        client.close()
                        clients.remove(client)
                        aliases.remove(alias)
                except: #the ID doesn't exist in the ids list, which means that there isn't a group chat with that ID.
                    #Basicly it means that the client is trying to connect to a chat that doest exist
                    print("No such id")
                    client.send('disconnect'.encode('utf-8'))
                    client.close()
                    clients.remove(client)
                    aliases.remove(alias)
            else: #the password doesn't exist in the passwords list, which means that there isn't a group chat with that pasword.
                print("No such password")
                client.send('disconnect'.encode('utf-8'))
                client.close()
                clients.remove(client)
                aliases.remove(alias)






if __name__ == "__main__":
    receive()