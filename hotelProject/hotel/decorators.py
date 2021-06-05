from django.shortcuts import redirect

def staff_login_required(job_titles=['S', 'M', 'R', 'HS', 'RS']):
    def decorator(view_func):
        def wrapper(request, login_url='loginstaff', *args, **kwargs):
            if (
                    not 'staff_id' in request.session and
                    not 'job_title' in request.session and
                    request.session['job_title'] not in job_titles
                ):
                return redirect(login_url)
            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def customer_login_required(function):
    def wrapper(request, login_url='login', *args, **kwargs):
        if not 'customer_id' in request.session:
            return redirect(login_url)
        else:
            return function(request, *args, **kwargs)
    return wrapper

