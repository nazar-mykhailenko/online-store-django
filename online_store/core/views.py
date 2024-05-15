from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, ItemFilterForm
from .models import Item, Category

# Create your views here.
def index(request):
    items = Item.objects.filter()
    if request.method == 'POST':
        filter_form = ItemFilterForm(request.POST)
        choises = [('', '')] + list(map(lambda c: (c.id, c.name), Category.objects.filter()))

        filter_form.fields['category'].choices = choises
        if filter_form.is_valid():
            items = filter_form.filter_items(items)
            print(filter_form.cleaned_data['category'])
    else:
        filter_form = ItemFilterForm()


    return render(request, "core/index.html",{
        "items" : items,
        'filter_form': filter_form
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

@login_required
def log_out(request):
    logout(request)
    return redirect('/')