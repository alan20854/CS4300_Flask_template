import requests
import json
import math
import pickle
import numpy as np
import matplotlib
import re

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

        def GetRMPProfessorPageContents(self, tid):
            page = requests.get("http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(tid))
            return page.content

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

if __name__ == "__main__":
    CornellUniversity = pickle.load(open("raw_rateMyProfessor_data.p", "rb"))

    prof_ratings = {}
    for prof in CornellUniversity.professorlist:
        regex = re.compile('[^a-zA-Z ]')
        name = regex.sub(' ', prof['tFname'] + " " + prof['tLname'])
        try:
            prof_ratings[name] = float(prof['overall_rating'])
        except:
            prof_ratings[name] = None
    pickle.dump(prof_ratings, open('prof_ratings.p', "wb"))

    #print(CornellUniversity.professorlist[0])
    # cardie_index = CornellUniversity.SearchProfessor("Claire Cardie")
    # #tid = CornellUniversity.GetProfessorTID(cardie_index)
    # print(cardie_index)
    # #print(tid) #521940
    # #CornellUniversity.GetRMPProfessorJSON(tid)
    # #cardie_content = CornellUniversity.GetRMPProfessorPageContents(521940)
    # #print(cardie_content)
    # #pruneProfReviewFile(cardie_content)
    # #CornellUniversity.PrintProfessorInfo()
    # #CornellUniversity.PrintProfessorDetail(CornellUniversity.indexnumber)
    # #CornellUniversity.PrintProfessorDetail("overall_rating")

    # print(CornellUniversity.professorlist[352])
    # ratings = []
    # #0-5, 6-10, 11-25, 26-50, 51-100, > 100
    # numComments = [0, 0, 0, 0, 0, 0]
    # sum_comments = 0
    # sum_ratings = 0
    # num_w_ratings = 0
    # for i in range(len(CornellUniversity.professorlist)):
    #     prof = CornellUniversity.professorlist[i]
    #     rating = prof['overall_rating']
    #     comments = prof['tNumRatings']
    #     sum_comments += comments
    #     if comments < 6:
    #         numComments[0] += 1
    #     elif comments < 11:
    #         numComments[1] += 1
    #     elif comments < 26:
    #         numComments[2] += 1
    #     elif comments < 51:
    #         numComments[3] += 1
    #     elif comments < 101:
    #         numComments[4] += 1
    #     else:
    #         numComments[5] += 1

    #     if rating != 'N/A':
    #         num_w_ratings += 1
    #         sum_ratings += float(rating)
    #         ratings.append(rating)
    #     #numComments.append(comments)
    # #print(ratings)
    # #print(numComments)
    # print(sum_comments / 2602)
    # print(sum_ratings / num_w_ratings)

    #plt = matplotlib.pyplot



    #[0, 110, 337, 669, 1297, 189]

        

