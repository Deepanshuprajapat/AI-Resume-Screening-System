from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.String(200)) # comma separated skills
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    candidates = db.relationship('Candidate', backref='job', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'skills_required': self.skills_required,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    resume_text = db.Column(db.Text)
    extracted_skills = db.Column(db.String(500))
    match_score = db.Column(db.Float, default=0.0) # Used for similarity ranking
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'extracted_skills': self.extracted_skills,
            'match_score': self.match_score,
            'job_id': self.job_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
