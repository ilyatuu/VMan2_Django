from django.shortcuts import render

# Create your views here.
def loginPage(request):
    template_name = 'authentication/login.html'
    return render(request, template_name, {})
