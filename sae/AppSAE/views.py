from django.shortcuts import render , HttpResponseRedirect
from .models import Description,Capteur
from . import models
from .forms import DescriptionForm , CapteurForm
import csv
from django.http import HttpResponse
from datetime import datetime , date
import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse
import json


#global id_capteur_edit
#id_capteur_edit = None

def index(request):
    #global id_capteur_edit
    liste = models.Description.objects.all()
    liste2 = models.Capteur.objects.all()
    return render(request, 'index/index.html',{"liste":liste,"liste2":liste2})
##########################################
############DESCRIPTION###################


def confirmationD(request):
    lform = DescriptionForm(request.POST)
    if lform.is_valid():
        D = lform.save()
        return HttpResponseRedirect ('/appsae/')
    else:
        return render(request,'Description/createD.html',{"form": lform})

def createD(request):
    if request.method == "POST":
        form = DescriptionForm(request)
        if form.is_valid():
            D = form.save()
            return render(request,'Description/confirmationD.html',{"D" : D})
        else:
            return render(request,'Description/createD.html',{"form": form})
    else :
        form = DescriptionForm()
        return render(request,'Description/createD.html',{"form" : form})

def readD(request, id):
    D = models.Description.objects.get (pk= id)
    return render(request,'Description/readD.html',{"D": D})

#def updateD(request,id):
 #   D = models.Description.objects.get(pk=id)
  #  form = DescriptionForm(D.dico())
   # return render(request, "Description/createD.html" ,{"form":form, "id": id})

#def traitementupdateD(request, id):
 #   lform = DescriptionForm(request.POST)
  #  if lform.is_valid():
   #     Description = lform.save(commit=False)
    #    Description.id = id;
     #   Description.save()
      #  return HttpResponseRedirect('/appsae/')
    #else:
     #   return render(request, 'Description/updateD.html', {"form": lform, "id": id})

def deleteD(request, id):
    Description = models.Description.objects.get(pk=id)
    Description.delete()
    return HttpResponseRedirect('/appsae/')

##########################################
############CAPTEUR###################


def confirmationC(request):
    lform = CapteurForm(request.POST)
    if lform.is_valid():
        C = lform.save()
        return HttpResponseRedirect ('/appsae/')
    else:
        return render(request,'Capteur/createC.html',{"form": lform})

def createC(request):
    if request.method == "POST":
        form = CapteurForm(request)
        if form.is_valid():
            C = form.save()
            return render(request,'Capteur/confirmationC.html',{"C" : C})
        else:
            return render(request,'Capteur/createC.html',{"form": form})
    else :
        form = CapteurForm()
        return render(request,'Capteur/createC.html',{"form" : form})

def readC(request, id):
    C = models.Capteur.objects.get (pk= id)
    return render(request,'Capteur/readC.html',{"C": C})

def updateC(request,id_capteur):
    C = models.Capteur.objects.get(pk=id_capteur)
    form = CapteurForm(C.dico())
    return render(request, "Capteur/createC.html" ,{"form":form, "id_capteur": id_capteur})

def traitementupdateC(request, id_capteur):
    #global id_capteur_edit
    lform = CapteurForm(request.POST)
    if lform.is_valid():
        Capteur = lform.save(commit=False)
        #id_capteur_edit = Capteur.id_capteur
        Capteur.id = id_capteur;
        Capteur.save()
        return HttpResponseRedirect('/appsae/')
    else:
        return render(request, 'Capteur/updateC.html', {"form": lform,"id_capteur":id_capteur})

def deleteC(request, id_capteur):
    Capteur = models.Capteur.objects.get(pk=id_capteur)
    Capteur.delete()
    return HttpResponseRedirect('/appsae/')




#####################################################
###########################SERVICE SUPP##############
#####################################################

def generate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Colonne1', 'Colonne2', 'Colonne3', 'Colonne4'])

    data = Description.objects.all()
    for item in data:
        writer.writerow([item.id_capteur, item.date, item.time,item.temp])

    return response


