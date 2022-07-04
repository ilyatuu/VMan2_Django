from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from . forms import *
from django.contrib import messages


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def dashboardPage(request):
    template_name = 'dashboard/home.html'
    return render(request, template_name, {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageRole(request):
    if request.method == "POST" and "save_role" in request.POST:
        form = UserRoleForm(request.POST or None)
        if form.is_valid:
            form.save()
            messages.success(request, f"Role saved successfully")
            return redirect('dashboard:manageRole')
    form = UserRoleForm(request.POST or None)
    template_name = 'dashboard/addRole.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageICD10Category(request):
    if request.method == "POST" and "save_icd_10_category" in request.POST:
        form = ICD10CategoryForm(request.POST or None)
        if form.is_valid:
            form.save()
            messages.success(request, f"ICD-10 category saved successfully")
            return redirect('dashboard:manageICD10Category')
    form = ICD10CategoryForm(request.POST or None)
    template_name = 'dashboard/icd10Category.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageOrganization(request):
    if request.method == "POST" and "save_organization" in request.POST:
        form = OrganizationForm(request.POST or None)
        if form.is_valid:
            form.save()
            messages.success(request, f"Organization saved successfully")
            return redirect('dashboard:manageICD10Category')
    form = OrganizationForm(request.POST or None)
    template_name = 'dashboard/organization.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageICD10(request):
    if request.method == "POST" and "save_icd_10" in request.POST:
        form = ICD10ListForm(request.POST or None)
        if form.is_valid:
            form.save()
            messages.success(request, f"ICD-10 saved successfully")
            return redirect('dashboard:manageICD10')
    form = ICD10ListForm(request.POST or None)
    template_name = 'dashboard/icd10.html'
    context = {
        'form': form
    }
    return render(request, template_name, context)
