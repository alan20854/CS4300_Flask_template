import csv
import matplotlib.pyplot as plt
import numpy as np

#['coursename', 'subject', 'professor','description']
with open('classes.csv','r') as g:
  reader = csv.DictReader(g)
  subject_class_count = {}
  subject_no_desc = {}
  subject_prof_count = {}
  prof_to_class = {}
  c=0
  d = 0
  for row in reader:
    #count classes
    c+=1
    if row['subject'] in subject_class_count:
      subject_class_count[row['subject']]+=1
    else:
      subject_class_count[row['subject']] = 1

    #count number of no description classes
    if row['description'] == "":
      d +=1
      if row['subject'] in subject_no_desc:
        subject_no_desc[row['subject']]+=1
      else:
        subject_no_desc[row['subject']] = 1
    elif row['subject'] not in subject_no_desc:
      subject_no_desc[row['subject']] = 0

    #count number professors
    for prof in row['professor']:
      if prof not in prof_to_class:
        prof_to_class[prof] = [row['coursename']]
        if row['subject'] in subject_prof_count:
          subject_prof_count[row['subject']]+=1
        else:
          subject_prof_count[row['subject']]=1
      else:
        prof_to_class[prof] +=[row['coursename']]

  plt.hist(list(subject_class_count.values()))
  plt.xlabel("Number of Courses")
  plt.ylabel("Number of Subjects")
  plt.title("Number of Courses vs Subjects")
  plt.savefig("coursevsub.png")
  plt.show() 
  
  plt.hist(list(subject_no_desc.values()))
  plt.xlabel("Number of Courses without Descriptions")
  plt.ylabel("Number of Subjects")
  plt.title("Number of Courses without Descriptions vs Subjects")
  plt.savefig("nodescvsub.png")
  plt.show() 
  
  # plt.hist(list(subject_no_desc.values()))
  # plt.xlabel("Number of Courses without Descriptions")
  # plt.ylabel("Number of Subjects")
  # plt.title("Number of Courses without Descriptions vs Subjects")
  # plt.show()  
  # plt.savefig("nodescvsub.png")


  mclass = ''

  for k,v in subject_class_count.items():
    if v == max(subject_class_count.values()):
      mclass = k
    print((k,v,subject_no_desc[k]))
  
  print((mclass,max(subject_class_count.values())))
  print(len(subject_class_count))
  print(c)
  print(d)
