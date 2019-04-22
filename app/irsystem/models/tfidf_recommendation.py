import pickle as pkl
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#vectorizer = pkl.load(open("vectorizer.pkl", "rb"))
#X = pkl.load(open("tdm.pkl", "rb"))
#corpus = pkl.load(open("corpus.pkl", "rb"))
#course_codes  = pkl.load(open("course_codes.pkl", "rb"))

vectorizer = pkl.load(open("./app/irsystem/models/vectorizer.pkl", "rb"))
X = pkl.load(open("./app/irsystem/models/tdm.pkl", "rb"))
corpus = pkl.load(open("./app/irsystem/models/corpus.pkl", "rb"))
course_codes  = pkl.load(open("./app/irsystem/models/course_codes.pkl", "rb"))

with open("./data/courseroster/full_json.txt") as f:
    cornell_course_descriptions = json.load(f)

all_majors = list(cornell_course_descriptions.keys())
course_numbers_to_description_map_for_all_majors = {}
for dept in all_majors:
    for course in cornell_course_descriptions[dept]:
        course_numbers_to_description_map_for_all_majors[dept + ' ' + course['courseNumber']] = {'desc': course['description'], 
        'prof': course['professor'], 'prerequisite': course['prerequisite'], 'offered': course['offered'], 'length': course['courseLength']}

def recommend_classes_for_class(list_class_ids, list_tags:
    '''
    class_id = 'CS 2110' for example
    n = integer
    returns: [('CS 3110', description), ('CS 4820', description), ('CS 2112', description)]
    '''
    prof_ratings = pkl.load(open('../../../data/ratemyprofessor/prof_ratings.p', 'rb'))

    # A list of each class's description
    classes_representation = ""
    for class_id in list_class_ids:
        split_course_id = class_id.split(' ')
        dept = split_course_id[0]
        course_number = split_course_id[1]
        classes_representation += ' ' +  (course_numbers_to_description_map_for_all_majors[class_id]['desc'])
    for tag in list_tags:
        classes_representation += ' ' + tag
    test_x = vectorizer.transform([classes_representation])
    sim_scores = cosine_similarity(X, test_x).flatten()
    top_score_indices = np.argsort(sim_scores)[::-1][0:20]

    ### filter cross-listed courses
    top_10_class_indices = []
    prev_score = None
    for idx in top_score_indices:
        if sim_scores[idx] == prev_score:
            continue
        else:
            prev_score = sim_scores[idx]
            top_10_class_indices.append(idx)

    courseids = [course_codes[x] for x in top_10_class_indices]
    course_with_rating = []
    for course in courseids:
        if len(course_numbers_to_description_map_for_all_majors[course]['prof']) > 0:
            prof_name = course_numbers_to_description_map_for_all_majors[course]['prof'][0]
            if prof_name in prof_ratings:
                rating = prof_ratings[prof_name]
            else:
                course_with_rating.append((course, 0))
            course_with_rating.append((course, rating))
        else: 
            course_with_rating.append((course, 0))
    course_with_rating.sort(key=lambda x: x[1], reverse=True)

    top_10_courses = course_with_rating[0:min(len(course_with_rating), 10)]
    top_n_similar_classes_dict_and_rating = [(course_numbers_to_description_map_for_all_majors[similar_class], rating) for similar_class, rating in top_10_courses]

    # top_10_class_indices = top_10_class_indices[0:min(len(top_10_class_indices), 10)]
    # top_similar_classes = [course_codes[x] for x in top_10_class_indices]
    # top_n_similar_classes_and_descriptions = [course_numbers_to_description_map_for_all_majors[similar_class] for similar_class in top_similar_classes]

    return top_n_similar_classes_dict_and_rating

print(recommend_classes_for_class(['CS 5740', 'CS 4670', 'CS 3110'], []))


