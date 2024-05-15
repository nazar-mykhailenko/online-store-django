from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
from .models import Item

# Create your views here.
def index(request):
    items = Item.objects.filter()
    return render(request, "core/index.html",{
        "items" : items
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