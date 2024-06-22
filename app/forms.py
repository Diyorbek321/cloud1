from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth.models import Group

from app.models import Inventory, Sales, Customer


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "group")


class RoleCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'content_type', 'codename']


class InventoryItem(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'text', 'quantity']


class SalesItem(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['name', 'product_name', 'quantity', 'price']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']


class ModifyUserRoleForm(forms.Form):
    user_id = forms.IntegerField(label='user_id')
    new_role = forms.ChoiceField(
        choices=[
            ('', 'Select Role'),
            ('admin', 'admin'),
            ('manager', 'manager'),
            ('sales_rep', 'sales'),
            ('warehouse_staff', 'warehouse'),
            ('customer', 'customer')
        ],
        label='new_role'
    )
