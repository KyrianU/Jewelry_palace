from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .forms import ProductForm, ReviewForm
from .models import Product, Category, Review

# Create your views here.


def all_products(request):
    """A view to show all the products, including sorting and search queries"""

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'drection' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
                products = products.order_by(sortkey)

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = (Q(name__icontains=query) |
                       Q(description__icontains=query))
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_item': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """A view to show individual product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_review(request, product_id):
    """
    A view to add a new review
    """

    product = get_object_or_404(Product, pk=product_id)
    user_review = product.reviews.all()

    if user_review:
        messages.error(request,
                       'You have already reviewed this product.')
        return redirect(reverse('product_detail', args=[product.id]))

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product

            review.save()
            print('review')
            messages.success(request,
                             'Your product review has been submitted.')
            return redirect(reverse('product_detail', args=[product_id]))
        else:
            messages.error(request,
                           'An error occured whilst saving your review')
    else:
        form = ReviewForm()

        template = 'products/add_review.html'
        context = {
            'product': product,
            'form': form,
        }

        return render(request, template, context)


@login_required
def edit_review(request, product_id, review_id):
    """Edit an existing review for a product by the logged-in user."""
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(
        Review, pk=review_id, product=product, user=request.user)

    form = ReviewForm(request.POST or None, instance=review)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your review has been updated successfully!")
        return redirect("product_detail", product_id=product.id)

    return render(request, "products/edit_review.html", {
        "form": form, "product": product, "review": review})


@login_required
def delete_review(request, product_id, review_id):
    """Delete a review if the logged-in user is the owner."""
    review = get_object_or_404(
        Review, pk=review_id, product_id=product_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect("product_detail", product_id=product_id)

    return render(
        request, "products/confirm_delete_review.html",
        {"review": review, "product": review.product})


def add_product(request):
    "add product to the store"
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product, \
                           Please ensure the form is valid.')
    else:
        form = ProductForm()

        template = 'products/add_product.html'
        context = {
            'form': form,
        }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    Edit a product in the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid'
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    Delete product from the app
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
