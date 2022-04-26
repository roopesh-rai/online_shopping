from django.shortcuts import render, redirect
from django.views import View
from online_shopping.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from .models import Customer, Product, OrderPlaced, Cart, checkoutform, Invoice, InvoiceItems
from math import ceil
from django.http import HttpResponse, JsonResponse
from .forms import CustomerRegistraionForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from .models import Contact
from django.conf import settings
from django.views.generic import TemplateView
from django.core.mail import send_mail
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import stripe

stripe.api_key = STRIPE_SECRET_KEY

def home(request):
    products = Product.objects.all()
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) + (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'app/home.html', params)

class ProductView(View):
    def get(self, request):
        totalitem=0
        topwears = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        mobliles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwear': bottomwear, 'mobliles': mobliles, 'laptops':laptops, 'totalitem':totalitem})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    product_id = request.GET.get('prod_id')
    print(product_id)
        # product = Product.objects.get(id=product_id)
    status = request.POST.get('Cancel')
    order = OrderPlaced.objects.filter(status='Cancel')
    order.delete()
    print(request.POST)
    return render(request, 'app/orders.html', {'order_placed': op})

class OrderView(View):
    def get(self, request, pk):
        op = OrderPlaced.objects.filter(user=request.user)
        print(request.POST)
        product = Product.objects.get(pk=pk)
        prod_id = Product.objects.get(id=product.id)
        print(product)
        OrderPlaced(product=product)
        status = request.POST.get('Cancel')
        order = OrderPlaced.objects.filter(status='Cancel', product=product)
        order.delete()
        return render(request, 'app/orders.html', {'order_placed': op})

    def post(self, request, pk):
        op = OrderPlaced.objects.filter(user=request.user)
        print(request.POST)
        product = Product.objects.get(pk=pk)
        prod_id = Product.objects.get(id=product.id)
        print(product)
        OrderPlaced(product=product)
        status = request.POST.get('Cancel')
        order = OrderPlaced.objects.filter(status='Cancel' not in status, product=product)
        OrderPlaced(status='Cancel')
        return render(request, 'app/orders.html', {'order_placed': op})

@login_required
def cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        totalitem=0
        user = request.user
        cart= Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/add_to_cart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        totalitem = 0
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/product_details.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})

# @login_required
def buynow(request):
    return render(request, 'app/buy_now.html')

