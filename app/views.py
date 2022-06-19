from http.client import HTTPResponse
from itertools import product
from math import prod
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from django. contrib import messages
from .models import Customer,Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# def home(request):
#  return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'totalitem':totalitem} )

# def product_detail(request):
#  return render(request, 'app/productdetail.html')


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem=0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user = request.user)).exists()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', { 'product': product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user= request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id = product_id)
    Cart(user = user, product = product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
       user = request.user
       cart = Cart.objects.filter(user = user)
       amount = 0.0
       shipping_amt = 50.0
       total_amt = 0.0
       cart_product = [p for p in Cart.objects.all() if p.user == user]
       if cart_product:
           for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount 
               total_amt = amount + shipping_amt
       if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', {'carts':cart, 'total_amt':total_amt, 'amount':amount, 'cart_product':cart_product, 'totalitem':totalitem}) 

def quantitycart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        operation = request.GET['opr']
        c = Cart.objects.get(Q(product = product_id) & Q(user = request.user))
        if operation == "p":
            c.quantity += 1
            c.save()
        elif operation == "m":
            c.quantity -= 1
            c.save()
        elif operation == "r":
            c.delete()
        else:
            return HTTPResponse('error')
        
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
                    'quantity' : c.quantity,
                    'amount' : amount,
                    'totalamount' : amount + shipping_amount
                }       
        return JsonResponse(data)

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    totalitem=0
    address = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html',{'address':address, 'active':'btn btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
    totalitem=0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'order_placed':op, 'totalitem':totalitem})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request):
    totalitem=0
    mobiles = Product.objects.filter(category='M')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html',{'mobiles':mobiles, 'totalitem':totalitem})

def laptop(request):
    totalitem=0
    laptops = Product.objects.filter(category='L')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html',{'laptops':laptops, 'totalitem':totalitem})

def topwear(request):
    totalitem=0
    topwear = Product.objects.filter(category = 'TW')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/topwear.html', {'topwear':topwear, 'totalitem':totalitem} )

def bottomwear(request):
    totalitem=0
    bottomwear = Product.objects.filter(category = 'BW')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/bottomwear.html', {'bottomwear':bottomwear, 'totalitem':totalitem} )

def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    totalitem=0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 50.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product :
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html', {'add':add, 'total_amount':total_amount, 'cart_item':cart_item, 'totalitem':totalitem})

@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('add_btn')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user = user, customer = customer, product = c.product, quantity = c.quantity).save()
        c.delete()
    return redirect('orders')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    totalitem=0
    def get(self, request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render (request,'app/profile.html', {'form':form, 'active':'btn btn-primary', 'totalitem':totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congrats !!! Profile Updated Successfully')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render (request, 'app/profile.html', {'form':form,'active':'btn btn-primary', 'totalitem':totalitem})