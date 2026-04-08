from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from models import db, Job, Candidate
from services.resume_parser import parse_resume_from_pdf
from services.matcher import calculate_match_score

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return jsonify([job.to_dict() for job in jobs])

@api_bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    new_job = Job(
        title=data.get('title'),
        description=data.get('description'),
        skills_required=data.get('skills_required', '')
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job.to_dict()), 201

@api_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@api_bp.route('/jobs/<int:job_id>/candidates', methods=['GET'])
def get_candidates(job_id):
    Job.query.get_or_404(job_id) # Verify job exists
    candidates = Candidate.query.filter_by(job_id=job_id).order_by(Candidate.match_score.desc()).all()
    return jsonify([c.to_dict() for c in candidates])

@api_bp.route('/candidates/upload', methods=['POST'])
def upload_resume():
    from flask import current_app
    
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    job_id = request.form.get('job_id')
    name = request.form.get('name', 'Unknown')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    
    if not job_id:
        return jsonify({'error': 'job_id is required'}), 400
        
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Ensure upload folder exists
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # NLP processing and ML ranking
        extracted_text, extracted_skills = parse_resume_from_pdf(filepath)
        match_score = calculate_match_score(extracted_text, job.description, extracted_skills, job.skills_required)
        
        candidate = Candidate(
            name=name,
            email=email,
            phone=phone,
            resume_text=extracted_text,
            extracted_skills=extracted_skills,
            match_score=match_score,
            job_id=job.id
        )
        
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify(candidate.to_dict()), 201
        
    return jsonify({'error': 'File type not allowed'}), 400
