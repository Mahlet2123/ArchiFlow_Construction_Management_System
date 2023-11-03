from functools import wraps
from django.contrib.auth.decorators import user_passes_test

def superuser_required(function=None):
    """
    Decorator to check if the user is a superuser.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url='error_page',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator