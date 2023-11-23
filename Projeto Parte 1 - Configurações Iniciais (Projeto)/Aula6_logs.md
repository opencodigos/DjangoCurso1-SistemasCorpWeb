***LOGS***

**Dev: Letícia Lima**

O pacote **`django-requestlogs`** permite a gravação de logs de requisições HTTP em um banco de dados. Isso pode ser útil para análise de desempenho e solução de problemas. O pacote também fornece uma interface web para visualização dos logs.

**Precisamos Instalar essa biblioteca.**

**Documentação: https://pypi.org/project/django-requestlogs/**

**`pip install django-requestlogs`**

Adicionar no ***core/settings.py***

```
MIDDLEWARE = [
    ...
    'requestlogs.middleware.RequestLogsMiddleware',
]
```

```
REST_FRAMEWORK={
    ...
    'EXCEPTION_HANDLER': 'requestlogs.views.exception_handler',
}
```

Documentação: https://docs.djangoproject.com/en/4.1/topics/logging/#topic-logging-parts-loggers

```python
# Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'requestlogs_to_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'info.log',
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

REQUESTLOGS = {
    'SECRETS': ['password', 'token'],
    'METHODS': ('PUT', 'PATCH', 'POST', 'DELETE'),
}
```

No primeiro bloco de código, **`LOGGING`**, estão sendo definidos os parâmetros do logger de informações para as requisições, que será gravado em um arquivo chamado **`info.log`**.

No segundo bloco, **`REQUESTLOGS`**, estão sendo definidas as opções de gravação de logs para as requisições, **como as informações que devem ser ocultadas e quais métodos HTTP devem ser registrados**. exemplo senhas, token de cliente/sistema.

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

Outro detalhe, em produção o arquivo **info.log quando voce criar ele no linux precisa ter permissões.**

```python
sudo chmod -R 777 path/info.log
```