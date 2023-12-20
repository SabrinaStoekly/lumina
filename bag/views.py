from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_bag(request):
    """Renders the bag contents page."""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag', {})

    if item_id in bag:
        if isinstance(bag[item_id], int):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
        messages.success(request, f'Added {quantity} {product.name}(s) to your bag')  # Display quantity added
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {quantity} {product.name}(s) to your bag')  # Display quantity added

    request.session['bag'] = bag

    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product in the shopping bag."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('bag:bag'))

def remove_from_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)

    if 'bag' in request.session:
        bag = request.session['bag']
        if item_id in bag:
            del bag[item_id]
            request.session['bag'] = bag
            messages.success(request, f'Removed {product.name} from your bag')  # Message when item is removed
            return redirect('bag:bag')

    # If the item was not removed, display an error message
    messages.error(request, f'Failed to remove {product.name} from your bag')
    return redirect('bag:bag')
