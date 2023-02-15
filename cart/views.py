from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem
from store.models import Product

def _cart_session(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_product_item_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_obj = Cart.objects.get(cart_id=_cart_session(request))
    except Cart.DoesNotExist:
        cart_obj = Cart.objects.create(cart_id=_cart_session(request))
        cart_obj.save()

    try:
        cart_item =CartItem.objects.get(product=product, cart=cart_obj)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart_obj
        )
        cart_item.save()
    return redirect('cart')

def remove_product_item_from_cart(request, product_id):
    cart_obj = Cart.objects.get(cart_id=_cart_session(request), is_deleted=False)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart_obj)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_product_from_cart(request, product_id):
    cart_obj = Cart.objects.get(cart_id=_cart_session(request), is_deleted=False)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart_obj)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    tax = 0
    try:
        cart_obj = Cart.objects.get(cart_id=_cart_session(request))
        cart_items = CartItem.objects.filter(cart=cart_obj, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (0.16 * total)
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'cart.html', context)
