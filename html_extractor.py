from bs4 import BeautifulSoup,BeautifulStoneSoup
def removing_blanks_for_no_subject(data):
    for item in data:
        if item == u'\xa0':
            data[data.index(item)]='*'
    return map(str,data)

def boundary_detection(soup):
    boundary=[]
    tableheader = soup.find_all('td',class_="tableheader")
    for item in tableheader:
        boundary.append(item.get_text())
    return map(str,boundary)

def slots_and_days(boundary):
    slots,days=[],[]
    for item in boundary:
        if "AM" in item or "PM" in item:
            slots.append(item)
        else:
            days.append(item)
    return (map(str,slots),map(str,days))

def table_data_extraction(soup):
    tableheader = soup.find_all('td',align="center")
    data = []
    temp = []
    for item in tableheader:
        if item.get('colspan'):
            data += int(item.get('colspan'))*[item.get_text()]
        else:
            data.append(item.get_text())
    data = removing_blanks_for_no_subject(data)
    return data

def subject_and_venue_extraction(data):
    subject_venue_dict = {}
    for d in data:
        if d[:subject_code_length+1] not in subject_venue_dict.keys() and d!='*':
            subject_venue_dict[str(d[0:subject_code_length+1])]=d[subject_code_length+1:]
    return subject_venue_dict

def creating_triple_tupple(day_data,subject_venue_dict,slots):
    tripple_tupple_data = []
    for i,item in enumerate(day_data):
        if item != '*':
            tripple_tupple_data.append((item[:subject_code_length+1],subject_venue_dict[item[:subject_code_length+1]],slots[i] ))
        else:
            tripple_tupple_data.append('*')
    return tripple_tupple_data

with open("timetable.html") as f:
    html_doc = f.read()
soup = BeautifulSoup(html_doc,'lxml')

boundary = boundary_detection(soup)
slots,days = slots_and_days(boundary)
number_of_slots = len(slots)
data=table_data_extraction(soup)
subject_code_length = 6
subjects_venues_dict = subject_and_venue_extraction(data)

temp = data
timetable = {}
for day in days[1:]:
    timetable[day]=creating_triple_tupple(temp[:number_of_slots],subjects_venues_dict,slots)
    temp = temp[number_of_slots:]
for item in timetable.keys():
    print item,timetable[item]
"""for item in data:
    if item.has_key('class'):
        day = str(item.string)
        timetable[str(item.string)] = []
    else:
        timetable[day].append(str(item.b))
    #timetable[str(item[0])]=map(str,item[1:])

print timetable
#for line in a:
#    print line.get()
"""
