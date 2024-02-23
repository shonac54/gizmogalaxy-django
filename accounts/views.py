from django.shortcuts import render,redirect
from .forms import Registrationform
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



#Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart,CartItem





#register
def register(request):
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please activate your account "
            message      = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to={to_email})
            send_email.send()

            #messages.success(request,'Thank youfor registering with us.We have sent you a verification email to your email address.Please verify it.')
            return redirect('/accounts/login/?command=verification&email=' +email)



    else:
        form = Registrationform()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()

            except:
                pass

            auth.login(request, user)
            # messages.success(request,"You are now logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')





@login_required(login_url='login')
def logout(request):

    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('login')

    
def activate(request,uidb64,token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! Your account is activated ')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')



@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)



            #Forgot password email
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password "
            message      = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to={to_email})
            send_email.send()


            messages.success(request,'password reset email has been sent to your email address')
            return redirect('login')
        
        else:
            messages.error(request,'Account does not exists')
            return redirect('forgotPassword')


    return render(request,'accounts/forgotPassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password )
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('login')

        else:
            messages.error(request,'Password do not match!')
            return redirect('resetPassword')
        
    else:
        return render(request,'accounts/resetPassword.html')


    

def admin_home(request):
    return render(request, 'admin_home.html')
from django.contrib.auth import authenticate
   
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')  # Adjusted to match the form field name
        password = request.POST.get('pwd')   # Adjusted to match the form field name

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Assuming you have a user object, you can use login()
            login(request, user)
            return redirect('admin_home')  # Redirect to the admin home page after successful login
        else:
            # Handle invalid login credentials
            return render(request, 'accounts/admin_login.html', {'error': 'yes'})

    return render(request, 'accounts/admin_login.html')



def admin_dashboard_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You are not logged in.')
        return redirect('admin_login')

    return render(request, 'accounts/admin_dashboard.html')

def admin_logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('admin_login')

from django.shortcuts import render
from .models import Account

def registered_users_view(request):
    users = Account.objects.all()
    context = {'users': users}
    return render(request, 'user_table.html', context)