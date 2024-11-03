from django.shortcuts import render

# Create your views here.
def timeout_view(request):
    return render(request, 'timeout.html')