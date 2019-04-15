from gensim.models.doc2vec import Doc2Vec
import json
import pickle

model= Doc2Vec.load("d2v.model")
cs_representations_simple = pickle.load( open( "cs_representations_simple.p", "rb" ))
with open("./data/courseroster/full_json.txt") as f:
    cornell_course_descriptions = json.load(f)

def recommend_n_classes_for_class(class_id, n):
    '''
    class_id = 'CS 2110' for example
    n = integer
    returns: [('CS 3110', description), ('CS 4820', description), ('CS 2112', description)]
    '''
    dept = class_id[0:2]
    course_number = class_id[3:]
    data = [(value[0], value[1]) for _, value in cs_representations_simple.items()]
    course_numbers_for_major = [data['courseNumber'] for data in cornell_course_descriptions[dept]]
    course_descriptions_for_major = [data['description'] for data in cornell_course_descriptions[dept]]
    index_for_class = course_numbers_for_major.index(course_number)
    similar_docs = model.docvecs.most_similar(str(index_for_class))
    similar_docs_indices = [int(val[0]) for val in similar_docs]
    top_n_similar_docs_indices = similar_docs_indices[:n]
    similar_classes = [course_numbers_for_major[int(val[0])] for val in similar_docs]
    top_n_similar_classes = similar_classes[:n]
    top_n_similar_classes_with_dept = [('CS ' + course_numbers_for_major[i], course_descriptions_for_major[i]) for i in top_n_similar_docs_indices]
    return top_n_similar_classes_with_dept

# print(recommend_n_classes_for_class('CS 3110', 5))


