from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomerRegistraionForm, SellerProfileForm, ProductUploadForm
from django.contrib import messages
from .models import Seller
from app.models import Product
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistraionForm()
        return render(request, 'seller/register.html', {'form': form})

    def post(self, request):
        form = CustomerRegistraionForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            user = form.save()
            group = Group.objects.get(name='seller')
            user.groups.add(group)
        return render(request, 'seller/register.html', {'form': form})

def login(request):
    return render(request, 'seller/login.html')

class ProfileUploadView(View):
    def get(self, request):
        form = ProductUploadForm()
        return render(request, 'seller/profileuploadform.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            usr = request.user
            title = form.cleaned_data['title']
            selling_price = form.cleaned_data['selling_price']
            discounted_price = form.cleaned_data['discounted_price']
            description = form.cleaned_data['description']
            brand = form.cleaned_data['brand']
            category = form.cleaned_data['category']
            product_img = form.cleaned_data['product_img']
            prod = Product(user=usr, title=title, selling_price=selling_price, discounted_price=discounted_price, description=description, brand=brand, category=category, product_img=product_img)
            prod.save()
            messages.success(request, 'Profile Updated Successfully')
        return render(request, 'seller/profileuploadform.html', {'form': form, 'active': 'btn-primary'})

# @method_decorator(login_required, name='dispatch')
class SellerProfileView(View):
    def get(self, request):
        form = SellerProfileForm()
        return render(request, 'seller/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = SellerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            stage_of_business = form.cleaned_data['stage_of_business']
            company_name = form.cleaned_data['company_name']
            company_size = form.cleaned_data['company_size']
            company_address = form.cleaned_data['company_address']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            gst = form.cleaned_data['gst']
            reg = Seller(user=usr, first_name=first_name, last_name=last_name, phone=phone, email=email, stage_of_business=stage_of_business, company_name=company_name, company_size=company_size, company_address=company_address, city=city, zipcode=zipcode, state=state, gst=gst)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        return render(request, 'seller/profile.html', {'form': form, 'active': 'btn-primary'})

def password_reset(request):
    return render(request, 'seller/password_reset.html')

def dashboard(request):
    return render(request, 'seller/dashboard.html')

@login_required
def edit_profile(request):
    # form = CustomerProfileForm(request.POST)
    try:
        if request.method == 'POST':
            # request.user.seller.usr = request.user
            request.user.Seller.first_name = request.POST.get('first_name', '')
            request.user.seller.last_name = request.POST.get('last_name', '')
            request.user.seller.phone = request.POST.get('phone', '')
            request.user.seller.email = request.POST.get('email', '')
            request.user.seller.stage_of_business = request.POST.get('stage_of_business', '')
            request.user.seller.company_name = request.POST.get('company_name', '')
            request.user.seller.company_size = request.POST.get('company_size', '')
            request.user.seller.company_address = request.POST.get('company_address', '')
            request.user.seller.city = request.POST.get('city', '')
            request.user.seller.zipcode = request.POST.get('zipcode', '')
            request.user.seller.state = request.POST.get('state', '')
            request.user.seller.gst = request.POST.get('gst', '')
            request.user.seller.save()
            messages.success(request, 'Profile Updated Successfully')
        # return redirect('dashboard')
        return render(request, 'seller/editprofile.html')
    except Exception:
        # return redirect("profile")
        return redirect("sellerprofile")


def detail_view(request, id):
    context = {}
    context["data"] = Seller.objects.get(id=id)
    return render(request, "seller/seller_details.html", context)

@login_required
def show_prod(request):
    if request.user.is_authenticated:
        totalitem=0
        user = request.user
        prod = Product.objects.filter(user=user)
        cart_product = [p for p in Product.objects.all() if p.user == user]
        if cart_product:
            return render(request, 'seller/user_product.html', {'prods': prod})
        else:
            return HttpResponse("No Products by this user")