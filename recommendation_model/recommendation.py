from gensim.models.doc2vec import Doc2Vec
import json
import pickle

model= Doc2Vec.load("d2v_just_description.model")
eng_representations_simple = pickle.load( open( "eng_representations_just_descriptions.p", "rb" ))
#print(eng_representations_simple.keys())
# with open("../data/courseroster/full_json.txt") as f:
#     cornell_course_descriptions = json.load(f)

eng_majors = ['BEE', 'BME', 'CHEME', 'CEE', 'CS', 'EAS','ECE', 'AEP', 'BEE', 'INFO', 'MSE', 'MAE', 'ORIE']
# course_numbers_and_descriptions_for_eng_majors = []
# for dept in eng_majors:
#     for course in cornell_course_descriptions[dept]:
#         course_numbers_and_descriptions_for_eng_majors.append((dept + ' ' + course['courseNumber'], course['description']))

course_numbers_and_descriptions_for_eng_majors = [(key, value) for key, value in eng_representations_simple.items()]
#print([key for (key, value) in course_numbers_and_descriptions_for_eng_majors])
def recommend_n_classes_for_class(class_id, n):
    '''
    class_id = 'CS 2110' for example
    n = integer
    returns: [('CS 3110', description), ('CS 4820', description), ('CS 2112', description)]
    '''
    split_course_id = class_id.split(' ')
    dept = split_course_id[0]
    course_number = split_course_id[1]
    index_for_class = [course[0] for course in course_numbers_and_descriptions_for_eng_majors].index(class_id)
    similar_docs = model.docvecs.most_similar(str(index_for_class))
    print(similar_docs)
    similar_docs_indices = [int(val[0]) for val in similar_docs]
    top_n_similar_docs_indices = similar_docs_indices[:n]
    similar_classes_and_descriptions = [course_numbers_and_descriptions_for_eng_majors[int(val[0])] for val in similar_docs]
    top_n_similar_classes_and_descriptions = similar_classes_and_descriptions[:n]
    return [val[0] for val in top_n_similar_classes_and_descriptions]

print(recommend_n_classes_for_class('CS 3152', 5))


