# -*- coding: utf-8 -*-
from dorkdoc.models import Patient, Form
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail
from django import forms
from ragendja.template import render_to_response
import time
import logging
from google.appengine.ext import db
from google.appengine.ext.db import Key

class PatientForm(forms.Form):
    medical_record_number = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

class FormDateTimeForm(forms.Form):
    date_of_visit = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()

class FormVitalsForm(forms.Form):
    temp = forms.IntegerField()
    pulse_apical = forms.IntegerField()
    pulse_radial = forms.IntegerField()
    respirations = forms.IntegerField()
    blood_pressure = forms.IntegerField()
    weight_actual = forms.IntegerField()
    weight_reported = forms.IntegerField()

class FormVisitForm(forms.Form):
    visit_regular = forms.BooleanField(required=False)
    visit_prn = forms.BooleanField(required=False)
    visit_high_tech = forms.BooleanField(required=False)

class FormHomeboundForm(forms.Form):
    homebound_shortness = forms.BooleanField(required=False)
    homebound_req_wheel_chair = forms.BooleanField(required=False)
    homebound_req_walker = forms.BooleanField(required=False)
    homebound_req_cane = forms.BooleanField(required=False)
    homebound_req_crutches = forms.BooleanField(required=False)
    homebound_stairs = forms.BooleanField(required=False)
    homebound_poor_endurance = forms.BooleanField(required=False)

class FormCardioForm(forms.Form):
    cardio_wnl = forms.BooleanField(required=False)
    pulses_regular = forms.BooleanField(required=False)
    pulses_irregular = forms.BooleanField(required=False)
    pulses_weak = forms.BooleanField(required=False)
    pulses_strong = forms.BooleanField(required=False)
    pulses_bounding = forms.BooleanField(required=False)
    edema_pitting = forms.BooleanField(required=False)
    edema_nonpitting = forms.BooleanField(required=False)
    edema_plus1 = forms.BooleanField(required=False)
    edema_plus2 = forms.BooleanField(required=False)
    edema_plus3 = forms.BooleanField(required=False)
    edema_plus4 = forms.BooleanField(required=False)

class FormGastroForm(forms.Form):    
    gastro_wnl = forms.BooleanField(required=False)
    gastro_last_bm = forms.DateField()
    gastro_ruq = forms.IntegerField()
    gastro_luq = forms.IntegerField()
    gastro_rlq = forms.IntegerField()
    gastro_llq = forms.IntegerField()
    appetite = forms.CharField()

# login_required means that a user has to login to access the view
# this is the main view for dorkdoc. it just asks you to enter a medical record number and
# redirects you to the patient once it's done
@login_required
def index(request):
    # this calls the template index.html and passes no data
    return render_to_response(request, 'dorkdoc/index.html')

# this is the view that either displays a form for creating a new patient or processes it
@login_required
def createpatient(request):
    # this code path is when the user's POSTed to us
    if request.method == 'POST':
        # set up the form object
        form = PatientForm(request.POST)
        # if the form is valid, do this stuff
        if form.is_valid():
            # pull out the data from the form
            medical_record_number = form.cleaned_data['medical_record_number']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            #TODO: figure out how to ensure uniqueness
            # create a Patient object with that data
            patient = Patient(medical_record_number = medical_record_number,
                              first_name = first_name,
                              last_name = last_name)
            # save the object to the DB
            patient.put()
            # this grabs all the forms associated to that patient
            forms = Form.all().filter('patient =', patient.key())
            # this calls the template patient_detail.html and passes the patient and the forms
            return render_to_response(request, 'dorkdoc/patient_detail.html', 
                { 'patient' : patient,
                  'forms'   : forms
                }
            )
            
    # this code path is when the user GETs this URL
    else:
        # create a blank form object
        form = PatientForm()
    
    # this passes the form data to the createpatient template
    return render_to_response(request, 'createpatient.html', {'form' : form })

