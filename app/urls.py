"""online_shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import viewsbasic
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('orders/', views.orders, name='orders'),
    # path('orders/<int:pk>', views.PaymentdoneView.as_view(), name='ordersdata'),
    path('orders/<int:pk>', views.OrderView.as_view(), name='ordersdata'),
    path('add_to_cart/', views.cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<int:pk>', views.CheckoutView.as_view(), name='checkoutdata'),
    # path('success/', views.SuccessView.as_view(), name='success'),
    # path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('landing/', views.ProductLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    # path('checkoutform/', views.check_out_form, name='checkoutform'),
    path('checkoutform/', views.check_out_form, name='checkoutform'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('product_details/<int:pk>', views.ProductDetailView.as_view(), name='product_details'),
    path('change_password/', auth_view.PasswordChangeView.as_view(template_name='app/change_password.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='change_password'),
    path('buynow/', views.buynow, name='buynow'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('basic/', views.basic, name="basic"),
    path('mobile/', views.mobiles, name="mobile"),
    path('mobile/<slug:data>', views.mobiles, name="mobiledata"),
    path('laptop/', views.laptops, name="laptop"),
    path('laptop/<slug:data>', views.laptops, name="laptopdata"),
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name="login"),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset/', views.password_reset, name='password-reset'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'),name='passwordchangedone'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('address/', views.address, name='address'),
    path('search/', views.search, name='search'),
    path('charge/', views.charge, name='charge'),
    # path('esewa-request/', views.EsewaRequestView.as_view(), name='esewarequest'),
    # path('stripe/', views.stripe, name='stripe'),
    path('topwear/', views.topwear, name='topwear'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    # path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('payment_success/', views.PaymentSuccess.as_view(), name = "payment_success"),
    path('payment_cancel/', views.PaymentCancel.as_view(), name = "payment_cancel"),
    path('show_invoice/', views.ShowInvoice.as_view(), name = "show_cancel"),
    path('invoice_download/', views.DownloadInvoice.as_view(), name = "download_invoice"),
    path('share_invoice/', views.ShareInvoice.as_view(), name = "share_invoice"),
    path('create-payment-intent/<pk>/', views.StripeIntentView.as_view(), name='create-payment-intent'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)