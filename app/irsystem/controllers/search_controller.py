from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import pickle

project_name = "Course Finder"
net_id = "Alan Yan: ayy23, Jimmy Chen: jzc8, Thomas Chen: trc82, Victoria Litvinova: vl242"

#cs_classes = pickle.load(open("../data/courseroster/CS_course_names.p", "rb"))
cs_classes = ['CS 1110: Intro Computing Using Python', 'CS 1112: Intro Computing Using MATLAB', 'CS 1132: Short Course in MATLAB', 'CS 1133: Short Course in Python', 'CS 1380: Data Science for All', 'CS 1710: Intro to Cognitive Science', 'CS 1998: Freshmen Team Projects', 'CS 2043: UNIX Tools and Scripting', 'CS 2110: Obj-Oriented Prog & Data Struc', 'CS 2111: Programming Practicum', 'CS 2300: Intermed Design&Prog for Web', 'CS 2770: Computational Sustainability', 'CS 2800: Discrete Structures', 'CS 2802: Discrete Structures - Honors', 'CS 3110: Data Struct & Functional Progr', 'CS 3152: Intro Game Architecture', 'CS 3300: Data-Driven Web Applications', 'CS 3410: Systems Programming', 'CS 3420: Embedded Systems', 'CS 3758: Autonomous Mobile Robots', 'CS 4090: Teaching Experience in CS', 'CS 4120: Introduction to Compilers', 'CS 4121: Practicum in Compilers', 'CS 4152: Adv Game Architecture', 'CS 4160: Formal Verification', 'CS 4220: Num Analysis: Lin&Nonlin Equat', 'CS 4300: Language and Information', 'CS 4410: Operating Systems', 'CS 4411: Practicum in Oper Syst', 'CS 4450: Intro to Computer Networks', 'CS 4670: Intro to Computer Vision', 'CS 4700: Foundations of Artif Inllgnce', 'CS 4701: Prac in A I', 'CS 4744: Computational Linguistics', 'CS 4754: Human Robot Interaction', 'CS 4786: Machine Learning Data Science', 'CS 4787: Principles of Large-Scale ML', 'CS 4820: Intro Analysis of Algorithms', 'CS 4850: Math Foundations Inform Age', 'CS 4852: Networks II: Market Design', 'CS 4990: International Research Intern', 'CS 4998: Team Projects', 'CS 4999: Independent Reading & Research', 'CS 5120: Introduction to Compilers', 'CS 5121: Practicum in Compilers', 'CS 5150: Software Engineering', 'CS 5152: Open-Source Software Engr.', 'CS 5199: Comp Program & Problem Solving', 'CS 5304: Data Science in the Wild', 'CS 5412: Cloud Computing', 'CS 5430: System Security', 'CS 5431: Practicum in System Security', 'CS 5433: Blockchains & Cryptocurrencies', 'CS 5625: Interactive Computer Graphics', 'CS 5670: Intro to Computer Vision', 'CS 5726: Learning and Decision Making', 'CS 5740: Natural Language Processing', 'CS 5786: Machine Learning Data Science', 'CS 5787: Deep Learning', 'CS 5854: Networks and Markets', 'CS 5998: MEng Internship', 'CS 5999: Master of Engineering Project', 'CS 6110: Adv Progr Languages', 'CS 6241: Data Science Numerics', 'CS 6320: Database Systems', 'CS 6360: Educational Technology', 'CS 6700: Advanced Artificial Intelligen', 'CS 6740: Advanced Language Technologies', 'CS 6780: Advanced Machine Learning', 'CS 6831: Designing Secure Cryptography', 'CS 6860: Logics of Programs', 'CS 7090: Computer Science Colloquium', 'CS 7190: Sem in Prog Lang and Compilers', 'CS 7194: Great Works in Prog. Lang.', 'CS 7290: Scientific Computing Seminar', 'CS 7490: Syst Res Seminar', 'CS 7493: Computer Security Seminar', 'CS 7690: Seminar in Computer Graphics', 'CS 7790: Seminar in Artificial Intell.', 'CS 7792: Special Topics - Machine Learn', 'CS 7794: Sem in Natural Lang Understndg', 'CS 7796: Robotics Seminar', 'CS 7890: Sem Theory of Alg & Comp', 'CS 7893: Cryptography Seminar', 'CS 7999: Independent Research', 'CS 9999: Thesis Research']
@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		#course_id = query[:query.find(':')]
		#print(course_id)
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, cs_classes=cs_classes)



