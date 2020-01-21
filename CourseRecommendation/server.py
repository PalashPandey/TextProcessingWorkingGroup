import os
from flask import *
import pandas as pd
import math
import json
from pandas.io.json import json_normalize

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'





@app.route('/homepage')
def homepage():
	return render_template('old_index.html' )


if __name__ == '__main__':
	app.run(debug=True, port=55 )
