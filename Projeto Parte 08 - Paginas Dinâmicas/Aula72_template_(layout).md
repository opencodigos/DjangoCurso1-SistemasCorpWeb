# Template (Layout)

Dev: Letícia Lima

Tem algumas referencias, templates que podemos olhar. Estou fazendo um site/sistema para area medica. Então filtrei por “Medicina”.

**Referencia:** 
https://preview.colorlib.com/#medically 

https://preview.colorlib.com/#mediplus

https://colorlib.com/wp/cat/medical/

**obs: para fazer pesquisa de imagens: Fonoaudiologia sem copyright freepik**

Não sou nenhuma designer, estou pegando essas referencia para ter uma ideia de como vou estruturar os blocos na pagina. Como vou desenvolver o codigo para deixar dinamico para usuario final cadastrar os objetos. 

**Com base na referencia vou montrar o layout usando boostrap blz ?**

Vou criar esses components para usar nas paginas. Deixar as coisas mais dinâmicas para que usuário tenha a liberdade de editar os dados no Dashboard Admin do Django.

- **Banner Slide**
- **Banner 1**
- **Serviços**
- **Banner 2**
- **Area de Especialidades**
- **Banner 3**
- **Banner 4**
- **Footer**
- **FAQ**
- **Contato**

### **Templates**

layout/index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" 
						integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
  </head>
  <body>
    <h1>Hello, world!</h1>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" 
						integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
  </body>
</html>
```

Um Pouco de bootstrap. 

https://getbootstrap.com/docs/5.3/getting-started/introduction/

Com base nesse layout que pegamos do bootstrap vamos modelar nossa pagina inicial.

### **1 - Slide**

```html
<!-- Slide inicial -->
    <section>
        <div id="carouselExampleIndicators" class="carousel carousel-dark slide mb-6" data-bs-ride="carousel"
            data-bs-theme="light">
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active"
                    aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"
                    aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"
                    aria-label="Slide 3"></button>
            </div>
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img src="https://blog.ipog.edu.br/wp-content/uploads/2018/05/direitos-trabalhistas-dos-m%C3%A9dicos.jpg"
                        class="object-fit-cover d-block w-100" height="600" alt="...">
                    <div class="carousel-caption">
                        <div class="row align-items-center text-start" style="height: 600px;">
                            <div class="col-md-8 pt-5 mt-5">
                                <span class="text-primary">BEM-VINDO À ABC EMPRESA</span>
                                <h1 class="mb-4">Estamos aqui para o seu cuidado</h1>
                                <p class="mb-4">Bem, bem longe, atrás das montanhas de palavras, distante dos países
                                    Vokalia e Consonantia, vivem os textos cegos. Separados, eles vivem em
                                    Bookmarksgrove.
                                </p>
                                <p>Espero que isso atenda às suas necessidades!</p>
                                <p><a href="#" class="btn btn-primary py-3 px-4">Saiba mais</a></p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <img src="https://i2.wp.com/cremers.org.br/wp-content/uploads/2021/12/prontuario_site_gettyimages.png?fit=727%2C381&ssl=1"
                        class="object-fit-cover d-block w-100" height="600" alt="...">
                    <div class="carousel-caption">
                        <div class="row align-items-center text-start" style="height: 600px;">
                            <div class="col-md-8 pt-5 mt-5">
                                <span class="text-primary">BEM-VINDO À ABC EMPRESA</span>
                                <h1 class="mb-4">Estamos aqui para o seu cuidado</h1>
                                <p class="mb-4">Bem, bem longe, atrás das montanhas de palavras, distante dos países
                                    Vokalia e Consonantia, vivem os textos cegos. Separados, eles vivem em
                                    Bookmarksgrove.
                                </p>
                                <p>Espero que isso atenda às suas necessidades!</p>
                                <p><a href="#" class="btn btn-primary py-3 px-4">Saiba mais</a></p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <img src="https://d2dxldo5hhj2zu.cloudfront.net/img/983x,jpeg/https://d3043uog1ad1l6.cloudfront.net/uploads/2020/02/medico.jpg"
                        class="object-fit-cover d-block w-100" height="600" alt="...">
                    <div class="carousel-caption">
                        <div class="row align-items-center text-start" style="height: 600px;">
                            <div class="col-md-8 pt-5 mt-5">
                                <span class="text-primary">BEM-VINDO À ABC EMPRESA</span>
                                <h1 class="mb-4">Estamos aqui para o seu cuidado</h1>
                                <p class="mb-4">Bem, bem longe, atrás das montanhas de palavras, distante dos países
                                    Vokalia e Consonantia, vivem os textos cegos. Separados, eles vivem em
                                    Bookmarksgrove.
                                </p>
                                <p>Espero que isso atenda às suas necessidades!</p>
                                <p><a href="#" class="btn btn-primary py-3 px-4">Saiba mais</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>
    </section>
    <!-- Fim Slide inicial -->
