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
        course_numbers_to_description_map_for_all_majors[dept + ' ' + course['courseNumber']] = course['description']

def recommend_classes_for_class(list_class_ids, list_tags):
    '''
    class_id = 'CS 2110' for example
    n = integer
    returns: [('CS 3110', description), ('CS 4820', description), ('CS 2112', description)]
    '''
    # A list of each class's description
    classes_representation = ""
    for class_id in list_class_ids:
        split_course_id = class_id.split(' ')
        dept = split_course_id[0]
        course_number = split_course_id[1]
        classes_representation += ' ' +  (course_numbers_to_description_map_for_all_majors[dept + ' ' + course_number])
    test_x = vectorizer.transform([classes_representation])
    sim_scores = cosine_similarity(X, test_x).flatten()
    top_score_indices = np.argsort(sim_scores)[::-1][0:20]


    top_10_class_indices = []
    prev_score = None
    for idx in top_score_indices:
        if sim_scores[idx] == prev_score:
            continue
        else:
            prev_score = sim_scores[idx]
            top_10_class_indices.append(idx)

        
    top_10_class_indices = top_10_class_indices[0:min(len(top_10_class_indices), 10)]
    top_similar_classes = [course_codes[x] for x in top_10_class_indices]
    top_n_similar_classes_and_descriptions = [(similar_class, course_numbers_to_description_map_for_all_majors[similar_class]) for similar_class in top_similar_classes]
    return top_n_similar_classes_and_descriptions

#print(recommend_classes_for_class(['CS 5740', 'CS 4670', 'CS 3110'], []))


