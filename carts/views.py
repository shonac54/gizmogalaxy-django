from django.shortcuts import render,redirect,get_object_or_404
from carts.models import Cart,CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist  
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def _cart_id(request):
    cart      = request.session.session_key
    if not cart:
        cart  = request.session.create()
    return cart



# #Increment the cart item
# def add_cart(request,product_id):
#     product   = Product.objects.get(id=product_id)  #get the product
#     try:
#         cart  = Cart.objects.get(cart_id=_cart_id(request))   #get the cart using the cart_id present in the session 

#     except Cart.DoesNotExist:
#         cart  = Cart.objects.create(
#             cart_id = _cart_id(request)
#         )
#     cart.save()

#     try:
#         cart_item = CartItem.objects.get(product=product,cart=cart)
#         cart_item.quantity += 1         #cart_item.quantity = cart_item.quantity + 1
#         cart_item.save()

#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(
#             product = product,
#             quantity = 1,
#             cart = cart,

#         )
#         cart_item.save()


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # Get the product

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the cart_id present in the session

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, user=request.user)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=request.user  # Associate the cart item with the authenticated user
            )
            cart_item.save()
    else:
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, user=None)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=None  # For non-logged-in users, associate the cart item with None
            )
            cart_item.save()

    return redirect('cart')











#decrement the cart item
def remove_cart(request,product_id,cart_item_id):
    
    product = get_object_or_404(Product,id=product_id)
    # cart_item = CartItem.objects.get(product=product,cart=cart)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete() 

    except:
            pass

    return redirect('cart')




# #clicking the remove  button to remove cart item
# def remove_cart_item(request,product_id,cart_item_id):
    
#     product = get_object_or_404(Product,id=product_id)
#     if request.user.is_authenticated:
#         cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)

#     else:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
#         cart_item.delete()
#     return redirect('cart')






def remove_cart_item(request, product_id, cart_item_id):
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product_id=product_id, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product_id=product_id, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except CartItem.DoesNotExist:
        pass

    return redirect('cart')




def cart(request, total=0, quantity=0, cart_item=None):
    cart_items = []  # Initialize cart_items here

    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_item=None):
    try:
        tax = 0
        grand_total=0
        # cart        = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items  = CartItem.objects.filter(cart=cart,is_active=True)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2 * total)/100
        grand_total = total + tax



    except ObjectDoesNotExist:

        pass   #just ignore


    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'store/checkout.html',context)