def about(request):
    return render(request, 'app/about.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            # totalamount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            # totalamount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        person = request.POST['person']
        context = request.POST['context']
        print(name, email, phone, person, context)
        contact = Contact(name=name, email=email, phone=phone, person=person, context=context)
        contact.save()
    return render(request, 'app/contact.html')

def tracker(request):
    return render(request, 'app/tracker.html')

@login_required
def checkout(request):
    user = request.user
    # prod_id = request.id
    add = Customer.objects.filter(user=user)
    # product = Product.objects.filter(id=id)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})

class CheckoutView(View):
    def get(self, request, pk):
        user = request.user
        product = Product.objects.get(pk=pk)
        add = Customer.objects.filter(user=user)
        prod_items = Product.objects.filter(Q(id=product.id))
        print(prod_items)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        prod = [p for p in Product.objects.all() if p.id == product.id]
        print(prod)
        if prod:
            for p in prod:
                tempamount = (1 * p.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
        return render(request, 'app/checkout.html', {'add': add, 'product': product, 'totalamount': totalamount, 'prod_items': prod_items})

@login_required
def payment_done(request, **kwargs):
    try:
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        # product = Product.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
            c.delete()
        return redirect("stripe")

    except Exception:
        return HttpResponse("Please provide address")

class PaymentdoneView(View):
    def get(self, request, pk):
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        product = Product.objects.get(pk=pk)
        prod_items = Product.objects.filter(Q(id=product.id))
        print("rr")
        for c in prod_items:
            print(c)
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
            c.delete()
        return redirect("ordersdata")

def basic(request):
    return render(request, 'app/basic.html')

def mobiles(request, data=None):
    if data==None:
        mobiles = Product.objects.filter(category='Mobiles')
    elif data=='Realme' or data=='POCO':
        mobiles = Product.objects.filter(category='Mobiles').filter(brand=data)
    elif data=='Below':
         mobiles = Product.objects.filter(category='Mobiles').filter(discounted_price__lt=10000)
    elif data=='Above':
         mobiles = Product.objects.filter(category='Mobiles').filter(discounted_price__gt=10000)
    return render(request, 'app/mobiles.html', {'mobiles': mobiles})

def laptops(request, data=None):
    if data==None:
        laptops = Product.objects.filter(category='Laptop')
    elif data=='DELL' or data=='ASUS':
        laptops = Product.objects.filter(category='Laptop').filter(brand=data)
    elif data=='Below':
         laptops = Product.objects.filter(category='Laptop').filter(discounted_price__lt=50000)
    elif data=='Above':
         laptops = Product.objects.filter(category='Laptop').filter(discounted_price__gt=50000)
    return render(request, 'app/laptops.html', {'laptops': laptops})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistraionForm()
        return render(request, 'app/register.html', {'form': form})

    def post(self, request):
        form = CustomerRegistraionForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/register.html', {'form': form})

def login(request):
    return render(request, 'app/login.html')

def password_reset(request):
    return render(request, 'app/password_reset.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

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
            messages.success(request, 'Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

@login_required
def edit_profile(request):
    # form = CustomerProfileForm(request.POST)
    try:
        if request.method == 'POST':
            # request.user.customer.usr = request.user
            request.user.customer.name = request.POST.get('name', '')
            request.user.customer.locality = request.POST.get('locality', '')
            request.user.customer.city = request.POST.get('city', '')
            request.user.customer.state = request.POST.get('state', '')
            request.user.customer.zipcode = request.POST.get('zipcode', '')
            request.user.customer.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('checkout')
        return render(request, 'app/editprofile.html')
    except Exception:
        # return redirect("profile")
        return redirect("profile")


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})

def searchMatch(query, item):
    if query in item.description.lower() or query in item.title.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    products = Product.objects.all()
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) + (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': 'Please Make Sure To Enter Relevant Search Qukwargsery'}
    return render(request, 'app/search.html', params)

@login_required
def check_out_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        pmethod = request.POST['pmethod']
        context = request.POST['context']
        print(name, email, phone, pmethod, context)
        checkoutt = checkoutform(name=name, email=email, phone=phone, pmethod=pmethod, context=context)
        if pmethod == 'stripe':
            return redirect('stripe')
        checkoutt.save()
    return render(request, 'app/checkout_form.html')

# def stripe(request):
#     return render(request, 'app/stripe.html')

class ProductLandingPageView(TemplateView):
    template_name = 'app/landing.html'

    def get_context_data(self, **kwargs):
        # product = Product.objects.get(title="Test Product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            # "product": product,
            "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY
        })
        return context

def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount='{totalamount}',
            currency='INR',
            description='A Django Charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')

def topwear(request):
    return render(request, 'app/topwear.html')


class CreateCheckoutSessionView(View):
    def post(self, request, pk, *args, **kwargs):
        BASE_URL = "http://127.0.0.1:8000"
        product = Product.objects.get(pk=pk)
        prod_items = Product.objects.filter(Q(id=product.id))
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': product.stripe_price_id,
                    'quantity': 1,
                },
            ],
            metadata = {
              "product_id":product.id
            },
            mode='payment',
            success_url=BASE_URL + '/success/',
            cancel_url=BASE_URL + '/cancel/',
        )
        return redirect(checkout_session.url)

