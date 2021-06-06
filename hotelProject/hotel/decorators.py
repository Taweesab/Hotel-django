from django.shortcuts import redirect

def staff_login_required(job_titles=['S', 'M', 'R', 'HS', 'RS']):
    def decorator(view_func):
        def wrapper_func(request, login_url='login', *args, **kwargs):
            if (
                    False
                ):
                return redirect(login_url)
            else:
                return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def customer_login_required(function):
    def wrapper(request, login_url='login', *args, **kwargs):
        if not 'staff_id' in request.session:
            return redirect(login_url)
        else:
            return function(request, *args, **kwargs)
    return wrapper

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            role = None
            if request.user.job_title != None :
                role = request.user.job_title

            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('/')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function