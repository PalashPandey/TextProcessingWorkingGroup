import os
from flask import *
import pandas as pd
import math
import json
from pandas.io.json import json_normalize
import csv
from collections import defaultdict
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def test_html():
	return render_template('index.html') 


#We will render the html page
@app.route('/background_query')
def get_course_id():
	course_id = request.args.get('course_id',0,type=str)
	return course_id.upper()

def query_csv(course_id):
	csv_url = 'https://raw.githubusercontent.com/PalashPandey/TextProcessingWorkingGroup/master/CourseRecommendation/static/course_df.csv'
	df = pd.read_csv(csv_url,sep='\t')
	course_name = (df.loc[df['CourseID']==course_id]['CourseName'])
	course_description = (df.loc[df['CourseID']==course_id]['DescriptionBlock'])
	credits = (df.loc[df['CourseID']==course_id]['Credits'])[0]
	course_name = str(course_name.tolist()[0])
	course_description = str(course_description.tolist()[0])
	final_list = (df.loc[df['CourseID'] == course_id]['Top10Recommendations'])
	final_list = ast.literal_eval(final_list[0])
	#return course_name,final_list
	return [course_id,course_name,course_description,str(credits),str(final_list)]


def return_JSON(parse_list):
	final_dict = {"CourseID":parse_list[0],"courseName":parse_list[1],"courseDescription":parse_list[2],"credits":parse_list[3],"recList":parse_list[4]}
	str_obj = json.dumps(final_dict)
	json_obj = json.loads(str_obj)
	
	return json_obj	


if __name__ == '__main__':
	app.run(debug=True, port=55 )
