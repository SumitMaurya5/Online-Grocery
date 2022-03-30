from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.views.generic import TemplateView,View
from django.db.models import Count
from .forms import CartAddProductForm
from django.db.models import Q


def mainPage(request):
    if request.session.get('Email'):
        user=request.session['Email']
        z=Registeration.objects.get(Email=user)
        model=Products.objects.filter()[:20]
        if request.GET:
            try:
                q = request.GET.get('search')
                if q:
                    prod= Products.objects.filter(Q(title__icontains=q))
                    data = {
                        'pro' : prod
                    }
            except:
                pass
            return render(request,'index.html',data)
        return render(request,'index.html',{'model':model,'z':z})
    else:
        models=Products.objects.all()[::5]
        return render(request,'index.html',{'models':models})
def search(request):
    if request.method == 'GET':
        searchs = request.GET.get('search')
        post = Products.objects.all().filter(Q(title__icontains=searchs))
        return render(request, 'search.html', {'post':post})   

def login(request):
    if request.method=="POST":
        try:
            Email=request.POST['Email']
            Password=request.POST["Password"]
            mod=Registeration.objects.get(Email=Email)
            if mod.Password==Password:
                request.session['Email']=Email
                messages.success(request,'done')
                return redirect('index')
            else:
                messages.error(request,"Wrong password")
        except:
            messages.info(request,'User not found') 
    return render(request,'login.html')

def logout(request):
    if 'Email' in request.session:
        del request.session['Email']
        return redirect('login')
    else:
        return redirect('login')



def category(request):
    model=Category.objects.all()
    mod=Products.objects.all()

    data = {}
    for i in model:
        qs = Products.objects.filter(category=i).count()
        data[i] = qs

    return render(request,'category.html',{'model':model,'qs':data,'mod':mod})

def productview(request,title):
    mod=Products.objects.get(title=title)
    model=Products.objects.all()[:]
    print(model)
    return render(request,'single-product.html',{'mod':mod,'model':model})


def categorywise(request,title):
    model=Category.objects.all()
    cat=Category.objects.get(title=title)
    form1 =Products.objects.all().filter(category=cat)

    data = {}
    for i in model:
        qs = Products.objects.filter(category=i).count()
        data[i] = qs

    return render(request,'category.html',{'form1': form1,'qs':data,'model':model})


class AddtoCartView(TemplateView):
    template_name="addtocart.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        product_id=self.kwargs['pro_id']
        print(product_id)
        product_obj=Products.objects.get(id=product_id)
        print(product_obj)
        cart_id=self.request.session.get('cart_id', None)
        print(cart_id)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            print(cart_obj)
            product_in_cart=cart_obj.cartproduct_set.filter(product=product_obj)
            print(product_in_cart)
            if product_in_cart.exists():
                cartproduct=product_in_cart.last()
                cartproduct.quantity+=1
                cartproduct.subtotal+=product_obj.selling_price
                cartproduct.save()
                cart_obj.total+=product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct=CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total+=product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj=Cart.objects.create(total=0)
            self.request.session['cart_id']=cart_obj.id
            cartproduct=CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total+=product_obj.selling_price
            cart_obj.save()
        return context 
# @require_POST
# def Cuopan_apply(request):
#     now = timezone.now()
#     form = CoupanApplyForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['code']
#         try:
#             coupan = Coupan.objects.get(code__iexact=code,
#                                         valid_from_ite=now,
#                                         valid_to_gte=now,
#                                         active=True)
#             request.session['coupan_id'] = coupan.id
#         except Coupan.DoesNotExist:
#             request.session['coupan_id'] = None
#     return redirect('cart:cart')

class ManageCartView(View):
    def get(self,request,*args,**kwargs):
        cp_id=self.kwargs["cp_id"]
        action =request.GET.get("action")
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart
        
        if action=="inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        elif action=="dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity==0:
                cp_obj.delete()

        elif action =="rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect ("mycart")


class EmptyCartView(View):
    def get(self,request,*args,**kwargs):
        cart_id=request.session.get("cart_id", None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.save()
        return redirect("mycart")

class MyCartView(TemplateView):
    template_name="cart.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id",None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart

        return context

def contact(request):
    return render(request,'contact.html')