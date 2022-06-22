from django.shortcuts import render

# Create your views here.
def dashboardPage(request):
    template_name = 'dashboard/home.html'
    return render(request, template_name, {})
