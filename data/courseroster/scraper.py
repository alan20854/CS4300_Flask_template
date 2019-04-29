from urllib import request
import json
import csv
import pickle
import io
engineering_subs = ['AEP', 'BME', 'CHEME', 'CEE', 'CS', 'EAS', 
'ECE', 'ENGRC', 'ENGRD', 'ENGRG', 'ENGRI', 'INFO', 'MSE', 'MAE',
'NSE', 'ORIE', 'STSCI', 'SYSEN']

course_codes = []

def scrape(roster="SP19", subject="CS"):
  """
  Returns a json object from the course website

  Parameters:
    roster - string representing roster
    subject - string representing subject
  """
  print("Current subject:" + subject)
  urlbase = "https://classes.cornell.edu/api/2.0/search/classes.json?"
  if roster:
    urlbase += "roster=" + roster +"&"
  if subject:
    urlbase += "subject=" + subject +"&"
  urlbase = urlbase[:-1]
  response = request.urlopen(urlbase).read()
  return json.loads(response.decode('utf-8'))

def create_map(json):
  """
  Returns a list of dictionaries.

  Professors is a list of professors for the course

  Parameters:
    json - json object from scrape
  """
  res = []
  for c in json['data']['classes']:
    data = {}

    if c['catalogOutcomes']:
      outcomes=""
      for s in c['catalogOutcomes']: 
        outcomes+= " " + s
    else:
      outcomes = None

    data['courseNumber'] = c['catalogNbr']
    data['courseTitle'] = c['titleLong']
    data['description'] = c['description']

    if c['catalogWhenOffered'] != None: 
      data['offered'] = c['catalogWhenOffered'][:-1].split(', ')
      if 'Fall' in data['offered']:
        data['url'] = "https://classes.cornell.edu/browse/roster/FA19" +  "/class/" + c['subject']+"/" +c['catalogNbr']
      else:
        data['url'] = "https://classes.cornell.edu/browse/roster/SP19" +  "/class/" + c['subject']+"/" +c['catalogNbr']
    else: 
      data['offered'] = None
      data['url'] = "https://classes.cornell.edu/browse/roster/FA19" +  "/class/" + c['subject']+"/" +c['catalogNbr']

    data['outcomes'] = outcomes
    data['subject'] = c['subject']
    course_codes.append(data['subject'] + " " + data['courseNumber'])
    classsec = c['enrollGroups'][0]['classSections'][0]
    data['professor'] = []
    try: 
      data['prerequisite'] = c['catalogPrereqCoreq']
    except: 
      data['prerequisite'] = None

    try:
      if int(c['endDt'][:2]) - int(c['startDt'][:2]) < 4:
        data['courseLength'] = "7 Week"
      else:
        data['courseLength'] = 'Full'
    except:
        data['courseLength'] = None

    for meet in classsec['meetings']:
      for inst in meet['instructors']:
        name = inst['firstName'] + " " + inst['lastName']
        if name not in data['professor']:
          data['professor'].append(name) 
    res.append(data)
  return res

def create_csv(classes):
  """
  Creates a csv file from the list classes

  Professors is a list of professors for the course

  Parameters:
    classes - list
  """
  with open('classes.csv','a') as g:
    rows = ['courseNumber', 'courseTitle', 'subject', 'offered', 'professor','description', 'outcomes']
    writer = csv.DictWriter(g, fieldnames=rows)
    for r in classes:
      writer.writerow(r)

def get_class_names(json):
  """
  Returns the list of abbreviated course names with their numbers.

  Parameters:
    json - json object from scrape
  """
  res = []
  for c in json['data']['classes']:
    if c['description'] != None:
      name = ""
      name += c['subject'] + " " + c['catalogNbr'] + ": " + c["titleShort"]
      res.append(name)
  return res


#https://classes.cornell.edu/api/2.0/config/subjects.json?roster=SP19

def get_subjects(roster = "SP19"):
  urlbase = "https://classes.cornell.edu/api/2.0/config/subjects.json?roster="
  urlbase += roster
  response = request.urlopen(urlbase).read()
  response = json.loads(response.decode('utf-8'))
  subjects = []
  for sub in response['data']['subjects']:
    subjects.append(sub['value'])
  return subjects

def get_EN_class_names(subjects):
  names = []
  for x in subjects:
    data = scrape(subject=x)
    names += get_class_names(data)
  return names  

def add_crosslisted(courses_json, course_info):
  for _, courses in courses_json.items():
    for c in courses:
      if course_info['courseTitle'] == c['courseTitle']:
        c['crosslisted'].append(course_info['subject'] + " " + course_info['courseNumber'])

    
def filter_crosslisted(courses_dict):
  filtered_json = {}
  seen_course_names = []
  for sub, course_lst in courses_dict.items():
    filtered_sub = []
    for course in course_lst: 
      if course['courseTitle'] not in seen_course_names:
        seen_course_names.append(course["courseTitle"])
        course['crosslisted'] = []
        filtered_sub.append(course)
      else:
        add_crosslisted(filtered_json, course)
    filtered_json[sub] = filtered_sub
  return filtered_json      


print("Starting data collection")
sp_subjects = set(get_subjects())
fa_subjects = set(get_subjects('FA19'))
subjects = sp_subjects.union(fa_subjects)
print("Obtained subjects")
# with open('classes.csv','w') as g:
#   rows = ['courseNumber', 'courseTitle', 'subject', 'offered', 'professor','description', 'outcomes']
#   writer = csv.DictWriter(g, fieldnames=rows)
#   writer.writeheader()
# #subjects = ["CS", "PHYS", "INFO"]
# for x in subjects:
#   data = scrape(subject=x)
#   classes = create_map(data)
#   create_csv(classes)

# new_json = scrape(subject="CS")
# class_names = get_class_names(new_json)
# with open('CS_course_names.p', 'wb') as f:
#   pickle.dump(class_names, f)

# with open('en_course_names.p', 'wb') as f:
#   pickle.dump(get_EN_class_names(engineering_subs), f)

# en_json={}
# for sub in engineering_subs:
#   new_json = create_map(scrape(subject=sub))
#   en_json[sub] = new_json

# with open('en_json.txt', 'w') as output:
#   json.dump(en_json, output)

full_json = {}
for sub in subjects: 
  try:
    sp_json = create_map(scrape(subject=sub))
  except:
    continue

  try:
    fa_json = create_map(scrape("FA19", subject=sub))
  except:
    continue
  combined_json = sp_json
  for fa_class in fa_json:
    only_fa = True
    for sp_class in sp_json:
      if fa_class['courseTitle'] == sp_class['courseTitle']:
        only_fa = False
    if only_fa:
      combined_json.append(fa_class)
  full_json[sub] = sp_json
  
full_json = filter_crosslisted(full_json)
# print(full_json)

with io.open('full_json.json', 'w', encoding='utf-8') as output:
  json.dump(full_json, output, ensure_ascii=False)

with open('course_codes_II.pkl', 'wb') as f:
  pickle.dump(course_codes, f)

# with open('cs_json.txt', 'w') as output:
#   json.dump(cs_json, output)


#make graph of num professors vs major
#make graph of coursestaht have 0 description vs major
#print 10 for CS
#json for one course
#figure out if crosslisted