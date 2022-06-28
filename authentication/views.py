from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
import threading

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
