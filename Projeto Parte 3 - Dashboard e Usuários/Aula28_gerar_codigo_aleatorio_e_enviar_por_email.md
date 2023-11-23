# **Gerar uma senha e enviar por e-mail**

**Dev: Letícia Lima**

Para gerar uma senha e enviar para usuario é muito simples. Com base nas instruções anteriores que fizemos basta fazer algumas alterações. Primeiro, que tipo de senha vamos enviar para usuário, eu pensei em 2 alternativas, um numero de 6 digitos aleatorio ou CPF.  Ai tanto faz, se for numero de CPF teriamos que criar um campo. Vamos fazer com um numero aleatorio e enviar para e-mail certo.

Vamos utilizar a bilbioteca nativa do Django para envio de e-mail. **EmailMessage**.

Na documentação tem um exemplo que vamos seguir, podemos usar qualquer biblioteca dessa de envio de e-mail com django. 

https://docs.djangoproject.com/en/4.1/topics/email/

apps/contas/forms.py

```python
import random # escolha aleatoria
import string # contem todas as letras do alfabeto, etc.
from django.core.mail import send_mail

class CustomUserCreationForm(forms.ModelForm):
			...
			def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if self.user.is_authenticated:
            password = ''.join(random.choices(string.digits, k=6)) # Gerar uma senha 
            user.set_password(password) # salvo essa senha
            user.force_change_password = True # força mudança de senha quando logar.
            send_mail( # Envia email para usuario
                'Sua senha provisória',
                f'Sua senha provisório para entrar na plataforma é: {password}',
                'email@email.com', # De (em produção usar o e-mail que está no settings: settings.DEFAULT_FROM_EMAIL)
                [user.email], # para
                fail_silently=False,
            )
        else:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
 
```

Para usar numeros e letras na senha: `password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))`

**Mais detalhes e explorar mais sobre a bibliotecas usadas.** 
**string**: https://docs.python.org/3/library/string.html
**random**: [https://docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html?highlight=random#module-random)

Como estamos usando o backend do django para simular envio de e-mail a gente consegue testar. E resultado ficou bem legal neh pessoal.