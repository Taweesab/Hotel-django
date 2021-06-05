from django.shortcuts import redirect

def staff_login_required(function,job_title=[("S", "Staff"),
        ("A", "Admin"),
        ("M", "Manager"),
        ("R", "Receptionist"),
        ("HS", "Hotel Staff"),
        ("RS", "Restaurant Staff"),]):
    def wrapper(request, login_url='login', *args, **kwargs):
        if not 'staff_id' in request.session:
            return redirect(login_url)
        else:
            return function(request, *args, **kwargs)
    return wrapper

def customer_login_required(function):
    def wrapper(request, login_url='login', *args, **kwargs):
        if not 'customer_id' in request.session:
            return redirect(login_url)
        else:
            return function(request, *args, **kwargs)
    return wrapper

