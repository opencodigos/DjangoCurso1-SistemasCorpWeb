# Generated by Django 5.1.2 on 2024-11-04 03:06

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostagemForum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo')),
                ('descricao', models.TextField(max_length=350, verbose_name='Descrição')),
                ('data_publicacao', models.DateField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('ativo', models.BooleanField(default=False, verbose_name='Publicar Postagem?')),
                ('anexar_imagem', models.ImageField(blank=True, null=True, upload_to='postagem-forum/', verbose_name='Imagem Anexo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_postagem_forum', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Postagem Forum',
                'verbose_name_plural': 'Postagem Forum',
                'ordering': ['-data_criacao'],
            },
        ),
    ]
