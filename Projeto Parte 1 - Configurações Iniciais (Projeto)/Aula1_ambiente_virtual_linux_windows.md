***Ambiente Virtual Linux/Windows**

**Dev: Letícia Lima**

**Criar o ambiente virtual Linux/Windows**

```bash
## Windows
python -m venv .venv
source .venv/Scripts/activate # Ativar ambiente

## Linux 
## Caso não tenha virtualenv. "pip install virtualenv"
virtualenv .venv
source .venv/bin/activate # Ativar ambiente
```

**Instalar os seguintes pacotes Iniciais.**

```bash
pip install django
pip install pillow
```

**Para criar o arquivo *requirements.txt***

```bash
pip freeze > requirements.txt
```