# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

# we use this as the base for all our objects since we want every object to have these
# two audit fields - created date and last modified date
class Base(polymodel.PolyModel):
    created_date = db.DateTimeProperty(auto_now_add=True)
    last_modified_date = db.DateTimeProperty(auto_now=True)
    
# this contains all the information about a particular patient
class Patient(Base):
    # the medical record number of a patient. I assume it is alphanumeric.
    medical_record_number = db.StringProperty(required=True, multiline=False)
    # first name of a patient
    first_name = db.StringProperty(required=True, multiline=False)
    # last name of a patient
    last_name = db.StringProperty(required=True, multiline=False)

# this contains all the information about a particular instance of a form
class Form(Base):
    # this is the foreign key to the patient the form is about
    patient = db.ReferenceProperty(Patient, required=True)
    # the date of the patient visit
    date_of_visit = db.DateProperty(required=True)
    # the start time of the patient visit
    start_time_of_visit = db.TimeProperty(required=True)
    # the end time of the patient visit
    end_time_of_visit = db.TimeProperty(required=True)
    # vitals info
    temp = db.IntegerProperty()
    pulse_apical = db.IntegerProperty()
    pulse_radial = db.IntegerProperty()
    respirations = db.IntegerProperty()
    blood_pressure = db.IntegerProperty()
    weight_actual = db.IntegerProperty()
    weight_reported = db.IntegerProperty()
    # type of visit info
    visit_regular = db.BooleanProperty()
    visit_prn = db.BooleanProperty()
    visit_high_tech = db.BooleanProperty()
    # homebound status info
    homebound_shortness = db.BooleanProperty()
    homebound_req_wheel_chair = db.BooleanProperty()
    homebound_req_walker = db.BooleanProperty()
    homebound_req_cane = db.BooleanProperty()
    homebound_req_crutches = db.BooleanProperty()
    homebound_stairs = db.BooleanProperty()
    homebound_poor_endurance = db.BooleanProperty()
    # SA cardio info
    cardio_wnl = db.BooleanProperty()
    pulses_regular = db.BooleanProperty()
    pulses_irregular = db.BooleanProperty()
    pulses_weak = db.BooleanProperty()
    pulses_strong = db.BooleanProperty()
    pulses_bounding = db.BooleanProperty()
    edema_pitting = db.BooleanProperty()
    edema_nonpitting = db.BooleanProperty()
    edema_plus1 = db.BooleanProperty()
    edema_plus2 = db.BooleanProperty()
    edema_plus3 = db.BooleanProperty()
    edema_plus4 = db.BooleanProperty()
    # SA gastro intestinal info
    gastro_wnl = db.BooleanProperty()
    gastro_last_bm = db.DateProperty()
    gastro_ruq = db.IntegerProperty()
    gastro_luq = db.IntegerProperty()
    gastro_rlq = db.IntegerProperty()
    gastro_llq = db.IntegerProperty()
    appetite = db.TextProperty()
