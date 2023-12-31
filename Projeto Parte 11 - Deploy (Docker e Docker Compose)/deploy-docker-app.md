**Configuração para Deploy**

- **Configuração do Nginx**
    
    Nginx vai servir nossa aplicação e arquivos estáticos.
    
    Como estamos trabalhando com docker vamos criar uma imagem do Nginx para usar em conjunto com nossos outros serviços da aplicação.
    
    https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html
    
    **Adicionar no arquivo requirements.txt**
    
    ```python
    uWSGI>=2.0.22,<3.0
    ```
    
    **Cria uma pasta “proxy”**
    
    **default.conf.tpl**
    
    Configuração do Nginx usando o **template engine** **`envsubst`**:
    
    - Escuta a porta especificada.
    - Define uma rota para arquivos estáticos.
    - Direciona o tráfego para o servidor uWSGI especificado.
    
    ```python
    server {
        listen ${LISTEN_PORT};
    
        location /static {
            alias /vol/static;
        }
    
        location / {
            uwsgi_pass              ${APP_HOST}:${APP_PORT};
            include                 /etc/nginx/uwsgi_params;
            client_max_body_size    10M;
        }
    }
    ```
    
    **uwsgi_params**
    
    Arquivo que define parâmetros uWSGI utilizados na configuração do Nginx.
    
    ```python
    uwsgi_param QUERY_STRING $query_string;
    uwsgi_param REQUEST_METHOD $request_method;
    uwsgi_param CONTENT_TYPE $content_type;
    uwsgi_param CONTENT_LENGTH $content_length;
    uwsgi_param REQUEST_URI $request_uri;
    uwsgi_param PATH_INFO $document_uri;
    uwsgi_param DOCUMENT_ROOT $document_root;
    uwsgi_param SERVER_PROTOCOL $server_protocol;
    uwsgi_param REMOTE_ADDR $remote_addr;
    uwsgi_param REMOTE_PORT $remote_port;
    uwsgi_param SERVER_ADDR $server_addr;
    uwsgi_param SERVER_PORT $server_port;
    uwsgi_param SERVER_NAME $server_name;
    ```
    
    Dentro dela vamos criar nosso arquivo Dockerfile
    
    ```python
    FROM nginxinc/nginx-unprivileged:1-alpine
    LABEL maintainer="Ngnix"
    
    # Copia arquivos necessarios para o container
    COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
    COPY ./uwsgi_params /etc/nginx/uwsgi_params
    COPY ./run.sh /run.sh
    
    # Crio 3 variais de ambiente para usar depois
    #  configurar a porta na qual o serviço dentro do contêiner estará na conexões.
    ENV LISTEN_PORT=8000
    # Essa variável pode ser utilizada para configurar o host (endereço)
    ENV APP_HOST= host
    # Porta da minha aplicação
    ENV APP_PORT=9000
    
    USER root # Entro com usuário root
    
    # Rodo o comando para criar pastas de volume,
    # criar um arquivo de configuração do nginx
    # aplicar as permissões necessarias para escrever no arquivo
    RUN mkdir -p /vol/static && \
        chmod 755 /vol/static && \
        touch /etc/nginx/conf.d/default.conf && \
        chown nginx:nginx /etc/nginx/conf.d/default.conf && \
        chmod +x /run.sh
    
    VOLUME /vol/static # um volume para armazenar os arquivos static se precisar
    
    USER nginx # Muda para usuário do nginx
    
    # executado quando o contêiner é iniciado.
    CMD ["/run.sh"]
    ```
    
    **run.sh**
    
    ```python
    #!/bin/sh
    
    set -e
    
    # Printa as variaveis para ver o valor delas se está passando
    echo "LISTEN_PORT=${LISTEN_PORT}"
    echo "APP_HOST=${APP_HOST}"
    echo "APP_PORT=${APP_PORT}"
    
    # envsubst É uma ferramenta que substitui variáveis de ambiente em arquivos de texto
    envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
    
    # nginx  Inicia o servidor web Nginx.
    # -g 'daemon off;' Configura o Nginx para não rodar como um daemon (em primeiro plano)
    nginx -g 'daemon off;'
    ```
    
    Em resumo, essa linha está substituindo dinamicamente as variáveis de ambiente definidas no Dockerfile no arquivo de configuração **`default.conf.tpl`** e gerando o arquivo final **`default.conf`** que será utilizado pelo Nginx.
    
