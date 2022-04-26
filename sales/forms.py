from django import forms
from django.contrib.auth.models import User
from .models import Seller
from app.models import Product
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm

class CustomerRegistraionForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # mobile = forms.IntegerField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        # fields = ['username', 'email', 'mobile', attrs'password1', 'password2']
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'phone', 'email', 'stage_of_business', 'company_name', 'company_size', 'company_address', 'city', 'zipcode', 'state', 'gst']
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'phone': forms.NumberInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'stage_of_business': forms.Select(attrs={'class': 'form-control'}),
                   'company_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'company_size': forms.Select(attrs={'class': 'form-control'}),
                   'company_address': forms.TextInput(attrs={'class': 'form-control'}),
                   'city': forms.TextInput(attrs={'class': 'form-control'}),
                   'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
                   'state': forms.Select(attrs={'class': 'form-control'}),
                   'gst': forms.TextInput(attrs={'class': 'form-control'})
                }

# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'phone', 'email', 'stage_of_business', 'company_name', 'company_size', 'company_address', 'city', 'zipcode', 'state', 'gst')

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_img']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'discounted_price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'description': forms.TextInput(attrs={'class': 'form-control'}),
                   'brand': forms.TextInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'form-control'}),
                   'product_img': forms.FileInput(attrs={'class': 'form-control'})
                }


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Enter Your Registered Email'), max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))