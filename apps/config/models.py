from django.db import models
from django.core.exceptions import ValidationError

class Logo(models.Model):
    title = models.CharField('Título/Alt', max_length=100)
    image = models.ImageField('Logo', upload_to='images')

    class Meta:
        verbose_name = 'Logo'
        verbose_name_plural = 'Logo'

    def __str__(self):
        return self.title

    def clean(self):
        model = self.__class__
        if model.objects.count() >= 2 and not self.pk:
            raise ValidationError('Já existe uma 2 logomarca cadastrada.')
        
        
class SEOHome(models.Model):
    meta_description = models.CharField('Meta descrição', max_length=255)
    meta_keywords = models.CharField('Palavras chaves', max_length=255, help_text='Separadas por virgula')

    class Meta:
        verbose_name = 'SEO Home'
        verbose_name_plural = 'SEO Home'

    def __str__(self) -> str:
        return 'Meta tags da Página Home'

    def clean(self):
        model = self.__class__
        if model.objects.exists() and self.pk != model.objects.first().pk:
            raise ValidationError('Já existe meta tags cadastradas para a Home.')
        
        
class GoogleAnalytics(models.Model):
    ga_id = models.CharField('Código GA', max_length=75)

    class Meta:
        verbose_name = 'Google Analytics'
        verbose_name_plural = 'Google Analytics'

    def __str__(self) -> str:
        return 'Código Google Analytics'

    def clean(self) -> None:
        model = self.__class__
        if model.objects.exists() and self.pk != model.objects.first().pk: 
            raise ValidationError('Já existe um Código GA cadastrado.')
        
        
class Scripts(models.Model):
    SCRIPT_PLACE = (
        ('HD', 'Head/Cabeçalho'),
        ('FT', 'Footer/Rodapé'),
    )
    name = models.CharField('Nome do Script', max_length=75)
    script = models.TextField('Script', help_text='Adicione o script completo, inclusive com as tags <script></script>.')
    place = models.CharField('Local', max_length=2, choices=SCRIPT_PLACE, help_text='Escolha onde o script deve ser inserido.')
    is_active = models.BooleanField('Ativo?', default=True, help_text='Os scripts inativos deixarão de ser inseridos nas páginas.')

    class Meta:
        verbose_name = 'Script'
        verbose_name_plural = 'Scripts'

    def __str__(self) -> str:
        return self.name