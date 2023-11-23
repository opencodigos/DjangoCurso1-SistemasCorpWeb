# Modelo

Dev: Letícia Lima

Vou utilizar o app **‘pages’** para criar os components e utilizar nas paginas.  

Vamos monstar a estrutura dos modelos para adicionar os componentes nas paginas que temos. De um jeito bem simples vou explicar pra vocês via codigo.

Esse modelo são todas as paginas que existem. Por exemplo, inicio, sobre, faq, blog, contato. São paginas estatícas que vamos adicionar os componentes para aparecer.  Então nesse modelo vamos definir isso ok.

apps/pages/models.py

```python
class Pagina(models.Model): 
    nome = models.CharField(max_length=100, 
                              help_text='Digite o nome da pagina. Ex: Inicio, Contato...')

    class Meta:
        verbose_name = '0 - Paginas'
        verbose_name_plural = '0 - Paginas'
        ordering = ['id']

    def __str__(self):
        return self.nome
```

Nesse modelo vamos definir os tipos de blocos que podemos criar. Será um bloco Slide, Banner_1, Contato, Footer, Especialidades. Lembrando estou gerando esses nomes com base no layout que mostrei para vocês. Ai consigo dar o nome para esses blocos.

```python
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
```

Nesse modelo conteudo fica todo conteudo de pode ser criado que vamos usar no bloco. Criei um modelo assim simples de inicio que pode ser estudado depois para melhorias. Nesse caso vamos imaginar todas as possibilidades de blocos. Banner, slide1, cards. Então efetuamos o cadastro desses textos. Se for uma lista de dados a gente vai criando mais de 1. Depois no modelo bloco vocês vão entender.

```python
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
```

No modelo bloco vamos relacionar as coisas. Por exemplo para criar uma pagina Inicio. Vamos supor que temos 3 conteudo criados para um slide. O campo ordem é a ordem de exibição do bloco na pagina. Tem o titulo do bloco que pode ou não ser exibido no template ai depende, se for um bloco de cards por exemplo a gente pode colocar esse titulo para mostrar. Agora um slide não precisa mostrar o titulo, descrição é mesma coisa. O campo pagina é um foreignkey para dizer qual pagina vai aparecer esse bloco. Seleciona o tipo de bloco, se é um slide, banner etc… e o conteudo que será mostrado nesse bloco, é um manytomany então pode ser mais de um. por exemplo o slide podemos fazer com 3 conteudos, ou cards que podemos ter 10. ai é só selecionar. E ativo para mostrar se esse bloco está ativo ou não. 

```python
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
        verbose_name = '3 - Bloco'
        verbose_name_plural = '3 - Bloco'
        ordering = ['id']

    def __str__(self):
        return 'Pagina {} - {} - {}'.format(
            self.pagina.nome, self.ordem, self.titulo)
```