```

### 2 - Banner 1

```html
<!-- Bloco 1 - Intro -->
    <section>
        <div class="container py-lg-5">
            <div class="row">
                <div class="col-md-6 col-lg-5">
                    <div class="d-flex align-items-center">
                        <img src="https://media.unimedcampinas.com.br/cd19560e-c394-481d-99a5-702d4a89d590"
                            class="rounded-5 object-fit-cover d-block w-100" height="550" alt="">
                    </div>
                </div>
                <div class="col-md-6 col-lg-7 pl-lg-5 py-md-5">
                    <div class="row justify-content-start pb-3">
                        <div class="col-md-12 p-4 p-lg-5">
                            <h2 class="mb-4">Somos a <span class="text-primary">ABC EMPRESA</span>, uma empresa medica
                            </h2>
                            <p>Nossa missão é fornecer soluções inovadoras e de alta qualidade para atender às
                                necessidades da área da saúde.</p>
                            <p>Nosso compromisso é oferecer equipamentos de última geração que proporcionem resultados
                                precisos e confiáveis.</p>
                            <p>
                                <a href="#" class="btn btn-primary py-3 px-4">Sobre Nos</a>
                                <a href="#" class="btn btn-secondary py-3 px-4">Entre em contato conosco</a>
                            </p>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </section>
    <!-- Fim Bloco 1 - Intro -->
```

### 3 - Serviços

```html
<!-- Bloco Nossos Serviços -->
    <section>
        <div class="container py-lg-5">
            <div class="row justify-content-center pb-5">
                <div class="col-md-12">
                    <h2 class="mb-3">Nossos Serviços</h2>
                </div>
            </div>
            <div class="row g-4">
                <div class="col-md-6 d-flex align-self-stretch">
                    <div class="d-flex gap-4">
                        <div class="rounded bg-primary text-white p-5">
                            <i class="fas fa-medkit fa-3x"></i>
                        </div>
                        <div class="media-body pl-md-4">
                            <h3 class="text-dark text-decoration-none mb-3">Kits Médicos</h3>
                            <p>Oferecemos uma variedade de kits médicos completos e prontos para uso e montados para
                                atender às necessidades específicas de cada tipo de
                                procedimento médico. </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 d-flex align-self-stretch">
                    <div class="d-flex gap-4">
                        <div class="rounded bg-primary text-white p-5">
                            <i class="fas fa-stethoscope fa-3x"></i>
                        </div>
                        <div class="media-body pl-md-4">
                            <h3 class="text-dark text-decoration-none mb-3">Produtos Químicos</h3>
                            <p>Nossa empresa oferece uma ampla variedade de produtos químicos essenciais para o campo da
                                saúde. Trabalhamos com os melhores fornecedores para garantir a qualidade e segurança.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 d-flex align-self-stretch">
                    <div class="d-flex gap-4">
                        <div class="rounded bg-primary text-white p-5">
                            <i class="fas fa-user-md fa-3x"></i>
                        </div>
                        <div class="media-body pl-md-4">
                            <h3 class="text-dark text-decoration-none mb-3">Equipe Qualificada</h3>
                            <p>Contamos com uma equipe altamente qualificada de profissionais de saúde. Nossos
                                especialistas possuem amplo conhecimento e experiência garantindo um atendimento de
                                qualidade e eficiência.</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 d-flex align-self-stretch">
                    <div class="d-flex gap-4">
                        <div class="rounded bg-primary text-white p-5">
                            <i class="fas fa-syringe fa-3x"></i>
                        </div>
                        <div class="media-body pl-md-4">
                            <h3 class="text-dark text-decoration-none mb-3">Equipamentos</h3>
                            <p>Oferecemos uma ampla variedade equipamentos médicos de última geração. Nossos equipamentos
                                são projetados para atender às necessidades de diferentes áreas da saúde.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Fim Bloco Nossos Serviços -->
```

### 4 - Banner 2

```html
<!-- Banner 1 -->
    <section>
        <div class="banner">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-9 text-center">
                        <h2 class="fw-bold">Sua saúde é nossa prioridade</h2>
                        <p>Podemos administrar seu projeto dos sonhos. Um pequeno rio chamado ABC Empresa flui próximo
                            ao nosso local.</p>
                        <p class="mb-0"><a href="#" class="btn btn-primary btn-lg px-4 py-3">Pesquisar Áreas</a></p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Fim Banner 1 -->
