from django.contrib import messages 
from django.db.models import Q


def add_form_errors_to_messages(request, form):
    for field, error_list in form.errors.items():
        for error in error_list:
            messages.error(request, f"Erro no campo '{form[field].label}': {error}")


# def filtrar_modelo(modelo, **filtros):
#     queryset = modelo.objects.all()
#     for campo, valor in filtros.items():
#         lookup = f"{campo}__icontains"
#         queryset = queryset.filter(**{lookup: valor})
#     return queryset

# Filtro (OR)
def filtrar_modelo(modelo, **filtros):
    queryset = modelo.objects.all()
    
    q_objects = Q()  # Inicializa um objeto Q vazio

    for campo, valor in filtros.items():
        q_objects |= Q(**{campo + '__icontains': valor})

    queryset = queryset.filter(q_objects)
    return queryset