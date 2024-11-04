### Configurações/SEO

Dev: Letícia Lima 

Vamos fazer algumas configurações no site de modo global. Como logo, scritps, meta tags, google Analytics e Adsense. 

- **Logo**


```python
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
```

```python
<img src="{{ logo.image.url }}" width="150" alt="{{ logo.title }}" title="{{ logo.title }}" class="logo">
```

- **SEOHome**


```python
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
```

    

Header

```
{% block meta_description_keyword %}
        <meta name="description" content="{{ seo.meta_description }}" />
        <meta name="keywords" content="{{ seo.meta_keywords }}"/>
{% endblock %}
```

- **GoogleAnalytics**


```python
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
```

```python

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZKDYWDF34R"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', '{{ ga_code.ga_id }}');
</script>
```

- **Scripts**


```python
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
```

```html
Header
{% for header_script in header_scripts %}
        {{ header_script.script|safe }}
{% endfor %}
    
{% for footer_script in footer_scripts %}
    {{ footer_script.script|safe }}
{% endfor %}
```

- **Context**

Context para exibir nos template de modo global  

```python
def get_logo(request):
    return {
        'logo': Logo.objects.all().first()
    }

def get_seo(request):
    return {
        'seo': SEOHome.objects.first()
    }

def get_ga_code(request):
    return {
        'ga_code': GoogleAnalytics.objects.first()
    }

def get_scripts(request):
    return {
        'header_scripts': Scripts.objects.filter(place='HD', is_active=True),
        'footer_scripts': Scripts.objects.filter(place='FT', is_active=True),
    }
```

- **Cookies — NOVO**


```jsx
<div id="cookieModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>We value your privacy</h2>
        </div>
        <div class="modal-body">
            <p>We use cookies on this website to enhance your user experience. By clicking "I agree", you are giving your consent for us to set cookies.</p>
            <p>For more information on what data is contained in the cookies, please see our <a href="/privacy-policy/">Privacy Policy</a> page.</p>
        </div>
        <div class="modal-footer">
            <button id="rejectCookies">I decline</button>
            <button id="acceptCookies">I agree</button>
        </div>
    </div>
</div>

```

```jsx
// Seleciona o modal
const modal = document.getElementById('cookieModal');

// Verifica se o cookie já foi aceito
const cookiesAccepted = getCookie('cookiesAccepted');
if (cookiesAccepted !== 'true') {
    // Abre o modal automaticamente
    modal.style.display = 'block';
}

// Fecha o modal ao clicar no botão "I decline"
document.getElementById('rejectCookies').addEventListener('click', function () {
    modal.style.display = 'none';
});

// Fecha o modal ao clicar no botão "I agree"
document.getElementById('acceptCookies').addEventListener('click', function () {
    modal.style.display = 'none';
    // Define o cookie como aceito
    setCookie('cookiesAccepted', 'true', 365);
});

// Funções para manipular cookies
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
} 
```

```jsx
/* Estilo básico para o modal */
.modal {
    display: none; /* oculta o modal por padrão */
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.4); /* fundo semi-transparente */
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
}

.modal-header, .modal-footer {
    padding: 10px 0;
    text-align: center;
}

.modal-body {
    padding: 10px 0;
}

```