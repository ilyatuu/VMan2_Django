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
        if form.is_valid():
            form.save()
            messages.success(request, f"Role saved successfully")
            return redirect('dashboard:manageRole')
    get_role = UserRole.objects.all().order_by('role_name')
    form = UserRoleForm()
    template_name = 'dashboard/addRole.html'
    context = {
        'form': form,
        'get_role': get_role
    }
    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def updateRole(request, id):
    get_role_to_update = get_object_or_404(UserRole, pk = id)
    form = UserRoleForm(request.POST or None, instance = get_role_to_update)
    if request.method == "POST" and "update_role" in request.POST:
        form = UserRoleForm(request.POST or None, instance = get_role_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f"Role updated successfully")
            return redirect('dashboard:manageRole')
    get_role = UserRole.objects.all().order_by('role_name')
    template_name = 'dashboard/addRole.html'
    context = {
        'form': form,
        'get_role': get_role,
        'get_role_to_update': get_role_to_update,
    }
    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageICD10Category(request):
    if request.method == "POST" and "save_icd_10_category" in request.POST:
        form = ICD10CategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, f"ICD-10 category saved successfully")
            return redirect('dashboard:manageICD10Category')
    get_icd_10_category = ICD10Category.objects.all().order_by('icd10_category_name')
    form = ICD10CategoryForm()
    template_name = 'dashboard/icd10Category.html'
    context = {
        'form': form,
        'get_icd_10_category': get_icd_10_category
    }
    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def updateICD10Category(request, id):
    get_icd10_to_update = get_object_or_404(ICD10Category, pk = id)
    form = ICD10CategoryForm(request.POST or None, instance = get_icd10_to_update)
    if request.method == "POST" and "update_icd_10_category" in request.POST:
        form = ICD10CategoryForm(request.POST or None, instance = get_icd10_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f"ICD-10 category updated successfully")
            return redirect('dashboard:manageICD10Category')
    get_icd_10_category = ICD10Category.objects.all().order_by('icd10_category_name')
    template_name = 'dashboard/icd10Category.html'
    context = {
        'form': form,
        'get_icd_10_category': get_icd_10_category,
        'get_icd10_to_update': get_icd10_to_update
    }
    return render(request, template_name, context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageOrganization(request):
    if request.method == "POST" and "save_organization" in request.POST:
        form = OrganizationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, f"Organization saved successfully")
            return redirect('dashboard:manageOrganization')
    get_organization = Organization.objects.all().order_by('organization_name')
    form = OrganizationForm()
    template_name = 'dashboard/organization.html'
    context = {
        'form': form,
        'get_organization': get_organization
    }
    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def updateOrganization(request, id):
    get_organization_to_update = get_object_or_404(Organization, pk = id)
    form = OrganizationForm(request.POST or None, instance = get_organization_to_update)
    if request.method == "POST" and "update_organization" in request.POST:
        form = OrganizationForm(request.POST or None, instance = get_organization_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f"Organization updated successfully")
            return redirect('dashboard:manageOrganization')
    get_organization = Organization.objects.all().order_by('organization_name')
    template_name = 'dashboard/organization.html'
    context = {
        'form': form,
        'get_organization': get_organization,
        'get_organization_to_update': get_organization_to_update
    }
    return render(request, template_name, context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageICD10(request):
    if request.method == "POST" and "save_icd_10" in request.POST:
        form = ICD10ListForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, f"ICD-10 saved successfully")
            return redirect('dashboard:manageICD10')
    get_icd10_list = ICD10List.objects.all().order_by('icd10_code')
    form = ICD10ListForm()
    template_name = 'dashboard/icd10.html'
    context = {
        'form': form,
        'get_icd10_list': get_icd10_list
    }
    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def updateICD10List(request, id):
    get_icd10_list_to_update = get_object_or_404(ICD10List, pk = id)
    form = ICD10ListForm(request.POST or None, instance = get_icd10_list_to_update)
    if request.method == "POST" and "update_icd_10" in request.POST:
        form = ICD10ListForm(request.POST or None, instance = get_icd10_list_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f"ICD10 updated successfully")
            return redirect('dashboard:manageICD10')
    get_icd10_list = ICD10List.objects.all().order_by('icd10_code')
    template_name = 'dashboard/icd10.html'
    context = {
        'form': form,
        'get_icd10_list': get_icd10_list,
        'get_icd10_list_to_update': get_icd10_list_to_update
    }
    return render(request, template_name, context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageCSMFDataset(request):
    if request.method == "POST" and "process_csmf_dataset_button" in request.POST:
        form = CSMFDataForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print("*******************************************")
            print("Perform data manipulation and ML model here")
            print("*******************************************")
            messages.success(request, f"CSMF Dataset submitted for proccessing")
            return redirect('dashboard:manageCSMFDataset')
        else:
            messages.error(request, f"CSMF Dataset submission failed")
            return redirect('dashboard:manageCSMFDataset')
    form = CSMFDataForm()
    template_name = 'dashboard/csmfData.html'
    context = {
        'form': form,
    }
    return render(request, template_name, context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageAuthorization(request):
    if request.method == "POST" and "authorize_user_button" in request.POST:
        form = AuthorizationForm(request.POST or None)
        # print(form.data['authorize_user'])
        if form.is_valid():
            form.save()
            messages.success(request, f"User authorised successfully successfully")
            return redirect('dashboard:manageAuthorization')
        else:
            messages.error(request, f"User authorization failed")
            # print(form.errors)
            return redirect('dashboard:manageAuthorization')
    form = AuthorizationForm()
    get_authorization_list = Authorization.objects.all().order_by('authorize_user')
    template_name = 'dashboard/authorised.html'
    context = {
        'form': form,
        'get_authorization_list': get_authorization_list
    }
    return render(request, template_name, context)
