from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty at the moment")
        return redirect(reverse('products:all_products'))

    context = {
        'order_form': OrderForm(),
    }

    return render(request, 'checkout/checkout.html', context)


