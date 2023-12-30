# Deploy Django + Postgres, Nginx e Gunicorn no Ubuntu 22.04

Dev: Letícia Lima

Como fazer Deploy e configurar o Django com Postgres, Nginx e Gunicorn no Ubuntu 22.04.

Referencia: [https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04#step-10-configure-nginx-to-proxy-pass-to-gunicorn](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04#step-10-configure-nginx-to-proxy-pass-to-gunicorn)

- **Plataforma de Hospedagem**
    
    Para fazer o deploy existe varias alternativas de servidores hoje em dia. 
    
    - **Serviços de Nuvem:** Plataformas como AWS (Amazon Web Services), Google Cloud Platform (GCP), Microsoft Azure, Heroku, DigitalOcean entre outras, oferecem opções de hospedagem para aplicativos Django.
    - **Servidores Dedicados ou VPS:** Se preferir mais controle, você pode optar por um servidor dedicado ou VPS (Virtual Private Server) e configurar o ambiente por conta própria.
    
    **Por costume vou utilizar a DigitalOcean.**  
    
    Crie uma conta: [DigitalOcean | Cloud Hosting for Builders](https://m.do.co/c/7b0eeb0b772c)
    
    Inicialmente voce pode criar uma conta gratuitamente e utilizar. No momento da criação da conta a digitalOcean vai pedir para confirmar a conta com algum cartão de credito ou pelo paypal.
    
     ![image](https://github.com/djangomy/DjangoCurso1-SistemasCorpWeb/assets/58613583/f99f146c-47a1-4aff-8701-594519e7f155)

    Depois que ter criado o projeto precisamos criar nossa droplet para nossa aplicação Django.
    
    Vou criar um servidor com ubuntu 22.04, bem pequeno mesmo somente para configuração dessa aplicação.
    
     ![image](https://github.com/djangomy/DjangoCurso1-SistemasCorpWeb/assets/58613583/7f349aa2-8cee-4fa3-be09-664feb40270c)

    vamos conectar no nosso servidor, voce pode usar o SSH ou pode entrar no proprio console do digitalOcean.
    
    ```python
    ssh -l root IP
    
    password ***
    ```
    
    Bom pessoal Primeiro passo feito
    
- **Configuração do Ambiente**
    - **Instalação do Python e Dependências:** Certifique-se de que a versão correta do Python está instalada no servidor. Use ferramentas como **virtualenv** para criar ambientes virtuais e gerenciar dependências.
    - **Configuração do Banco de Dados:** Configure o banco de dados que sua aplicação Django utilizará. Exemplos incluem PostgreSQL, MySQL ou SQLite.
    
    **Instalar as dependências**
    
    **Ubuntu** já vem com python da uma verificada python3 --version.
    
    pode usar `sudo apt-get install python-is_python3`
    
    ```python
    sudo apt update
    sudo apt install python3-pip python3-venv python3-dev python-is-python3 libpq-dev postgresql postgresql-contrib nginx curl 
    ```
    
    **Configuração do Banco de Dados**
    
    Vou usar o PostgreSQL
    
    ```python
    sudo -u postgres psql
     
    CREATE DATABASE sistema;
    CREATE USER leticia WITH PASSWORD 'batatinha123';
    ALTER ROLE postgres SET client_encoding TO 'utf8';
    ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
    ALTER ROLE postgres SET timezone TO 'UTC'; 
    GRANT ALL PRIVILEGES ON DATABASE sistema TO leticia;
    \list
    \q
    ```
    
    **Vamos criar um ambiente virtual**
    
    ```python
    pwd 
    /root
    
    mkdir projects
    
    cd /projects/
    
    pip install virtualenv
    python -m venv "nome"
    
    mkdir .envs
    
    ls -la
    
    cd .envs
    
    virtualenv sistemaCorp 
    
    source sistemaCorp/bin/activate
    
    pip install django gunicorn psycopg2-binary
    ```
    
- **Gestão de Ambientes de Produção**
    - **Configuração do Ambiente de Produção:** Ajuste as configurações da sua aplicação para o ambiente de produção, incluindo a alteração do modo de depuração (**DEBUG**).
    - **Configuração de Variáveis de Ambiente:** Utilize variáveis de ambiente para armazenar informações sensíveis, como chaves secretas, senhas de banco de dados, etc.
    
    Modo DEBUG
    
    No arquivo de configurações do Django (normalmente **`settings.py`**), o modo de depuração (**DEBUG**) é frequentemente definido como **`True`** durante o desenvolvimento. No entanto, para ambientes de produção, é altamente recomendável definir **`DEBUG`** como **`False`**. Isso desativa mensagens detalhadas de erro para os usuários finais e melhora a segurança.
    
    Exemplo no arquivo **`settings.py`**:
    
    ```python
    DEBUG = False
    ```
    
    Vamos arrumar o ALLOWED_HOSTS
    
    ```python
    ALLOWED_HOSTS = ['seu_dominio.com', 'IP_do_servidor']
    
    alterar para:
    
    ALLOWED_HOSTS = []
    ALLOWED_HOSTS.extend(
        filter(
            None,
            os.environ.get('ALLOWED_HOSTS', '').split(','),
        )
    )
    
    .env
    ALLOWED_HOSTS=localhost,127.0.0.1,67.205.156.70
    ```
    
    As variaveis de ambiente do postgres no nosso projeto Django.
    
    Mas antes um detalhe muito importante pra voce que tem dados no seu projeto. E precisse fazer a migração. Antes de configurar o postgres vamos trabalhar com Dumpdata e Loaddata.
    
    - **DumpData e LoadData**
        
        **NOTA:**
        1- os campos no banco de dados tem que estar existentes
        2- nao pode ter nenhum registro nas tabelas que seram importadas as informações.
        
        **Exemplo: Primeiro visualizar as informações**
        
        cursos é o aplicativo do django 
        
        ```jsx
        python manage.py dumpdata cursos > cursos.json
        ```
        
        **Faz backup completo da base oficial**
        
        ```jsx
        python manage.py dumpdata > ~/bkp.json
        
        ou
        
        # Excluir as permissões
        python manage.py dumpdata --exclude auth.permission > db.json
        
        Banco de dados completo
        python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
        ```
        
        **Excluir as permissões:** Este comando gera um arquivo **`db.json`** que contém todos os dados do seu banco de dados, exceto as informações relacionadas às permissões de usuários. As permissões geralmente estão associadas ao aplicativo de autenticação (**`auth`**), e este comando exclui essas permissões do backup.
        
        **Banco de dados completo, excluindo permissões e tipos de conteúdo:**
        
        Este comando gera um arquivo **`db.json`** que contém todos os dados do seu banco de dados, excluindo as informações sobre permissões de usuários (**`auth.permission`**) e tipos de conteúdo (**`contenttypes`**). O modelo de dados padrão do Django inclui a tabela **`contenttypes`**, que é usada para armazenar informações sobre os modelos existentes no sistema.
        
        O propósito de excluir permissões e tipos de conteúdo pode ser útil em cenários de migração de dados, backup/restauração seletiva ou outras situações em que você deseja ter mais controle sobre quais dados estão incluídos ou excluídos do backup. Isso permite uma flexibilidade maior ao manipular dados do banco de dados usando o **`dumpdata`**.
        
        **Depois loaddata**
        
        pega o arquivo .json extraido cursos.json
        
        ```jsx
        python manage.py loaddata --app cursos cursos.json
        ```
        
        Banco inteiro
        
        ```python
        python manage.py loaddata db.json
        ```
        
        **Caso de Erros possiveis soluções que vai resolver.**
        
        Faça o Dumpdata com definição no inicio para tratar encoding. que vai funcionar. Depois usa o loaddata no nosso banco de dados normalmente.
        
        ```python
        python -Xutf8 ./manage.py dumpdata > data.json
        
        PYTHONIOENCODING=utf-8 python manage.py dumpdata --exclude auth.permission \
        	--exclude contenttypes > db.json
        ```
        
    
    Feito o Dumpdata agora vamos configurar o banco de dados no nosso projeto. Por que agora é Postgres.
    
    Aqui está um exemplo:
    
    ```python
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE'),
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
    ```
    
    No seu arquivo .env voce faz essa configuração.
    
    ```python
    DB_ENGINE=django.db.backends.postgresql_psycopg2
    DB_NAME=sistema
    DB_USER=leticia
    DB_PASSWORD=batatinha123
    DB_HOST=localhost
    DB_PORT='5432'
    ```
    
    Lembrando essas configurações de banco são importante e nao deve ir para commit. A versão commit pode deixar assim para usuario entender. arquivo _env. 
    
    ```python
    DB_ENGINE=django.db.backends.postgresql_psycopg2
    DB_NAME='nome_do_seu_banco'
    DB_USER='nome_do_seu_usuario'
    DB_PASSWORD='sua_senha'
    DB_HOST='localhost'
    DB_PORT='5432'
    ```
    
    - **Gestão de Mídia e Arquivos Estáticos**
        - **Configuração de Servidores de Mídia:** Se sua aplicação lida com uploads de arquivos, configure servidores de mídia (por exemplo, Amazon S3) para armazenar esses arquivos.
        - **Configuração de Arquivos Estáticos:** Configure o servidor web ou use serviços como Whitenoise para lidar com arquivos estáticos em produção.
        
        No inicio do curso já tinhamos feito essas configurações. Mas vamos dar uma olhada se está ok. São as configurações dos arquivos static do projeto. Muito importante.
        
        ```python
        STATIC_ROOT = os.path.join(BASE_DIR,'static')
        STATIC_URL = '/static/' 
        
        # STATICFILES_DIRS = [ # talvez em Produção podesse usar assim.
        #     BASE_DIR / 'static',
        # ]
        
        MEDIA_ROOT=os.path.join(BASE_DIR,'media')
        MEDIA_URL = '/media/'
        ```
        
        Vou testar isso no servidor mesmo. Estou usando windows não vou perder tempo configurando o postgres no windows. Outro video faço isso.  
        
        <aside>
        💡 Importante: Se voce fez o dumpdata e tem arquivos de media voce pode enviar esses arquivos ou adicionar depois manualmente.
        .gitignore
        
        remove “media” e manda.
        
        </aside>
        
    
- **Enviar o projeto para servidor**
    
    Clonar nosso projeto django. Se você criou um reposítorio como foi dito inicialmente do curso. Você deve ter um projeto no github. Isso facilita muito a trabalhar.
    
    vamos gerar um token no github.
    
    ```python
    token = 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
    git clone https://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@github.com/djangomy/site_sistema.git
    
    ou voce pode tentar com senha ou chave SSH.
    git clone https://github.com/djangomy/site_sistema.git
    
    git checkout Aula_deploy
    
    scp -r /media root@147.182.186.69:/root/projects/site_sistema
    ```
    
- **Rodar Projeto**
    
    Já podemos rodar o projeto e testar. 
    
    Faça o commit das alterações que fizemos. Deixe tudo meio pronto. E vamos passar para o servidor. 
    
    1 - Criar o arquivo .env
    
    ```python
    cp _env .env 
    ```
    
    2 - Fazer as Migrações
    
    ```python
    python manage.py makemigrations
    
    python manage.py migrate
    ```
    
    3 - Loaddata
    
    ```python
    python manage.py loaddata db.json
    ```
    
    testar 
    
    ```python
    python manage.py collectstatic 
    
    python manage.py runserver 0.0.0.0:8000
    ```
    
    Se precisar, Habilitar Firewall
    
    ```python
    sudo ufw enable
    
    sudo ufw allow 22
    sudo ufw allow 8000
    ```
    
- **Configuração do Servidor Web**
    
    pode desativar virtualenv
    
    ```python
    deactivate
    ```
    
    - **Servidor WSGI:** Utilize um servidor WSGI (Web Server Gateway Interface) como Gunicorn ou uWSGI para servir sua aplicação Django.
    - **Configuração do Nginx ou Apache:** Configure um servidor web reverso como Nginx ou Apache para lidar com solicitações HTTP e encaminhá-las para o servidor WSGI.
    
    **Configuração do Gunicorn usando Socket:**
    
    ```python
    sudo nano /etc/systemd/system/gunicorn.socket
    ```
    
    Dentro do arquivo **`site_sistema.socket`**, ajuste o conteúdo:
    
    ```python
    [Unit]
    Description=gunicorn socket
    
    [Socket]
    ListenStream=/root/projects/site_sistema/gunicorn.sock
    
    [Install]
    WantedBy=sockets.target
    ```
    
    **Cria Serviço para Gunicorn**
    
    ```python
    sudo nano /etc/systemd/system/gunicorn.service
    ```
    
    ```python
    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target
    
    [Service]
    User=root
    Group=www-data
    WorkingDirectory=/root/projects/site_sistema
    ExecStart=/root/projects/.envs/sistemaCorp/bin/gunicorn \
              --access-logfile - \
              --workers 3 \
              --bind unix:/root/projects/site_sistema/gunicorn.sock \
              core.wsgi:application
    ```
    
    **Recarregar o daemon do systemd após criar o arquivo de serviço:**
    
    ```python
    sudo systemctl start gunicorn.socket
    
    # habilite-o para o systemd inicie automaticamente
    sudo systemctl enable gunicorn.socket
    
    sudo systemctl status gunicorn.socket
    ```
    
    ```python
    # verifique a existência na pasta do projeto que configuramos
    
    file /root/projects/site_sistema/gunicorn.sock
    ```
    
    ```python
    # Status do Gunicorn
    sudo systemctl status gunicorn
    ```
    
    Logs
    
    ```python
    sudo journalctl -u gunicorn
    ```
    
    Se você fizer alterações no `/etc/systemd/system/gunicorn.service`arquivo, recarregue o daemon
    
    ```python
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn
    ```
    
    **Permissões** 
    
    ```python
    sudo chmod +x /root /root/projects /root/projects/site_sistema
    sudo chown www-data:www-data /root/projects/site_sistema/gunicorn.sock
    sudo chmod 660 /root/projects/site_sistema/gunicorn.sock
    ```
    
    **Pode testar** 
    
    ```python
    gunicorn --workers 3 --bind unix:/root/projects/site_sistema/gunicorn.sock core.wsgi:application
    ```
    
    **Configuração do Nginx**
    
    ```python
    sudo nano /etc/nginx/sites-available/site_sistema
    ```
    
    ```python
    server {
        listen 80;
        server_name 67.205.156.70;
    
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /root/projects/site_sistema;
        }
    
        location / {
            include proxy_params;
            proxy_pass http://unix:/root/projects/site_sistema/gunicorn.sock;
        }
    }
    ```
    
    Em seguida, crie um link simbólico para ativar o site no Nginx:
    
    ```python
    sudo ln -s /etc/nginx/sites-available/site_sistema /etc/nginx/sites-enabled
    sudo nginx -t
    sudo service nginx restart
    ```
    
    Depois que configura o nginx a gente pode remover a porta 8000 e liberar as configurações do e normal nas portas `80`e `443`— permitindo assim conexões HTTP e HTTPS, respectivamente.
    
    ```python
    sudo ufw delete allow 8000
    ```
    
    ```python
    sudo ufw allow 'Nginx Full'
    ```
    
    Recarregue os serviços e reinicie o Nginx:
    
    ```python
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn.service
    sudo systemctl restart nginx
    ```
    
- **Artigo: Configuração de Domínio e SSL**
    - **Registro de Domínio:** Registre um domínio para sua aplicação.
    - **Configuração de SSL/TLS:** Configure um certificado SSL/TLS para garantir uma comunicação segura entre o cliente e o servidor.
    
    Domínio podemos conseguir comprando em algum host de sua preferencia. Eu gosto muito da goDaddy ou hostinger. Mas tem varios por ai. 
    
    O SSL é a mesma coisa. Quando compra o dominio é possivel vincular a um pacote com os certificados SSL/TLS.
    
    A configuração do certificado geralmente o host que você adqueriu o dominio e a compra do certificado, fornece a documentação de configurações. Mas pra adiantar vocês o certificado no nosso caso implementamos no servidor na configuração do nginx. 
    
    Exemplo:
    
    cria uma pasta cert e coloca os arquivos que você vai baixar do host no servidor e depois conecta ele com nosso server para reconhecer o certificado. 
    
    ```python
    server {
        listen 80;
        server_name seu_dominio.com www.seu_dominio.com;
    
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /caminho/para/seu/projeto;
        }
    
        location / {
            include proxy_params;
            proxy_pass http://localhost:8000;  # Deve corresponder à configuração do servidor WSGI
        }
    }
    
    # Adicione as configurações SSL/TLS abaixo
    server {
        listen 443 ssl;
        server_name seu_dominio.com www.seu_dominio.com;
    
        ssl_certificate /caminho/para/certificado/fullchain.pem;
        ssl_certificate_key /caminho/para/certificado/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384';
    
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /caminho/para/seu/projeto;
        }
    
        location / {
            include proxy_params;
            proxy_pass http://localhost:8000;  # Deve corresponder à configuração do servidor WSGI
        }
    }
    ```
    
    Ou
    
    **Obtenção de Certificado SSL/TLS:**
    
    - Você pode obter um certificado SSL/TLS gratuito usando serviços como Let's Encrypt. Instale o cliente Certbot para Let's Encrypt:
    
    ```python
    sudo apt-get update
    sudo apt-get install certbot python3-certbot-nginx
    ```
    
    Execute o Certbot para obter e instalar automaticamente um certificado:
    
    ```python
    sudo certbot --nginx
    ```
    
    depois reinicia o nginx
    
    ```python
    sudo service nginx restart
    ```
    
    Eu não vou entrar muito em detalhes sobre isso. é que eu não comprei o certificado.
    
- **Artigo: Monitoramento e Logs**
    - **Configuração de Ferramentas de Monitoramento:** Use ferramentas como Prometheus, Grafana, ou serviços específicos da plataforma de hospedagem para monitorar o desempenho da sua aplicação.
    - **Configuração de Logs:** Configure registros adequados para ajudar na depuração e no monitoramento.
    
    ```python
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'requestlogs_to_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/var/logs/info.log',
            },
        },
        'loggers': {
            'requestlogs': {
                'handlers': ['requestlogs_to_file'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    ```
    
    Como usar:
    
    ```python
    import logging
    
    logger = logging.getLogger('requestlogs')
    
    def minha_view(request):
        # Alguma lógica da view
    
        # Exemplo de registro de log
        logger.info('Esta é uma mensagem de log informativa.')
    
        # Mais lógica da view
        return render(request, 'template.html')
    ```
    
    Substitua **`'Esta é uma mensagem de log informativa.'`** pela mensagem específica que você deseja registrar. O método **`info`** é usado para mensagens informativas, mas você também pode usar outros métodos de logging, como **`debug`**, **`warning`**, **`error`**, etc., dependendo do nível de severidade da mensagem.
    
    ```python
    sudo tail -F /var/logs/info.log
    ```
    
- **Artigo: Backup e Recuperação**
    - **Rotinas de Backup:** Implemente rotinas regulares de backup para garantir a segurança dos dados.
    - **Procedimentos de Recuperação:** Tenha procedimentos de recuperação em caso de falhas.
    
    Bibliotecas para Django 
    
    **django-dbbackup**
    
    Para agendar tarefas automatizadas
    
    **Celery e Celery Beat**
    
    Em breve entrarei com detalhes sobre isso. E conteudo que terei que estudar um pouco mais para trazer aqui. Vlw.