```

```css
.banner {
        background-image: url('https://i2.wp.com/cremers.org.br/wp-content/uploads/2021/12/prontuario_site_gettyimages.png');
        padding: 8em 0;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        position: relative;
    }
```

### 5 - Areas de Especialidades

```html
<!-- Areas Especialidades -->
    <section>
        <div class="container text-center py-lg-5">
            <div class="row justify-content-center pb-5">
                <div class="col-md-12">
                    <h2 class="mb-3">Áreas de Especialidades</h2>
                </div>
            </div>
            <div class="row gap-3">
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-gratis/jovem-medico-bonito-em-uma-tunica-medica-com-estetoscopio_1303-17818.jpg?w=2000"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Medicina</a></h3>
                    <p>Envolve o diagnóstico, tratamento e prevenção de doenças e lesões, utilizando uma variedade de
                        abordagens, como medicamentos, cirurgias e terapias.</p>
                </div>
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-gratis/enfermeira-negra-em-seu-espaco-de-trabalho_52683-100580.jpg?w=2000"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Enfermagem</a></h3>
                    <p>Cuida dos pacientes, fornecendo cuidados diretos, administrando medicamentos, monitorando sinais
                        vitais e auxiliando no processo de recuperação.</p>
                </div>
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-premium/fisioterapeuta-tratando-perna-ferida-de-paciente-do-sexo-masculino_229060-150.jpg"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Fisioterapia</a></h3>
                    <p>Ajuda na reabilitação e tratamento de lesões ou condições físicas por meio de terapias físicas,
                        exercícios e técnicas manuais.</p>
                </div>
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-gratis/dentista-examinando-uma-paciente-do-sexo-feminino-com-ferramentas_107420-65429.jpg?w=360"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Odontologia</a></h3>
                    <p>Envolve o diagnóstico, prevenção e tratamento de doenças e condições orais, como cáries, doença
                        periodontal e problemas de má oclusão.</p>
                </div>
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-gratis/jovem-mulher-caucasiana-recebendo-massagem-anti-idade_1098-18121.jpg"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Estética</a></h3>
                    <p>A estética está relacionada a procedimentos e tratamentos que visam melhorar a aparência estética
                        do corpo.</p>
                </div>
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-premium/fonoaudiologa-jovem-ensinando-garotinho-com-defeitos-de-pronunciacao-para-dizer-o-som-u-durante_116547-18715.jpg"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Fonoaudiologia</a></h3>
                    <p>A fonoaudiologia lida com distúrbios da comunicação, linguagem, fala, voz e deglutição,
                        oferecendo diagnóstico, terapia e reabilitação nessas áreas.</p>
                </div>
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-premium/pedicure-descascamento-de-pes-procedimento-de-pedicura-de-calo-em-pe-pelas-maos-de-podologo-em-luvas-brancas-no-salao-de-beleza_170532-3613.jpg"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Podologia</a></h3>
                    <p>A podologia é especializada no estudo, diagnóstico e tratamento de doenças e condições dos pés e
                        tornozelos, como unhas encravadas, calosidades e deformidades.</p>
                </div>
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-premium/depilacao-a-laser-de-diodo-esteticista-remove-cabelo-no-braco-feminino-bonito-depilacao-para-procedimento-a-laser-de-pele-lisa_213455-4698.jpg?w=2000"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Laserpuntura</a></h3>
                    <p>A laserpuntura é uma terapia que combina os princípios da acupuntura com o uso de lasers de baixa
                        intensidade para estimular pontos específicos do corpo.</p>
                </div>
                <div class="col p-4 bg-light rounded-5">
<img src="https://img.freepik.com/fotos-gratis/veterinario-verificando-a-saude-do-filhote_23-2148728396.jpg"
                        class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                    <h3><a class="link-dark text-decoration-none" href="#">Veterinária</a></h3>
                    <p>A medicina veterinária é dedicada ao cuidado da saúde e bem-estar dos animais, incluindo
                        diagnóstico, tratamento e prevenção de doenças em animais domésticos e selvagens.</p>
                </div>
            </div>
        </div>
    </section>
    <!-- Area Especialidades -->