# this is the patient view for dorkdoc. it shows you some basic info about the patient and then
# lets you either view past forms or create a new form.
@login_required
def patient(request, medical_record_number):
    # this grabs the specific patient record based on the url (from urls.py)
    patient = Patient.all().filter('medical_record_number =', medical_record_number).get()
    # this grabs all the forms associated to that patient
    forms = Form.all().filter('patient =', patient.key())
    # this calls the template patient_detail.html and passes the patient and the forms
    return render_to_response(request, 'dorkdoc/patient_detail.html', 
        { 'patient' : patient,
          'forms'   : forms
        }
    )

# this is the view that is the first page of creating a form
@login_required
def createform1(request, medical_record_number):
    logging.debug("createform1 invoked")
    # this code path is when the user's POSTed to us
    if request.method == 'POST':
        # set up the form object
        form = FormDateTimeForm(request.POST)
        # if the form is valid, do this stuff
        if form.is_valid():
            logging.debug("Form is valid")
            # this grabs the specific patient record based on the url (from urls.py)
            patient = Patient.all().filter('medical_record_number =', medical_record_number).get()
            # pull out the data from the form
            date_of_visit = form.cleaned_data['date_of_visit']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            #TODO: figure out how to ensure uniqueness
            # create a Form object with that data
            formobject = Form(date_of_visit          = date_of_visit,
                              start_time_of_visit    = start_time,
                              end_time_of_visit      = end_time,
                              patient                = patient)
            # save the object to the datastore
            formobject.put()
            logging.debug("Saved form to the datastore")
            # this calls the template createform2.html and passes the form object and the new form we're going to use
            #return render_to_response(request, "createform2.html",
            #    { "formobject" : formobject }
            #)
            return HttpResponseRedirect("/dorkdoc/patient/" + medical_record_number + "/form/create/step2/" + str(formobject.key()))
        else:
            logging.debug("Form isn't valid!")      
    # this code path is when the user GETs this URL
    else:
        # create a blank form object
        form = FormDateTimeForm()
    
    # this passes the form data to the create form 1 template
    return render_to_response(request, 'createform1.html', 
        { 'medical_record_number' : medical_record_number,
          'form'                  : form 
        }
    )

# this is the view that is the second page of creating a form
@login_required
def createform2(request, medical_record_number, form_key):
    logging.debug("createform2 invoked")
    # this code path is when the user's POSTed to us
    if request.method == 'POST':
        # set up the form object
        form = FormVitalsForm(request.POST)
        # if the form is valid, do this stuff
        if form.is_valid():
            logging.debug("Form is valid")
            # pull out the data from the form
            temp = form.cleaned_data['temp']
            pulse_apical = form.cleaned_data['pulse_apical']
            pulse_radial = form.cleaned_data['pulse_radial']
            respirations = form.cleaned_data['respirations']
            blood_pressure = form.cleaned_data['blood_pressure']
            weight_actual = form.cleaned_data['weight_actual']
            weight_reported = form.cleaned_data['weight_reported']
            # load the form object for the key in the url
            formobject = db.get(Key(form_key))
            # update the form with the values
            formobject.temp = temp
            formobject.pulse_apical = pulse_apical
            formobject.pulse_radial = pulse_radial
            formobject.respirations = respirations
            formobject.blood_pressure = blood_pressure
            formobject.weight_actual = weight_actual
            formobject.weight_reported = weight_reported
            # save the object to the datastore
            formobject.put()
            logging.debug("Saved form to the datastore")
            return HttpResponseRedirect("/dorkdoc/patient/" + medical_record_number + "/form/create/step3/" + form_key)
        else:
            logging.debug("Form isn't valid!")
            
    # this code path is when the user GETs this URL
    else:
        # create a blank form object
        form = FormVitalsForm()
    
    # this passes the form data to the create form 2 template
    return render_to_response(request, 'createform2.html', 
        { 'medical_record_number' : medical_record_number,
          'form'                  : form 
        }
    )