- **Docker Compose Produção**
    
    Vamos criar um arquivo docker-compose para usar no servidor de produção. Nesse arquivo vamos ter 3 serviços, multplocontainer trabalhando em conjunto para servir nossa aplicação. 
    
    - **Aplicação Django**
    - **Banco de dados**
    - **Nginx**
    
    Copia o arquivo docker-compose.yml —> docker-compose-deploy.yml
    
    ```python
    version: '3.9'
    
    services:
      sistemacorp:
        build:
          context: .
        command: >
          sh -c "echo 'Sistema Corporativo' && run.sh"
        restart: always
        volumes:
          - static-data:/vol/web
          - media-data:/vol/web/media
          - ./SistemaCorp:/SistemaCorp 
        env_file:
          - sistema.env
        environment:
          - SECRET_KEY=${SECRET_KEY}
          - DEBUG=${DEBUG}
          - POSTGRES_HOST=${POSTGRES_HOST}
          - POSTGRES_DB=${POSTGRES_DB}
          - POSTGRES_USER=${POSTGRES_USER}
          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
        depends_on:
          - db
    
      db:
        image: postgres:13-alpine
        restart: always
        volumes:
          - postgres-data:/var/lib/postgresql/data
        env_file:
          - sistema.env
        environment:
          - POSTGRES_DB=${POSTGRES_DB}
          - POSTGRES_USER=${POSTGRES_USER}
          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    
      proxy:
        build:
          context: ./proxy
        restart: always
        depends_on:
          - sistemacorp
        ports:
          - 80:8000
        volumes:
          - static-data:/vol/static
    
    volumes:
      postgres-data:
      static-data:
      media-data:
    ```
    
    1. **`version: '3.9'`**: Define a versão do formato do arquivo Docker Compose. Neste caso, é a versão 3.9.
    2. **`sistemacorp`**: Configuração do serviço para a aplicação chamada "sistemacorp".
        - **`build`**: Configuração para construir a imagem do Docker a partir do contexto atual (**`.`**).
        - **`command`**: Define o comando a ser executado quando o contêiner é iniciado. Aqui, ele imprime "codeDjango" e executa o script **`run.sh`**.
        - **`restart: always`**: Indica que o contêiner deve ser reiniciado sempre que parar ou falhar.
        - **`volumes`**: Monta volumes para arquivos estáticos, arquivos de mídia e um diretório local chamado "SistemaCorp".
        - **`env_file`**: Especifica o arquivo que contém variáveis de ambiente (no formato **`.env`**).
        - **`environment`**: Define variáveis de ambiente diretamente, incluindo aquelas provenientes do arquivo **`.env`**.
        - **`depends_on`**: Especifica que este serviço depende do serviço **`db`**.
    3. **`db`**: Configuração do serviço que usa a imagem oficial do PostgreSQL.
        - **`image`**: Especifica a imagem a ser usada (PostgreSQL versão 13 no Alpine Linux).
        - **`container_name`**: Nome do contêiner como "sistemacorppostgress".
        - **`volumes`**: Monta um volume para armazenar dados do PostgreSQL.
        - **`env_file`**: Especifica o arquivo que contém variáveis de ambiente para o PostgreSQL.
        - **`environment`**: Define variáveis de ambiente diretamente.
    4. **`proxy`**: Configuração do serviço para um proxy.
        - **`build`**: Configuração para construir a imagem do Docker a partir do contexto no diretório **`./proxy`**.
        - **`restart: always`**: Indica que o contêiner deve ser reiniciado sempre que parar ou falhar.
        - **`depends_on`**: Especifica que este serviço depende do serviço **`sistemacorp`**.
        - **`ports`**: Mapeia a porta 80 do host para a porta 8000 do contêiner.
        - **`volumes`**: Monta um volume para arquivos estáticos.
    5. **`volumes`**: Define volumes para uso nos serviços.
        - **`postgres-data`**: Volume para armazenar dados do PostgreSQL.
        - **`static-data`**: Volume para arquivos estáticos.
        - **`media-data`**: Volume para arquivos de mídia.
    
    **Docker de produção** esse compose descreve a configuração para vários serviços (aplicação, banco de dados PostgreSQL, proxy) e suas interações, incluindo dependências e mapeamentos de portas. Ele é útil para orquestrar e gerenciar múltiplos contêineres como uma aplicação única.
    
    Importante:
    
    Estamos trabalhando com as credenciais reais. Então no seu arquivo _env vc renomeia para sisitema.env e altera as credenciais do  seu banco de dados.
    
