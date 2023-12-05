# ProjetoChatRedes
Projeto de Redes I 2023.2

# Servidor : 

O script servidor.py é a espinha dorsal do sistema de chat, proporcionando uma plataforma robusta para a comunicação entre clientes. Utilizando a biblioteca de sockets e threads em Python, o servidor gerencia conexões simultâneas, salas de chat e operações administrativas.

## 1. Funcionalidades Principais:

* Salas de Chat: O servidor suporta a criação dinâmica de salas, permitindo que usuários ingressem em espaços específicos para interagir entre si.

* Comandos Administrativos: Um administrador, identificado pelo apelido "admin", pode executar comandos especiais como kick e ban para moderar o ambiente de chat. Isso adiciona uma camada de segurança e controle sobre a comunidade.

* Proteção contra Palavras Proibidas: O servidor é equipado com um mecanismo que detecta e impede a utilização de palavras proibidas. Se um cliente tentar enviar uma mensagem contendo a palavra "flamengo", o servidor envia uma notificação indicando a proibição.

* Persistência de Dados: O servidor mantém uma lista de apelidos dos clientes e suas respectivas salas, além de registrar usuários banidos em um arquivo "lista-ban.txt" para garantir consistência entre sessões.

## 2. Fluxo de Execução:

* Inicialização: O servidor é iniciado, aguardando conexões de clientes na porta especificada (por exemplo, 50000).

* Conexões e Salas: Quando um cliente se conecta, fornece um apelido e escolhe uma sala, o servidor o adiciona à lista de clientes na sala correspondente.

* Administração: Se o apelido fornecido for "admin", o servidor solicita uma senha para autenticação. Com sucesso, o administrador pode executar comandos especiais.

* Comunicação: O servidor gerencia a troca de mensagens entre clientes na mesma sala, aplicando verificações e restrições, como a proibição da palavra "flamengo".

* Encerramento: Se um cliente desconectar ou for expulso, o servidor atualiza suas listas e notifica os demais participantes.

# Cliente :

O script cliente.py representa a interface do usuário para interagir com o sistema de chat. Ele permite que usuários escolham um apelido, entrem em uma sala e participem de conversas em tempo real.

1. Funcionalidades Principais:

* Conexão ao Servidor: O cliente inicia estabelecendo uma conexão com o servidor, fornecendo um apelido e escolhendo uma sala para participar.

* Receber e Enviar Mensagens: O cliente mantém duas threads independentes para receber mensagens do servidor e enviar suas próprias mensagens. Isso garante uma interação contínua e simultânea.

* Controle de Comandos: O cliente pode enviar comandos especiais, como "/kick" e "/ban" se tiver privilégios de administrador, garantindo uma participação ativa na moderação do chat.

* Notificações: Se o servidor detectar a palavra proibida "flamengo" em uma mensagem, o cliente recebe uma notificação indicando que a palavra é proibida.

* Encerramento Consciente: O cliente pode desconectar-se do chat de maneira controlada, encerrando a comunicação e liberando recursos.

* Esses scripts combinados criam um ambiente interativo e dinâmico de chat, promovendo a comunicação eficaz entre os usuários, enquanto o servidor implementa medidas de segurança e administração para manter a ordem no sistema.
