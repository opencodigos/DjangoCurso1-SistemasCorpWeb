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
ENV APP_HOST=sistemacorp
# Porta da minha aplicação
ENV APP_PORT=9000

# Entro com usuário root
USER root

# Rodo o comando para criar pastas de volume,
# criar um arquivo de configuração do nginx
# aplicar as permissões necessarias para escrever no arquivo
RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

# um volume para armazenar os arquivos static se precisar
VOLUME /vol/static 

# Muda para usuário do nginx
USER nginx 

# executado quando o contêiner é iniciado.
CMD ["/run.sh"]