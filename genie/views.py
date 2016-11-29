from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import csv,os
from genie.models import day,subject,slot

# Create your views here.
def home_page(request):
    return render(request,'home.html')
def show_subejcts_for_a_day(request):
    if request.method == 'GET':
        d = request.GET['day']
        output= {}
        subjects = [item.name for item in subject.objects.filter(day__name = str(d))]
        for name in subjects:
            for s in slot.objects.filter(subject_with_this_slot__name=str(name)):
                data = eval(s.day_time)
                output[str(name)] = data[str(d)]
        #subject_slot = [ slot.objects.filter(subject_with_this_slot__name=str(item)) for item in subjects ]
        #temp = [item.name for item in subject_slot] 
        #print temp
        response = JsonResponse({'subject_list':subjects,'day':d,'output':output})
    return response

def mark_attendance(request):
    present = 'p'
    absent = 'a'
    if request.method == 'GET':
        d = request.GET['day']
        data = str(request.GET['data'])
        subjects = [item.name for item in subject.objects.filter(day__name = str(d))]
        index = 0
        for item in subject.objects.filter(day__name = str(d)):
            if data[index]==present:
                item.attendace+=1
            item.total+=1 
            index+=1
            print item.name,item.attendace,item.total
            item.save()
        response = JsonResponse({'day':d,'subjects':subjects})
    return response
def show_attendance(request):
    pass
