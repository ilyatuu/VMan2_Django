from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from . forms import *


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def dashboardPage(request):
    template_name = 'dashboard/home.html'
    return render(request, template_name, {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageRole(request):
    form = UserRoleForm(request.POST or None)
    template_name = 'dashboard/addRole.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageICD10Category(request):
    form = ICD10CategoryForm(request.POST or None)
    template_name = 'dashboard/icd10Category.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageOrganization(request):
    form = OrganizationForm(request.POST or None)
    template_name = 'dashboard/organization.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageICD10(request):
    form = ICD10ListForm(request.POST or None)
    template_name = 'dashboard/icd10.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)
