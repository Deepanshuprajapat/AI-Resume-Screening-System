const API_URL = 'http://127.0.0.1:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    loadJobs();

    // DOM Elements
    const jobForm = document.getElementById('jobForm');
    const resumeForm = document.getElementById('resumeForm');
    const resumeFile = document.getElementById('resumeFile');
    const fileName = document.getElementById('fileName');

    // Display selected filename
    resumeFile.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileName.textContent = e.target.files[0].name;
        }
    });

    // Create Job Submission
    jobForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            title: document.getElementById('jobTitle').value,
            description: document.getElementById('jobDesc').value,
            skills_required: document.getElementById('jobSkills').value
        };

        try {
            const res = await fetch(`${API_URL}/jobs`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                jobForm.reset();
                loadJobs(); // refresh list
            }
        } catch (error) {
            console.error('Error creating job:', error);
        }
    });

    // Upload Resume Submission
    resumeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const file = resumeFile.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('resume', file);
        formData.append('job_id', document.getElementById('uploadJobId').value);
        formData.append('name', document.getElementById('candidateName').value);
        formData.append('email', 'test@test.com'); // Could add field later
        formData.append('phone', '0000000000');

        const statusLabel = document.getElementById('uploadStatus');
        statusLabel.textContent = 'Processing resume with AI...';

        try {
            const res = await fetch(`${API_URL}/candidates/upload`, {
                method: 'POST',
                body: formData
            });
            if (res.ok) {
                resumeForm.reset();
                fileName.textContent = '';
                statusLabel.textContent = 'Candidate successfully screened and ranked!';
                setTimeout(() => statusLabel.textContent = '', 3000);
                
                // Refresh candidates if we are currently viewing this job
                loadCandidates(document.getElementById('uploadJobId').value);
            } else {
                statusLabel.textContent = 'Failed to process resume.';
            }
        } catch (error) {
            console.error('Upload error:', error);
            statusLabel.textContent = 'Connection error.';
        }
    });
});

async function loadJobs() {
    try {
        const res = await fetch(`${API_URL}/jobs`);
        if (!res.ok) return;
        const jobs = await res.json();
        
        const jobList = document.getElementById('jobList');
        const uploadSelect = document.getElementById('uploadJobId');
        
        jobList.innerHTML = '';
        uploadSelect.innerHTML = '<option value="">Select a Job</option>';

        jobs.forEach(job => {
            // Populate Dropdown
            const option = document.createElement('option');
            option.value = job.id;
            option.textContent = job.title;
            uploadSelect.appendChild(option);

            // Populate List
            const div = document.createElement('div');
            div.className = 'list-item';
            div.innerHTML = `
                <div class="job-title">${job.title}</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 5px;">
                    Skills: ${job.skills_required || 'None specified'}
                </div>
            `;
            div.onclick = () => {
                document.getElementById('selectedJobTitle').textContent = `(for ${job.title})`;
                loadCandidates(job.id);
            };
            jobList.appendChild(div);
        });
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

async function loadCandidates(jobId) {
    if (!jobId) return;
    try {
        const res = await fetch(`${API_URL}/jobs/${jobId}/candidates`);
        if (!res.ok) return;
        const candidates = await res.json();
        
        const candidateList = document.getElementById('candidateList');
        candidateList.innerHTML = '';
        
        if (candidates.length === 0) {
            candidateList.innerHTML = '<p style="color: var(--text-secondary);">No applications for this job yet.</p>';
            return;
        }

        candidates.forEach(c => {
            const matchPercentage = Math.round(c.match_score * 100);
            
            // Generate visual color based on score
            let color = '#10b981'; // green
            let bg = 'rgba(16, 185, 129, 0.2)';
            if (matchPercentage < 40) {
                color = '#ef4444'; // red
                bg = 'rgba(239, 68, 68, 0.2)';
            } else if (matchPercentage < 70) {
                color = '#f59e0b'; // yellow
                bg = 'rgba(245, 158, 11, 0.2)';
            }

            const div = document.createElement('div');
            div.className = 'list-item';
            div.innerHTML = `
                <span class="score-badge" style="color: ${color}; background: ${bg};">${matchPercentage}% Match</span>
                <div class="candidate-name">${c.name}</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 5px;">
                    Extracted Skills: ${c.extracted_skills || 'None'}
                </div>
            `;
            candidateList.appendChild(div);
        });
    } catch (error) {
        console.error('Error loading candidates:', error);
    }
}
