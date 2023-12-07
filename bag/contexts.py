from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    # Initialize variables
    bag_items = []
    total = 0
    product_count = 0
    delivery = 0
    free_delivery_delta = 0
    grand_total = 0

    # Retrieve bag data from session
    bag = request.session.get('bag', {})

    # Iterate through items in the bag
    for item_id, item_data in bag.items():
        # Get product details for the item
        product = get_object_or_404(Product, pk=item_id)

        # Check if item_data is an integer 
        if isinstance(item_data, int):
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })

    # Calculate delivery cost and grand total
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        grand_total = total + delivery
    else:
        grand_total = total

    # Create context dictionary with bag details
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
