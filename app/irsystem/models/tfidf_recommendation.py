import pickle as pkl
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random
import re
import io

# vectorizer = pkl.load(open("vectorizer.pkl", "rb"))
# X = pkl.load(open("tdm.pkl", "rb"))
# course_codes  = pkl.load(open("../../../app/irsystem/models/course_codes.pkl", "rb"))
# master_course_codes_list =  pkl.load(open("../../../data/courseroster/course_codes_II.pkl", "rb"))

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())

vectorizer = pkl.load(open("../../../app/irsystem/models/vectorizer.pkl", "rb"))
X = pkl.load(open("../../../app/irsystem/models/tdm.pkl", "rb"))
course_codes  = pkl.load(open("../../../app/irsystem/models/course_codes.pkl", "rb"))
master_course_codes_list =  pkl.load(open("../../../data/courseroster/course_codes_II.pkl", "rb"))
prof_ratings = pkl.load(open('../../../data/ratemyprofessor/prof_ratings.p', 'rb'))


with open("../../../data/courseroster/full_json.json", encoding='utf-8') as f:
    cornell_course_descriptions = json.load(f)

all_majors = list(cornell_course_descriptions.keys())
course_numbers_to_description_map_for_all_majors = {}
for dept in all_majors:
    for course in cornell_course_descriptions[dept]:
        course_numbers_to_description_map_for_all_majors[dept + ' ' + course['courseNumber']] = {'desc': course['description'], 
        'prof': course['professor'], 'url': course['url'], 'prerequisite': course['prerequisite'], 'offered': course['offered'], 'courseLength': course['courseLength'],
        'title': course['courseTitle'], 'crosslisted': course['crosslisted']}

# Returns a list of class ids corresponding to class ids actually in the json
# Also removes duplicate classes that the user inputs
def preprocess_class_ids(list_class_ids, cornell_course_descriptions):
    # dept code like CS, or INFO
    all_majors = list(cornell_course_descriptions.keys())
    result_list_class_ids = []

    for class_id in list_class_ids:
        for dept in all_majors:
            for course in cornell_course_descriptions[dept]:
                crosslisted_courses = course['crosslisted']
                full_course_code = dept + ' ' + course['courseNumber']
                # If class_id matches a class in the list of cross listed or the current class
                if class_id in crosslisted_courses or class_id == full_course_code:
                    result_list_class_ids.append(full_course_code)
    return result_list_class_ids

def recommend_classes_for_class(list_class_ids, tag_list, ratio):
    '''
    n = integer
    returns: [('CS 3110', description), ('CS 4820', description), ('CS 2112', description)]
    '''
    # A combined string of each class's description

    list_class_ids = preprocess_class_ids(list_class_ids, cornell_course_descriptions)

    similarity_score_cutoff = 0.00
    top_similar_classes = []
    if list_class_ids != []:
        classes_representation = ""
        for class_id in list_class_ids:
            split_course_id = class_id.split(' ')
            dept = split_course_id[0]
            course_number = split_course_id[1]
            classes_representation += ' ' +  (course_numbers_to_description_map_for_all_majors[dept + ' ' + course_number]['desc'])
            break;
        test_x = vectorizer.transform([classes_representation])
        sim_scores_from_classes = cosine_similarity(X, test_x).flatten()
        ranked_scores_from_classes = np.sort(sim_scores_from_classes)[::-1]
        ranked_indices = np.argsort(sim_scores_from_classes)[::-1]

        for i in range(len(ranked_scores_from_classes)):
            if ranked_scores_from_classes[i]< similarity_score_cutoff:
                ranked_indices = ranked_indices[0:i]
                break
        ranked_course_codes = [course_codes[x] for x in ranked_indices]

        top_similar_classes = filter_top_20(list_class_ids, ranked_course_codes) 

    top_similar_classes_tags = []
    if tag_list != []:
        # Incorporate the tags
        classes_related_to_tags = set()
        for tag in tag_list:
            classes_related_to_tag = [(course_number, description['desc']) for course_number, description in course_numbers_to_description_map_for_all_majors.items() if description['desc'] != None and tag in description['desc']]
            classes_related_to_tags.update(classes_related_to_tag)
        classes_related_to_tags_descriptions = [description for _, description in classes_related_to_tags]
        random.Random(1).shuffle(classes_related_to_tags_descriptions)
        classes_related_to_tags_descriptions = classes_related_to_tags_descriptions[0:min(15, len(classes_related_to_tags_descriptions))]
        classes_related_to_tags_descriptions = ' '.join(classes_related_to_tags_descriptions)
        test_x_tags = vectorizer.transform([classes_related_to_tags_descriptions])
        sim_scores_from_tags = cosine_similarity(X, test_x_tags).flatten()
        ranked_scores_from_tags = np.sort(sim_scores_from_tags)[::-1]
        ranked_tag_indices = np.argsort(sim_scores_from_tags)[::-1]
        for i in range(len(ranked_scores_from_tags)):
            if sim_scores_from_tags[i]< similarity_score_cutoff:
                ranked_tag_indices = ranked_tag_indices[0:i]
                break
        ranked_similar_classes_tags = [course_codes[x] for x in ranked_tag_indices]
        top_similar_classes_tags = filter_top_20(tag_list, ranked_similar_classes_tags) 

    top_10_results = apply_slider_priority(ratio, top_similar_classes, top_similar_classes_tags)

    top_10_results_with_descriptions = [(similar_class, course_numbers_to_description_map_for_all_majors[similar_class]) for similar_class in top_10_results]

    rank_by_rating = []
    for courseid, course_info in top_10_results_with_descriptions: 
        for key, value in course_info.items():
            course_info[key] = value
            regex = re.compile('[^a-zA-Z0-9]')
            if isinstance(value, str):
                value = regex.sub(' ', value)
                course_info[key] = value
        
        if course_info['prof'] != None and len(course_info['prof']) > 0:
            try: 
                instructor_rating = prof_ratings[course_info['prof'][0]]
                course_info['replacementRating'] = False
            except: 
                instructor_rating = 3.0
                course_info['replacementRating'] = True
            course_info['rating'] = instructor_rating
            if instructor_rating is None:
                instructor_rating = 3
            rank_by_rating.append((courseid, course_info, instructor_rating))
    final_ranking = [(similar_class, info) for similar_class, info,_ in rank_by_rating]
    
    return final_ranking

