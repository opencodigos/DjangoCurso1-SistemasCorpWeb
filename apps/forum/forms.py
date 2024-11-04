from django import forms
from django.conf import settings
from .models import PostagemForum

class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'})) 
    class Meta:
        model = PostagemForum
        fields = ['usuario', 'titulo', 'descricao', 'data_publicacao', 'ativo', 'anexar_imagem']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostagemForumForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'