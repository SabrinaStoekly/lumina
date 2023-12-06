from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
import inflect

def all_products(request):
    products = Product.objects.all()
    query = None
    categories = None
    no_products_found = False
    no_categories_found = False

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET.getlist('category')            
            existing_categories = Category.objects.filter(name__in=categories)
            if len(existing_categories) != len(categories):
                no_categories_found = True
            else:
                products = products.filter(category__name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if query:
                p = inflect.engine()
                singular_query = p.singular_noun(query)
                plural_query = p.plural_noun(query)

                queries = Q(name__icontains=query) | Q(description__icontains=query) | \
                          Q(name__icontains=singular_query) | Q(name__icontains=plural_query)
                products = products.filter(queries)

    if not products.exists() and not no_categories_found:
        no_products_found = True

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'no_products_found': no_products_found,
        'no_categories_found': no_categories_found,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)
