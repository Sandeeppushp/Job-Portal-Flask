from flask import Blueprint, Flask, request, jsonify, render_template,session,send_from_directory,redirect,url_for
import requests
import os
import shutil
import sqlite3

jobs = Blueprint('jobs', __name__)






@app.route('/job_posting', methods=['POST'])
def job_posting():
    data = request.get_json()
    job_title = data['job_title']
    job_type = data['job_type']
    job_role = data['job_role']
    job_salary_range = data['job_salary_range']
    job_skill = data['job_skill']
    job_experience = data['job_experience']
    job_location = data['job_location']
    job_description = data['job_description']
    company_email = data['company_email']
    
    return jsonify({'data':'Sucess'})








@rmloginapi.route('/company_search_candidate', methods=['POST'])
def company_search_candidate():
    data = request.get_json()
    candidate_email = data['company_email']
    candidate_name = data['candidate_name']
    candidate_expected_salary = data['candidate_experience']
    candidate_expected_salary = data['candidate_skills']
    candidate_expected_salary = data['candidate_past_experiences']
    candidate_expected_salary = data['candidate_prefered_location']
    candidate_expected_salary = data['candidate_profile_summary']
    candidate_expected_salary = data['candidate_certification']
    candidate_expected_salary = data['candidate_designation']
    candidate_expected_salary = data['candidate_current_salary']
    
    return jsonify({'data':'Sucess'})





    




@rmloginapi.route('/candidate_search_jobs', methods=['POST'])
def candidate_search_jobs():
    data = request.get_json()
    candidate_email = data['candidate_email']
    job_title = data['job_title']
    job_type = data['job_type']
    job_role = data['job_role']
    job_salary_range = data['job_salary_range']
    job_skill = data['job_skill']
    job_experience = data['job_experience']
    job_location = data['job_location']
    job_description = data['job_description']
    company_email = data['company_email'] 
    return jsonify({'data':'Sucess'})
