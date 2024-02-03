from django.db import models
 
 
class Pagina(models.Model): 
    nome = models.CharField(max_length=100, 
                              help_text='Digite o nome da pagina. Ex: Inicio, Contato...')

    class Meta:
        verbose_name = '0 - Paginas'
        verbose_name_plural = '0 - Paginas'
        ordering = ['id']

    def __str__(self):
        return self.nome
    
    
## Tipos de Blocos, SLIDE, BANNER_1, BANNER_2, BANNER_3 etc...
class TipoBloco(models.Model): 
    nome = models.CharField(max_length=100, 
                              help_text='Digite o nome do bloco. Ex: SLIDE, BANNER_1...')
    class Meta:
        verbose_name = '1 - Tipo de Bloco'
        verbose_name_plural = '1 - Tipo de Bloco'
        ordering = ['id']

    def __str__(self):
        return '{} - {}'.format(self.id, self.nome)
    
    
## Podemos montar varios conteudos para usar no bloco
class Conteudo(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True, help_text='Nome do conteúdo para identificar na lista.')
    imagem = models.ImageField(upload_to='paginas/imagem/', null=True, blank=True)
    icone = models.CharField(max_length=100, null=True, blank=True,help_text='Codigo do Icon, Ex: fas fa-user')
    
    cor_label = models.CharField(max_length=100, null=True, blank=True,help_text='Codigo do RGB, Ex: #FA4343')
    
    titulo_1 = models.CharField(max_length=100, null=True, blank=True, help_text="Titulo")
    titulo_2 = models.CharField(max_length=200, null=True, blank=True, help_text="Subtitulo")
    
    descricao_1 = models.CharField(max_length=200, null=True, blank=True, help_text="Descrição mais curta até 200 caracteres")
    descricao_2 = models.TextField(null=True, blank=True, help_text="Descrição mais longa")
    descricao_3 = models.CharField(max_length=200, null=True, blank=True, help_text="Descrição mais curta até 200 caracteres")
    descricao_4 = models.CharField(max_length=200, null=True, blank=True, help_text="Descrição mais curta até 200 caracteres")

    
    titulo_botao_1 = models.CharField(max_length=50, null=True, blank=True,help_text="Titulo do Botão 1")
    rota_botao_1 = models.CharField(max_length=50, null=True, blank=True,help_text="Nome da Rota que configurou no urls.py")
    
    titulo_botao_2 = models.CharField(max_length=50, null=True, blank=True,help_text="Titulo do Botão 2")
    rota_botao_2 = models.CharField(max_length=50, null=True, blank=True,help_text="Nome da Rota que configurou no urls.py")
    
    class Meta:
        verbose_name = '2 - Conteúdo'
        verbose_name_plural = '2 - Conteúdo'
        ordering = ['id']

    def __str__(self):
        return '{} - {}'.format(self.nome,
                                     self.titulo_1)


## Modelo para criar varios blocos
class Blocos(models.Model): 
    ordem = models.CharField(max_length=3, null=True, help_text="Ordem de exibição do bloco")
    titulo = models.CharField(max_length=100, help_text="Titulo pode ser exibido no template")
    descricao = models.TextField(blank=True, null=True, help_text="Descrição do bloco")
    pagina = models.ForeignKey(Pagina, on_delete=models.CASCADE, related_name="pagina_conteudo") # Aonde será exibido esse bloco
    bloco = models.ForeignKey(TipoBloco, on_delete=models.CASCADE, related_name="bloco_conteudo", null=True) # Tipo de Bloco, SLIDE, BANNER_1, BANNER_2
    conteudo = models.ManyToManyField(Conteudo)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '3 - Blocos'
        verbose_name_plural = '3 - Blocos'
        ordering = ['id']

    def __str__(self):
        return 'Pagina {} - {} - {}'.format(
            self.pagina.nome, self.ordem, self.titulo)