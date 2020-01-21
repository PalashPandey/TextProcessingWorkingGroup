from IPython import get_ipython

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sklearn
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)
from sklearn.manifold import TSNE
import spacy
import en_core_web_sm
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

data = requests.get("http://catalog.drexel.edu/coursedescriptions/quarter/undergrad/")

data.text[:1000]


link_page_soup = BeautifulSoup(data.text, 'html.parser')


# To find all the links to course descriptions

list_link_divs = link_page_soup.find_all("div", class_="qugcourses")
len(list_link_divs)


list_links_a = []
for div in list_link_divs:
#     print(div.find_all("a"))
#     print("*"*100)
    for a in div.find_all("a",  href=True):
#         print("http://catalog.drexel.edu/" + a['href'])
        list_links_a.append("http://catalog.drexel.edu/" + a['href'] )


course_name_description_list = []
for course_link in list_links_a:
    course_soup = BeautifulSoup(requests.get(course_link).text, 'html.parser')
    for course in course_soup.find_all("div", class_="courseblock"):
#         print(course.find("p" , class_ = "courseblocktitle").text)
#         print(course.find("p" , class_ = "courseblockdesc").text)        
        course_name_description_list.append([course.find("p" , class_ = "courseblocktitle").text, course.find("p" , class_ = "courseblockdesc").text ])

# As you can probably see, the data that we extract is fairly messy, we need some preprocessing before we can start to play with it.

course_df = pd.DataFrame(course_name_description_list)
course_df.columns = ["TitleBlock" , "DescriptionBlock"]
course_df


# We can use regular expressions to extract the three pieces of data that we need from the TitleBlock. 


course_df = pd.concat([course_df,  course_df.TitleBlock.str.extract(r"(.*\s*\d{3,5})\s*(.*)(\d.\d)") ], axis =1 )

course_df.columns = ["TitleBlock" , "DescriptionBlock", "CourseID" , "CourseName" , "Credits" ]



course_df.DescriptionBlock = course_df.DescriptionBlock.str.replace("\n", "")

# You might remember TF-IDF from our last meeting. It is a way to represent sentences (documents) using their frequency and unique-ness. We use TF-IDF here to get vector representation of our course descriptions. 


tfidf_vectorizer = TfidfVectorizer(use_idf=True)
tfidf_matrix = tfidf_vectorizer.fit_transform(course_df["DescriptionBlock"])



tfidf_matrix.shape




course_df["tf_idf_vector"] = pd.DataFrame(tfidf_matrix.todense()).values.tolist()


course_df["tf_idf_vector"]


course_df["CourseID"] = course_df["CourseID"].str.replace("\xa0", ' ')
course_df.columns


def get_tf_idf_by_course(course_name):
    return np.array(np.array(course_df[course_df["CourseID"] == course_name]["tf_idf_vector"])[0]).reshape(1, -1)


def get_cosine_similarity(course_a , course_b):
    return sklearn.metrics.pairwise.cosine_similarity(get_tf_idf_by_course(course_a) , get_tf_idf_by_course(course_b) )     



sklearn.metrics.pairwise.cosine_similarity(get_tf_idf_by_course("CS 171") , get_tf_idf_by_course("INFO 151") ) 
# get_tf_idf_by_course("CS 172")



get_cosine_similarity("CS 171", "INFO 152")



get_cosine_similarity("CS 171", "ENGL 101")



get_cosine_similarity("ENGL 101", "ENGL 102")



sklearn.metrics.pairwise.cosine_similarity(np.array(course_df["tf_idf_vector"].values[0]).reshape(1, -1)  )     




course_df["tf_idf_vector"] = course_df["tf_idf_vector"].apply(lambda x: np.array(x))

course_df["tf_idf_vector"]



tf_idf_cosine_sim = linear_kernel(tfidf_matrix , tfidf_matrix)



def get_recommendations(title, cosine_sim=tf_idf_cosine_sim):

    try:
        # Get the index of the movie that matches the title
        idx = pd.Index(course_df["CourseID"]).get_loc(title)
    #     # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        # Most similar is the course itself
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]
        final_recommendations =  course_df[['CourseID'] ].iloc[movie_indices]['CourseID'].values
        print(final_recommendations)
        # Return the top 10 most similar movies
    except Exception as e:
        print(title)
        print(e)
        final_recommendations = []
    return final_recommendations

# get_recommendations("CS 172", tf_idf_cosine_sim)

# get_recommendations("INFO 151", tf_idf_cosine_sim)

# get_recommendations("ENGL 101", tf_idf_cosine_sim)


course_df["Top10Recommendations"] = course_df["CourseID"].apply(lambda x : get_recommendations(x, tf_idf_cosine_sim) )

course_df.to_csv('course_df.csv')