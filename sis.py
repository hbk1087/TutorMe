import requests
import json

base_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'

term = '1' + '23' + '6'

base_url = base_url + '&term=' + term

page = '4'

hello= "world"

base_url = base_url + '&page=' + page

# subject = 'CS'

# base_url = base_url + '&subject=' + subject

# catalog_nbr = '3240'

# base_url = base_url + '&catalog_nbr=' + catalog_nbr

url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&page=1'

# for c in clist:
#     r = requests.get(url + '&subject=' + c[0] + '&catalog_nbr=' + c[1])
#     for c in r.json():
#         print(c['subject'], c['catalog_nbr'] + '-' + c['class_section'], c['component'], c['descr'], \
#                 c['class_nbr'], c['class_capacity'], c['enrollment_available'])

r = requests.get(base_url)
for c in r.json():
    print(c['subject'], c['catalog_nbr'], c['instructors'])