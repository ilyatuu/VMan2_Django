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
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import threading
import shortuuid
from dashboard.models_crvs_2 import *
from .forms import *
import xmltodict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from itertools import chain

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

        get_user_region = request.POST.get('user_region')

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
                profile.region = get_user_region
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
        get_data_from_crvs = SubmissionDefs.objects.all()
        my_crvs_data = []
        for xml_data in get_data_from_crvs:
            new_data_xml = xml_data.xml
            soup = BeautifulSoup(new_data_xml,"xml")
            get_region = soup.find('Id10005R').text

            my_data_dict = {
                'get_region': get_region,
            }
            my_crvs_data.append(my_data_dict)
        print(my_crvs_data)
        # print(my_data_dict)
        #Get unique value from list (Distinct region)
        #--------------------------------------------------
        #
        # extracted_my_crvs_data = set(my_crvs_data)
        # new_my_crvs_data = list(extracted_my_crvs_data)
        #
        #---------------------------------------------------
        # response = set(chain.from_iterable(sub.values() for sub in my_crvs_data))
        # print(response)
        response_my_crvs_data = list({v['get_region']:v for v in my_crvs_data}.values())
        print(response_my_crvs_data)

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
        'get_users': get_users,
        'crvs_data': response_my_crvs_data
    }
    return render(request, 'authentication/addUser.html', context = context)



def activate(request, uidb64, token, ext):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f"Your account has been activated.")
        return redirect('authentication:loginPage')
    else:
        return HttpResponse('Activation link is invalid!')
