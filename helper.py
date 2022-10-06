
# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from vman_dboard.models import SubmissionDefs
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import xml.etree.ElementTree as ET

from django.conf import settings
import os

dict_data = {}

# option 1
def index(request):
    return HttpResponse("Hellow, world!")

# option 2
def dashboard(request):
    records = SubmissionDefs.objects.all()
    json_array = []
    for record in records :
        rec_xml = record.xml
        odk_xml = BeautifulSoup(record.xml,"xml")
        jobj = {
            "id":record.id,
            "xml":record.xml,
            "region":odk_xml.find('Id10005R').text,
            "district":odk_xml.find('Id10005D').text,
            "ward":odk_xml.find('Id10005W').text
        }
        json_array.append(jobj)

    create_json_va(rec_xml)

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
    return render(request, "index.html", context)


# custom method
def create_json_va(xml):
    # Read dictionary file. We'll probably need to read this once
    with open(os.path.join(settings.BASE_DIR, 'static/data/dictionary2.json')) as dict_file:
        dict_data = json.load(dict_file)
        #print(dict_data)
        #print(dict_data["Id10002_lab_en"])
        #print(dict_data["start-time"])
        #print(type(dict_data))
        #print(dict_data.get("start-time"))

    # Prepare json output
    json_arr = []
    e = ET.ElementTree(ET.fromstring(xml))
    for elt in e.iter():
        if elt.tag == dict_data["start-time"]:
            json_obj = {
                    "id":elt.tag,
                    "value":elt.text,
                    "label_en":dict_data["start-time_lab_en"],
                    "label_sw":dict_data["start-time_lab_sw"]
                }
            json_arr.append(json_obj)

        if elt.tag == dict_data["end"]:
            json_obj = {
                    "id":elt.tag,
                    "value":elt.text,
                    "label_en":dict_data["end_lab_en"],
                    "label_sw":dict_data["end_lab_sw"]
                }
            json_arr.append(json_obj)
        if elt.tag == dict_data["today"]:
            json_obj = {
                    "id":elt.tag,
                    "value":elt.text,
                    "label_en":dict_data["today_lab_en"],
                    "label_sw":dict_data["today_lab_sw"]
                }
            json_arr.append(json_obj)
        if elt.tag == dict_data["deviceid"]:
            json_obj = {
                    "id":elt.tag,
                    "value":elt.text,
                    "label_en":dict_data["deviceid_lab_en"],
                    "label_sw":dict_data["deviceid_lab_sw"]
                }
            json_arr.append(json_obj)
        if elt.tag == dict_data["phonenumber"]:
            json_obj = {
                    "id":elt.tag,
                    "value":elt.text,
                    "label_en":dict_data["phonenumber_lab_en"],
                    "label_sw":dict_data["phonenumber_lab_sw"]
                }
            json_arr.append(json_obj) 
        if elt.tag == dict_data["Id10002"]:
            json_obj = {
                    "id":elt.tag,
                    "value":elt.text,
                    "label_en":dict_data["Id10002_lab_en"],
                    "label_sw":dict_data["Id10002_lab_sw"]
                }
            json_arr.append(json_obj) 
        if elt.tag == dict_data["Id10003"]:
            json_obj = {
                    "id":elt.tag,
                    "value":elt.text,
                    "label_en":dict_data["Id10003_lab_en"],
                    "label_sw":dict_data["Id10003_lab_sw"]
                }
            json_arr.append(json_obj)        
    print(json_arr)
    return json_arr
       