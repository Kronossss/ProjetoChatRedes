import socket
import threading

# Definindo um apelido e sala
apelido = input('Escolha um apelido: ')
sala = input('Escolha uma sala: ')

# Conectando com o servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 50000))

# Enviando apelido e sala para o servidor
cliente.send(f'{apelido}@{sala}'.encode('utf-8'))

parar_thread = False

def receber():
    while True:
        global parar_thread
        if parar_thread:
            break
        try:
            # Recebendo a mensagem do servidor
            mensagem = cliente.recv(1024).decode('utf-8')
            if mensagem == 'NICK':
                # Enviando o apelido e sala para o servidor
                cliente.send(f'{apelido}@{sala}'.encode('utf-8'))
                proxima_mensagem = cliente.recv(1024).decode('utf-8')
                if proxima_mensagem == 'PASS':
                    senha = input('Senha de administrador: ')
                    cliente.send(senha.encode('utf-8'))
                    if cliente.recv(1024).decode('utf-8') == 'SENHA_ERRADA':
                        print('Senha incorreta! Desconectando...')
                        parar_thread = True
                elif proxima_mensagem == 'BAN':
                    print('Você está banido do servidor!')
                    cliente.close()
                    parar_thread = True
            else:
                print(mensagem)
        except:
            # Fechando a conexão
            print('Ocorreu um erro!')
            cliente.close()
            break

def escrever():
    while True:
        if parar_thread:
            break
        mensagem = f'{apelido}: {input("")}'
        if mensagem[len(apelido)+2:].startswith('/'):
            if apelido == 'admin':
                if mensagem[len(apelido)+2:].startswith('/kick'):
                    cliente.send(f'KICK {mensagem[len(apelido)+2+6:]}'.encode('utf-8'))
                elif mensagem[len(apelido)+2:].startswith('/ban'):
                    cliente.send(f'BAN {mensagem[len(apelido)+2+5:]}'.encode('utf-8'))
            else:
                print('Comando só pode ser executado por um admin!')
        else:
            cliente.send(mensagem.encode('utf-8'))

# Iniciando as threads
receber_thread = threading.Thread(target=receber)
receber_thread.start()

escrever_thread = threading.Thread(target=escrever)
escrever_thread.start()