# Priority 0 is all classes, and priority 1.0 is all tags
def apply_slider_priority(priority, course_recommendations, tag_recommendations):
    num_recommendations = min(10, len(course_recommendations + tag_recommendations))
    final_recommendations = []
    for i in range(num_recommendations):
        if random.random() <= priority: 
            try:
                final_recommendations.append(tag_recommendations.pop(0))
            except:
                final_recommendations.append(course_recommendations.pop(0))
        else: 
            try:
                final_recommendations.append(course_recommendations.pop(0))
            except:
                final_recommendations.append(tag_recommendations.pop(0))               

    return final_recommendations

def get_prereq(course_info, course_codes ,depth=10):
    sentence = course_info['prerequisite']
    regex = re.compile('[\W]')
    sentence = regex.sub(' ', sentence)

    prereqs = []
    tokens = sentence.split(' ')
    
    if len(tokens) > 0 and depth > 0:
        for i in range(len(tokens) - 1): 
            bigram = tokens[i] + " " + tokens[i + 1]
            # print(bigram)
            if bigram in master_course_codes_list:
                prereqs.append(bigram)
            
        # print(prereqs)
        # print("************")
        # print(preprocess_class_ids(prereqs, cornell_course_descriptions))
        for course_id in preprocess_class_ids(prereqs, cornell_course_descriptions):
            if course_id not in prereqs:
                prereqs+= get_prereq(course_numbers_to_description_map_for_all_majors[course_id], course_codes, depth-1)
    
    return prereqs

def filter_top_20(input_lst, course_codes):
    num_courses = min(20, len(course_codes))
    prereq_list = []

    for input_course_id in input_lst:
        if input_course_id in course_codes:
            course_info = course_numbers_to_description_map_for_all_majors[input_course_id]
            prereq_list += get_prereq(course_info, course_codes)

    top_20_codes = []
    for i in range(num_courses):
        course_info = course_numbers_to_description_map_for_all_majors[course_codes[i]]
        
        overlap = False
        for crosslisted_code in course_info['crosslisted']:
            if crosslisted_code in input_lst or crosslisted_code in prereq_list:
                overlap = True

        if course_codes[i] in input_lst or course_codes[i] in prereq_list or overlap:
            continue
        top_20_codes.append(course_codes[i])
        
    return top_20_codes

# for key, value in recommend_classes_for_class(['CS 4780'], ['statistics'], 0.0):
#     print(key)
#     print(value)
#     print("**************************************")
# print(recommend_classes_for_class(['CS 3110'], ['statistics'], 0.0))
