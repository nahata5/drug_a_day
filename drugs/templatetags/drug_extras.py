from django import template

register = template.Library()
from drugs.models import Drug
import requests
import json
import os
# Create your views here.

#Drug API Call
base_url = 'http://rxnav.nlm.nih.gov/REST/Ndfrt/'
headers = {'Accept': 'application/json','content-type': 'application/json'}
def SearchDrug(drug, kind):
    search_url = '%ssearch?conceptName=%s&kindName=%s' % (base_url, drug, kind)
    return requests.get(search_url, headers=headers).json()

def DrugInfo(drug):
    nui = SearchDrug(drug, 'DRUG_KIND')['groupConcepts'][0]['concept'][0]['conceptNui']
    search_url = '%sallInfo/%s' % (base_url, nui)
    return requests.get(search_url, headers=headers).json()

def mayTreat(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_indication = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'may_treat {NDFRT}':
            drug_indication.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_indication

def mayPrevent(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_prevent = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'may_prevent {NDFRT}':
            drug_prevent.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_prevent

def hasPE(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_effect = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'has_PE {NDFRT}':
            drug_effect.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_effect

def hasMOA(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_moa = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'has_MoA {NDFRT}':
            drug_moa.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_moa

def hasCI(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_ci = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'CI_with {NDFRT}':
            drug_ci.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_ci
#End API Calls

@register.inclusion_tag('drugs/pe.html')
def show_pe(drug):
	pe = hasPE(drug)
	return {'pe': pe}

@register.inclusion_tag('drugs/ci.html')
def show_ci(drug):
	ci = hasCI(drug)
	return {'ci': ci}

@register.inclusion_tag('drugs/may_treat.html')
def show_may_treat(drug):
	may_treat = mayTreat(drug)
	return {'may_treat': may_treat}

@register.inclusion_tag('drugs/may_prevent.html')
def show_may_prevent(drug):
	may_prevent = mayPrevent(drug)
	return {'may_prevent': may_prevent}

@register.inclusion_tag('drugs/moa.html')
def show_moa(drug):
	moa = hasMOA(drug)
	return {'moa': moa}