```

### 6 - Banner 3

```html
<!-- Indices -->
    <section>
        <div class="banner">
            <div class="container py-lg-5">
                <div class="row d-flex align-items-center">
                    <div class="col-md-5">
                        <span>INDICE DE SATISFAÇÃO</span>
                        <h2 class="mb-4 fs-1">Mais de 5.100 profissionais confiam em nós</h2>
                        <p class="mb-0 fs-2"><a href="#"
                                class="btn btn-outline-secondary btn-lg px-4 py-3">Depoimentos</a></p>
                    </div>
                    <div class="col-md-7">
                        <div class="row pt-4">
                            <div class="col-md-6 d-flex justify-content-center">
                                <div class="fs-2">
                                    <strong class="text-primary">30</strong>
                                    <span>Anos de Experiência</span>
                                </div>
                            </div>
                            <div class="col-md-6 d-flex justify-content-center">
                                <div class="fs-2">
                                    <strong class="text-primary">+100.000</strong>
                                    <span>Equipamentos</span>
                                </div>
                            </div>
                            <div class="col-md-6 d-flex justify-content-center">
                                <div class="fs-2">
                                    <strong class="text-primary">+6.000</strong>
                                    <span>Profissionais</span>
                                </div>
                            </div>
                            <div class="col-md-6 d-flex justify-content-center">
                                <div class="fs-2">
                                    <strong class="text-primary">100%</strong>
                                    <span>De Satisfação</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Fim Indice -->
```

### 7 - Depoimentos

```html
<!-- Depoimentos -->
    <section>
        <div class="container py-lg-5">
            <div class="row justify-content-center pb-5">
                <div class="col-md-10 text-center">
                    <h2 class="mb-4">Obtenha todas as atualizações aqui</h2>
                    <p>Depoimentos de profissionais que utilizaram nossos produtos</p>
                </div>
            </div>

            <div id="carouselExample" class="carousel slide" data-bs-ride="carousel" data-bs-interval="5000">
                <div class="carousel-inner text-center">
                    <div class="carousel-item active">
<img src="https://img.freepik.com/fotos-gratis/jovem-medico-bonito-em-uma-tunica-medica-com-estetoscopio_1303-17818.jpg?w=2000"
                            class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                        <p class="fst-italic fs-3"><i class="fas fa-quote-left fa-2x"></i> Recentemente, tive a
                            oportunidade de utilizar um monitor
                            cardíaco portátil durante uma estadia no hospital. Fiquei extremamente impressionado com a
                            eficácia e a utilidade desse equipamento médico. <i class="fas fa-quote-right fa-2x"></i>
                        </p>
                        <p>12 de junho 2023</p>
                        <p><strong>Leticia Lima</strong></p>
                    </div>
                    <div class="carousel-item">
<img src="https://img.freepik.com/fotos-gratis/jovem-medico-bonito-em-uma-tunica-medica-com-estetoscopio_1303-17818.jpg?w=2000"
                            class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                        <p class="fst-italic fs-3"><i class="fas fa-quote-left fa-2x"></i> tive a oportunidade de
                            utilizar um monitor
                            cardíaco portátil durante uma estadia no hospital. Fiquei extremamente impressionado com a
                            eficácia e a utilidade desse equipamento médico. <i class="fas fa-quote-right fa-2x"></i>
                        </p>
                        <p>12 de junho 2023</p>
                        <p><strong>Leticia Lima</strong></p>
                    </div>
                    <div class="carousel-item">
<img src="https://img.freepik.com/fotos-gratis/jovem-medico-bonito-em-uma-tunica-medica-com-estetoscopio_1303-17818.jpg?w=2000"
                            class="rounded-circle object-fit-cover" width="150" height="150" alt="">
                        <p class="fst-italic fs-3"><i class="fas fa-quote-left fa-2x"></i> oportunidade de utilizar um
                            monitor
                            cardíaco portátil durante uma estadia no hospital. Fiquei extremamente impressionado com a
                            eficácia e a utilidade desse equipamento médico. <i class="fas fa-quote-right fa-2x"></i>
                        </p>
                        <p>12 de junho 2023</p>
                        <p><strong>Leticia Lima</strong></p>
                    </div>
                </div>
            </div>

        </div>
    </section>
