import threading
import socket
option=input('Choose an option:\n 1) Connect to a group chat\n 2) Create a new group chat\n 3) Disconnect\n')
if option == "1":
    alias = input('ENTER YOUR NAME: ')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.2', 59000))
    identity = input('ENTER THE ID OF THE GROUP YOU WANT TO JOIN: ')
    password = input('ENTER THE PASSWORD: ')
    def client_receive():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "alias?":
                    client.send(alias.encode('utf-8'))
                elif message == "enter group chat id:":
                    client.send(identity.encode('utf-8'))
                elif message == "password?":
                    client.send(password.encode('utf-8'))
                elif message == "option?":
                    client.send(option.encode('utf-8'))
                elif message == "disconnect":
                    print('Sorry, we are unable to connect you to the group chat')
                    client.close()
                else:
                    print(message)

            except:
                print('An error happened')
                client.close()
                break


    def client_send():
        while True:
            message = f'{alias}: {input("")}'
            client.send(message.encode('utf-8'))


    receive_thread = threading.Thread(target=client_receive)
    receive_thread.start()

    send_thread = threading.Thread(target=client_send)
    send_thread.start()

if option == "2":
    alias = input('ENTER YOUR NAME: ')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.2', 59000))
    password = input('CHOOSE A PASSWORD FOR THE GROUP: ')
    identity='1'

    def client_receive():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "alias?":
                    client.send(alias.encode('utf-8'))
                elif message == "password?":
                    client.send(password.encode('utf-8'))
                elif message == "enter group chat id:":
                    client.send(identity.encode('utf-8'))
                elif message == "option?":
                    client.send(option.encode('utf-8'))
                elif message == "disconnect":
                    print('Sorry, we are unable to connect you to the group chat')
                    client.close()
                elif message == "disconnect option":
                    print('Disconnecting . . . Bye!')
                    client.close()
                elif message == "wrong option":
                    print('You entered an invalid option. We are disconnecting you.')
                    client.close()
                    break
                else:
                    print(message)

            except:
                print('An error happened')
                client.close()
                break


    def client_send():
        while True:
            message = f'{alias}: {input("")}'
            client.send(message.encode('utf-8'))


    receive_thread = threading.Thread(target=client_receive)
    receive_thread.start()

    send_thread = threading.Thread(target=client_send)
    send_thread.start()