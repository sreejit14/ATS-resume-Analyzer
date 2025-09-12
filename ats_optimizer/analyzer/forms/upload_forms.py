from django import forms
from django.core.exceptions import ValidationError

class ResumeUploadForm(forms.Form):
    """Form for uploading resume files"""
    
    resume_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt'
        }),
        help_text="Upload your resume (PDF, DOC, DOCX, or TXT format, max 10MB)"
    )
    
    def clean_resume_file(self):
        """Validate uploaded resume file"""
        resume_file = self.cleaned_data.get('resume_file')
        
        if not resume_file:
            raise ValidationError("Please select a resume file to upload.")
        
        # Check file size (limit to 10MB)
        if resume_file.size > 10 * 1024 * 1024:
            raise ValidationError("File size cannot exceed 10MB.")
        
        # Check file extension
        file_name = resume_file.name.lower()
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
        
        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            raise ValidationError(
                "Only PDF, DOC, DOCX, and TXT files are allowed."
            )
        
        # Check if file is not empty
        if hasattr(resume_file, 'read'):
            current_pos = resume_file.tell()
            resume_file.seek(0)
            first_bytes = resume_file.read(100)
            resume_file.seek(current_pos)
            
            if not first_bytes:
                raise ValidationError("The uploaded file appears to be empty.")
        
        return resume_file

class JobDescriptionForm(forms.Form):
    """Form for job description input"""
    
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Paste the complete job description here...'
        }),
        help_text="Minimum 50 characters required"
    )
    
    def clean_job_description(self):
        """Validate job description"""
        job_description = self.cleaned_data.get('job_description')
        
        if not job_description or len(job_description.strip()) < 50:
            raise ValidationError(
                "Job description must be at least 50 characters long."
            )
        
        return job_description.strip()
