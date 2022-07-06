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
    get_role = UserRole.objects.all().order_by('role_name')
    form = UserRoleForm(request.POST or None)
    template_name = 'dashboard/addRole.html'
    context = {
        'form': form,
        'get_role': get_role
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
    get_icd_10_category = ICD10Category.objects.all().order_by('icd10_category_name')
    form = ICD10CategoryForm(request.POST or None)
    template_name = 'dashboard/icd10Category.html'
    context = {
        'form': form,
        'get_icd_10_category': get_icd_10_category
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
            return redirect('dashboard:manageOrganization')
    get_organization = Organization.objects.all().order_by('organization_name')
    form = OrganizationForm(request.POST or None)
    template_name = 'dashboard/organization.html'
    context = {
        'form': form,
        'get_organization': get_organization
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
    get_icd10_list = ICD10List.objects.all().order_by('icd10_code')
    form = ICD10ListForm(request.POST or None)
    template_name = 'dashboard/icd10.html'
    context = {
        'form': form,
        'get_icd10_list': get_icd10_list
    }
    return render(request, template_name, context)
