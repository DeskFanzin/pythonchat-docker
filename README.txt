trabalho feito por: Arthur Bubolz - 140548 e Gabriel Martins - 142356

Chat feito em Flask-socketIO, gunicorn, nginx e docker.

COMO FUNCIONA?
    Este trabalho consiste em um chat que permite a comunicação entre usuários, de maneira simples.
    Quando o usuário entra no servidor, ele pode colocar um nome como login e entrar no chat.
    Ao entrar no chat, o usuário pode enviar mensagens para todos os outros usuários que estão logados.

COMO RODAR?
    Para rodar o chat, é necessário ter o docker instalado.
    Após isso, basta rodar o comando:
        docker-compose up --build --scale app=2
    O chat estará rodando na porta 80 do localhost e do ip da máquina na rede local.
    Para parar, basta rodar o comando:
        docker-compose down

COMO FUNCIONA, DE MANEIRA TECNICA?
    O chat é feito em Flask-socketIO, que é um framework que permite a comunicação entre o servidor e o cliente.
    O aplicativo é feito em Flask, que é um framework de python para web.
    Este é rodado em gunicorn, que é um servidor http para python.
    Um servidor é rodado em nginx, que é um servidor http que fará o proxy reverso com o servidor WSGI, aberto pelo gunicorn.
    O servidor é rodado em docker, que é um container, de certo modo uma virtual machine, para rodar aplicações.
    E este é rodado em docker-compose, que é uma ferramenta para rodar vários containers ao mesmo tempo.
    O servidor é rodado em 2 containers, para que seja possível a replicação, ou seja, se um dos servidores cair, o outro continua funcionando.
