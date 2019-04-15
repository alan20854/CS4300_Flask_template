import pickle
import testRMPScraper.RateMyProfScraper

CornellUniversity = pickle.load(open("raw_rateMyProfessor_data.p", "rb"))
for i in len(CornellUniversity.professorlist):
	print(CornellUniversity.professorlist[i])
	if i == 5:
		break