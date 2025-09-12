from django.db import models
class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    experience_level = models.CharField(max_length=50, blank=True, null=True)
    job_type = models.CharField(max_length=50, blank=True, null=True)


class ResumeAnalysis(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/')
    ats_score = models.FloatField()
    semantic_similarity = models.FloatField()
    matching_keywords = models.JSONField()
    missing_keywords = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    applicant_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    parsed_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')
    feedback = models.TextField(blank=True, null=True)
