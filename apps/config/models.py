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