- **Deploy no Servidor da DigitalOcean**
    
    Para fazer o deploy no servidor não tem secredo. Agora com Docker é muito mais simples. 
    
    Primeiro vamos criar nosso servidor e instalar a dependencia que é o docker. 
    
    ```python
    sudo apt update
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io
    sudo docker --version
    
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version
    ```
    
    Passamos o projeto para servidor temos que fazer alguns ajustes. 
    
    **_env —> sistema.env** e faz as modificações das credenciais. 
    
    **Passar a pasta media para o servidor.** Por que a pasta media a gente não manda no commit. 
    
    ```python
    scp -r SistemaCorp/media root@IP:/site_sistema/SistemaCorp/
    ```
    
    Por fim depois de tudo configurado a gente roda o up/build para subire construir os container.
    
    como temos o docker-compose-deploy.yml com todos os serviços, basta rodar o seguinte codigo.
    
    ```python
    sudo docker-compose -f docker-compose-deploy.yml up -d --build
    ```
    
    **Depois a gente precisa carregar os dados do dicionario.** 
    
    > Importante: Em Produção a gente não inicia o loaddata junto com os serviços. Por que sobrescreve o banco de dados. A gente faz uma unica vez por meio desse codigo e mandei as configurações iniciais. Depois vai alimentando o banco de dados conforme a rotina de uso.
    > 
    
    ```python
    docker exec -it sistemacorp python -Xutf8 manage.py loaddata /scripts/sistema.fixture.json
    ```
    
    <aside>
    💡 Importante: 
    O arquivo docker-compose-deploy é arquivo de produção pois contem o nginx e configurações das portas do servidor.
    
    O arquivo docker-compose.yml é arquivo de dev/teste para rodar local.
    
    </aside>
    
    ## **Correções**
    
    **Arquivos Static e Media não carregam** 
    
    ```python
    server {
        listen ${LISTEN_PORT};
    
        location /static/ {
            alias /vol/web/static/;
        } 
        location / {
            uwsgi_pass              ${APP_HOST}:${APP_PORT};
            include                 /etc/nginx/uwsgi_params;
            client_max_body_size    10M;
        }
    }
    ```
    
    **O WhiteNoise é uma biblioteca do Django que permite servir arquivos estáticos diretamente através do servidor web em vez de depender de um servidor separado, como o Nginx. Aqui está um guia básico de como configurar o WhiteNoise:** https://whitenoise.readthedocs.io/en/latest/django.html
    
    settings.py
    
    ```python
    add no requirements: whitenoise
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    STATIC_ROOT = '/vol/web/static'
    MEDIA_ROOT = '/vol/web/media'
    ```
    
    urls.py
    
    ```python
    if settings.DEBUG:
        urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
    ```
    
    **Firewell ou proxy (Não acessa IP)**
    
    ```python
    sudo ufw enable
    sudo ufw allow 22 80 8000 9000
    ```
    
    Verifica o proxy do nginx se ta chamando a aplicação.