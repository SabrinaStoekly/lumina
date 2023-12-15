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