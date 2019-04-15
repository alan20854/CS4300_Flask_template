from urllib import request
import json
import csv
import pickle


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
    data['offered'] = c['catalogWhenOffered']
    data['outcomes'] = outcomes
    data['subject'] = c['subject']
    classsec = c['enrollGroups'][0]['classSections'][0]
    data['professor'] = []
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

print("Starting data collection")
subjects = get_subjects()
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

new_json = scrape(subject="CS")
class_names = get_class_names(new_json)
print(class_names)
with open('CS_course_names.p', 'wb') as f:
  pickle.dump(class_names, f)

full_json = {}
for sub in subjects:  
  new_json = create_map(scrape(subject=sub))
  if sub == 'CS':
    cs_json = new_json

  full_json[sub] = new_json

with open('full_json.txt', 'w') as output:
  json.dump(full_json, output)

with open('cs_json.txt', 'w') as output:
  json.dump(cs_json, output)


#make graph of num professors vs major
#make graph of coursestaht have 0 description vs major
#print 10 for CS
#json for one course
#figure out if crosslisted