from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm

import inflect
import re

def all_products(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    categories = request.GET.getlist('category')
    no_products_found = False
    no_categories_found = False

    if categories:
        existing_categories = Category.objects.filter(name__in=categories)
        if len(existing_categories) != len(categories):
            no_categories_found = True
        else:
            category_queries = Q()
            for category in existing_categories:
                category_queries |= Q(category=category)
            
            products = products.filter(category_queries)

    if query:
        p = inflect.engine()
        plural_query = p.plural(query)
        singular_query = p.singular_noun(query) or query

        # Create a regex pattern for whole word matching
        pattern = r'\b(?:{}|{})\b'.format(re.escape(query), re.escape(plural_query))
        pattern_singular = r'\b{}\b'.format(re.escape(singular_query))

        search_queries = (
            Q(name__iregex=pattern) |
            Q(description__iregex=pattern) |
            Q(name__iregex=pattern_singular)
        )
        
        products = products.filter(search_queries)

        if categories:
            # Apply category filter to the search results
            category_queries = Q()
            for category_name in categories:
                category_queries |= Q(category__name=category_name)
            
            products = products.filter(category_queries)

        # Check if no products are found
        if not products.exists():
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

@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            if 'image' not in request.FILES:  
                messages.error(request, 'Please upload an image for the product.')
            else:
                save_product(request, form)  
                return redirect('all_products')  
    else:
        form = ProductForm()  # Create a new form instance

    return render(request, 'products/add_product.html', {'form': form})

def save_product(request, form, product=None):
    template = 'products/add_product.html' if product is None else 'products/edit_product.html'
    context = {'form': form, 'product': product} if product else {'form': form}

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product) if product else ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Successfully {"added" if not product else "updated"} product!')
            return redirect('product_detail', product.pk)
        else:
            messages.error(request, f'Failed to {"add" if not product else "update"} product. Please ensure the form is valid.')
    else:
        if product:
            messages.info(request, f'You are editing {product.name}')

    return render(request, template, context)