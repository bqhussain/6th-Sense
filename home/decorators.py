from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test




def patient_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a patient,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.profile.is_therapist==False,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



# from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.contrib.auth.decorators import user_passes_test
#
#
#
#
# def patient_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     '''
#     Decorator for views that checks that the logged in user is a patient,
#     redirects to the log-in page if necessary.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_patient,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator
#
#
# def therapist_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='tlogin'):
#     '''
#     Decorator for views that checks that the logged in user is a therapist,
#     redirects to the log-in page if necessary.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_therapist,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator