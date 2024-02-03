from django import forms
from perfil.models import Perfil
    
class PerfilForm(forms.ModelForm):
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=200
    )
    class Meta:
        model = Perfil
        fields = ['foto', 'ocupacao', 'genero', 'telefone',
                  'cidade','estado', 'descricao']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PerfilForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'