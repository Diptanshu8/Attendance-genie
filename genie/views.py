from django.shortcuts import render
import csv,os

# Create your views here.
def home_page(request):
    return render(request,'home.html')
def mark_attendance(request):
    path = os.getcwd()+'/genie/timetable.csv'
    day = 'Monday'
    with open(path,'r') as f:
        r = csv.DictReader(f)
        for row in r:
            if row['Day'] == day:
                subjects = eval(row['subject'])
    if request.method =='POST':
        return render(request,'note_attendance.html',{'subject_name':request.POST['subject_name']})
    return render(request,'note_attendance.html',{'subject_name':subjects})
def show_attendance(request):
    pass
