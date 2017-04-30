from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import csv,os
import json
import datetime
from genie.models import day,subject,slot
import yaml

try:
    config = yaml.load(file("genie.conf",'r'))
except:
    print "No config exists"
# Create your views here.
def loading_timetable():
    #addr="timetable.txt"
    addr = config['timetable']['file']
    with open(addr,"r") as f:
        timetable = json.loads(f.read())
    return timetable
def loading_database():
    addr = config['database']['file']
    #addr = "attendance.csv"
    database={}
    with open(addr,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                database[row[0]]=map(eval,row[1:])
            except:
                pass
    return database
def updating_database(database):
    #addr = "attendance.csv"
    addr = config['database']['file']
    first_row = ('Subject name','attended','absence')
    with open(addr,'w') as f:
        writer = csv.writer(f)
        writer.writerow(first_row)
        for subject in database.keys():
            row = [str(subject),database[subject][0],database[subject][1]]
            writer.writerow(row)
            print row
    return "Updated!"

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
    timetable= loading_timetable()
    database = loading_database()
    date = datetime.date.today().strftime("%d/%m/%y")
    if request.method == 'GET':
        d = request.GET['day']
        data = str(request.GET['data'])
        subjects = [item for item in timetable[d] if item!="*"]
        for i,subject in enumerate(subjects):
            if date in database[subject[0]][0] or date in database[subject[0]][1]:
                status = "Attendance already marked"
                break
            elif data[i] == 'p' or data[i]=='P':
                database[subject[0]][0].append(date)
            elif data[i] =='a' or data[i] == 'A':
                database[subject[0]][1].append(date)
        if 'status' not in locals():
            status = updating_database(database)
        response = JsonResponse({'day':d,'status':status})
    return response
###PREVIOUS SYNTAX... leave it till database integration is not done
        #subjects = [item.name for item in subject.objects.filter(day__name = str(d))]
        #index = 0
        #for item in subject.objects.filter(day__name = str(d)):
        #    if data[index]==present:
        #        item.attendance+=1
        #    item.total+=1 
        #    index+=1
        #    print item.name,item.attendnace,item.total
        #    item.save()
def show_attendance(request):
    timetable= loading_timetable()
    database = loading_database()
    if request.method == 'GET':
        subject_name = request.GET['subject']
        output_attended_count = len(database[subject_name][0])
        output_attended_dates = database[subject_name][0]
        output_missed_count = len(database[subject_name][1])
        output_missed_dates = database[subject_name][1]
        output= {"present":output_attended_count,"present_dates":output_attended_dates,"absent":output_missed_count,"absent_dates":output_missed_dates}
        response = JsonResponse({'subject':subject_name,'score':output})
    return response
