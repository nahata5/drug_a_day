from django.db import models

import requests
import json
# Create your models here.

class Drug(models.Model):
	generic_name = models.CharField(max_length=200, unique=True)
	active_met = []
	ci = []
	induces = []
	inhibit = []
	may_diagnose = []
	may_prevent = []
	may_treat = []
	metabolized_by = []
	moa = []
	pe = []
	site_metabolize = []



	def __unicode__(self):
		return self.generic_name

	# may_prevent = mayPrevent(generic_name)
	# moa = hasMOA(generic_name)
	# pe = hasPE(generic_name)
	# ci = hasCI(generic_name)



