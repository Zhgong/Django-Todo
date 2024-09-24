from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import ToDo
from .serializers import ToDoSerializer

class ToDoViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all().order_by('-created_at')
    serializer_class = ToDoSerializer

def index(request):
    return render(request, 'todo/index.html')
