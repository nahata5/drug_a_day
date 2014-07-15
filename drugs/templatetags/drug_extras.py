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

def Inhibited(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_inhibited_by = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'effect_may_be_inhibited_by {NDFRT}':
            drug_inhibited_by.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_inhibited_by

def activeMET(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_active_met = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'has_active_metabolites {NDFRT}':
            drug_active_met.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_active_met

def induces(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_induces = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'induces {NDFRT}':
            drug_induces.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_induces

def mayDiagnose(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_may_diagnose = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'may_diagnose {NDFRT}':
            drug_may_diagnose.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_may_diagnose

def metabolizedBy(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_metabolized_by = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'metabolized_by {NDFRT}':
            drug_metabolized_by.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_metabolized_by

def siteMetabolize(drug):
    drug_roles = DrugInfo(drug)['fullConcept']['groupRoles'][0]['role']
    drug_site_metabolize = []
    for i in range(0, len(drug_roles)):
        if drug_roles[i]['roleName'] == 'site_of_metabolism {NDFRT}':
            drug_site_metabolize.append(drug_roles[i]['concept'][0]['conceptName'])
    return drug_site_metabolize


# def api_call(drug):
#     active_met.append(activeMET(drug))
#     ci.append(hasCI(drug))
#     induces.append(Induces(drug))
#     inhibit.append(Inhibited(drug))
#     may_diagnose.append(mayDiagnose(drug))
#     may_prevent.append(mayPrevent(drug))
#     may_treat.append(mayTreat(drug))
#     metabolized_by.append(metabolizedBy(drug))
#     moa.append(hasMOA(drug))
#     pe.append(hasPE(drug))
#     site_metabolize.append(siteMetabolize(drug))

#End API Calls



#Day Template Register


# @register.inclusion_tag('drugs/yesterday.old.html')
# def show_yesterday():
# 	# drug_yesterday = Drug.objects.get(pk=2)
# 	# return {
# 	# 'day': 'yesterday',
# 	# 'drug_yesterday': drug_yesterday}

# @register.inclusion_tag('drugs/last_week.old.html')
# def show_last_week():
# 	drug_last_week = Drug.objects.get(pk=3)
# 	return {
# 	'day': 'last_week',
# 	'drug_last_week': drug_last_week}

@register.inclusion_tag('drugs/today.old.html')
def show_button(day):
    if day == 'today':
       drug_today = Drug.objects.get(pk=1)
       return {
       'day': day,
       'drug_today': drug_today}
    elif day == 'yesterday':
        drug_yesterday = Drug.objects.get(pk=2)
        return {
        'day': day,
        'drug_today': drug_yesterday}
    else:
        drug_last_week = Drug.objects.get(pk=3)
        return {
        'day': day,
        'drug_today': drug_last_week}





#Drug Call Template Registration
@register.inclusion_tag('drugs/api_calls/pe.html')
def show_pe(drug, day):
	pe = hasPE(drug)
	return {
    'day': day,
	# 'menu_title': 'Physiological Effects:',
	'pe': pe}

@register.inclusion_tag('drugs/api_calls/ci.html')
def show_ci(drug, day):
	ci = hasCI(drug)
	if ci:
		return {
        'day': day,
		'menu_title': 'Contraindications:',
		'ci': ci}

@register.inclusion_tag('drugs/api_calls/may_treat.html')
def show_may_treat(drug, day):
	may_treat = mayTreat(drug)
	return {
    'day': day,
	'menu_title': 'May Treat:',
	'may_treat': may_treat}

@register.inclusion_tag('drugs/api_calls/may_prevent.html')
def show_may_prevent(drug, day):
	may_prevent = mayPrevent(drug)
	if may_prevent:
		return {
        'day': day,
		'menu_title': 'May Prevent:',
		'may_prevent': may_prevent}

@register.inclusion_tag('drugs/api_calls/may_diagnose.html')
def show_may_diagnose(drug, day):
	may_diagnose = mayDiagnose(drug)
	if may_diagnose:
		return {
        'day': day,
		'menu_title': 'May Diagnose:',
		'may_diagnose': may_diagnose}

@register.inclusion_tag('drugs/api_calls/moa.html')
def show_moa(drug, day):
	moa = hasMOA(drug)
	if moa:
		return {
        'day': day,
		'menu_title': 'Mechanism of Action:',
		'moa': moa}

@register.inclusion_tag('drugs/api_calls/inhibit.html')
def show_inhibit(drug, day):
	inhibit = Inhibited(drug)
	if inhibit:
		return {'day': day,
		'menu_title': 'Inhibited by:',
		'inhibit': inhibit}

@register.inclusion_tag('drugs/api_calls/active_met.html')
def show_active_met(drug, day):
	active_met = activeMET(drug)
	if active_met:
		return {
        'day': day,
		'menu_title': 'Active Metabolites:',
		'active_met': active_met}

@register.inclusion_tag('drugs/api_calls/induces.html')
def show_induces(drug, day):
	drug_induces = induces(drug)
	if drug_induces:
		return {
        'day': day,
		'menu_title': 'May Induce:',
		'drug_induces': drug_induces}

@register.inclusion_tag('drugs/api_calls/metabolized_by.html')
def show_metabolized_by(drug, day):
	metabolized_by = metabolizedBy(drug)
	if metabolized_by:
		return {
        'day': day,
		'menu_title': 'Metabolized by:',
		'metabolized_by': metabolized_by}

@register.inclusion_tag('drugs/api_calls/site_metabolize.html')
def show_site_metabolize(drug, day):
    site_metabolize = siteMetabolize(drug)
    if site_metabolize:
        return {
        'day': day,
        'menu_title': 'Site of Metabolism',
        'site_metabolize': site_metabolize}




