from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import pickle

project_name = "Course Finder"
net_id = "Alan Yan: ayy23, Jimmy Chen: jzc8, Thomas Chen: trc82, Victoria Litvinova: vl242"

cs_classes = pickle.load(open("../../../data/courseroster/CS_course_names.p", "wb"))

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query + cs_classes[0]
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



