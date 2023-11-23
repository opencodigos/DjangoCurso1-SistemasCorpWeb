# **Autenticação Customizada**

Dev: Letícia Lima

Para implementar um modelo de autenticação com diferentes níveis de acesso, vamos utilizar as permissões de acesso do Django. Para isso, criaremos três tipos de usuário:

- **Administrador**
- **Colaborador**
- **Usuário**

Cada tipo de usuário terá um conjunto diferente de permissões que determinará quais partes do aplicativo ele poderá acessar.

Para gerenciar as permissões de acesso, vamos utilizar os grupos do Django. Isso nos permitirá associar um conjunto de permissões a cada tipo de usuário.

Em seguida, criaremos os grupos e associaremos as permissões a cada grupo, de acordo com o nível de acesso de cada tipo de usuário. Por exemplo, o grupo de administradores terá permissão para criar, editar e excluir usuários, enquanto o grupo de usuários terá apenas permissão para visualizar informações.

Por fim, vamos definir as visualizações que exigem autenticação e permissões específicas. Para isso, utilizaremos o decorador **`permission_required`** do Django, que permite verificar se o usuário possui as permissões necessárias para acessar a visualização.  

com base na documentação abaixo vamos deixar um modelo completo para futuras customizações. Vamos utilizar exatamente como está ai

Documentação: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#custom-users-admin-full-example

Criar um app chamado “**contas**” colocar a pasta dentro de “**apps**” onde definimos no inicio que ficariam nossos aplicativos.

```bash
python manage.py startapp contas
```

Adiciona no core/settings.py

```python
PROJECT_APPS = [
    'apps.base',
    'apps.contas',
    'apps.home',
]
```

**Com base na documentação de autentificação do django, este código é um bom ponto de partida para criar um modelo de usuário personalizado no Django com autenticação baseada em email.**

apps/contas/models.py

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
```

apps/contas/admin.py

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from contas.forms import UserCreationForm
from contas.models import MyUser

class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm
    model = MyUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)

admin.site.register(MyUser, MyUserAdmin)
```

core/settings.py

```python
...
AUTH_USER_MODEL = "contas.MyUser"
...
```

Admin do Django. Já podemos criar os grupos.

- **Administrador**
- **Colaborador**
- **Usuário**

rota rota: **/admin/auth/group/**

Não temos nada de permissão ainda. já podemos criar os grupos e deixar assim.