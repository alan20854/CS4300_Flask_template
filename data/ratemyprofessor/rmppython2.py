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

def pruneProfReviewFile(prContents):
    """Prunes the review page for a particular professor to only what is required namely the stats and the reviews
    
    Inputs:
    - prContents : Contents of the review webpage for a particular professor
    - filename   : Name of the file to write the output to
    
    Returns:
    - Pruned contents of the review page, which includes aggregate details of all reviews, as well as all individual reviews."""  

    print("Pruning review  page")
    nameStartS = "<h2 id=\"profName\""  #e.g. <h2 id="profName" style="color:black;">Salam&nbsp;Abdus</h2>
    deptStartS = "<li>Department: <strong>"
    qualityStartS = "title=\"Overall Quality is determined by the average rating of the Helpfulness and Clarity given by all users.\""  
    helpfulStartS = "title=\"Is this professor approachable, nice and easy to communicate with? How accessible is the professor and is he/she available during office hours or after class for additional help?\""
    clarityStartS = "title=\"How well does the professor teach the course material? Were you able to understand the class topics based on the professor's teaching methods and style?\""    
    easyStartS = "title=\"Is this class an easy A? How much work do you need to do in order to get a good grade?  Please note this category is NOT included in the"
    numRatStartS = "<p><span id=\"rateNumber\">Number of ratings <strong>"
    dateStartS = "<div class=\"date\">"
    clasStartS = "<div class=\"class\">"
    ratingStartS = "<div class=\"rating\">"
    commentStartS = "<p class=\"commentText\">"
    revqS = "Quality</p>"
    reveStartS = "<p class=\"rEasy status"
    revhStartS = "<p class=\"rHelpful status"
    revcStartS = "<p class=\"rClarity status"
    reviStartS = "<p class=\"rInterest status"
    
    
    pruneContent = []
    numReviewsSoFar = -1
    insideReview = False
    insideRating = False
    
    #Global properties
    name = ""
    dept = ""
    quality = ""
    helpful = ""
    clarity = ""
    easy = ""
    nr = ""
    
    #Properties of each review
    date = ""
    clas = ""
    comment = ""
    revQ = ""
    revH = ""
    revC = ""
    revE = ""
    revI = ""
    
    for line in prContents:
        print(line)
        if numReviewsSoFar == -1:   #Look for aggregate statistics only when reviews have not started
            nameInd = line.find(nameStartS)
            if nameInd != -1:   #Add the line containing the name
                lineContent = line[ line.find(">", nameInd + len(nameStartS)) + len(">"):]
                name = lineContent[:lineContent.find("</h2>")].replace("&nbsp;", " ")
                continue

            deptInd = line.find(deptStartS)
            if deptInd != -1:   #Add the line containing the name
                lineContent = line[ deptInd + len(deptStartS):]
                dept = lineContent[:lineContent.find("</strong>")].replace("&nbsp;", " ")
                continue                
                
            qualityInd = line.find(qualityStartS)
            if qualityInd != -1:    #Add the line containing the quality
                lineContent = line[ line.find("><strong>", qualityInd + len(qualityStartS)) + len("><strong>"):]
                quality =  lineContent[:lineContent.find("</strong>")]
                continue
                
            helpfulInd = line.find(helpfulStartS)
            if helpfulInd != -1:    #Add the line containing the helpful
                lineContent = line[ line.find("><strong>", helpfulInd + len(helpfulStartS)) + len("><strong>"):]
                helpful =  lineContent[:lineContent.find("</strong>")]
                continue
    
            clarityInd = line.find(clarityStartS)
            if clarityInd != -1:    #Add the line containing the clarity
                lineContent = line[ line.find("><strong>", clarityInd + len(clarityStartS)) + len("><strong>"):]
                clarity =  lineContent[:lineContent.find("</strong>")]
                continue
                
            easyInd = line.find(easyStartS)
            if easyInd != -1:   #Add the line containing the easiness
                lineContent = line[ line.find("><strong>", easyInd + len(easyStartS)) + len("><strong>"):]
                easy =  lineContent[:lineContent.find("</strong>")]
                continue
                  
            nrInd = line.find(numRatStartS)
            if nrInd != -1: #Add the line containing the number of ratings
                lineContent = line[ nrInd + len(numRatStartS):]
                nr =  lineContent[:lineContent.find("</strong>")]
                continue   
                  
            dateInd = line.find(dateStartS)
            if dateInd != -1:   #Indicate that the reviews are starting
                numReviewsSoFar += 1
                pruneContent.append( "Name:"+name )
                pruneContent.append( "Dept:"+dept )
                pruneContent.append( "Quality:"+quality )
                pruneContent.append( "Helpful:"+helpful )
                pruneContent.append( "Clarity:"+clarity )
                pruneContent.append( "Easy:"+easy )
                pruneContent.append( "NR:"+nr )
                continue
        elif not insideReview:
            dateInd = line.find(dateStartS)
            if dateInd != -1:   #Add the line containing the date
                lineContent = line[ dateInd + len(dateStartS) : ]
                date =  lineContent[:lineContent.find("</div>")]
                
                numReviewsSoFar += 1
                insideReview = True
                
                clas = ""
                comment = ""
                revQ = ""
                revH = ""
                revC = ""
                revE = ""
                revI = ""
                
                continue
        elif not insideRating:
            clasInd = line.find(clasStartS)
            if clasInd != -1:   #Add the line containing the class
                lineContent = line[ clasInd + len(clasStartS) : ]
                clas =  lineContent[:lineContent.find("</div>")]
                continue
                  
            if line.find(ratingStartS)!= -1:    #Signal that you are entering a rating
                insideRating = True
                
            commentInd = line.find(commentStartS)
            if commentInd != -1:    #Add the line containing the comment
                lineContent = line[ commentInd + len(commentStartS) : ]
                comment =  lineContent[:lineContent.find("</p")]
                pruneContent.append( "Date:"+date )
                pruneContent.append( "Class:"+clas )
                pruneContent.append( "RevQ:"+revQ )
                pruneContent.append( "RevH:"+revH )
                pruneContent.append( "RevC:"+revC )
                pruneContent.append( "RevE:"+revE )
                pruneContent.append( "RevI:"+revI )
                pruneContent.append( "Comment:"+comment )
                insideReview = False    #Signal that this is the end of the review
                continue      
        else:   #Get the rating scores for the review
            if line.find(revqS)!= -1:   #Add the quality
                if line.find("Poor")!= -1:
                    revQ = "Poor"
                elif line.find("Good")!= -1:
                    revQ = "Good"
                else:
                    revQ = "Average"
                continue
            
            reveInd = line.find(reveStartS)
            if reveInd != -1:   #Add the line containing the easiness rating of this review
                lineContent = line[ reveInd + len(reveStartS) : ]
                revE =  lineContent[:lineContent.find("\">")].replace("&nbsp;","")
                continue

            revhInd = line.find(revhStartS)
            if revhInd != -1:   #Add the line containing the helpfullness rating of this review
                lineContent = line[ revhInd + len(revhStartS) : ]
                revH =  lineContent[:lineContent.find("\">")].replace("&nbsp;","")
                continue
                  
            revcInd = line.find(revcStartS)
            if revcInd != -1:   #Add the line containing the clarity rating of this review
                lineContent = line[ revcInd + len(revcStartS) : ]
                revC =  lineContent[:lineContent.find("\">")].replace("&nbsp;","")
                continue
                  
            reviInd = line.find(reviStartS)
            if reviInd != -1:   #Add the line containing the interest rating of this review
                lineContent = line[ reviInd + len(reviStartS) : ]
                revI =  lineContent[:lineContent.find("\">")].replace("&nbsp;","")
                insideRating = False
                continue
            
    print("Professor list pruned to " + len(pruneContent) + " lines from " + len(prContents) + " lines")
    print(pruneContent)
    return pruneContent

CornellUniversity = RateMyProfScraper(298)
#pickle.dump(CornellUniversity, open( "raw_rateMyProfessor_data.p", "wb" ))

#CornellUniversity = pickle.load(open("raw_rateMyProfessor_data.p", "rb"))
#print(CornellUniversity.professorlist[0])
cardie_index = CornellUniversity.SearchProfessor("Claire Cardie")
tid = CornellUniversity.GetProfessorTID(cardie_index)
print(cardie_index)
print(tid) #521940
#CornellUniversity.GetRMPProfessorJSON(tid)
cardie_content = CornellUniversity.GetRMPProfessorPageContents(521940)
print(cardie_content)
pruneProfReviewFile(cardie_content)
#CornellUniversity.PrintProfessorInfo()
#CornellUniversity.PrintProfessorDetail(CornellUniversity.indexnumber)
#CornellUniversity.PrintProfessorDetail("overall_rating")

