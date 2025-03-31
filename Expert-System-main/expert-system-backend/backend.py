import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from difflib import SequenceMatcher

app = Flask(__name__)
CORS(app, resources={r"/evaluate": {"origins": "*"}}, allow_headers=["Content-Type"])

# Knowledge base (could be stored in database instead)

job_positions = [
    {
        "title": "Entry-Level Python Engineer",
        "needed_skills": ["Python course work", "Software Engineering course work"],
        "desired_skills": ["Agile course"],
        "qualifications": "Bachelor in CS"
    },
    {
        "title": "Python Engineer",
        "needed_skills": ["3 years Python development", "1 year data development", "Experience in Agile projects"],
        "desired_skills": ["Used Git"],
        "qualifications": "Bachelor in CS" 
    },
    {
        "title": "Project Manager",
        "needed_skills": ["3 years managing software projects", "2 years in Agile projects"],
        "desired_skills": [],
        "qualifications": "PMI Lean Project Management Certification"
    },
    {
        "title": "Senior Knowledge Engineer",
        "needed_skills": ["3 years using Python to develop Expert Systems", "2 years data architecture and development"],
        "desired_skills": [],
        "qualifications": "Masters in CS"
    }
]

def is_similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a, b).ratio() > threshold

@app.route('/evaluate', methods=['POST'])
def evaluate_applicant():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "Error", "reason": "Invalid JSON format"}), 400
    
    applicant_skills = [skill.strip().lower() for skill in data.get("skills", [])]
    applicant_qualifications = data.get("qualifications", "").strip().lower()
    
    print("\n--- Debugging Information ---")
    print("Raw Request Data:", data)
    print("Applicant Skills (Processed):", applicant_skills)
    print("Applicant Qualifications (Processed):", applicant_qualifications)
    print("\n--- Checking Job Positions ---")
    
    if not isinstance(applicant_skills, list) or not isinstance(applicant_qualifications, str):
        return jsonify({"status": "Error", "reason": "Invalid JSON format"}), 400
    
    qualified_jobs = []
    for job in job_positions:
        print(f"\nChecking for {job['title']}...")
        print("Required Skills:", job["needed_skills"])
        print("Desired Skills:", job["desired_skills"])
        print("Required Qualification:", job["qualifications"])
    
        normalized_needed_skills = [skill.strip().lower() for skill in job["needed_skills"]]
        normalized_qualification = job["qualifications"].strip().lower()
    
        print("Checking Skills Match...")
        skill_match = all(
            any(is_similar(job_skill, applicant_skill) for applicant_skill in applicant_skills) 
            for job_skill in normalized_needed_skills
        )
        print("Skills Match Result:", skill_match)
        
        print("Checking Qualification Match...")
        qualification_match = is_similar(normalized_qualification, applicant_qualifications)
        print("Qualification Match Result:", qualification_match)
        
        print("Checking Desired Skills Match...")
        desired_skill_match = any(
            any(is_similar(desired_skill, applicant_skill) for applicant_skill in applicant_skills)
            for desired_skill in job["desired_skills"]
        )
        print("Desired Skills Match Result:", desired_skill_match)
        
        print("Skills Match:", skill_match)
        print("Qualification Match:", qualification_match)
        print("Desired Skills Match:", desired_skill_match)
    
        if skill_match and qualification_match:
            if desired_skill_match:
                qualified_jobs.append(f"{job['title']} - You have a desired skill for this position!")
            else:
                qualified_jobs.append(job['title'])
                
    print("--- End Debugging ---\n")
    
    if qualified_jobs:
        return jsonify({"status": "Accepted", "positions": qualified_jobs})
    else:
        return jsonify({"status": "Rejected", "reason": "Applicant does not meet required skills and qualifications."})
    
if __name__ == '__main__':
    app.run(debug=True)
