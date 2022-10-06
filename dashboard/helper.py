
# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from . models_crvs_2 import SubmissionDefs
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import xml.etree.ElementTree as ET

from django.conf import settings
import os

# dict_data = {}

# custom method
def create_json_va(xml):
    # Read dictionary file. We'll probably need to read this once
    with open('dashboard/dictionary.json') as dict_file:
        global dict_data
        dict_data = json.load(dict_file)

        # Prepare json output
        json_arr = []
        e = ET.ElementTree(ET.fromstring(xml))
        for elt in e.iter():
            json_obj = get_json_va(elt.tag,elt.text)
            if json_obj:
                json_arr.append(json_obj)
        return json_arr


def get_json_va(qn_id,qn_val):
    for qn in dict_data:
        if qn_id == qn['id']:
            json_obj = {
                "id":qn_id,
                "value":qn_text,
                "label_en":qn['label_en'],
                "label_sw":qn['label_sw']
            }
            return json_obj
