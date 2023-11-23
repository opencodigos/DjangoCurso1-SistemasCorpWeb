# **Detalhe Imagem Anexo (Modal)**
 
Dev: Letícia Lima

Adicionamos um modal simples para renderizar a imagem em anexo.

apps/forum/templates/detalhe-postagem-forum.html

```python
{% if postagem.anexar_imagem %}  
<a data-bs-toggle="modal" href="#exampleModal" role="button">
    <i class="link-info fas fa-image fa-2x me-2"></i></a>
<div class="modal fade" id="exampleModal" tabindex="-1" 
    aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
            <div class="modal-header">
            <h2 class="modal-title fs-5" id="exampleModalLabel">
                <i class="link-info fas fa-image fa-2x me-2"></i></h2>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <img src="{{ postagem.anexar_imagem.url }}" alt="Imagem da postagem" class="img-fluid">
            </div> 
        </div>
    </div>
</div>
{% endif %}
```