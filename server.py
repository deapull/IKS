import socket

HOST, PORT = '', 80 #Налаштування порта і хоста

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Перший сокет, використовує адреси Ipv4. Другий сокет, який використовує TCP
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind((HOST, PORT))# Надання адреси хоста і порт для сокета, який ми створили
my_socket.listen(1) #Команда для того, щоб сокет слухав запити

print('Сервер відкритий на порту:', PORT)

while True:
    print("Очікую підключення...")
    connection, address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')#Вся інформація про запит
    #print(request)
    string_list = request.split(' ')
    method = string_list[0]
    #print(method)
    requesting_file = string_list[1]

    print('Запит клієнта', requesting_file)

    myfile = requesting_file.split()[0]
    myfile = myfile.lstrip('/')
    if (myfile == ''):
        myfile = 'index.html'

    try:
        file = open(myfile, 'rb')
        response = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'

        if (myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif (myfile.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode(
            'utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()