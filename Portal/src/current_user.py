from threading import local
from django.utils.deprecation import MiddlewareMixin

# Thread-local storage for storing user instance per request thread
_user = local()

class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware to store the current user in thread-local storage.
    Allows access to the authenticated user from anywhere
    (like forms.py or models.py) without explicitly passing the request.
    """
    def process_request(self, request):
        _user.value = request.user


def get_current_user():
    """
    Retrieve the current user stored in the thread-local variable.
    Returns None if not found (e.g. outside request cycle).
    """
    try:
        return _user.value
    except AttributeError:
        return None


def reg_valid():
    """
    Placeholder function used for global context processors or quick registration flags.
    Currently, returns a simple dictionary with a true flag.
    """
    return {"flag": True}
