from functools import wraps

from django.http import Http404


def post_only(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            return fn(request, *args, **kwargs)
        raise Http404
    return wrapper