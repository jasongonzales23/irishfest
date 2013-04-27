from django.core.management import call_command, setup_environ
from inventory import settings
from datetime import datetime
from datetime import date

setup_environ(settings)

DJANGO_SETTINGS_MODULE=irishfest.settings

CURR_DATETIME = 'fishies' #date.today()

output_filename = CURR_DATETIME 
output = open(output_filename, 'w')

call_command('dumpdata', 'inventory', format='json', indent=4, stdout=output)
output.close()
#manage.py dumpdata inventory auth --indent 4 > BACKUP_FILENAME

