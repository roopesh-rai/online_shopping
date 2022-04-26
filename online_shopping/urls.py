"""online_shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from  other_app.views import Homepath('<id>', detail_view ),                                  path('<id>', detail_view ),
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import HomePageView
from sales import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from sales.forms import LoginForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('stripe/', HomePageView.as_view(), name='stripe'),
    path('seller/register/', views.CustomerRegistrationView.as_view(), name='sellerregister'),
    path('seller/accounts/login/', auth_view.LoginView.as_view(template_name='seller/login.html', authentication_form=LoginForm, redirect_field_name='/seller/register'), name="sellerlogin"),
    path('seller/logout/', auth_view.LogoutView.as_view(next_page='sellerlogin'), name='sellerlogout'),
    path('seller/profile/', views.SellerProfileView.as_view(), name="sellerprofile"),
    path('seller/password-reset/', auth_view.PasswordResetView.as_view(template_name='seller/password_reset.html', form_class=MyPasswordResetForm), name='seller_password_reset'),
    path('seller/password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='seller/password_reset_done.html'), name='seller_password_reset_done'),
    # path('seller/password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='seller/password_reset_confirm.html', form_class=MySetPasswordForm), name='seller_password_reset_confirm'),
    path('seller/password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='seller/password_reset_complete.html'), name='seller_password_reset_complete'),
    path('seller/dashboard/', views.dashboard, name='dashboard'),
    path('seller/editprofile/', views.edit_profile, name="sellereditprofile"),
    path('seller/productupload/', views.ProfileUploadView.as_view(), name="productuplaod"),
    # path('seller/seller_details/<int:id>', views.detail_view, name='sellerdetails'),
    path('seller/userproduct/', views.show_prod, name="userproduct")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

