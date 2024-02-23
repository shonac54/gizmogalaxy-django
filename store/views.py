from django.shortcuts import render,get_object_or_404
from . models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q
#for paginator
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator


# Create your views here.
def store(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products =  Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    
    context = {
        'products':paged_products,
        'product_count':product_count,
    }




    return render(request,'store/store.html',context)






def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as e:
        raise e
    

    context={
        'single_product':single_product,
        'in_cart':in_cart,
    }

    return render(request,'store/product_detail.html',context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)




from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
from category.models import Category  # Import Category model

def add_product(request):
    # Your authentication check goes here

    error = ""
    
    # Retrieve categories from the database
    categories = Category.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            error = "no"
            # Redirect to the manage_product page upon successful form submission
            return redirect('manage_product')
        else:
            error = "yes"
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form, 'error': error, 'categories': categories})


def manage_product(request):
    # Your authentication check goes here
    
    products = Product.objects.all()
    
    return render(request, 'manage_product.html', {'products': products})

def edit_product(request, pid):
    # Your authentication check goes here
    
    error = ""
    product = Product.objects.get(id=pid)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            error = "no"
        else:
            error = "yes"
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'error': error, 'product': product})

def delete_product(request, pid):
    # Your authentication check goes here
    
    product = Product.objects.get(id=pid)
    product.delete()
    
    return redirect('manage_product')