# this is the view that is the second page of creating a form
@login_required
def createform3(request, medical_record_number, form_key):
    logging.debug("createform3 invoked")
    # this code path is when the user's POSTed to us
    if request.method == 'POST':
        # set up the form object
        form = FormVisitForm(request.POST)
        # if the form is valid, do this stuff
        if form.is_valid():
            logging.debug("Form is valid")
            # pull out the data from the form
            visit_regular = form.cleaned_data['visit_regular']
            visit_prn = form.cleaned_data['visit_prn']
            visit_high_tech = form.cleaned_data['visit_high_tech']
            # load the form object for the key in the url
            formobject = db.get(Key(form_key))
            # update the form with the values
            formobject.visit_regular = visit_regular
            formobject.visit_prn = visit_prn
            formobject.visit_high_tech = visit_high_tech
            # save the object to the datastore
            formobject.put()
            logging.debug("Saved form to the datastore")
            return HttpResponseRedirect("/dorkdoc/patient/" + medical_record_number + "/form/create/step4/" + form_key)
        else:
            logging.debug("Form isn't valid!")
            
    # this code path is when the user GETs this URL
    else:
        # create a blank form object
        form = FormVisitForm()
    
    # this passes the form data to the create form 3 template
    return render_to_response(request, 'createform3.html', 
        { 'medical_record_number' : medical_record_number,
          'form'                  : form 
        }
    )

# this is the view that is the fourth page of creating a form
@login_required
def createform4(request, medical_record_number, form_key):
    logging.debug("createform4 invoked")
    # this code path is when the user's POSTed to us
    if request.method == 'POST':
        # set up the form object
        form = FormHomeboundForm(request.POST)
        # if the form is valid, do this stuff
        if form.is_valid():
            logging.debug("Form is valid")
            # pull out the data from the form
            homebound_shortness = form.cleaned_data['homebound_shortness']
            homebound_req_wheel_chair = form.cleaned_data['homebound_req_wheel_chair']
            homebound_req_walker = form.cleaned_data['homebound_req_walker']
            homebound_req_cane = form.cleaned_data['homebound_req_cane']
            homebound_req_crutches = form.cleaned_data['homebound_req_crutches']
            homebound_stairs = form.cleaned_data['homebound_stairs']
            homebound_poor_endurance = form.cleaned_data['homebound_poor_endurance']
            # load the form object for the key in the url
            formobject = db.get(Key(form_key))
            # update the form with the values
            formobject.homebound_shortness = homebound_shortness
            formobject.homebound_req_wheel_chair = homebound_req_wheel_chair
            formobject.homebound_req_walker = homebound_req_walker
            formobject.homebound_req_cane = homebound_req_cane
            formobject.homebound_req_crutches = homebound_req_crutches
            formobject.homebound_stairs = homebound_stairs
            formobject.homebound_poor_endurance = homebound_poor_endurance
            # save the object to the datastore
            formobject.put()
            logging.debug("Saved form to the datastore")
            return HttpResponseRedirect("/dorkdoc/patient/" + medical_record_number + "/form/create/step5/" + form_key)
        else:
            logging.debug("Form isn't valid!")
            
    # this code path is when the user GETs this URL
    else:
        # create a blank form object
        form = FormHomeboundForm()
        
    # this passes the form data to the create form 3 template
    return render_to_response(request, 'createform4.html', 
        { 'medical_record_number' : medical_record_number,
          'form'                  : form 
        }
    )

