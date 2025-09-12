from django import forms
from django.core.exceptions import ValidationError
from ..models import JobPosting

class JobPostingForm(forms.ModelForm):
    """Form for creating job postings"""
    
    class Meta:
        model = JobPosting
        fields = ['title', 'company', 'description', 'location', 'experience_level', 'job_type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Job description...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job location (optional)'
            }),
            'experience_level': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Select experience level'),
                ('entry', 'Entry Level'),
                ('junior', 'Junior'),
                ('mid', 'Mid Level'),
                ('senior', 'Senior'),
                ('lead', 'Lead/Principal')
            ]),
            'job_type': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Select job type'),
                ('full-time', 'Full Time'),
                ('part-time', 'Part Time'),
                ('contract', 'Contract'),
                ('freelance', 'Freelance'),
                ('internship', 'Internship')
            ])
        }
    
    def clean_title(self):
        """Validate job title"""
        title = self.cleaned_data.get('title')
        
        if not title or len(title.strip()) < 3:
            raise ValidationError("Job title must be at least 3 characters long.")
        
        return title.strip()

class CombinedUploadForm(forms.Form):
    """Combined form for both job posting and resume upload"""
    
    # Job posting fields
    job_title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter job title'
        })
    )
    
    company_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company name'
        })
    )
    
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Paste the complete job description here...'
        })
    )
    
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Job location (optional)'
        })
    )
    
    experience_level = forms.ChoiceField(
        choices=[
            ('', 'Select experience level'),
            ('entry', 'Entry Level'),
            ('junior', 'Junior'),
            ('mid', 'Mid Level'),
            ('senior', 'Senior'),
            ('lead', 'Lead/Principal')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    job_type = forms.ChoiceField(
        choices=[
            ('', 'Select job type'),
            ('full-time', 'Full Time'),
            ('part-time', 'Part Time'),
            ('contract', 'Contract'),
            ('freelance', 'Freelance'),
            ('internship', 'Internship')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Resume upload field
    resume_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt'
        })
    )
    
    def clean_resume_file(self):
        """Validate uploaded resume file"""
        resume_file = self.cleaned_data.get('resume_file')
        
        if not resume_file:
            raise ValidationError("Please select a resume file to upload.")
        
        # File size validation
        if resume_file.size > 10 * 1024 * 1024:
            raise ValidationError("File size cannot exceed 10MB.")
        
        # File extension validation
        file_name = resume_file.name.lower()
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
        
        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            raise ValidationError("Only PDF, DOC, DOCX, and TXT files are allowed.")
        
        return resume_file
    
    def clean_job_description(self):
        """Validate job description"""
        job_description = self.cleaned_data.get('job_description')
        
        if not job_description or len(job_description.strip()) < 50:
            raise ValidationError("Job description must be at least 50 characters long.")
        
        return job_description.strip()
