from django.contrib import admin
from dorkdoc.models import *

class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['medical_record_number', 'first_name', 'last_name']}),
        ('Date Information', {'fields': ['created_date', 'last_modified_date']})
    ]
    # this controls what fields are shown when viewing the existing patients in the admin interface
    # it has the comma at the end because it needs to be a tuple
    list_display = ('medical_record_number',)

class FormAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['patient', 'date_of_visit', 'start_time_of_visit', 'end_time_of_visit']}),
        ('Date Information', {'fields': ['created_date', 'last_modified_date']}),
        ('Vitals',           {'fields': ['temp', 'pulse_apical', 'pulse_radial', 'respirations', 'blood_pressure', 
                                         'weight_actual', 'weight_reported']}),
        ('Visit',            {'fields': ['visit_regular', 'visit_prn', 'visit_high_tech']}),
        ('Homebound Status', {'fields': ['homebound_shortness', 'homebound_req_wheel_chair',
                                         'homebound_req_walker', 'homebound_req_cane', 'homebound_req_crutches',
                                         'homebound_stairs', 'homebound_poor_endurance']}),
        ('SA Cardio',        {'fields': ['cardio_wnl', 'pulses_regular', 'pulses_irregular', 'pulses_weak',
                                         'pulses_strong', 'pulses_bounding', 'edema_pitting',
                                         'edema_nonpitting', 'edema_plus1', 'edema_plus2', 'edema_plus3',
                                         'edema_plus4']}),
        ('SA Gastro',        {'fields': ['gastro_wnl', 'gastro_last_bm', 'gastro_ruq', 'gastro_luq',
                                         'gastro_rlq', 'gastro_llq', 'appetite']})
    ]
    list_display = ('patient', 'date_of_visit')

admin.site.register(Patient, PatientAdmin)
admin.site.register(Form, FormAdmin)
