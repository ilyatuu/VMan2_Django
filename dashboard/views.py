from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from . forms import *
from . models_crvs import *
# from VMAN_V2.models import *
from django.contrib import messages
import json
import xmltodict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def dashboardPage(request):
    get_data_from_crvs = SubmissionDefs.objects.all()
    my_crvs_data = []
    for xml_data in get_data_from_crvs:
        new_data_xml = xml_data.xml
        soup = BeautifulSoup(new_data_xml)
        start_date = soup.find('start-time')
        end_date = soup.find('end')
        get_today = soup.find('today')
        get_instance_id = soup.find('instanceID')
        get_device_id = soup.find('deviceid')
        get_phonenumber = soup.find('phonenumber')
        get_into = soup.find('intro')
        get_respondent_background = soup.find('respondent_backgr')

        my_data_dict = {
            'start_date': start_date.text,
            'end_date': end_date.text,
            'today': get_today.text,
            'deviceid': get_instance_id,
            'phonenumber': get_phonenumber.text,
            'instanceID': get_instance_id,
            'intro_tag': get_into.text,
            'respondent_backgr': get_respondent_background
        }
        my_crvs_data.append(my_data_dict)
    print(my_crvs_data)


    template_name = 'dashboard/home.html'
    context = {
        'crvs_data_2': get_data_from_crvs,
        'crvs_data': my_crvs_data
    }
    return render(request, template_name, context = context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def vaRecordsPage(request):
    get_data_from_crvs = SubmissionDefs.objects.all()[:10]
    my_crvs_data = []
    print(type(get_data_from_crvs))
    #
    # Loop one record at a time
    # and extract data to create dictionary
    # for that record
    #
    for xml_data in get_data_from_crvs:
        new_data_xml = xml_data.xml
        soup = BeautifulSoup(new_data_xml,"xml")
        get_start_time = soup.find('start-time').text
        get_end_time = soup.find('end').text
        get_interview_date = soup.find('Id10012').text
        get_interview_end = soup.find('Id10481').text
        get_instance_id = soup.find('instanceID').text
        get_device_id = soup.find('deviceid')
        get_phonenumber = soup.find('phonenumber')
        get_serial_number = soup.find('D2SN').text
        get_respondent_background = soup.find('respondent_backgr')
        get_region = soup.find('Id10005R').text
        get_district = soup.find('Id10005D').text
        get_ward = soup.find('Id10005W').text
        get_interviwer_name = soup.find('Id10010').text
        get_interviwer_phone = soup.find("Id10010Phone").text
        get_interviwer_national_id = soup.find("Id10010c").text
        get_gps_space_string = soup.find('gps_location').text
        get_gps_location_in_list = list(get_gps_space_string.split(" "))
        get_death_narrative = soup.find('Id10476').text
        # get_gps_location_in_list = [get_gps_space_string]


        my_data_dict = {
            'get_start_time': get_start_time,
            'get_end_time': get_end_time,
            'get_interview_date': get_interview_date,
            'get_interview_end': get_interview_end,
            'deviceid': get_instance_id,
            'phonenumber': get_phonenumber.text,
            'get_serial_number': get_serial_number,
            'respondent_backgr': get_respondent_background,
            'get_region': get_region,
            'get_district': get_district,
            'get_ward': get_ward,
            'get_interviwer_name': get_interviwer_name,
            'get_interviwer_phone': get_interviwer_phone,
            'get_interviwer_national_id': get_interviwer_national_id,
            'get_gps_latitude': get_gps_location_in_list[0],
            'get_gps_longitude': get_gps_location_in_list[1],
            'get_gps_location': get_gps_location_in_list[-1],
            'get_death_narrative': get_death_narrative
        }
        my_crvs_data.append(my_data_dict)
    # print(my_crvs_data)
    print(my_data_dict)


    template_name = 'dashboard/vaRecord.html'
    context = {
        'crvs_data': my_crvs_data
    }
    return render(request, template_name, context)


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
def manageCodingWork(request):
    template_name = 'dashboard/codingWork.html'
    context = {}
    return render(request, template_name, context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageAuthorization(request):
    if request.method == "POST" and "authorize_user_button" in request.POST:
        form = AuthorizationForm(request.POST or None)
        # print(form.data['authorize_user'])
        if form.is_valid():
            form.save()
            messages.success(request, f"User authorised successfully")
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def updateAuthorization(request, id):
    get_action_to_update = get_object_or_404(Authorization, pk = id)
    form = AuthorizationForm(request.POST or None, instance = get_action_to_update)
    if request.method == "POST":
        form = AuthorizationForm(request.POST or None, instance = get_action_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f"User authorization updated successfully")
            return redirect('dashboard:manageAuthorization')
    get_authorization_list = Authorization.objects.all().order_by('authorize_user')
    template_name = 'dashboard/authorised.html'
    context = {
        'form': form,
        'get_authorization_list': get_authorization_list,
        'get_action_to_update': get_action_to_update
    }
    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def deleteAuthorization(request, id):
    get_action_to_delete = get_object_or_404(Authorization, pk = id)
    get_action_to_delete.delete()
    messages.success(request, f"User authorization deleted successfully")
    return redirect('dashboard:manageAuthorization')
