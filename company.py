from flask import Blueprint, Flask, request, jsonify, render_template,session,send_from_directory,redirect,url_for
import flask
import requests
import os
import shutil
import sqlite3
import uuid
import datetime
import jwt

from functools import wraps
from flask import current_app
#secret_key=current_app.config["SECRET_KEY"]
company_api = Blueprint('company_api', __name__)


conn_company = sqlite3.connect('company.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)

conn_jobs = sqlite3.connect('jobs.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)

conn_session = sqlite3.connect('session.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)

    	




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        #try:
            # decoding the payload to fetch the stored details
        #print(token)
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"],algorithms="HS256")
        except:
            return jsonify({'message' : 'Invalid Token'}), 401
        current_user=conn_company.execute('SELECT company_email FROM company_main WHERE public_id = "'+data['public_id']+'"').fetchone()
        if current_user==[]:
            return jsonify({'message' : 'Invalid User'}), 401
        
        return f(current_user, *args, **kwargs)

    return decorated



#tested
@company_api.route('/company_login', methods=['POST'])
def company_login():
    user_agent=str(request.headers.get('User-Agent'))
    ip_address=request.environ['HTTP_X_FORWARDED_FOR']
    datetime_now=datetime.datetime.now()

    user_session_data=conn_session.execute("SELECT * FROM UserSession where ip='"+ip_address+"' ORDER BY id DESC LIMIT 10;").fetchall()
    #print(user_session_data)
    if len(user_session_data)==10 and (datetime.datetime.now()-datetime.datetime.strptime(str(user_session_data[-1][6]), '%Y-%m-%d %H:%M:%S.%f')).seconds < 60:
      return jsonify({'data':'Too Many Attempts, Please wait for 1 Minute'}),429

    conn_session.execute("INSERT INTO UserSession(user,ip,user_agent,category,endpoint,datetime) values(?,?,?,?,?,?)" ,('',ip_address,user_agent,'company','/company_login',datetime_now))
    conn_session.commit() 

    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400


    if data==None or not 'company_email' in data or not 'company_password' in data:
        return jsonify({'message' : 'Invalid Body'}),400

    company_email = data['company_email']
    company_password = data['company_password'] 



    company_details=conn_company.execute('SELECT * FROM company_main WHERE company_email = "'+company_email+'" LIMIT 1').fetchall()
    if company_details==[]:
    	return jsonify({'data':'Not registered, Please Register and Login'}),404


    company_details=conn_company.execute('SELECT * FROM company_main WHERE company_email = "'+company_email+'" and company_password = "'+company_password+'" LIMIT 1').fetchall()
    if company_details==[]:
    	return jsonify({'data':'Invalid Username or Password'}),404


    public_id = str(uuid.uuid4())
    
    payload = {'company_email':company_email, 'public_id':public_id,  'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)}
    token=jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    conn_company.execute("UPDATE company_main SET public_id='"+public_id+"' where company_email = '"+company_email+"'")
    conn_company.commit()

    conn_session.execute("UPDATE UserSession SET user='"+company_email+"' where ip = '"+ip_address+"' and datetime = '"+str(datetime_now)+"'")
    conn_session.commit()

    # response = flask.jsonify({'token':token})
    # response.headers.set('Content-Type', 'application/json')
    # return response, 200
    
    return jsonify({'token':token}),200







@company_api.route('/company_update_token', methods=['POST'])
@token_required
def company_update_token(company_email):
    if company_email==None:
        return jsonify({'message' : 'Invalid Token'}), 401
    
    company_email=company_email[0]

    public_id = str(uuid.uuid4())

    payload = {'company_email':company_email, 'public_id':public_id,  'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes = 5)}
    token=jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    conn_company.execute("UPDATE company_main SET public_id='"+public_id+"' where company_email = '"+company_email+"'")
    conn_company.commit()

    return jsonify({'token':token})







#tested
@company_api.route('/company_register', methods=['POST'])
def company_register():
    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400


    if data==None or not 'company_email' in data or not 'company_password' in data or not 'company_name' in data or not 'company_country' in data or not 'company_city' in data or not 'company_phone' in data or not 'company_total_employees' in data or not 'company_about' in data:
        return jsonify({'message' : 'Invalid Body'}),400


    company_email = data['company_email']
    
    company_details=conn_company.execute('SELECT * FROM company_main WHERE company_email = "'+company_email+'" LIMIT 1').fetchall()
    if company_details==[]:

        company_name = data['company_name']
        company_country = data['company_country']
        company_city = data['company_city']
        company_phone = data['company_phone']
        company_total_employees = data['company_total_employees']
        company_about = data['company_about']
        company_password = data['company_password']

        conn_company.execute("INSERT INTO company_main(company_name,company_country,company_city,company_phone,company_total_employees,company_about,company_email,company_password,datetime) values(?,?,?,?,?,?,?,?,?)" ,(company_name,company_country,company_city,company_phone,company_total_employees,company_about,company_email,company_password,datetime.datetime.now()))
        conn_company.commit()    
        return jsonify({'data':'Sucess'})

    else:
        return jsonify({'data':'You are already registered with us. Please Login.'}),422




@company_api.route('/company_check_register', methods=['POST'])
def company_check_register():
    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400


    if data==None or not 'company_email' in data:
        return jsonify({'message' : 'Invalid Body'}),400

    company_email=data['company_email']

    company_details=conn_company.execute('SELECT * FROM company_main WHERE company_email = "'+company_email+'" LIMIT 1').fetchall()
    if company_details==[]:
        return jsonify({'data':False}),404

    else:
        return jsonify({'data':True}),200








@company_api.route('/company_post_job', methods=['POST'])
@token_required
def company_post_job(company_email):
    if company_email==None:
        return jsonify({'message' : 'Invalid Token'}), 401
    company_email=company_email[0]

    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400


    
    if data==None or not 'job_title' in data or not 'job_type' in data or not 'job_role' in data or not 'job_salary_range' in data or not 'job_skill' in data or not 'job_experience' in data or not 'job_location' in data or not 'job_description' in data:
        return jsonify({'message' : 'Invalid Body'}),400

    job_title = data['job_title']
    job_type = data['job_type']
    job_role = data['job_role']
    job_salary_range = data['job_salary_range']
    job_skill = data['job_skill']
    job_experience = data['job_experience']
    job_location = data['job_location']
    job_description = data['job_description']


    job_id=datetime.datetime.utcnow()


    conn_jobs.execute("INSERT INTO jobs_table(job_title,job_type,job_role,job_salary_range,job_skill,job_experience,job_location,job_description,company_email,job_id,datetime) values(?,?,?,?,?,?,?,?,?,?,?)" ,(job_title,job_type,job_role,job_salary_range,job_skill,job_experience,job_location,job_description,company_email,job_id,datetime.datetime.now()))
    conn_jobs.commit()    
    
    return jsonify({'data':'Job Posted Sucessfully'}),200




@company_api.route('/company_all_job', methods=['POST'])
@token_required
def company_all_job(company_email):
    if company_email==None:
        return jsonify({'message' : 'Invalid Token'}), 401
    company_email=company_email[0]

    job_details=conn_jobs.execute('SELECT job_title,job_role,job_experience,job_location FROM jobs_table WHERE company_email = "'+company_email+'"').fetchall()

    return jsonify({'data':job_details}),200






@company_api.route('/company_delete_posted_jobs', methods=['POST'])
@token_required
def company_delete_posted_jobs(company_email):
    if company_email==None:
        return jsonify({'message' : 'Invalid Token'}), 401
    company_email=company_email[0]

    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400


    
    if data==None or not 'job_title' in data or not 'job_type' in data:
        return jsonify({'message' : 'Invalid Body'}),400


    job_type=data['job_type']
    job_title=data['job_title']

    try:
        conn_jobs.execute("DELETE from jobs_table where job_title = '"+job_title+"' and job_type = '"+job_type+"'")
        conn_jobs.commit()
        return jsonify({'msg':'Job Deleted Sucessfully.'}),200
    except:
        return jsonify({'msg':'Cannot Delete, Invalid Job Title or Type'}),404





