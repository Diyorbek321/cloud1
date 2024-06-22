from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView

from app.forms import CustomUserCreationForm, RoleCreationForm, PermissionForm, InventoryItem, SalesItem, CustomerForm, \
    ModifyUserRoleForm


# Create your views here.
class AdminTemplateView(LoginRequiredMixin, View):
    allowed_groups = ['admin']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'admin.html')


class AdminListView(ListView):
    template_name = 'admin.html'
    model = User.objects.all()
    context_object_name = 'users'


class UsersTemplateView(LoginRequiredMixin, View):
    allowed_groups = ['manager', 'admin']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user_management.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = form.cleaned_data['group']
            user.groups.add(user_group)
            return redirect('user_list')  # Redirect to a user list or another page
        return render(request, 'user_management.html', {'form': form})


class UserListView(LoginRequiredMixin, View):
    allowed_groups = ['manager', 'admin']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        users = User.objects.all()
        return render(request, 'user_list.html', {'users': users})


class ModifyUserRoleView(LoginRequiredMixin, FormView):
    template_name = 'user_management.html'
    form_class = ModifyUserRoleForm
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        user_id = form.cleaned_data['user_id']
        new_role = form.cleaned_data['new_role']

        user = get_object_or_404(User, id=user_id)

        # Clear all groups the user belongs to
        user.groups.clear()

        # Assign the user to the new group
        if new_role:
            group, created = Group.objects.get_or_create(name=new_role)
            user.groups.add(group)

        user.save()
        return super().form_valid(form)


class RolesTemplateView(LoginRequiredMixin, View):
    allowed_groups = ['admin']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = RoleCreationForm()
        return render(request, 'roles.html', {'form': form})

    def post(self, request):
        form = RoleCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')  # Redirect to role list after successful creation
        return render(request, 'roles.html', {'form': form})


class RoleListView(LoginRequiredMixin, View):
    allowed_groups = ['admin']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        roles = Group.objects.all()
        return render(request, 'role_list.html', {'roles': roles})


class PermissionsTemplateView(View):  # Removed PermissionRequiredMixin
    allowed_groups = ['admin']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        user_groups = request.user.groups.values_list('name', flat=True)

        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = PermissionForm()
        return render(request, 'permissions.html', {'form': form})

    def post(self, request):
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perm_list')  # Redirect to permission list after successful creation
        return render(request, 'permissions.html', {'form': form})


class PermissionListView(PermissionRequiredMixin, View):
    allowed_groups = ['admin']

    def dispatch(self, request, *args, **kwargs):
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')

        user_groups = request.user.groups.values_list('name', flat=True)

        # Check if the user is in the allowed group
        if not any(group in self.allowed_groups for group in user_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        permissions = Permission.objects.all()
        return render(request, 'permission_lst.html', {'permissions': permissions})


class InventoryTemplateView(LoginRequiredMixin, View):
    allowed_groups = ['admin', 'manager', 'warehouse']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = InventoryItem()
        return render(request, 'inventory.html', {'form': form})

    def post(self, request):
        form = InventoryItem(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Redirect to role list after successful creation
        return render(request, 'inventory.html', {'form': form})


class SalesTemplateView(LoginRequiredMixin, View):
    allowed_groups = ['admin', 'manager', 'sales']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = SalesItem()
        return render(request, 'sales.html', {'form': form})

    def post(self, request):
        form = SalesItem(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales')  # Redirect to role list after successful creation
        return render(request, 'sales.html', {'form': form})


class CustomerTemplateView(LoginRequiredMixin, View):
    allowed_groups = ['admin', 'manager', 'customer']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CustomerForm()
        return render(request, 'customer.html', {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer')  # Redirect to role list after successful creation
        return render(request, 'customer.html', {'form': form})


class SettingsTemplateView(LoginRequiredMixin, View):
    allowed_groups = ['admin']

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        # Check if the user is in the allowed group
        if not any(group in user_groups for group in self.allowed_groups):
            return redirect('error_page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = RoleCreationForm()
        return render(request, 'settings.html', {'form': form})

    def post(self, request):
        form = RoleCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')  # Redirect to role list after successful creation
        return render(request, 'settings.html', {'form': form})


# @unauthenticated_user
class LoginTemplateView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Perform authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Check user groups and redirect accordingly
            if user.groups.filter(name='admin').exists():
                return redirect('admin')  # Replace with your admin page URL name
            elif user.groups.filter(name='customer').exists():
                return redirect('customer')  # Replace with your users page URL name
            elif user.group.filter(name='manager').exists():
                return redirect('users')
            elif user.group.filter(name='sales'):
                return redirect('sales')
            elif user.group.filter(name='warehouse'):
                return redirect('warehouse')
            else:
                return redirect('roles')  # Fallback URL if the user is not in any specific group
        else:
            # Authentication failed, redirect back to login with an error message (optional)
            return render(request, 'login.html', {'error': 'Invalid username or password'})


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class ErrorTemplateView(TemplateView):
    template_name = '404.html'
