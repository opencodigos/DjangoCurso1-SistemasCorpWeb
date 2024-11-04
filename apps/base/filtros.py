

def filtrar_modelo(modelo, **filtros):
    queryset = modelo.objects.all()
    for campo, valor in filtros.items():
        lookup = f"{campo}__icontains"
        queryset = queryset.filter(**{lookup: valor})
    return queryset
 