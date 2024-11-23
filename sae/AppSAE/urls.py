from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('filtre-dates/', views.filtre_dates, name='filtre_dates'),
    path('filtre2',views.filtre2),
    path('capteurs/rechercher/', views.rechercher_capteurs, name='rechercher_capteurs'),
    path('graph/', views.graph, name='graph'),
    path('filtrer_capteurs/', views.filtrer_capteurs, name='filtrer_capteurs'),
    ####################################
    ##########DESCRIPTION###############
    ####################################
    path('Description/createD/', views.createD),
    path('Description/confirmationD/', views.confirmationD),
#    path('Description/updateD/<str:id>/',views.updateD),
#    path('Description/traitementupdateD/<str:id>/',views.traitementupdateD),
    path('Description/deleteD/<str:id>/', views.deleteD),
    ####################################
    ############CAPTEUR#################
    ####################################
    path('Capteur/createC/', views.createC),
    path('Capteur/confirmationC/', views.confirmationC),
    path('Capteur/updateC/<str:id_capteur>/', views.updateC),
    path('Capteur/traitementupdateC/<str:id_capteur>/', views.traitementupdateC),
    path('Capteur/deleteC/<str:id_capteur>/', views.deleteC),
    ####################################################
    #################SERVICE SUPLEMENTAIRE##############
    ###################################################
    path('Description/csv/', views.generate_csv, name='generate_csv'),

]