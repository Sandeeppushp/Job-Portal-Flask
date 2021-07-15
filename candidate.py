from flask import Blueprint, Flask, request, jsonify, render_template,session,send_from_directory,redirect,url_for
import requests
import os
import shutil
import sqlite3
import uuid
import jwt
import datetime
from functools import wraps
from flask import current_app

candidate_api = Blueprint('candidate_api', __name__)



conn_candidate = sqlite3.connect('candidate.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)
conn_jobs = sqlite3.connect('jobs.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)
conn_session = sqlite3.connect('session.db' , detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread=False)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
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
        current_user=conn_candidate.execute('SELECT candidate_email FROM candidate_main WHERE public_id = "'+data['public_id']+'"').fetchone()
        if current_user==[]:
            return jsonify({'message' : 'Invalid User'}), 401
        
        return f(current_user, *args, **kwargs)

    return decorated


@candidate_api.route('/candidate_login', methods=['POST'])
def candidate_login():

    user_agent=str(request.headers.get('User-Agent'))
    ip_address=request.environ['HTTP_X_FORWARDED_FOR']
    datetime_now=datetime.datetime.now()

    user_session_data=conn_session.execute("SELECT * FROM UserSession where ip='"+ip_address+"' ORDER BY id DESC LIMIT 10;").fetchall()
    #print(user_session_data)
    if len(user_session_data)==10 and (datetime.datetime.now()-datetime.datetime.strptime(str(user_session_data[-1][6]), '%Y-%m-%d %H:%M:%S.%f')).seconds < 60:
      return jsonify({'data':'Too Many Attempts, Please wait for 1 Minute'}),429

    conn_session.execute("INSERT INTO UserSession(user,ip,user_agent,category,endpoint,datetime) values(?,?,?,?,?,?)" ,('',ip_address,user_agent,'candidate','/candidate_login',datetime_now))
    conn_session.commit() 


    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400


    if data==None or not 'candidate_email' in data or not 'candidate_password' in data:
        return jsonify({'message' : 'Invalid Body'}),400

    candidate_email = data['candidate_email']
    candidate_password = data['candidate_password']


    candidate_details=conn_candidate.execute('SELECT * FROM candidate_main WHERE candidate_email = "'+candidate_email+'" LIMIT 1').fetchall()
    if candidate_details==[]:
    	return jsonify({'data':'Not registered, Please Register and Login'}),404


    candidate_details=conn_candidate.execute('SELECT * FROM candidate_main WHERE candidate_email = "'+candidate_email+'" and candidate_password = "'+candidate_password+'" LIMIT 1').fetchall()
    if candidate_details==[]:
    	return jsonify({'data':'Invalid Username or Password'}),404


    public_id = str(uuid.uuid4())

    payload = {'candidate_email':candidate_email, 'public_id':public_id,  'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes = 5)}
    token=jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    conn_candidate.execute("UPDATE candidate_main SET public_id='"+public_id+"' where candidate_email = '"+candidate_email+"'")
    conn_candidate.commit()

    conn_session.execute("UPDATE UserSession SET user='"+candidate_email+"' where ip = '"+ip_address+"' and datetime = '"+str(datetime_now)+"'")
    conn_session.commit()

    return jsonify({'token':token}),200



@candidate_api.route('/candidate_update_token', methods=['POST'])
@token_required
def candidate_update_token(candidate_email):
    if candidate_email==None:
        return jsonify({'message' : 'Invalid Token'}), 401
    
    candidate_email=candidate_email[0]

    public_id = str(uuid.uuid4())

    payload = {'candidate_email':candidate_email, 'public_id':public_id,  'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes = 5)}
    token=jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    conn_candidate.execute("UPDATE candidate_main SET public_id='"+public_id+"' where candidate_email = '"+candidate_email+"'")
    conn_candidate.commit()

    return jsonify({'token':token}),200



@candidate_api.route('/candidate_register', methods=['POST'])
def candidate_register():
    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400

    #print(data)

    if data==None or not 'candidate_name' in data or not 'candidate_gender' in data or not 'candidate_dob' in data or not 'candidate_mobile' in data or not 'candidate_email' in data or not 'candidate_experience' in data or not 'candidate_skills' in data or not 'candidate_past_experiences' in data:
        return jsonify({'message' : 'Invalid Body'}),400
    
    if data==None or not 'candidate_prefered_location' in data or not 'candidate_education' in data or not 'candidate_profile_summary' in data or not 'candidate_accomplishments' in data or not 'candidate_certification' in data or not 'candidate_designation' in data or not 'candidate_skills' in data or not 'candidate_current_salary' in data:
        return jsonify({'message' : 'Invalid Body'}),400
    
    if data==None or not 'candidate_expected_salary' in data or not 'candidate_password' in data:
        return jsonify({'message' : 'Invalid Body'}),400
    

    candidate_email = data['candidate_email']
    
    candidate_details=conn_candidate.execute('SELECT * FROM candidate_main WHERE candidate_email = "'+candidate_email+'" LIMIT 1').fetchall()
    if candidate_details==[]:
	    candidate_name = data['candidate_name']
	    candidate_gender = data['candidate_gender']
	    candidate_dob = data['candidate_dob']
	    candidate_mobile = data['candidate_mobile']
	    candidate_experience = data['candidate_experience']
	    candidate_skills = data['candidate_skills']
	    candidate_past_experiences = data['candidate_past_experiences']
	    candidate_prefered_location = data['candidate_prefered_location']
	    candidate_education = data['candidate_education']
	    candidate_profile_summary = data['candidate_profile_summary']
	    candidate_accomplishments = data['candidate_accomplishments']
	    candidate_certification = data['candidate_certification']
	    candidate_designation = data['candidate_designation']
	    candidate_current_salary = data['candidate_current_salary']
	    candidate_expected_salary = data['candidate_expected_salary']
	    candidate_password = data['candidate_password'] 

	    conn_candidate.execute("""INSERT INTO candidate_main(candidate_name,candidate_email,candidate_gender,candidate_dob,candidate_mobile,candidate_experience,candidate_skills,candidate_past_experiences,
	    	candidate_prefered_location,candidate_education,candidate_profile_summary,candidate_accomplishments,candidate_certification,candidate_designation,
	    	candidate_current_salary,candidate_expected_salary,candidate_password,datetime) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""" ,(candidate_name,candidate_email,candidate_gender,candidate_dob,candidate_mobile,
                candidate_experience,candidate_skills,candidate_past_experiences,candidate_prefered_location,candidate_education,candidate_profile_summary,candidate_accomplishments,candidate_certification,
                candidate_designation,candidate_current_salary,candidate_expected_salary,candidate_password,datetime.datetime.now()))
	    conn_candidate.commit()
	    return jsonify({'data':'Sucess'}),200

    else:
            return jsonify({'data':'You are already registered with us. Please Login.'}),422




@candidate_api.route('/candidate_check_register', methods=['POST'])
def candidate_check_register():
    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400


    if data==None or not 'candidate_email' in data:
        return jsonify({'message' : 'Invalid Body'}),400

    candidate_email=data['candidate_email']

    candidate_details=conn_candidate.execute('SELECT * FROM candidate_main WHERE candidate_email = "'+candidate_email+'" LIMIT 1').fetchall()
    if candidate_details==[]:
        return jsonify({'data':'Not Registered'}),404

    else:
        return jsonify({'data':'Registered'}),200


@candidate_api.route('/candidate_search_job', methods=['POST'])
@token_required
def candidate_search_job(candidate_email):
    if candidate_email==None:
        return jsonify({'message' : 'Invalid Token'}), 401

    data = request.get_json()
    if data==None or not 'job_title' in data:
        return jsonify({'message' : 'Invalid Body'}),400

    job_title=data['job_title']

    jobs_details=conn_jobs.execute('SELECT job_title,job_type,job_role,job_salary_range,job_skill,job_experience,job_location,job_description,job_id FROM jobs_table WHERE job_title LIKE "%'+job_title+'%"').fetchall()
    if jobs_details==[]:
        return jsonify({'data':'No Jobs Found'}),404

    else:
        return jsonify({'data':jobs_details}),200



@candidate_api.route('/candidate_apply_job', methods=['POST'])
@token_required
def candidate_apply_job(candidate_email):
    if candidate_email==None:
        return jsonify({'message' : 'Invalid Token'}), 401
        
    candidate_email=candidate_email[0]

    try:
        data = request.get_json()
    except:
        return jsonify({'message' : 'Bad Request'}),400



    if data==None or not 'job_id' in data:
        return jsonify({'message' : 'Invalid Body'}),400

    job_id=data['job_id']

    jobs_apply_check=conn_jobs.execute('SELECT candidate_email from jobs_applied_table WHERE job_id = "'+job_id+'"').fetchall()
    if jobs_apply_check==[]:
        conn_jobs.execute("""INSERT INTO jobs_applied_table(job_id,candidate_email,datetime) values(?,?,?)""" ,(job_id,candidate_email,datetime.datetime.now()))
        conn_jobs.commit()
        return jsonify({'msg':'Job Applied Sucessfully'}),200

    else:
        return jsonify({'msg':'Already Applied'}),422







