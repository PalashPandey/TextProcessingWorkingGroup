import os
from flask import *
import pandas as pd
import math
import json
from pandas.io.json import json_normalize
import csv
from collections import defaultdict
import json
import ast
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def test_html():
	return render_template('index.html') 


#We will render the html page
@app.route('/background_query', methods=['GET', 'POST'] )
def get_course_id():
	print(request.args.get('course_name', "INFO 151", type=str) )
	# print(ast.literal_eval(request.data.decode("utf-8", "ignore"))["course_name"] )
	course_id = request.args.get('course_name', "INFO 151", type=str)
	result_list = query_csv(course_id.upper())
	print(result_list)
	result_json = return_JSON(result_list)
	return result_json


csv_url = 'https://raw.githubusercontent.com/PalashPandey/TextProcessingWorkingGroup/master/CourseRecommendation/static/course_df_pipe.csv'
df = pd.read_csv(csv_url,sep='|')

def query_csv(course_id):
	course_name = (df.loc[df['CourseID']==course_id]['CourseName'])
	course_description = (df.loc[df['CourseID']==course_id]['DescriptionBlock'])
	print(float(df.loc[df['CourseID']==course_id]['Credits'].values[0]))

	credits = float(df.loc[df['CourseID']==course_id]['Credits'].values[0])
	course_name = str(course_name.tolist()[0])
	course_description = str(course_description.tolist()[0])
	print(course_name)

	final_list = (df.loc[df['CourseID'] == course_id]['Top10Recommendations'])

	print(ast.literal_eval(final_list.values[0]))

	final_list = ast.literal_eval(final_list.values[0])
	final_list_with_json = []
	for course in final_list:
		final_list_with_json.append({"CourseID": course,"courseName": str(df.loc[df['CourseID']==course]['CourseName'].tolist()[0])  ,"courseDescription": str(df.loc[df['CourseID']==course]['DescriptionBlock'].tolist()[0]) ,"credits": float(df.loc[df['CourseID']==course]['Credits'].values[0]) }
)
	#return course_name,final_list
	return [course_id,course_name,course_description,str(credits),final_list_with_json]


def return_JSON(parse_list):
	final_dict = {"CourseID":parse_list[0],"courseName":parse_list[1],"courseDescription":parse_list[2],"credits":parse_list[3],"recList":parse_list[4]}
	str_obj = json.dumps(final_dict)
	json_obj = json.loads(str_obj)
	
	return json_obj	


if __name__ == '__main__':
	app.run(debug=True, port=30 )
