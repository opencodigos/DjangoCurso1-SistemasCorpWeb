### ****Docker e Docker Compose ****

Como fazer Deploy e configurar o Django com Postgres, Nginx Docker e Docker compose.

https://www.digitalocean.com/community/tutorials/how-to-build-a-django-and-gunicorn-application-with-docker

Cria uma conta aqui: 

[DigitalOcean | Cloud Hosting for Builders](https://m.do.co/c/7b0eeb0b772c)

- **O que é Docker**
    
    **Docker:**
    
    `Docker` é uma plataforma de código aberto que permite automatizar o processo de desenvolvimento, implantação e execução de aplicativos em contêineres. 
    
    **`Contêineres`** são ambientes leves e isolados que encapsulam um aplicativo e suas dependências, garantindo consistência e facilitando a implantação em diferentes ambientes.
    
    **Exemplo:**
    
    Imagine que você está desenvolvendo um aplicativo web. Com Docker, você pode empacotar esse aplicativo, juntamente com todas as suas dependências (como bibliotecas, runtime, etc.), em um contêiner. Isso cria uma unidade portátil e consistente que pode ser executada em qualquer sistema que suporte o Docker, independentemente das diferenças de configuração entre sistemas operacionais ou ambientes de desenvolvimento
    
    ```bash
    # Exemplo de uso básico do Docker
    # Criar um contêiner a partir da imagem do Node.js
    docker run -it node:latest
    
    # Dentro do contêiner, você pode executar comandos do Node.js, como:
    node app.js
    ```
    
    **Exemplo 2: Utilizando Dockerfile. O que mais gosto de usar.** 
    
    **Um Dockerfile é um arquivo de configuração usado para construir uma imagem Docker.** Aqui está um exemplo simples de um Dockerfile para criar uma imagem que executa um servidor web Python usando o framework Flask:
    
    1. Crie um novo diretório para o seu projeto e navegue até ele:
    
    ```bash
    mkdir hello_docker
    cd hello_docker
    ```
    
    1. Crie um arquivo chamado **`app.py`** com o seguinte conteúdo:
    
    ```python
    from flask import Flask
    
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Olá, Docker!"
    
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
    
    ```
    
    1. Crie um arquivo chamado **`Dockerfile`** no mesmo diretório com o seguinte conteúdo:
        
        Geralmente usamos uma imagem do python. Teve casos que eu precisei configurar uma imagem do ubuntu por conta de versão de pacotes (bibliotecas) 
        
        Olha que legal nesse arquivo do Dockerfile a gente monta tudo para criar uma imagem. 
        
    
    ```
    # Use uma imagem base leve do Python
    FROM python:3.8-slim
    
    # Defina o diretório de trabalho no contêiner
    WORKDIR /app
    
    # Copie o arquivo de aplicativo para o diretório de trabalho
    COPY app.py .
    
    # Instale as dependências do Flask
    RUN pip install Flask
    
    # Exponha a porta 5000 para fora do contêiner
    EXPOSE 5000
    
    # Defina o comando padrão para executar o aplicativo quando o contêiner for iniciado
    CMD ["python", "app.py"]
    
    ```
    
    1. Agora, construa a imagem Docker usando o Dockerfile:
    
    ```bash
    docker build -t "nome para seu container" .
    ```
    
    Este comando cria uma imagem chamada "nome para seu container" com base nas instruções do Dockerfile.
    
    1. Por fim, execute um contêiner usando a imagem recém-criada:
    
    ```bash
    docker run -p 5000:5000 "nome para seu container"
    ```
    
- **Docker e Docker Compose**
    
    **Docker Compose** é uma ferramenta que permite definir e executar aplicativos **Docker multicontêiner em um único arquivo**, facilitando a orquestração de vários contêineres que trabalham em conjunto.
    
    **Exemplo:**
    
    Suponha que seu aplicativo web dependa de um banco de dados e um servidor web. Com o Docker Compose, você pode definir esses serviços em um arquivo chamado **`docker-compose.yml`**.
    
    ```yaml
    # Exemplo de docker-compose.yml
    version: '3.9'
    services:
      web: # Meu app
        image: nginx:latest
        ports:
          - "8080:80"
      database: # Banco de dados
        image: postgres:latest
        environment:
          POSTGRES_PASSWORD: mysecretpassword
    
    ```
    
    Este arquivo descreve dois serviços: um contêiner com o servidor web Nginx e outro com um banco de dados PostgreSQL. O Docker Compose simplifica a execução desses serviços juntos.
    
    ```bash
    # Usando Docker Compose para iniciar os serviços
    docker-compose up
    ```
    
    Isso inicia ambos os contêineres de acordo com a configuração definida no arquivo **`docker-compose.yml`**.
    
    1. **Docker:**
        - O Docker é uma plataforma que permite criar, distribuir e executar aplicativos em contêineres.
        - Contêineres são ambientes leves e isolados que encapsulam um aplicativo e suas dependências, garantindo consistência em diferentes ambientes.
        - Docker pode referir-se tanto à plataforma como um todo quanto ao software que você instala em seu sistema operacional para criar e gerenciar contêineres.
    2. **Docker Compose:**
        - Docker Compose é uma ferramenta que permite definir e gerenciar aplicativos Docker multicontêiner usando um arquivo de configuração YAML.
        - Ele simplifica a orquestração de vários contêineres que precisam trabalhar em conjunto.
        - O arquivo **`docker-compose.yml`** define serviços, redes e volumes, permitindo que você especifique toda a configuração de seu aplicativo em um único arquivo.
    
    Resumindo, o Docker refere-se à plataforma de contêineres e ao software para criar e gerenciar contêineres. O Docker Compose é uma ferramenta para orquestrar vários contêineres, permitindo definir a configuração de um aplicativo multicontêiner em um único arquivo. A imagem Docker, por sua vez, é um artefato que contém um sistema de arquivos com o aplicativo e suas dependências, e pode ser usado para criar contêineres.
    
- **Instalação do Docker e Docker Compose**
    
    Instalação do Docker para windows:
    
    https://docs.docker.com/desktop/install/windows-install/
    
    Acessa esse link e faça o download e instala normalmente. Esse Docker para windows contem todos os serviços do Docker e Docker compose que precisamos. 
    
    No Linux:
    
    https://docs.docker.com/engine/install/ubuntu/
    
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
    
- **Configuração do Projeto**
    - **DumpData e LoadData**
        - **DumpData:** Em programação, "dump" pode ser usado para descrever a ação de salvar o estado atual de um programa, objeto ou estrutura de dados para um arquivo ou outra forma de armazenamento persistente.
        - **LoadData:** Similarmente, "load" pode se referir à ação de carregar um estado previamente salvo de um programa, objeto ou estrutura de dados a partir de um arquivo ou outra fonte de armazenamento persistente.
        
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
        
        **O propósito de excluir permissões e tipos de conteúdo pode ser útil em cenários de migração de dados**, backup/restauração seletiva ou outras situações em que você deseja ter mais controle sobre quais dados estão incluídos ou excluídos do backup. Isso permite uma flexibilidade maior ao manipular dados do banco de dados usando o **`dumpdata`**.
        
        **Caso de Erros possiveis soluções que vai resolver.**
        
        Faça o Dumpdata com definição no inicio para tratar encoding. que vai funcionar. Depois usa o loaddata no nosso banco de dados normalmente.
        
        A linha **`PYTHONIOENCODING=utf-8` e `-Xutf8`** é um comando de ambiente em Python que define a codificação de caracteres para a entrada e saída padrão do Python.
        
        ```python
        python -Xutf8 ./manage.py dumpdata > data.json
        
        PYTHONIOENCODING=utf-8 python manage.py dumpdata --exclude auth.permission \
        	--exclude contenttypes > db.json
        ```
        
        **Depois loaddata**
        
        Banco inteiro
        
        ```python
        python manage.py loaddata db.json
        ```
        
    
    **Feito o Dumpdata agora vamos configurar o banco de dados no nosso projeto. Por que agora é Postgres.**
    
    Aqui está um exemplo:
    
    ```python
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('POSTGRES_ENGINE'),
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT'),
        }
    }
    ```
    
    Lembrando essas configurações de banco são importante e nao deve ir para commit. A versão commit pode deixar assim para usuario entender. arquivo _env. 
    
    ```python
    POSTGRES_ENGINE=django.db.backends.postgresql
    POSTGRES_DB="nome-db"
    POSTGRES_USER="nome-usuario"
    POSTGRES_PASSWORD="senha"
    POSTGRES_HOST="nome-host"
    POSTGRES_PORT=5432
    ```
    
    Preparar algumas **variavéis de ambiente.**
    
    Você pode preparar tudo que é importante para colocar no seu arquivo .env
    
    ```python
    SECRET_KEY = os.getenv('SECRET_KEY', 'changeme')
    
    DEBUG = bool(int(os.getenv('DEBUG', 0)))
    
    ALLOWED_HOSTS = []
    ALLOWED_HOSTS.extend(
        filter(
            None,
            os.getenv('ALLOWED_HOSTS', '').split(','),
        )
    )
    
    # CORS
    CORS_ALLOW_HEADERS = list(default_headers) + [
        'X-Register',
    ]
    
    # Configuração para permitir todas as origens no CORS (Cross-Origin Resource Sharing).
    # NÃO UTILIZE EM PRODUÇÃO se CORS_ORIGIN_ALLOW_ALL estiver definido como True.
    CORS_ORIGIN_ALLOW_ALL = os.getenv('CORS_ORIGIN_ALLOW_ALL')
    
    # Configuração para permitir credenciais no CORS (por exemplo, cookies).
    CORS_ALLOW_CREDENTIALS = os.getenv('CORS_ALLOW_CREDENTIALS')
    
    # Lista de origens confiáveis para CSRF (Cross-Site Request Forgery).
    CSRF_TRUSTED_ORIGINS = []
    CSRF_TRUSTED_ORIGINS.extend(
        filter(
            None,
            os.getenv('CSRF_TRUSTED_ORIGINS', '').split(','),
        )
    )
    
    # Lista de origens permitidas no CORS.
    CORS_ALLOWED_ORIGINS = []
    CORS_ALLOWED_ORIGINS.extend(
        filter(
            None,
            os.getenv('CORS_ALLOWED_ORIGINS', '').split(','),
        )
    )
    ```
    
    _env
    
    ```python
    SECRET_KEY=django-insecure-uwx*g5p#-%qb50y9rx8s97=%&8t-8qq89zqi94ao4h+x6vm%md
    
    ALLOWED_HOSTS=localhost,127.0.0.1
    
    CORS_ALLOWED_ORIGINS=https://seusite.com,http://seusite.com
    CORS_ORIGIN_ALLOW_ALL=True
    CORS_ALLOW_CREDENTIALS=False
    CSRF_TRUSTED_ORIGINS=''
    
    DEBUG=1
    SUPER_USER=ADMIN
    EMAIL=leticiateste@gmail.com
    
    POSTGRES_ENGINE=django.db.backends.postgresql
    POSTGRES_DB="nome-db"
    POSTGRES_USER="nome-usuario"
    POSTGRES_PASSWORD="senha"
    POSTGRES_HOST="nome-host"
    POSTGRES_PORT=5432
    
    EMAIL_HOST=smtp.office365.com
    EMAIL_HOST_USER=email@hotmail.com
    EMAIL_HOST_PASSWORD=sua_senha
    EMAIL_PORT=587 
    EMAIL_USE_TLS=True 
    DEFAULT_FROM_EMAIL=email@hotmail.com
    SERVER_EMAIL=DEFAULT_FROM_EMAIL
    ```
    
    - **Gestão de Mídia e Arquivos Estáticos**
        
        settings.py
        
        ```python
        **STATIC_URL = '/static/static/'
        MEDIA_URL = '/static/media/'
        
        MEDIA_ROOT = '/vol/web/media'
        STATIC_ROOT = '/vol/web/static'**
        ```
        
    
- **Organização da Estrutura de Pasta no Projeto**
    
    Organize o seu projeto Django de maneira que os arquivos estejam prontos para serem containerizados. Certifique-se de ter um **`Dockerfile`** na raiz do seu projeto.
    
    Cria uma pasta para colocar o projeto Django.
    
    Vou criar uma pasta chamada “SistemaCorp”
    
    **Arquivos da Pasta SistemaCorp**
    
    *apps*
    
    *core*
    
    *static*
    
    *media*
    
    *manage.py*
    
    **Arquivos na pasta Raiz**
    
    *Dockerfile*
    
    *docker-compose.yml*
    
    *.dockerignore*
    
    ```
    # Git
    .git
    .gitignore
    
    # Docker
    .docker
    
    # Python
    SistemaCorp/__pycache__/
    SistemaCorp/*/__pycache__/
    SistemaCorp/*/*/__pycache__/
    SistemaCorp/*/*/*/__pycache__/
    .env/
    .venv/
    venv/
    
    # Local PostgreSQL data
    data/
    /data
    ```
    
    *requirements.txt*
    
    *README.md*
    
    *_env*
    
    *.gitignore* 
    
    *.gitattributes* 
    
    ```python
    .html linguist-detectable=false
    ```
    
    Cria uma pasta “scripts” na raiz
    
    **Arquivos da pasta scripts**
    
    *db.json* —> sistema.fixture.json
    
- **Configuração do Dockerfile**
    
    ```python
    FROM python:3.9-alpine3.13 
    LABEL maintainer="Sistema Corporativo"
    
    ENV PYTHONUNBUFFERED 1
    
    COPY ./requirements.txt /requirements.txt
    COPY ./SistemaCorp /SistemaCorp
    COPY ./scripts /scripts
    
    WORKDIR /SistemaCorp
    EXPOSE 8000
    
    RUN apk add --update --no-cache postgresql-client git openssh-client
    
    RUN mkdir ~/.ssh/ && ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
    
    RUN apk add --no-cache su-exec
    
    RUN --mount=type=ssh python -m venv /py && \
        /py/bin/pip install --upgrade pip && \
        apk add --update --no-cache --virtual .tmp-deps \
            build-base postgresql-dev musl-dev linux-headers && \
        /py/bin/pip install -r /requirements.txt && \
        apk del .tmp-deps && \
        adduser --disabled-password --no-create-home app && \
        mkdir -p /vol/web/static && \
        mkdir -p /vol/web/media && \
        mkdir -p /logs && \
        chown -R app:app /vol && \
        chown -R app:app /vol/web && \
    		chown -R app:app /logs && \
        chmod -R 755 /vol && \
        chmod -R +x /scripts
    
    ENV PATH="/scripts:/py/bin:$PATH"
    
    # USER app
    
    CMD ["run.sh"]
    ```
    
    - **FROM python:3.9-alpine3.13:** Define a imagem base que será usada. Neste caso, é uma imagem leve do Alpine Linux com Python 3.9 instalado.
    - **LABEL maintainer="Sistema Corporativo"**: Adiciona uma etiqueta para identificar o mantenedor da imagem.
    - **ENV PYTHONUNBUFFERED 1:** Define uma variável de ambiente para garantir que a saída do Python seja exibida imediatamente (sem buffer).
    - **COPY ./requirements.txt /requirements.txt:** Copia o arquivo requirements.txt do diretório local para o diretório raiz (/) na imagem.
    - **COPY ./SistemaCorp /SistemaCorp:** Copia o conteúdo do diretório local ./SistemaCorp para o diretório /SistemaCorp na imagem.
    - **COPY ./scripts /scripts:** Copia o conteúdo do diretório local ./scripts para o diretório /scripts na imagem.
    - **WORKDIR /SistemaCorp:** Define o diretório de trabalho para /SistemaCorp.
    - **EXPOSE 8000:** Informa que o contêiner escuta na porta 8000.
    - **RUN apk add --update --no-cache postgresql-client git openssh-client:** Instala pacotes necessários usando o gerenciador de pacotes do Alpine Linux (apk).
    - **RUN mkdir ~/.ssh/ && ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts:** Cria um diretório ~/.ssh/ e adiciona a chave RSA do GitHub ao arquivo known_hosts.
    - **RUN apk add --no-cache su-exec:** Instala o pacote su-exec.
    - **RUN --mount=type=ssh python -m venv /py && ...:** Cria um ambiente virtual Python (/py) usando o módulo venv. Este comando usa o recurso --mount para montar as chaves SSH, permitindo o acesso privado a repositórios privados durante a construção da imagem.
    - **ENV PATH="/scripts:/py/bin:$PATH":** Adiciona o caminho /scripts e /py/bin ao PATH para que os scripts e binários do Python sejam encontrados.
    - **CMD ["run.sh"]:** Define o comando padrão que será executado quando o contêiner for iniciado. Neste caso, ele executa o script run.sh.
    
    run.sh
    
    ```python
    #!/bin/sh
    
    set -e -x
    
    echo "$@"
    
    chown -R app:app /vol && 
    chown -R app:app /vol/web && 
    
    ls -la /vol/
    ls -la /vol/web
    ls -la /scripts/
    
    su-exec app rundjango.sh
    ```
    
    - **`set -e -x`**: Configura o script para sair imediatamente se qualquer comando retornar um código de erro (**`e`**) e exibe cada comando à medida que é executado (**`x`**). Isso ajuda na depuração e no rastreamento de execução.
    - **`echo "$@"`**: Imprime todos os argumentos passados para o script. Isso é útil para depuração para ver quais argumentos foram fornecidos.
    - **`chown -R app:app /vol && chown -R app:app /vol/web`**: Muda o proprietário dos diretórios **`/vol`** e **`/vol/web`** para o usuário e grupo **`app`**. Isso é geralmente feito para garantir que o aplicativo em execução no contêiner tenha permissões de leitura e gravação nesses diretórios.
    - **`ls -la /vol/`**: Lista os arquivos e diretórios no diretório **`/vol/`**
    - **`ls -la /vol/web`**: Lista os arquivos e diretórios no diretório **`/vol/web`**.
    - **`ls -la /scripts/`**: Lista os arquivos e diretórios no diretório **`/scripts/`**.
    - **`su-exec app rundjango.sh`**: Usa o utilitário **`su-exec`** para executar o script **`rundjango.sh`** como o usuário **`app`**.
    - **`su-exec`** é uma alternativa ao **`su`** projetada para ser mais fácil de usar em ambientes de contêiner, pois evita a necessidade de iniciar um novo shell.
    
    rundjango.sh 
    
    ```bash
    #!/bin/sh
    
    set -e
    
    python manage.py collectstatic --noinput
    
    python manage.py migrate
    
    # inicia uwsgi (EM FOREGROUND, melhor para uso em docker)
    uwsgi --socket :9000 --workers 4 --master --enable-threads --module core.wsgi
    ```
    
    - **`set -e`**: Configura o script para sair imediatamente se qualquer comando retornar um código de erro. Isso é útil para garantir que o script pare de executar se algo der errado.
    - **`python manage.py collectstatic --noinput`**: Coleta arquivos estáticos do Django. Isso é necessário, por exemplo, ao implantar em produção para reunir todos os arquivos estáticos (CSS, JavaScript, etc.) em um local para facilitar o serviço por um servidor web.
    - **`python manage.py migrate`**: Aplica todas as migrações pendentes do Django ao banco de dados. As migrações são usadas para atualizar o esquema do banco de dados conforme o modelo de dados do aplicativo evolui.
    - **`uwsgi --socket :9000 --workers 4 --master --enable-threads --module core.wsgi`**: Inicia o servidor uWSGI para servir o aplicativo Django. Alguns parâmetros importantes:
        - **`-socket :9000`**: Define o socket no qual o uWSGI escuta as solicitações.
        - **`-workers 4`**: Especifica o número de processos de trabalho.
        - **`-master`**: Inicia o modo mestre do uWSGI, o que pode ser útil para gerenciar vários processos de trabalho.
        - **`-enable-threads`**: Ativa suporte a threads.
        - **`-module core.wsgi`**: Especifica o módulo WSGI que o uWSGI deve carregar para iniciar o aplicativo.
    - **WSGI e uWSGI**
        
        **`WSGI`** (Web Server Gateway Interface) e **`uWSGI`** são protocolos e servidores web que ajudam a facilitar a comunicação entre servidores web e aplicações web, especialmente aquelas escritas em linguagens de programação como Python.
        
        ### **WSGI (Web Server Gateway Interface):**
        
        O WSGI é uma especificação para a interface entre servidores web e aplicações Python. Ele define um contrato padrão que permite que servidores web e aplicações Python comuniquem-se de maneira eficiente. Com o WSGI, desenvolvedores podem escrever aplicações web em Python que podem ser executadas em diferentes servidores web compatíveis com WSGI sem a necessidade de modificar o código da aplicação.
        
        Alguns pontos-chave do WSGI:
        
        - **Padrão**: Define um padrão de interface entre servidores web e aplicações Python.
        - **Flexibilidade**: Permite que diferentes servidores web e frameworks Python se comuniquem de maneira uniforme.
        - **Modularidade**: Facilita a criação de aplicações web modulares e a escolha de servidores web compatíveis.
        
        ### **uWSGI:**
        
        O uWSGI, por outro lado, é um servidor de aplicação e um protocolo que implementa o WSGI. Ele é mais do que apenas um servidor WSGI; é um sistema extensível e modular que suporta diversos protocolos para se comunicar com as aplicações, incluindo WSGI.
        
        Alguns pontos-chave do uWSGI:
        
        - **Servidor de Aplicação**: Além de suportar WSGI, o uWSGI pode ser usado como um servidor de aplicação para executar várias linguagens de programação além do Python.
        - **Modularidade e Extensibilidade**: Oferece uma arquitetura modular que permite adicionar funcionalidades extras como cache, balanceamento de carga, entre outros.
        - **Eficiência e Desempenho**: Projetado para ser eficiente e escalável, sendo capaz de lidar com um grande número de solicitações simultâneas.
        - **Adoção Ampla**: Amplamente utilizado na comunidade Python para implantar aplicações web em produção.
        
        Em resumo, enquanto o WSGI é uma especificação para a interface entre servidores web e aplicações Python, o uWSGI é uma implementação específica dessa interface, além de ser um servidor de aplicação versátil. Muitas vezes, ambos os termos são mencionados juntos porque o uWSGI é frequentemente utilizado como servidor WSGI em ambientes Python.
        
    
    Um detalhes que gosto de adicionar no script rundjango.sh é uma chamada para wait_for_db
    
    que Espera db ficar disponível antes de continuar a iniciar o aplicativo. Isso é interessante por que na criação do Docker da imagem na configuração do Django, banco de dados podemos aguardar o carregamento ok.
    
    Atualiza rundjango.sh coloca em primeiro
    
    ```python
    #!/bin/sh
    
    set -e
    
    # Espera db disponível antes de continuar a iniciar o aplicativo
    python manage.py wait_for_db
    
    ...
    ```
    
    Cria um command script no projeto para ser executado.  
    
    Não consegui achar a referencia desse codigo. Mas peguei de alguma documentação de curso que eu fiz. 
    
    *apps/config/management/commands/wait_for_db.py*
    
    ```python
    import time
    import datetime  # Adicionado para usar o timeout
    
    from psycopg2 import OperationalError as Psycopg2OpError
    from django.db.utils import OperationalError
    from django.core.management.base import BaseCommand
    
    class Command(BaseCommand):
        """Django command to wait for the database."""
    
        def handle(self, *args, **options):
            """Entrypoint for the command."""
            self.stdout.write('Waiting for the database...')
            db_up = False
            max_attempts = 30  # Defina o número desejado de tentativas
            attempt_count = 0
    
            # Defina o tempo máximo desejado em segundos
            timeout_seconds = 60
            start_time = datetime.datetime.now()
    
            while not db_up and attempt_count < max_attempts and (
                    datetime.datetime.now() - start_time).seconds < timeout_seconds:
                try:
                    self.check(databases=['default'])
                    db_up = True
                except (Psycopg2OpError, OperationalError):
                    attempt_count += 1
                    self.stdout.write(f'Database unavailable, waiting 1 second... (Attempt {attempt_count})')
                    time.sleep(1)
    
            if db_up:
                self.stdout.write(self.style.SUCCESS('Database available!'))
            else:
                self.stdout.write(self.style.ERROR('Database did not become available within the specified timeout.'))
    ```
    
- **Configuração do Docker Compose**
    
    *docker-compose.yml*
    
    ```python
    version: '3.9' # Define a versão do formato do arquivo Docker Compose
    
    services:
      sistemacorp: # Nome da Aplicação
        build: # Configuração para construir a imagem do Docker
          context: .
        command: >
          sh -c "python manage.py wait_for_db &&
                python manage.py makemigrations &&
                python manage.py migrate &&
                python -Xutf8 manage.py loaddata /scripts/sistema.fixture.json &&
                python manage.py runserver 0.0.0.0:8000"
        ports:
          - 8000:8000 # Mapeia a porta 8000 do contêiner para a porta 8000 do host
        volumes: # Monta volumes incluindo arquivos estáticos e de mídia do Django.
          - ./data/web:/vol/web
          - ./SistemaCorp:/SistemaCorp
          - ./SistemaCorp/media:/vol/web/media
        env_file:
          - sistema.env # como usar o .env no docker-compose
        environment: # Define variáveis de ambiente diretamente
          - SECRET_KEY=devsecretkey
          - DEBUG=1
          - POSTGRES_HOST=db
          - POSTGRES_DB=devdb
          - POSTGRES_USER=devuser
          - POSTGRES_PASSWORD=changeme
        depends_on:
          - db
    
      db: # Usa a imagem oficial do PostgreSQL versão 13 no Alpine Linux
        image: postgres:13-alpine
        env_file:
          - sistema.env # como usar o .env no docker-compose
        environment:
          - POSTGRES_DB=devdb
          - POSTGRES_USER=devuser
          - POSTGRES_PASSWORD=changeme
    ```
    
    Esse arquivo **`docker-compose.yml`** é utilizado para definir a configuração dos serviços Docker para sua aplicação Django e banco de dados PostgreSQL. Ele simplifica o processo de execução e interconexão desses serviços.
    
- **Comandos Docker**
    
    
    Comandos basicos
    
    ```html
    docker compose up: cria e inicia os contêineres;
    docker compose build: realiza apenas a etapa de build das imagens que serão utilizadas;
    docker compose logs: visualiza os logs dos contêineres;
    docker compose restart: reinicia os contêineres;
    docker compose ps: lista os contêineres;
    docker compose scale: permite aumentar o número de réplicas de um contêiner;
    docker compose start: inicia os contêineres;
    docker compose stop: paralisa os contêineres;
    docker compose down: paralisa e remove todos os contêineres e seus componentes como rede, imagem e volume
    docker compose version Show the Docker Compose version information
    docker compose top	Display the running processes
    docker compose port	Print the public port for a port binding.
    ```
    
    **Limpeza de Caches e Artefatos Temporários:**
    
    - Execute o comando **`sudo docker system prune -a`** para remover contêineres parados, redes não utilizadas e imagens sem tags.
    - Isso liberará espaço no seu sistema Docker.
    
    **Remover Imagens**
    
    ```html
    docker images –a
    docker image rmi -f <image_id>
    docker images rmi -f <image_id> <image_id>
    ```
    
    **Remover Container**
    
    ```html
    docker container -a
    docker container rm -f <container ID>
    docker container rm -f <container ID> <container ID>
    ```
    
    **Remover Volumes**
    
    ```html
    docker volume ls
    docker volume rm -f <volume_name> <volume_name>
    ```
    
    **Limpar Redes Não Utilizadas (Opcional):**
    
    - Se desejar, você pode limpar redes Docker não utilizadas:
        
        ```bash
        sudo docker network prune
        ```
        
    
    Comandos
    
    ```python
    # Para e remove todos os contêineres e seus componentes como rede, imagem e volume
    sudo docker-compose down
    
    # Para todos os containers
    sudo docker stop $(sudo docker ps -a -q)
    
    # Remove todos os containers
    docker rm -f $(docker ps -aq)
    
    # Para remover contêineres parados, redes não utilizadas e imagens sem tags
    sudo docker system prune -a
    
    # remove todos os volumes
    docker volume rm $(docker volume ls -q)
    
    # Roda o build da imagem
    docker-compose build 
    
    # Cria e inicia os containers
    docker-compose up 
    
    # Inicia os containers serviços em segundo plano e faz o build da imagem
    docker-compose -f docker-compose.yml up -d --build
    
    # Ver logs do Container
    docker logs -f "Nome container"
    ```
    
- **Rodando a Aplicação**
    
    ```python
    # Inicia os containers serviços em segundo plano e faz o build da imagem
    docker-compose -f docker-compose.yml up -d --build
    ```
    
    Correção do Erro
    
    `CORS_ORIGIN_ALLOW_ALL=1
    CORS_ALLOW_CREDENTIALS=0`
    
    ```python
    CORS_ORIGIN_ALLOW_ALL = bool(int(os.getenv('CORS_ORIGIN_ALLOW_ALL', 0))) 
    CORS_ALLOW_CREDENTIALS = bool(int(os.getenv('CORS_ALLOW_CREDENTIALS', 0)))
    ```