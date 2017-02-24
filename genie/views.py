from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import csv,os
import json
from genie.models import day,subject,slot

# Create your views here.
def loading_timetable():
    addr="timetable.txt"
    with open(addr,"r") as f:
        timetable = json.loads(f.read())
    return timetable
def home_page(request):
    return render(request,'home.html')
def show_subejcts_for_a_day(request):
    if request.method == 'GET':
        d = request.GET['day']
        timetable = loading_timetable()
        output = [item for item in timetable[d] if item!="*"]
        response = JsonResponse({'day':d,'output':output})
    return response
###PREVIOUS SYNTAX... leave it till database integration is not done
#        subjects = [item.name for item in subject.objects.filter(day__name = str(d))]
#        for name in subjects:
#            for s in slot.objects.filter(subject_with_this_slot__name=str(name)):
#                data = eval(s.day_time)
#                output[str(name)] = data[str(d)]
        #subject_slot = [ slot.objects.filter(subject_with_this_slot__name=str(item)) for item in subjects ]
        #temp = [item.name for item in subject_slot] 
        #print temp
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
                item.attendance+=1
            item.total+=1 
            index+=1
            print item.name,item.attendnace,item.total
            item.save()
        response = JsonResponse({'day':d,'subjects':subjects})
    return response
def show_attendance(request):
    if request.method == 'GET':
        subject_name = request.GET['subject']
        for item in subject.objects.filter(name=subject_name):
            output = 'You have attended {0} classes of {1}'.format(item.attendance,item.total)
        print output
        response = JsonResponse({'subject':subject_name,'score':output})
    return response
