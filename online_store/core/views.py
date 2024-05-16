from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import ItemFilterForm
from .models import Item, Category

# Create your views here.
def index(request):
    items = Item.objects.filter()
    choises = [('', '')] + list(map(lambda c: (c.id, c.name), Category.objects.filter()))
    if request.method == 'POST':
        filter_form = ItemFilterForm(request.POST)

        filter_form.fields['category'].choices = choises
        if filter_form.is_valid():
            items = filter_form.filter_items(items)
    else:
        filter_form = ItemFilterForm()
        filter_form.fields['category'].choices = choises


    return render(request, "core/index.html",{
        "items" : items,
        'filter_form': filter_form
    })

def details(request, pk):
    item = Item.objects.filter(pk=pk).first()
    if not item:
        return redirect('core:index')
    return render(request, 'core/details.html', {
        'item': item
    })

