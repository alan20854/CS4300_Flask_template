import pickle as pkl
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random

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
        'prof': course['professor'], 'prerequisite': course['prerequisite'], 'offered': course['offered'], 'length': course['courseLength'],
        'title': course['courseTitle']}

def recommend_classes_for_class(list_class_ids, tag_list):
    '''
    class_id = 'CS 2110' for example
    n = integer
    returns: [('CS 3110', description), ('CS 4820', description), ('CS 2112', description)]
    '''
    # A combined string of each class's description


    top_n_similar_classes_and_descriptions = []

    top_n_similar_classes_and_descriptions_tags = []

    if list_class_ids != []:
        classes_representation = ""
        for class_id in list_class_ids:
            split_course_id = class_id.split(' ')
            dept = split_course_id[0]
            course_number = split_course_id[1]
            classes_representation += ' ' +  (course_numbers_to_description_map_for_all_majors[dept + ' ' + course_number]['desc'])
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
        top_7_class_indices = top_10_class_indices[0:min(len(top_10_class_indices), 7)]
        top_similar_classes = [course_codes[x] for x in top_7_class_indices]
        top_n_similar_classes_and_descriptions = [(similar_class, course_numbers_to_description_map_for_all_majors[similar_class]) for similar_class in top_similar_classes]

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
        sim_scores_tags = cosine_similarity(X, test_x_tags).flatten()
        top_score_tag_indices = np.argsort(sim_scores_tags)[::-1][0:20]


        top_10_class_tag_indices = []
        prev_score = None
        for idx in top_score_tag_indices:
            if sim_scores_tags[idx] == prev_score:
                continue
            else:
                prev_score = sim_scores_tags[idx]
                top_10_class_tag_indices.append(idx)

        top_3_class_tag_indices = top_10_class_tag_indices[0:min(len(top_10_class_tag_indices), 3)]
        top_similar_classes_tags = [course_codes[x] for x in top_3_class_tag_indices]
        top_n_similar_classes_and_descriptions_tags = [(similar_class, course_numbers_to_description_map_for_all_majors[similar_class]) for similar_class in top_similar_classes_tags]



    res_list = top_n_similar_classes_and_descriptions + top_n_similar_classes_and_descriptions_tags
    random.Random(1).shuffle(res_list)
    return res_list

#print(recommend_classes_for_class(['CS 3110'], ['programming', 'statistics']))