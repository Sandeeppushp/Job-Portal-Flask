from flask import Blueprint, Flask, request, jsonify, render_template,session,send_from_directory,redirect,url_for
import random
import string
import sqlite3
import datetime
import time
import os
import base64
import company
import candidate

from waitress import serve

from flask_talisman import Talisman


app = Flask(__name__)
Talisman(app)


app.config['SECRET_KEY'] = 'protect this key at any cost'
app.register_blueprint(company.company_api)
app.register_blueprint(candidate.candidate_api)


conn_company = sqlite3.connect('company.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)
conn_candidate = sqlite3.connect('candidate.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)
conn_jobs = sqlite3.connect('jobs.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)
conn_session = sqlite3.connect('session.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)



conn_company.execute('''CREATE TABLE IF NOT EXISTS company_main
         (id INTEGER NOT NULL PRIMARY KEY,
         company_name TEXT,
         company_country TEXT,
         company_city TEXT,
         company_phone TEXT,
         company_total_employees TEXT,
         company_about TEXT,
         company_email TEXT,
         company_password TEXT,
         public_id TEXT,
         token TEXT,
         datetime timestamp
         );''')
conn_company.commit()


conn_candidate.execute('''CREATE TABLE IF NOT EXISTS candidate_main
         (id INTEGER NOT NULL PRIMARY KEY,
         candidate_name TEXT,
         candidate_gender TEXT,
         candidate_dob TEXT,
         candidate_mobile TEXT,
         candidate_mobile2 TEXT,
         candidate_email TEXT,
         candidate_email2 TEXT,
         candidate_experience TEXT,
         candidate_skills TEXT,
         candidate_past_experiences TEXT,
         candidate_prefered_location TEXT,
         candidate_education TEXT,
         candidate_profile_summary TEXT,
         candidate_accomplishments TEXT,
         candidate_certification TEXT,
         candidate_designation TEXT,
         candidate_current_salary TEXT,
         candidate_expected_salary TEXT,
         candidate_password TEXT,
         public_id TEXT,
         token TEXT,
         datetime timestamp
         );''')
conn_candidate.commit()



conn_jobs.execute('''CREATE TABLE IF NOT EXISTS jobs_table
         (id INTEGER NOT NULL PRIMARY KEY,
         job_title TEXT,
         job_type TEXT,
         job_role TEXT,
         job_salary_range TEXT,
         job_skill TEXT,
         job_experience TEXT,
         job_location TEXT,
         job_description TEXT,
         company_email TEXT,
         job_id TEXT,
         datetime timestamp
         );''')
conn_jobs.commit()

conn_jobs.execute('''CREATE TABLE IF NOT EXISTS jobs_applied_table
         (id INTEGER NOT NULL PRIMARY KEY,
         job_id TEXT,
         candidate_email TEXT,
         datetime timestamp
         );''')
conn_jobs.commit()



conn_session.execute('''CREATE TABLE IF NOT EXISTS UserSession
         (id INTEGER NOT NULL PRIMARY KEY,
         user TEXT,
         ip TEXT,
         user_agent TEXT,
         category TEXT,
         endpoint TEXT,
         datetime TIMESTAMP);''')
conn_session.commit()




def random_char(y):
        return ''.join(random.choice(string.digits) for x in range(y))







@app.before_first_request
def before_first_request_func():
    print("Job Portal is running...")



@app.before_request
def before_request():
    try:
        ip_address=request.environ['HTTP_X_FORWARDED_FOR']
    except:
        return jsonify({'data':'Forbidden'}),403
        
    user_agent=str(request.headers.get('User-Agent'))
    datetime_dt=datetime.datetime.today() 
    url=request.url 
    method=request.method

    #print(ip_address,user_agent)

    conn_IP_DB= sqlite3.connect('static/IP_DB/'+str(datetime_dt.date()).replace('-','_')+'.db')
    conn_IP_DB.execute('''CREATE TABLE IF NOT EXISTS IP_Main_Table
             (id INTEGER NOT NULL PRIMARY KEY,
             ip TEXT,
             user_agent TEXT,
             datetime TIMESTAMP,
             url text,
             method text);''')
    conn_IP_DB.commit()


    #checking multiple requests
    last_minute_time=datetime_dt-datetime.timedelta(minutes = 1)
    #select ip,datetime FROM IP_Main_Table where ip="111.93.42.146" AND (datetime BETWEEN '2021-03-08 16:00:00.000000' AND '2021-03-08 17:00:00.000000')

    check_requests_freq=conn_IP_DB.execute('SELECT * FROM IP_Main_Table WHERE ip="'+ip_address+'" AND (datetime BETWEEN "'+str(last_minute_time)+'" AND "'+str(datetime_dt)+'")').fetchall()
    #print(len(check_requests_freq))
    if len(check_requests_freq)>=20:
        return jsonify({'data':'Too Many Requests'}),429

    conn_IP_DB.execute("INSERT INTO IP_Main_Table(ip,user_agent,datetime,url,method) values(?,?,?,?,?)" ,(ip_address,user_agent,datetime_dt,url,method))
    conn_IP_DB.commit()






@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-access-token')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

  response.headers['server'] = 'Private Server'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '0'
  response.cache_control.max_age = 30
  return response
    




@app.route('/', methods=['GET','POST'])
def home():
    return 'Hello World',200
















if (__name__ == "__main__"):
    app.run(debug=True)
    #http = WSGIServer(('0.0.0.0',7000), app)
    #http.serve_forever()
    #serve(app, host='0.0.0.0', port=5000, threads=6) #WAITRESS!
    





