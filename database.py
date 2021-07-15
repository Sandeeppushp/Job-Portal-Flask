import sqlite3


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


import requests
import json

url = "https://db6a45ba26a5.ngrok.io/company_login"

payload = json.dumps({
  "company_email": "meon@gmail.com",
  "company_password": "meon@123"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

token=response.json()['token']
print(token)



class company:
	def __init__(self):
		pass

	def check_company_email_exixts(self,company_email):
		data=conn_company.execute('SELECT * FROM company_main WHERE company_email = "'+company_email+'" LIMIT 1').fetchall()
		return data

	def check_company_email_and_password(self,company_email,company_password):
		data=conn_company.execute('SELECT * FROM company_main WHERE company_email = "'+company_email+'" and company_password = "'+company_password+'" LIMIT 1').fetchall()
		return data

	def update_company_public_id(self,public_id,company_email):
		conn_company.execute("UPDATE company_main SET public_id='"+public_id+"' where company_email = '"+company_email+"'")
    	conn_company.commit()
    	return True

    def update_company_token(self,public_id,company_email):
    	conn_company.execute("UPDATE company_main SET public_id='"+public_id+"' where company_email = '"+company_email+"'")
    	conn_company.commit()
    	return True

    def register_company(self,company_name,company_country,company_city,company_phone,company_total_employees,company_about,company_email,company_password,datetime):
    	conn_company.execute("INSERT INTO company_main(company_name,company_country,company_city,company_phone,company_total_employees,company_about,company_email,company_password,datetime) values(?,?,?,?,?,?,?,?,?)" ,(company_name,company_country,company_city,company_phone,company_total_employees,company_about,company_email,company_password,datetime.datetime.now()))
    	conn_company.commit()  
    	return True

    def post_company_job(self,job_title,job_type,job_role,job_salary_range,job_skill,job_experience,job_location,job_description,company_email,job_id,datetime):
    	conn_jobs.execute("INSERT INTO jobs_table(job_title,job_type,job_role,job_salary_range,job_skill,job_experience,job_location,job_description,company_email,job_id,datetime) values(?,?,?,?,?,?,?,?,?,?,?)" ,(job_title,job_type,job_role,job_salary_range,job_skill,job_experience,job_location,job_description,company_email,job_id,datetime.datetime.now()))
    	conn_jobs.commit()    
    	return True

    def fetch_all_posted_jobs(self,company_email):
    	data=conn_jobs.execute('SELECT job_title,job_role,job_experience,job_location FROM jobs_table WHERE company_email = "'+company_email+'"').fetchall()
    	return data

    def delete_posted_job(self,job_title,job_type):
    	try:
    		conn_jobs.execute("DELETE from jobs_table where job_title = '"+job_title+"' and job_type = '"+job_type+"'")
    		conn_jobs.commit()
    		return True
    	except:
    		return False



class candidate:
	def __init__(self):
		pass

	def check_candidate_email_exists(self,candidate_email):
		data=conn_candidate.execute('SELECT * FROM candidate_main WHERE candidate_email = "'+candidate_email+'" LIMIT 1').fetchall()
		return data

	def check_candidate_email_and_password(self,candidate_email,candidate_password):
		data=conn_candidate.execute('SELECT * FROM candidate_main WHERE candidate_email = "'+candidate_email+'" and candidate_password = "'+candidate_password+'" LIMIT 1').fetchall()
		return data

	def update_candidate_public_id(self,public_id,candidate_email):
		conn_candidate.execute("UPDATE candidate_main SET public_id='"+public_id+"' where candidate_email = '"+candidate_email+"'")
    	conn_candidate.commit()
    	return True

    def update_candidate_token(self,public_id,candidate_email):
    	conn_candidate.execute("UPDATE candidate_main SET public_id='"+public_id+"' where candidate_email = '"+candidate_email+"'")
    	conn_candidate.commit()
    	return True

    def register_candidate(self,candidate_name,candidate_email,candidate_gender,candidate_dob,candidate_mobile,candidate_experience,candidate_skills,candidate_past_experiences,
	    	candidate_prefered_location,candidate_education,candidate_profile_summary,candidate_accomplishments,candidate_certification,candidate_designation,
	    	candidate_current_salary,candidate_expected_salary,candidate_password,datetime):
    	conn_candidate.execute("""INSERT INTO candidate_main(candidate_name,candidate_email,candidate_gender,candidate_dob,candidate_mobile,candidate_experience,candidate_skills,candidate_past_experiences,
	    	candidate_prefered_location,candidate_education,candidate_profile_summary,candidate_accomplishments,candidate_certification,candidate_designation,
	    	candidate_current_salary,candidate_expected_salary,candidate_password,datetime) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""" ,(candidate_name,candidate_email,candidate_gender,candidate_dob,candidate_mobile,
                candidate_experience,candidate_skills,candidate_past_experiences,candidate_prefered_location,candidate_education,candidate_profile_summary,candidate_accomplishments,candidate_certification,
                candidate_designation,candidate_current_salary,candidate_expected_salary,candidate_password,datetime.datetime.now()))
	    conn_candidate.commit()
	    return True


	def candidate_search_jobs(self,job_title):
		data=conn_jobs.execute('SELECT job_title,job_type,job_role,job_salary_range,job_skill,job_experience,job_location,job_description,job_id FROM jobs_table WHERE job_title LIKE "%'+job_title+'%"').fetchall()
		return data

	def check_candidate_applied_job(self,job_id):
		data=conn_jobs.execute('SELECT candidate_email from jobs_applied_table WHERE job_id = "'+job_id+'"').fetchall()
		return data

	def candidate_apply_job(self,job_id,candidate_email,datetime):
		conn_jobs.execute("""INSERT INTO jobs_applied_table(job_id,candidate_email,datetime) values(?,?,?)""" ,(job_id,candidate_email,datetime.datetime.now()))
        conn_jobs.commit()
        return True




class session:
	def __init__(self):
		pass


	def 