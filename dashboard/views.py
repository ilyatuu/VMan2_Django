from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from . forms import *
# from . models_crvs import *
from . models_crvs_2 import *
import plotly.express as px
# from VMAN_V2.models import *
from django.contrib import messages
import json
import xmltodict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
import pandas as pd
from . helper import create_json_va
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def dashboardPage(request):
    get_auth = Authorization.objects.get(authorize_user = request.user)
    get_user = request.user.username
    get_user_region = request.user.profile.region
    # print(get_user)
    # print(get_user_region)
    if get_auth.dashboard:
        records = SubmissionDefs.objects.all()
        records_count = SubmissionDefs.objects.all().count()
        json_array = []
        get_adult_ = []
        get_child_ = []
        get_neonatal_ = []
        for record in records :
            rec_xml = record.xml
            odk_xml = BeautifulSoup(record.xml,"xml")

            isAdult = odk_xml.find('isAdult').text
            isChild = odk_xml.find('isChild').text
            isNeonate = odk_xml.find('isNeonatal').text

            age_group = "none"
            if isAdult == "1":
                age_group = "Adult"
                get_adult_.append(age_group)
            if isChild == "1":
                age_group = "Child"
                get_child_.append(age_group)
            if isNeonate == "1":
                age_group = "Neonate"
                get_neonatal_.append(age_group)

            jobj = {
                "id":record.id,
                "xml":record.xml,
                "region":odk_xml.find('Id10005R').text,
                "district":odk_xml.find('Id10005D').text,
                "ward":odk_xml.find('Id10005W').text,
                "dec_sex":odk_xml.find('Id10019').text,
                "dec_agegroup":age_group,
                "int_date":odk_xml.find('today').text
            }
            json_array.append(jobj)

        #print(json_array)
        df = pd.DataFrame(json_array)
        get_region = df['region'].value_counts()


        get_only_region_age_df = df[['region','dec_agegroup']]
        get_only_region_age_df_stack = get_only_region_age_df.groupby(['region','dec_agegroup']).size().reset_index(name='counts')
        # print(get_only_region_age_df_stack)

        fig_region_age = px.bar(
            get_only_region_age_df_stack,
            x = 'region',
            y = 'counts',
            color = 'dec_agegroup',
            barmode = 'stack',
            title = "Distribution of number of deceased by age group",
            template = "ggplot2",
        )
        fig_region_age.update_layout(title={
            'font_size':20,
            'xanchor': 'center',
            'x': 0.5
        })
        region_age_chart = fig_region_age.to_html()

        fig = px.bar(
            get_region,
            title = "Distribution of number of VA entered by region",
            labels = {'index':'Regions', 'value':'Number of VA'},
            template = "ggplot2",
        )
        fig.update_layout(title={
            'font_size':20,
            'xanchor': 'center',
            'x': 0.5
        }, showlegend=False)
        region_chart = fig.to_html()


        template_name = 'dashboard/home.html'
        context = {
            'va_total':records_count,
            'get_adult_number': len(get_adult_),
            'get_child_number': len(get_child_),
            'get_neonatal_number': len(get_neonatal_),
            'chart': region_chart,
            'region_age_chart': region_age_chart,
        }
        return render(request, template_name, context = context)

############# Test pulling data with external object
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def vaRecordsPage(request):
    records = SubmissionDefs.objects.all()
    json_array = []
    for record in records :
        rec_xml = record.xml
        odk_xml = BeautifulSoup(record.xml,"xml")

        isAdult = odk_xml.find('isAdult').text
        isChild = odk_xml.find('isChild').text
        isNeonate = odk_xml.find('isNeonatal').text

        age_group = "none"
        if isAdult == "1":
            age_group = "Adult"
        if isChild == "1":
            age_group = "Child"
        if isNeonate == "1":
            age_group = "Neonate"

        jobj = {
            "id":record.id,
            "xml":record.xml,
            "region":odk_xml.find('Id10005R').text,
            "district":odk_xml.find('Id10005D').text,
            "ward":odk_xml.find('Id10005W').text,
            "dec_sex":odk_xml.find('Id10019').text,
            "dec_agegroup":age_group,
            "int_date":odk_xml.find('today').text
        }
        json_array.append(jobj)

    #print(json_array)
    df = pd.DataFrame(json_array)
    reg = df['region'].value_counts()

    # print(df)

    # Pagination
    paginator = Paginator(json_array,10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "page_obj":page_obj
    }
    return render(request, "dashboard/vaRecord.html", context)



