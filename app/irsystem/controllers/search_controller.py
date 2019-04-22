from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models import recommendation as Recommendation
import pickle

project_name = "Course Finder"
net_id = "Alan Yan: ayy23, Jimmy Chen: jzc8, Thomas Chen: trc82, Victoria Litvinova: vl242"

#cs_classes = pickle.load(open("./../data/courseroster/en_course_names.p", "rb"))

@irsystem.route('/', methods=['GET'])
def home():
	return render_template('search.html', name=project_name, netid=net_id)

@irsystem.route('/search', methods=['GET', 'POST'])
def search():
	#query = request.args.get('search')
	class_names = request.json
	print(class_names)
	if request.json:
		class_names = request.json['class_name'].split(',')
		tag_names = request.json['tag_name'].split(',')
		course_ids = []
		for i in class_names:
			course_ids.append(i[:i.find(':')])
		data = Recommendation.recommend_n_classes_for_class(course_ids[0], 5)
		json_dict = {}
		json_dict['recommendations'] = []
		for i in data:
			k, v = i
			class_dict = {}
			class_dict["course"] = k
			class_dict["description"] = v
			json_dict['recommendations'].append(class_dict)
		return(json.dumps(json_dict))

	return None
	#return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
