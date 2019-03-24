import requests
import json
import math
import pickle

#Adapted from https://github.com/Rodantny/Rate-My-Professor-Scraper-and-Search
class RateMyProfScraper:
        def __init__(self,schoolid):
            self.UniversityId = schoolid
            self.professorlist = self.createprofessorlist()
            self.indexnumber = False

        def createprofessorlist(self):#creates List object that include basic information on all Professors from the IDed University
            tempprofessorlist = []
            num_of_prof = self.GetNumOfProfessors(self.UniversityId)
            num_of_pages = math.ceil(num_of_prof / 20)
            i = 1
            while (i <= num_of_pages):# the loop insert all professor into list
                page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                    i) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                    self.UniversityId))
                temp_jsonpage = json.loads(page.content.decode('utf-8'))
                print(temp_jsonpage)
                temp_list = temp_jsonpage['professors']
                tempprofessorlist.extend(temp_list)
                i += 1
            return tempprofessorlist

        def GetNumOfProfessors(self,id):  # function returns the number of professors in the university of the given ID.
            page = requests.get(
                "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                    id))  # get request for page
            temp_jsonpage = json.loads(page.content.decode('utf-8'))
            num_of_prof = temp_jsonpage[
                              'remaining'] + 20  # get the number of professors at William Paterson University
            return num_of_prof

        def GetRMPProfessorJSON(self, tid):
            page = requests.get("https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(tid), timeout=10)
            json_page = json.loads(page.content.decode('utf-8'))
            print(json_page)

        def SearchProfessor(self, ProfessorName):
            self.indexnumber = self.GetProfessorIndex(ProfessorName)
            self.PrintProfessorInfo()
            return self.indexnumber

        def GetProfessorTID(self, indexnumber):
            return(self.professorlist[self.indexnumber]["tid"])


        def GetProfessorIndex(self,ProfessorName):  # function searches for professor in list
            for i in range(0, len(self.professorlist)):
                if (ProfessorName == (self.professorlist[i]['tFname'] + " " + self.professorlist[i]['tLname'])):
                    return i
            return False  # Return False is not found

        def PrintProfessorInfo(self):  # print search professor's name and RMP score
            if self.indexnumber == False:
                print("error")
            else:
                print(self.professorlist[self.indexnumber])

        def PrintProfessorDetail(self,key):  # print search professor's name and RMP score
            if self.indexnumber == False:
                print("error")
                return "error"
            else:
                print(self.professorlist[self.indexnumber][key])
                return self.professorlist[self.indexnumber][key]

#CornellUniversity = RateMyProfScraper(298)
#pickle.dump(CornellUniversity, open( "raw_rateMyProfessor_data.p", "wb" ))

CornellUniversity = pickle.load(open("raw_rateMyProfessor_data.p", "rb"))
#print(CornellUniversity.professorlist[0])
cardie_index = CornellUniversity.SearchProfessor("Claire Cardie")
tid = CornellUniversity.GetProfessorTID(cardie_index)
print(cardie_index)
print(tid)
CornellUniversity.GetRMPProfessorJSON(tid)
#CornellUniversity.PrintProfessorInfo()
#CornellUniversity.PrintProfessorDetail(CornellUniversity.indexnumber)
#CornellUniversity.PrintProfessorDetail("overall_rating")

