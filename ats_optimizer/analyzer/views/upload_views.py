from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from ..forms.validation_forms import CombinedUploadForm
from ..models import JobPosting

class ResumeUploadView(View):
    """Handle resume upload and job description input"""
    
    template_name = 'analyzer/upload.html'
    form_class = CombinedUploadForm
    
    def get(self, request):
        """Display the upload form"""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Process form submission and redirect to analysis"""
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Create JobPosting instance
                job_posting = JobPosting.objects.create(
                    title=form.cleaned_data['job_title'],
                    description=form.cleaned_data['job_description'],
                    company=form.cleaned_data['company_name'],
                    location=form.cleaned_data.get('location', ''),
                    experience_level=form.cleaned_data.get('experience_level', ''),
                    job_type=form.cleaned_data.get('job_type', '')
                )
                
                # Save uploaded file temporarily
                resume_file = form.cleaned_data['resume_file']
                file_name = f"temp_resume_{job_posting.id}_{resume_file.name}"
                file_path = default_storage.save(file_name, ContentFile(resume_file.read()))
                full_file_path = default_storage.path(file_path)
                
                # Store file info in session for processing view
                request.session['analysis_data'] = {
                    'job_posting_id': job_posting.id,
                    'file_path': full_file_path,
                    'original_filename': resume_file.name
                }
                
                messages.success(request, 'Resume uploaded successfully! Processing analysis...')
                return redirect('analyzer:process_resume')
                
            except Exception as e:
                messages.error(request, f'Error uploading resume: {str(e)}')
        
        return render(request, self.template_name, {'form': form})

class ProcessResumeView(View):
    def get(self, request):
        print("=== STARTING RESUME PROCESSING ===")
        analysis_data = request.session.get('analysis_data')
        
        if not analysis_data:
            messages.error(request, 'No analysis data found.')
            return redirect('analyzer:upload')
        
        try:
            from ..models import JobPosting, ResumeAnalysis
            from ..services import create_resume_processor
            import os
            
            # Get job posting
            job_posting = JobPosting.objects.get(id=analysis_data['job_posting_id'])
            print(f"Processing for job: {job_posting.title}")
            
            # Create analyzer and process
            analyzer = create_resume_processor()
            print("Starting analysis...")
            
            analysis_result = analyzer.analyze_resume(
                analysis_data['file_path'],
                job_posting.description
            )
            
            print(f"Analysis complete with status: {analysis_result['status']}")
            
            # Check if analysis was successful
            if analysis_result['status'] != 'completed':
                messages.error(request, f"Analysis failed: {analysis_result['feedback']}")
                return redirect('analyzer:upload')
            
            # Save results to database
            with open(analysis_data['file_path'], 'rb') as f:
                file_content = ContentFile(f.read())
                file_content.name = analysis_data['original_filename']
                
                resume_analysis = ResumeAnalysis.objects.create(
                    job_posting=job_posting,
                    resume_file=file_content,
                    ats_score=analysis_result['ats_score'],
                    semantic_similarity=analysis_result['semantic_similarity'],
                    matching_keywords=analysis_result['matching_keywords'],
                    missing_keywords=analysis_result['missing_keywords'],
                    applicant_name=analysis_result['applicant_name'],
                    email=analysis_result['email'],
                    phone_number=analysis_result['phone_number'],
                    parsed_text=analysis_result['resume_text'],
                    status=analysis_result['status'],
                    feedback=analysis_result['feedback']
                )
            
            # Clean up temp file
            if os.path.exists(analysis_data['file_path']):
                os.remove(analysis_data['file_path'])
            
            # Update session and redirect to results
            del request.session['analysis_data']
            request.session['analysis_id'] = resume_analysis.id
            
            messages.success(request, 'Resume analysis completed successfully!')
            return redirect('analyzer:results')
            
        except Exception as e:
            print(f"ERROR in processing: {str(e)}")
            messages.error(request, f'Processing failed: {str(e)}')
            return redirect('analyzer:upload')