```

### 8 - Banner 4

```html
<!-- Bloco 2 -->
    <section class="bg-light">
        <div class="container py-lg-5">
            <div class="row">
                <div class="col-md-6 col-lg-7 pl-lg-5 py-md-5">
                    <div class="row justify-content-start pb-3">
                        <div class="col-md-12 p-4 p-lg-5">
                            <h2 class="mb-4">Forum <span class="text-primary">ABC EMPRESA</span></h2>
                            <p>Caso tenha dúvidas, você pode se inscrever em nosso fórum. Lá, você encontrará uma
                                comunidade dedicada pronta para ajudar e compartilhar conhecimento.
                            </p>
                            <p>Nossos membros estão ansiosos para responder suas perguntas e fornecer orientações. Não
                                hesite em se juntar a nós e fazer parte dessa troca de informações valiosa. Esperamos
                                vê-lo lá!</p>
                            <p>
                                <a href="#" class="btn btn-primary py-3 px-4">Forum Online</a>
                                <a href="#" class="btn btn-secondary py-3 px-4">Entre em contato conosco</a>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-5">
                    <div class="d-flex align-items-center">
                        <img src="https://img.freepik.com/vetores-premium/forum-da-internet-comunicacao-de-pessoas-conversando-com-amigos-e-sociedade-isometrica_53562-8104.jpg?w=2000"
                            class="rounded-5 object-fit-cover d-block w-100" height="550" alt="">
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Fim Bloco 2 -->
```

### 9 - Contato

```html
<!-- Contato -->
    <section>
        <div class="container py-lg-5">
            <div class="row justify-content-center mb-5 pb-3">
                <div class="col-md-7 text-center">
                    <h2 class="mb-4">Entre em contato conosco</h2>
                </div>
            </div>
            <div class="row mb-5">
                <div class="col">
                    <div class="h-100 align-self-stretch box p-4 text-center bg-light">
                        <i class="fas fa-home fa-4x"></i>
                        <h3 class="mb-4">Endereço</h3>
                        <p>198 West 21th Street, Suite 721 New York NY 10016</p>
                    </div>
                </div>
                <div class="col">
                    <div class="h-100 align-self-stretch box p-4 text-center bg-light">
                        <i class="fas fa-phone fa-4x"></i>
                        <h3 class="mb-4">WhatsApp</h3>
                        <p><a class="link-dark text-decoration-none" href="tel://1234567920">(16) 9 9425-6485</a></p>
                    </div>
                </div>
                <div class="col">
                    <div class="h-100 align-self-stretch box p-4 text-center bg-light">
                        <i class="fas fa-at fa-4x"></i>
                        <h3 class="mb-4">E-mail</h3>
                        <p><a class="link-dark text-decoration-none"
                                href="mailto:contato.leticialima.me@gmail.com">contato.leticialima.me@gmail.com</a></p>
                    </div>
                </div>
                <div class="col">
                    <div class="h-100 align-self-stretch box p-4 text-center bg-light">
                        <i class="fas fa-globe fa-4x"></i>
                        <h3 class="mb-4">Site</h3>
                        <p><a class="link-dark text-decoration-none" href="#">seusite.com.br</a></p>
                    </div>
                </div>
            </div> 
            <div class="">
                <div class="d-flex">
                    <img src="https://img.freepik.com/fotos-premium/vista-lateral-do-medico-feminino-sorridente_23-2148453487.jpg?w=2000"
                        width="450" alt="">

                    <form class="row p-5 m-5" action="#" class="bg-light p-5">
                        <h4>Formulário de Contato</h4>
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="Seu nome">
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="Seu E-mail">
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="Titulo">
                        </div>
                        <div class="form-group">
                            <textarea name="" id="" cols="30" rows="7" class="form-control"
                                placeholder="Mensagem..."></textarea>
                        </div>
                        <div class="form-group">
                            <input type="submit" value="Enviar Mensagem" class="btn btn-secondary py-3 px-5">
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
```

### 10 - footer

```html
<!-- footer -->
    <section>
        <div class="container">
            <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
                <div class="col-md-4 d-flex align-items-center">
                    <a href="/" class="mb-3 me-2 mb-md-0 text-body-secondary text-decoration-none lh-1">
                        <svg class="bi" width="30" height="24">
                            <use xlink:href="#bootstrap"></use>
                        </svg>
                    </a>
                    <span class="mb-3 mb-md-0 text-body-secondary">© 2023 Company, Inc</span>
                </div>

                <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
                    <li class="ms-3"><a class="text-body-secondary" href="#">
                            <i class="fas fa-home"></i>
                        </a></li>
                    <li class="ms-3"><a class="text-body-secondary" href="#">
                            <i class="fas fa-at"></i>
                        </a></li>
                    <li class="ms-3"><a class="text-body-secondary" href="#">
                            <i class="fas fa-globe"></i>
                        </a></li>
                </ul>
            </footer>
        </div>
    </section>
```

### 11 - FAQ