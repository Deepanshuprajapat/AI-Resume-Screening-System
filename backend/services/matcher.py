from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_description, resume_skills="", job_skills=""):
    """
    Calculate the similarity between the resume and the job description.
    """
    if not resume_text or not job_description:
        return 0.0

    # Combine text and skills to give more weight to skills if needed
    text_list = [resume_text + " " + resume_skills, job_description + " " + job_skills]
    
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(text_list)
        
        # Calculate cosine similarity between the first document (resume) and second (job)
        # tfidf_matrix[0:1] is resume, tfidf_matrix[1:2] is job
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return min(max(round(cosine_sim[0][0], 4), 0.0), 1.0) # Ensure between 0 and 1
    except Exception as e:
        print(f"Error calculating score: {e}")
        return 0.0
