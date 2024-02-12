# from django.core.exceptions import PermissionDenied
# from .models import Therapist
#
# def therpist_required(function):
#     def wrap(request, *args, **kwargs):
#         entry = Therapist.objects.filter(email=request.user.email).count()
#         if entry > 0:
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#
#     return wrap
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test




def therapist_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a patient,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.profile.is_therapist,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator