# **Tratando erros formulários**

**Dev: Letícia Lima**

apps/base/utils.py

```jsx
from django.contrib import messages

def add_form_errors_to_messages(request, form):
    for field, error_list in form.errors.items():
        for error in error_list:
            messages.error(request, f"Erro no campo '{form[field].label}': {error}")
```

nas views que tem metodo post podemos adicionar as função para exibir os erros.

```jsx
# Adicionar mensagens de erro aos campos dos formulários
add_form_errors_to_messages(request, user_form)
add_form_errors_to_messages(request, perfil_form)
```

Validação de senha com Regex.

```jsx
import re

def clean_password1(self):
			password1 = self.cleaned_data.get('password1')
			if len(password1) < 8:
			    raise forms.ValidationError("A senha deve conter pelo menos 8 caracteres.")
			
			# Verifique se a senha contém pelo menos uma letra maiúscula, uma letra minúscula e um caractere especial
			maiusculas=re.search(r'[A-Z]', password1)
			minusculas=re.search(r'[a-z]', password1)
			caract_esp=re.search(r'[!@#$%^&*(),.?":{}|<>]', password1)
			if not maiusculas or not minusculas or not caract_esp:
			    raise forms.ValidationError("A senha deve conter \
												pelo menos 8 caracteres, uma letra maiúscula, uma letra \
												minúscula e um caractere especial.")
			return password1
```

login
```jsx
else:
	messages.error(request, 'Combinação de e-mail e senha inválida. \
	   Se o erro persistir, entre em contato com o administrador do sistema.')
```