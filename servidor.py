import socket
import threading

# Dicionário para mapear salas para suas respectivas listas de clientes
room_clients = {}

# Lista de apelidos dos clientes
apelidos = []

def broadcast(mensagem, sala):
    """Função que envia a mensagem para todos os clientes na mesma sala"""
    for cliente in room_clients[sala]:
        cliente.send(mensagem)

def handle(cliente, apelido, sala):
    while True:
        try:
            # Recebendo a mensagem do cliente
            msg = mensagem = cliente.recv(1024)

            # Verificando se a mensagem contém a palavra proibida "flamengo"
            if "flamengo" in msg.decode('utf-8').lower():
                # Enviando uma notificação ao cliente
                cliente.send('Não pode citar o time ruim aqui.'.encode('utf-8'))
            elif msg.decode('utf-8').startswith('KICK'):
                if apelido == 'admin':
                    nome_kick = msg.decode('utf-8')[5:]
                    kick_usuario(nome_kick)
                else:
                    cliente.send('Comando negado!'.encode('utf-8'))
            elif msg.decode('utf-8').startswith('BAN'):
                if apelido == 'admin':
                    nome_ban = msg.decode('utf-8')[4:]
                    kick_usuario(nome_ban)
                    with open('lista-ban.txt', 'a') as f:
                        f.write(f'{nome_ban}\n')
                    print(f'{nome_ban} foi banido!')
                else:
                    cliente.send('Comando negado!'.encode('utf-8'))
            else:
                # Enviando a mensagem para todos os clientes na mesma sala
                broadcast(mensagem, sala)
        except: 
            # Removendo e fechando o cliente
            if cliente in room_clients[sala]:
                room_clients[sala].remove(cliente)
                cliente.close()
                apelido = apelidos[room_clients[sala].index(cliente)]
                broadcast(f'{apelido} saiu do chat!'.encode('utf-8'), sala)
                apelidos.remove(apelido)
                break

def receber():
    while True:
        # Criando o socket
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Ligando o servidor ao host e a porta
        servidor.bind(('127.0.0.1', 50000))
        # Definindo o limite de conexões
        servidor.listen()

        # Aceitando a conexão do cliente
        cliente, endereco = servidor.accept()
        print(f'Conectado com {str(endereco)}')
        # Enviando a mensagem para o cliente
        cliente.send('NICK'.encode('utf-8'))
        # Recebendo o apelido e sala do cliente
        apelido_sala = cliente.recv(1024).decode('utf-8')
        apelido, sala = apelido_sala.split('@')

        with open('lista-ban.txt', 'r') as f:
            lista_ban = f.readlines()
        
        if apelido+'\n' in lista_ban:
            cliente.send('BAN'.encode('utf-8'))
            cliente.close()
            continue

        # Verificando se o apelido é de administrador
        if apelido == 'admin':
            cliente.send('PASS'.encode('utf-8'))
            senha = 'admin'
            # Verificando se a senha é correta
            if senha != 'admin':
                cliente.send('SENHA_ERRADA'.encode('utf-8'))
                cliente.close()
                continue

        # Adicionando o cliente na lista de clientes na mesma sala
        if sala not in room_clients:
            room_clients[sala] = []
        room_clients[sala].append(cliente)

        # Adicionando o apelido do cliente na lista de apelidos
        apelidos.append(apelido)

        print(f' {apelido} entrou na sala {sala}')
        # Enviando a mensagem de boas vindas para o cliente
        broadcast(f' {apelido} entrou no chat! '.encode('utf-8'), sala)
        # Enviando a mensagem para o cliente
        cliente.send('Conectado ao servidor! '.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(cliente, apelido, sala))
        thread.start()

def kick_usuario(nome):
    for sala, clientes_sala in room_clients.items():
        if nome in apelidos:
            nome_index = apelidos.index(nome)
            cliente_kick = clientes_sala[nome_index]
            clientes_sala.remove(cliente_kick)
            cliente_kick.send('Você foi expulso pelo admin!'.encode('utf-8'))
            cliente_kick.close()
            apelidos.remove(nome)
            broadcast(f'{nome} foi expulso pelo admin!'.encode('utf-8'), sala)

print('Servidor está ouvindo...')
receber()
