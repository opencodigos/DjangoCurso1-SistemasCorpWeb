import random # escolha aleatoria
import string # contem todas as letras do alfabeto, etc.
import re
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from contas.models import MyUser 

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput) 
    password2 = forms.CharField(label="Confirmação de Senha", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'email': 'E-mail',
            'first_name': 'Nome', 
            'last_name': 'Sobrenome',
            'is_active': 'Usúario Ativo?'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if self.user.is_authenticated:
            del self.fields['password1']
            del self.fields['password2']
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
             
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("A senha deve conter pelo menos 8 caracteres.")
        
        # Verifique se a senha contém pelo menos uma letra maiúscula, uma letra minúscula e um caractere especial
        if not re.search(r'[A-Z]', password1) or not re.search(r'[a-z]', password1) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError("A senha deve conter pelo menos 8 caracteres, \
                                        uma letra maiúscula, uma letra minúscula e um caractere \
                                        especial.")
        return password1           
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Senha não estão iguais!")
        return password2

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
                settings.DEFAULT_FROM_EMAIL, # De (em produção usar o e-mail que está no settings: settings.DEFAULT_FROM_EMAIL)
                [user.email], # para
                fail_silently=False,
            )
        else:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name','is_active']
        # help_texts = {'username': None}
        labels = {
            'email': 'E-mail', 
            'first_name': 'Nome', 
            'last_name': 'Sobrenome', 
            'is_active': 'Usúario tá Ativo?'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # get the 'user' from kwargs dictionary
        super().__init__(*args, **kwargs) 
        if not self.user.groups.filter(name__in=['administrador','colaborador']).exists():
            for group in ['is_active']: 
                del self.fields[group]
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'