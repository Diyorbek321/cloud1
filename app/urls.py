from django.urls import path
from app.views import AdminTemplateView, UsersTemplateView, RolesTemplateView, PermissionsTemplateView, \
    InventoryTemplateView, SalesTemplateView, CustomerTemplateView, SettingsTemplateView, LoginTemplateView, \
    CustomLogoutView, UserListView, RoleListView, PermissionListView, ErrorTemplateView, ModifyUserRoleView

urlpatterns = [
    path('', AdminTemplateView.as_view(), name='admin'),
    path('user/', UsersTemplateView.as_view(), name='users'),
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('role/', RolesTemplateView.as_view(), name='roles'),
    path('sales/', SalesTemplateView.as_view(), name='sales'),
    path('inventory/', InventoryTemplateView.as_view(), name='inventory'),
    path('customer/', CustomerTemplateView.as_view(), name='customer'),
    path('permission/', PermissionsTemplateView.as_view(), name='permisssions'),
    path('settings/', SettingsTemplateView.as_view(), name='settings'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('role_list/', RoleListView.as_view(), name='role_list'),
    path('perm_list/', PermissionListView.as_view(), name='perm_list'),
    path('error_page/', ErrorTemplateView.as_view(), name='error_page'),
    path('update_user/', ModifyUserRoleView.as_view(), name='update_role'),
]
