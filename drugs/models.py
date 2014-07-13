from django.db import models

import requests
import json
# Create your models here.

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


class Drug(models.Model):
	generic_name = models.CharField(max_length=200, unique=True)
	may_treat = []
	def __unicode__(self):
		return self.generic_name

	# may_prevent = mayPrevent(generic_name)
	# moa = hasMOA(generic_name)
	# pe = hasPE(generic_name)
	# ci = hasCI(generic_name)