# custom method
def render_va1(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            xml = request.POST['data']
            # print(xml)
            json_va = create_json_va(xml)
            return JsonResponse({'context': json_va})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

def create_json_va(xml):
    # Read dictionary file. We'll probably need to read this once
    with open('dashboard/dictionary.json') as dict_file:
        global dict_data
        dict_data = json.load(dict_file)

        # Prepare json output
        json_arr = []
        e = ET.ElementTree(ET.fromstring(xml))
        for elt in e.iter():
            json_obj = get_va_obj(elt.tag,elt.text)
            if json_obj:
                json_arr.append(json_obj)
        return json_arr

def get_va_obj(qn_id,qn_text):
    for qn in dict_data:
        if qn['id'].upper() == qn_id.upper():
            jobj = {
                "id":qn_id,
                "value":qn_text,
                "label_en":qn['label_en'],
                "label_sw":qn['label_sw']
            }
            return jobj
#######################################################

#######################################################
### Analysis page goes here
#######################################################
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageAnalysisPage(request):
    records = SubmissionDefs.objects.all()
    json_array = []
    for record in records :
        rec_xml = record.xml
        odk_xml = BeautifulSoup(record.xml,"xml")

        isAdult = odk_xml.find('isAdult').text
        isChild = odk_xml.find('isChild').text
        isNeonate = odk_xml.find('isNeonatal').text

        age_group = "none"
        if isAdult == "1":
            age_group = "Adult"
        if isChild == "1":
            age_group = "Child"
        if isNeonate == "1":
            age_group = "Neonate"

        jobj = {
            "id":record.id,
            "xml":record.xml,
            "region":odk_xml.find('Id10005R').text,
            "district":odk_xml.find('Id10005D').text,
            "ward":odk_xml.find('Id10005W').text,
            "dec_sex":odk_xml.find('Id10019').text,
            "dec_agegroup":age_group,
            "int_date":odk_xml.find('today').text
        }
        json_array.append(jobj)

    ### Generate dataframe for analysis
    df = pd.DataFrame(json_array)
    # print(df)

    template_name = 'dashboard/analysis.html'
    context = {
        #### All variables received here
        'df': df
    }
    return render(request, template_name, context)
#######################################################
### End of Analysis pape
#######################################################


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageRole(request):
    get_auth = Authorization.objects.get(authorize_user = request.user)
    if get_auth.system_role:
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
    else:
        return HttpResponseForbidden("You do not have permission to view this page")

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
    get_auth = Authorization.objects.get(authorize_user = request.user)
    if get_auth.icd_10_category:
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
    else:
        return HttpResponseForbidden("You do not have permission to view this page")


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
    get_auth = Authorization.objects.get(authorize_user = request.user)
    if get_auth.organization:
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
    else:
        return HttpResponseForbidden("You do not have permission to view this page")


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
    get_auth = Authorization.objects.get(authorize_user = request.user)
    if get_auth.icd_10_list:
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
    else:
        return HttpResponseForbidden("You do not have permission to view this page")


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
    get_auth = Authorization.objects.get(authorize_user = request.user)
    if get_auth.upload_csmf:
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
    else:
        return HttpResponseForbidden("You do not have permission to view this page")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageCodingWork(request):
    get_auth = Authorization.objects.get(authorize_user = request.user)
    if get_auth.coding_work:
        template_name = 'dashboard/codingWork.html'
        context = {}
        return render(request, template_name, context)
    else:
        return HttpResponseForbidden("You do not have permission to view this page")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def manageAuthorization(request):
    get_auth = Authorization.objects.get(authorize_user = request.user)
    if get_auth.user_authorization:
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
    else:
        return HttpResponseForbidden("You do not have permission to view this page")


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
