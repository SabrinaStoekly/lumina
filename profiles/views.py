from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AnonymousUser

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order

from django.contrib import messages

def profile(request):
    """ Display the user's profile if it exists. """
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None

        form = UserProfileForm(request.POST or None, instance=profile)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully')
            else:
                messages.error(request, 'Update failed. Please ensure the form is valid.')

        orders = profile.orders.all() if profile else None

        template = 'profiles/profile.html'
        context = {
            'form': form,
            'orders': orders,
            'on_profile_page': True
        }

        return render(request, template, context)
    else:
        # Handle the case when the user is not authenticated
        template = 'profiles/profile.html'
        context = {
            'form': None,
            'orders': None,
            'on_profile_page': True
        }

        return render(request, template, context)

def order_history(request, order_number):
    # Retrieve the order with the given order number or return a 404 error
    order = get_object_or_404(Order, order_number=order_number)

    # Display an informational message to the user
    messages.info(
        request,
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    )

    # Set the template and context for rendering
    template_name = 'checkout/checkout_success.html'
    context_data = {
        'order': order,
        'from_profile': True,
    }

    # Render the checkout success template with the order details
    return render(request, template_name, context_data)