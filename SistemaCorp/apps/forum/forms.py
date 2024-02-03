from django import forms
from .models import PostagemForum,PostagemForumComentario

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
    
class PostagemForumForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'})) 
    
    postagem_imagens = MultipleFileField(
        label='Selecione no máximo 5 imagens.',required=False) # Adiciona isso

    class Meta:
        model = PostagemForum
        fields = ['titulo', 'descricao', 'data_publicacao', 'ativo']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostagemForumForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                

class PostagemForumComentarioForm(forms.ModelForm):
    class Meta:
        model = PostagemForumComentario
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3})
        }