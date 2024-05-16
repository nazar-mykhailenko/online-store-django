from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from payment.models import Order, OrderDetails

from .forms import SignupForm, UpdateUserForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'login/signup.html', {
        'form': form
    })

@login_required
def log_out(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UpdateUserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UpdateUserForm(instance=request.user)

    orders = Order.objects.filter(user=request.user)

    return render(request, 'user_profile/profile.html', {
        'form': form,
        'orders': orders,
    })

@login_required
def order_details(request, id):
    order = Order.objects.get(pk=id)
    order_dets = OrderDetails.objects.filter(order=order)

    return render(request, 'user_profile/order_details.html', {
        'order': order,
        'order_details': order_dets
    })


class ChangePasswordView(PasswordChangeView):
    template_name = 'user_profile/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = '/profile/'
