from functools import wraps

from django.http import HttpResponse
from django.shortcuts import redirect


# def unauthenticated_user(view_func):
#     def wrapped_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('admin')
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapped_func


# def allowed_users(allowed_roles=[]):
#     def allowed_users(allowed_roles=[]):
#         def decorator(view_func):
#             @wraps(view_func)
#             def wrapped_func(request, *args, **kwargs):
#                 if request.user.is_authenticated:
#                     user_groups = request.user.groups.values_list('name', flat=True)
#                     if any(role in user_groups for role in allowed_roles):
#                         return view_func(request, *args, **kwargs)
#                     else:
#                         return HttpResponse('You are not authorized to view this page', status=403)
#                 else:
#                     return HttpResponse('You need to log in first', status=401)
#
#             return wrapped_func
#
#         return decorator
