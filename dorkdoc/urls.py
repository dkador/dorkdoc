# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('dorkdoc.views',
    (r'^$', 'index'),
	(r'^patient/create/$', 'createpatient'),
    (r'^patient/(?P<medical_record_number>\d+)/$', 'patient'),
    (r'^patient/(?P<medical_record_number>\d+)/form/create/step1/$', 'createform1'),
    (r'^patient/(?P<medical_record_number>\d+)/form/create/step2/(?P<form_key>[a-zA-Z0-9]+)/$', 'createform2'),
    (r'^patient/(?P<medical_record_number>\d+)/form/create/step3/(?P<form_key>[a-zA-Z0-9]+)/$', 'createform3'),
    (r'^patient/(?P<medical_record_number>\d+)/form/create/step4/(?P<form_key>[a-zA-Z0-9]+)/$', 'createform4'),
    (r'^patient/(?P<medical_record_number>\d+)/form/create/step5/(?P<form_key>[a-zA-Z0-9]+)/$', 'createform5'),
    (r'^patient/(?P<medical_record_number>\d+)/form/create/step6/(?P<form_key>[a-zA-Z0-9]+)/$', 'createform6')
)
