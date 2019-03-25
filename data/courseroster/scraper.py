from urllib import request
import json
import csv


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

  Professors is a set of professors for the course

  Parameters:
    json - json object from scrape
  """
  res = []
  for c in json['data']['classes']:
    data = {}
    data['coursename'] = c['subject'] + c['catalogNbr']
    data['description'] = c['description']
    data['subject'] = c['subject']
    classsec = c['enrollGroups'][0]['classSections'][0]
    data['professor'] = set()
    for meet in classsec['meetings']:
      for inst in meet['instructors']:
        name = inst['firstName'] + " " + inst['lastName']
        data['professor'].add(name)
    res.append(data)
  return res

def create_csv(classes):
  """
  Creates a csv file from the list classes

  Professors is a set of professors for the course

  Parameters:
    classes - list
  """
  with open('classes.csv','a') as g:
    rows = ['coursename', 'subject', 'professor','description']
    writer = csv.DictWriter(g, fieldnames=rows)
    for r in classes:
      writer.writerow(r)


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
with open('classes.csv','w') as g:
  rows = ['coursename', 'subject', 'professor','description']
  writer = csv.DictWriter(g, fieldnames=rows)
  writer.writeheader()
#subjects = ["CS", "PHYS", "INFO"]
for x in subjects:
  data = scrape(subject=x)
  classes = create_map(data)
  create_csv(classes)

#make graph of num professors vs major
#make graph of coursestaht have 0 description vs major
#print 10 for CS
#json for one course

#figure out if crosslisted