from django.shortcuts import render
from .models import Item

# Create your views here.
def index(request):
    items = Item.objects.filter()
    return render(request, "core/index.html",{
        "items" : items
    })