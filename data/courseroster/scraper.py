from urllib import request
import json


def scrape(search=True, roster="SP19", subject="CS"):
  """
  Returns a json object from the course website

  Parameters:
    search - boolean for whether to search
    roster - string representing roster
    subject - string representing subject
  """
  urlbase = "https://classes.cornell.edu/api/2.0/"
  if search:
    urlbase += "search/classes.json?"
    if roster:
      urlbase += "roster=" + roster +"&"
    if subject:
      urlbase += "subject=" + subject +"&"
    urlbase = urlbase[:-1]
  response = request.urlopen(urlbase).read()
  return json.loads(response.decode('utf-8'))

def create_map(json):
  """
  Returns a dictionary where the keys are the course names and the values
  are [subject, professors, coursedescription].

  Professors is a set of professors for the course

  Parameters:
    json - json object from scrape
  """
  res = {}
  for c in json['data']['classes']:
    coursename = c['subject'] + " " + c['catalogNbr']
    description = c['description']
    subject = c['subject']
    classsec = c['enrollGroups'][0]['classSections'][0]
    professor = set()
    for meet in classsec['meetings']:
      for inst in meet['instructors']:
        name = inst['firstName'] + " " + inst['lastName']
        professor.add(name)
    res[coursename] = [subject, professor, description]
  return res


subjects = ["CS"]
for x in subjects:
  data = scrape(subject=x)
  dct = create_map(data)
  print(dct)

#make graph of num professors vs major
#make graph of coursestaht have 0 description vs major
#print 10 for CS
#json for one course

#figure out if crosslisted