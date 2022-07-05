from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tokens import account_activation_token
import threading
import shortuuid

from .forms import *

# Create your views here.
# This class used to process email faster
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently = False)

### Login page logic goes here
def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        valuenext= request.POST.get('next')
        ### Check if username and password are provided
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            ### query from the database by comparing the existing user
            user = authenticate(username=username, password=password)
            if user is not None and valuenext == '':
                login(request, user)
                ### after login redirect user to the dashboard page
                return redirect('dashboard:dashboardPage')
            if user is not None and valuenext != '':
                login(request, user)
                messages.success(request, f"Hi {username}, wellcome back")
                return redirect(request.GET.get('next'))
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request = request, template_name = "authentication/login.html", context = context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def addNewUser(request):
    if request.method == 'POST':
        form = SignupForm(request.POST or None)
        form_profile = ProfileForm(request.POST or None)
        get_email = request.POST.get('email')
        get_fname = request.POST.get('first_name')
        get_lname = request.POST.get('last_name')
        full_name = get_fname+ ' ' + get_lname
        new_full_name = full_name.capitalize()

        user_token_1 = shortuuid.ShortUUID(shortuuid.get_alphabet())
        user_generated_token = user_token_1.random(length=100)
        required_user_token = user_generated_token

        print(form.is_valid())
        print(form_profile.errors)
        if form.is_valid() and form_profile.is_valid():
            user = form.save(commit=False)
            user.username = get_email
            user.is_active = False

            if User.objects.filter(email = get_email).exists():
                messages.error(request, f"This user already taken, please try again")
                return redirect('authentication:addNewUser')
            else:
                user.save()
                profile = form_profile.save(commit = False)
                profile.user = user
                profile.user_token = required_user_token
                profile.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your vman account'
                html_content = render_to_string('emailFolder/account_activation_email.html', {
                    'user': new_full_name,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'extra_token': required_user_token,
                    'token':account_activation_token.make_token(user),
                })
                text_content = strip_tags(html_content)
                email_from = settings.EMAIL_HOST_USER
                to_email = [get_email]
                email = EmailMultiAlternatives(
                    mail_subject, text_content, settings.EMAIL_HOST_USER, to_email
                )
                email.attach_alternative(html_content, "text/html")
                EmailThread(email).start()
                messages.success(request, f"New account has been created")
                return redirect('authentication:addNewUser')
                # return HttpResponse('<center>Please confirm your email address to complete the registration</center>')
        else:
            messages.warning(request, f"Sorry, failed to create account")
            return redirect('authentication:addNewUser')
    else:
        form = SignupForm()
        form_profile = ProfileForm()
        user_token_1 = shortuuid.ShortUUID(shortuuid.get_alphabet())
        get_users = User.objects.all().order_by('first_name', 'last_name')
        user_generated_token = user_token_1.random(length=100)
        required_user_code = user_generated_token
        print(required_user_code)
    context = {
        'form': form,
        'form_profile': form_profile,
        'get_users': get_users
    }
    return render(request, 'authentication/addUser.html', context = context)
