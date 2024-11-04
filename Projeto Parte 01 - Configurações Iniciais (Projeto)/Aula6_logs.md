***LOGS***

**Dev: Letícia Lima** 

O pacote **`django-requestlogs`** permite a gravação de logs de requisições HTTP em um banco de dados. Isso pode ser útil para análise de desempenho e solução de problemas. O pacote também fornece uma interface web para visualização dos logs.

**Precisamos Instalar essa biblioteca.**

**Documentação: https://pypi.org/project/django-requestlogs/**

**`pip install django-requestlogs`**

Adicionar no ***core/settings.py***

```
MIDDLEWARE = [ 
    'requestlogs.middleware.RequestLogsMiddleware',
]
```

```
REST_FRAMEWORK={ 
    'EXCEPTION_HANDLER': 'requestlogs.views.exception_handler',
}
```

Documentação: https://docs.djangoproject.com/en/4.1/topics/logging/#topic-logging-parts-loggers

```python
# Configuração padrão de Logs 
LOGGING = { # update 03/11/2024 
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'requestlogs_to_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'info.log',
            'when': 'midnight',  # Rotaciona a cada meia-noite
            'backupCount': 7,  # Mantém logs dos últimos 7 dias
            'formatter': 'verbose',  # Configuração de formatação
        },
    },
    'loggers': {
        'requestlogs': {
            'handlers': ['requestlogs_to_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
}

REQUESTLOGS = {
    'SECRETS': ['password', 'token'],
    'METHODS': ('PUT', 'PATCH', 'POST', 'DELETE'),
}
```

No primeiro bloco de código, **`LOGGING`**, estão sendo definidos os parâmetros do logger de informações para as requisições, que será gravado em um arquivo chamado **`info.log`**.

No segundo bloco, **`REQUESTLOGS`**, estão sendo definidas as opções de gravação de logs para as requisições, **como as informações que devem ser ocultadas e quais métodos HTTP devem ser registrados**. exemplo senhas, token de cliente/sistema.

update 03/11/2024

No Django (e no Python em geral), os níveis de log disponíveis são:

1. **DEBUG**: Para informações detalhadas, geralmente usadas para depuração. Esse nível inclui praticamente tudo.
2. **INFO**: Para informações gerais sobre o funcionamento normal do sistema. Esse nível é bom para acompanhar operações comuns, sem muitos detalhes.
3. **WARNING**: Para situações incomuns que não são erros, mas podem exigir atenção.
4. **ERROR**: Para erros que impedem uma operação específica, mas não interrompem o sistema como um todo.
5. **CRITICAL**: Para erros graves que podem exigir intervenção imediata.

No seu caso, com `level: 'INFO'`, o sistema registrará mensagens de `INFO`, `WARNING`, `ERROR` e `CRITICAL`.

Se você quer menos logs, use `WARNING` ou superior; se quer mais detalhes, use `DEBUG`.

Quando precisamos gerar log em alguma rota, script qualquer função em expecifico podemos chamar essa biblioteca logger e receber as informações no arquivo de .log que configuramos.

Por exemplo. Na view podemos fazer um tratamento assim, cria uma Exception para tratar os erros e enviar para nosso arquivo de log.

```python
import logging

error_logger = logging.getLogger()

def sendmail(data):
    ...

...
    try:
        data = response.data
        sendmail(data)
    except Exception as e: 
        error_logger.error(str(e) + "|" + str(data))
...
```

update 03/11/2024 

---

### Testando

Vamos fazer uma configuração simples para verificar se o logger está funcionando:

1. **arquivo urls.py** no seu projeto Django:
    
    ```python
    # No arquivo views.py do seu app Django
    import logging
    from django.http import JsonResponse
    
    # Obtenha o logger configurado
    logger = logging.getLogger('requestlogs')
    
    def test_logging_view(request):
        try:
            data = {'user': 'leticia', 'email': 'leticia@contato.com'}
            # Força um erro proposital para testar o log
            raise ValueError("Erro simulado no envio de email")
        except Exception as e:
            # Loga o erro usando o logger configurado
            logger.error(f"{str(e)} | {str(data)}")
            return JsonResponse({"status": "error", "message": "Ocorreu um erro."})
    
    ```
    
2. **Mapeie a função para uma URL** no arquivo `urls.py` do projeto:
    
    ```python
    from django.urls import path 
    
    urlpatterns = [
        path('test-logging/', test_logging_view, name='test_logging'),
    ]
    
    ```
    
3. **Acesse a URL** no navegador ou com uma ferramenta como `curl`:
    
    ```
    <http://localhost:8000/test-logging/
    
    ```
    

### Resultado Esperado

Após acessar a URL, o erro simulado deve ser registrado no `info.log`, com uma saída semelhante a esta:

```
2024-11-03 12:34:56 ERROR Erro simulado no envio de email | {'user': 'leticia', 'email': 'leticia@example.com'}

```

Esse teste confirma que o logger está funcionando no contexto do Django e que erros estão sendo registrados no arquivo de log.

---

Outro detalhe, em produção o arquivo **info.log quando voce criar ele no linux precisa ter permissões.**

```python
sudo chmod -R 777 path/info.log
```