# this is the view that is the fifth page of creating a form
@login_required
def createform5(request, medical_record_number, form_key):
    logging.debug("createform5 invoked")
    # this code path is when the user's POSTed to us
    if request.method == 'POST':
        # set up the form object
        form = FormCardioForm(request.POST)
        # if the form is valid, do this stuff
        if form.is_valid():
            logging.debug("Form is valid")
            # pull out the data from the form
            cardio_wnl = form.cleaned_data['cardio_wnl']
            pulses_regular = form.cleaned_data['pulses_regular']
            pulses_irregular = form.cleaned_data['pulses_irregular']
            pulses_weak = form.cleaned_data['pulses_weak']
            pulses_strong = form.cleaned_data['pulses_strong']
            pulses_bounding = form.cleaned_data['pulses_bounding']
            edema_pitting = form.cleaned_data['edema_pitting']
            edema_nonpitting = form.cleaned_data['edema_nonpitting']
            edema_plus1 = form.cleaned_data['edema_plus1']
            edema_plus2 = form.cleaned_data['edema_plus2']
            edema_plus3 = form.cleaned_data['edema_plus3']
            edema_plus4 = form.cleaned_data['edema_plus4']
            # load the form object for the key in the url
            formobject = db.get(Key(form_key))
            # update the form with the values
            formobject.cardio_wnl = cardio_wnl
            formobject.pulses_regular = pulses_regular
            formobject.pulses_irregular = pulses_irregular
            formobject.pulses_weak = pulses_weak
            formobject.pulses_strong = pulses_strong
            formobject.pulses_bounding = pulses_bounding
            formobject.edema_pitting = edema_pitting
            formobject.edema_nonpitting = edema_nonpitting
            formobject.edema_plus1 = edema_plus1
            formobject.edema_plus2 = edema_plus2
            formobject.edema_plus3 = edema_plus3
            formobject.edema_plus4 = edema_plus4
            # save the object to the datastore
            formobject.put()
            logging.debug("Saved form to the datastore")
            return HttpResponseRedirect("/dorkdoc/patient/" + medical_record_number + "/form/create/step6/" + form_key)
        else:
            logging.debug("Form isn't valid!")
            
    # this code path is when the user GETs this URL
    else:
        # create a blank form object
        form = FormCardioForm()
        
    # this passes the form data to the create form 5 template
    return render_to_response(request, 'createform5.html', 
        { 'medical_record_number' : medical_record_number,
          'form'                  : form 
        }
    )

# this is the view that is the sixth page of creating a form
@login_required
def createform6(request, medical_record_number, form_key):
    logging.debug("createform6 invoked")
    # this code path is when the user's POSTed to us
    if request.method == 'POST':
        # set up the form object
        form = FormGastroForm(request.POST)
        # if the form is valid, do this stuff
        if form.is_valid():
            logging.debug("Form is valid")
            # pull out the data from the form
            gastro_wnl = form.cleaned_data['gastro_wnl']
            gastro_last_bm = form.cleaned_data['gastro_last_bm']
            gastro_ruq = form.cleaned_data['gastro_ruq']
            gastro_luq = form.cleaned_data['gastro_luq']
            gastro_rlq = form.cleaned_data['gastro_rlq']
            gastro_llq = form.cleaned_data['gastro_llq']
            appetite = form.cleaned_data['appetite']
            # load the form object for the key in the url
            formobject = db.get(Key(form_key))
            # update the form with the values
            formobject.gastro_wnl = gastro_wnl
            formobject.gastro_last_bm = gastro_last_bm
            formobject.gastro_ruq = gastro_ruq
            formobject.gastro_luq = gastro_luq
            formobject.gastro_rlq = gastro_rlq
            formobject.gastro_llq = gastro_llq
            formobject.appetite = appetite
            # save the object to the datastore
            formobject.put()
            logging.debug("Saved form to the datastore")
            #TODO: go to form detail page
            return HttpResponseRedirect("/dorkdoc/patient/" + medical_record_number)
        else:
            logging.debug("Form isn't valid!")

    # this code path is when the user GETs this URL
    else:
        # create a blank form object
        form = FormGastroForm()

    # this passes the form data to the create form 6 template
    return render_to_response(request, 'createform6.html', 
        { 'medical_record_number' : medical_record_number,
          'form'                  : form 
        }
    )