def filtre_dates(request):
    start_date = request.GET.get('start_date')
    start_time = request.GET.get('start_time')
    end_date = request.GET.get('end_date')
    end_time = request.GET.get('end_time')

    start_datetime = None
    end_datetime = None

    if start_date and start_time:
        start_datetime = datetime.strptime(start_date + ' ' + start_time, '%Y-%m-%d %H:%M')

    if end_date and end_time:
        end_datetime = datetime.strptime(end_date + ' ' + end_time, '%Y-%m-%d %H:%M')

    descriptions = Description.objects.all()

    filtered_descriptions = []

    for description in descriptions:
        datetime_obj = datetime.combine(description.date, description.time)

        if start_datetime and datetime_obj < start_datetime:
            continue
        if end_datetime and datetime_obj > end_datetime:
            continue
        filtered_descriptions.append(description)

    return render(request, 'index/filtre_dates.html', {
        "descriptions": filtered_descriptions,
        "start_date": start_date,
        "start_time": start_time,
        "end_date": end_date,
        "end_time": end_time
    })


def filtre2(request):
    filtre2 = Description.objects.all().order_by('temp').values()
    return render(request, 'index/filtre2.html',{"filtre2":filtre2,})

def rechercher_capteurs(request):
    id_capteur = request.GET.get('id_capteur', '')
    capteurs = Capteur.objects.filter(id_capteur=id_capteur)

    donnees_table_externe = Description.objects.filter(id_capteur__id_capteur=id_capteur)

    context = {
        'capteurs': capteurs,
        'donnees_table_externe': donnees_table_externe,
        'id_capteur': id_capteur
    }
    return render(request, 'index/filtre1.html', context)

def graph(request):
    global nom_capteur_edit1
    global nom_capteur_edit
    capteurs = list(models.Capteur.objects.all())
    minutes= 0
    data = models.Description.objects.all().filter(id_capteur='A72E3F6B79BB').values_list('time', 'temp')
    #print(data)
    result_dict = {}
    for time, temp in data:
        minutes += 5
        #minutes = time.second
        result_dict[minutes] = temp

    minutes1 = 0
    data = models.Description.objects.all().filter(id_capteur='B8A5F3569EFF').values_list('time', 'temp')
    #print(data)
    result_dict1 = {}
    for time, temp in data:
        minutes1 += 5
        #minutes = time.second
        result_dict1[minutes1] = temp
    return render(request, 'index/graph.html', {'data': result_dict, 'data2': result_dict1,'capteurs': capteurs})


def filtrer_capteurs(request):
    id_capteur = request.GET.get('id_capteur', '')
    start_date = request.GET.get('start_date')
    start_time = request.GET.get('start_time')
    end_date = request.GET.get('end_date')
    end_time = request.GET.get('end_time')

    start_datetime = None
    end_datetime = None

    if start_date and start_time:
        start_datetime = datetime.strptime(start_date + ' ' + start_time, '%Y-%m-%d %H:%M')

    if end_date and end_time:
        end_datetime = datetime.strptime(end_date + ' ' + end_time, '%Y-%m-%d %H:%M')

    capteurs = Capteur.objects.filter(id_capteur=id_capteur)
    donnees_table_externe = Description.objects.filter(id_capteur__id_capteur=id_capteur)

    descriptions = Description.objects.all()
    filtered_descriptions = []

    for description in descriptions:
        datetime_obj = datetime.combine(description.date, description.time)
        if start_datetime and datetime_obj < start_datetime:
            continue
        if end_datetime and datetime_obj > end_datetime:
            continue
        filtered_descriptions.append(description)

    context = {
        'capteurs': capteurs,
        'donnees_table_externe': donnees_table_externe,
        'descriptions': filtered_descriptions,
        'id_capteur': id_capteur,
        'start_date': start_date,
        'start_time': start_time,
        'end_date': end_date,
        'end_time': end_time
    }

    return render(request, 'index/filtre_comb.html', context)