endpoint_secret = 'whsec_a02f2df803ffa596f42eed01d433d199d66144766f636cd3bf1fe207a14448b4'
@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  print(sig_header)
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
  except ValueError as e:
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    return HttpResponse(status=400)

  if event['type'] == 'checkout.session.completed':
      session = event['data']['object']

      customer_email = session["customer_details"]["email"]
      product_id = session["metadata"]["product_id"]
      product = Product.objects.get(title="Realme C21Y 32 GB")

      send_mail(
          subject="Here is your product",
          message="Thanks for your purchase.",
          recipient_list=[customer_email],
          from_email="roopesh.rai@plutustec.com",
      )

  # Passed signature verification
  return HttpResponse(status=200)

# def fulfill_order(session):
#   TODO: fill me in
#   print("Fulfilling order")


class SuccessView(TemplateView):
    template_name = "app/success.html"

class CancelView(TemplateView):
    template_name = "app/cancel.html"

class HomePageView(TemplateView):
    template_name = "app/stripe.html"
    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        # prod_id = request.id
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == self.request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
        # return render(self.request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})
        product = Product.objects.get(title="Realme C21Y 32 GB")
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
        })
        return context

class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(title="Realme C21Y 32 GB")
            intent = stripe.PaymentIntent.create(
                amount=product.discounted_price,
                currency='INR',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None


class PaymentSuccess(View):
    def get(self, request):
        return HttpResponse({'msg', 'Your Payment has been succeed'})


class PaymentCancel(View):
    def get(self, request):
        return HttpResponse({'msg', 'Your Payment has cancel'})


class ShowInvoice(View):
    def post(self, request, *args, **kwargs):
        template = get_template('stripe.html')
        data = request.data
        order_id = data['order_id']
        Order = OrderPlaced.objects.get(id=order_id)
        # payment = Payment.objects.get(order_id=Order)
        user = Order.user
        orderitems = OrderPlaced.objects.filter(order=Order)
        pdf = render_to_pdf('stripe.html', {'order_items': orderitems, 'user': user, 'order': Order})
        return HttpResponse(pdf, content_type='application/pdf')


class DownloadInvoice(View):
    def post(self, request):
        template = get_template('stripe.html')
        data = request.data
        order_id = data['order_id']
        Order = OrderPlaced.objects.get(id=order_id)
        # payment = Payment.objects.get(order_id=Order)
        user = Order.user
        invoice = Invoice(user=user, order_id=order_id)
        invoice.save()
        orderitems = OrderPlaced.objects.filter(order=Order)
        for i in orderitems:
            InvoiceItems.objects.create(invoice=invoice, product=i.product, product_pricee=i.price)

        pdf = render_to_pdf('stripe.html', {'invoice': invoice, 'order_items': orderitems, 'user': user, 'order': Order})

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % (data['order_id'])
            content = "inline; filename = '%s'" % (filename)
            content = "attachment; filename = '%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("not found")


class ShareInvoice(View):
    def post(self, request):
        template = get_template('stripe.html')
        data = request.data
        order_id = data['order_id']
        Order = OrderPlaced.objects.get(id=order_id)
        # payment = Payment.objects.get(order_id=Order)
        user = Order.user
        invoice = Invoice(user=user, order_id=order_id)
        invoice.save()
        orderitems = OrderPlaced.objects.filter(order=Order)
        for i in orderitems:
            InvoiceItems.objects.create(invoice=invoice, product=i.product, product_pricee=i.price)

        pdf = render_to_pdf('stripe.html', {'invoice': invoice, 'order_items': orderitems, 'user': user, 'order': Order})

        if pdf:
            filename = "Invoice.pdf"
            content = "attachment; filename = '%s'" % (filename)
            mail_subject = "Recent Order Details"
            email = EmailMessage(mail_subject, 'this is a message', settings.EMAIL_HOST_USER, [user.email])
            email.attach('new.pdf', pdf, "application/pdf")
            email.send()
        return HttpResponse({'msg': 'Invoice generated!'})