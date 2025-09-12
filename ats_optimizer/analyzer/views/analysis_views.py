from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator

from ..models import ResumeAnalysis

class ResultsView(View):
    """Display analysis results"""
    
    template_name = 'analyzer/results.html'
    
    def get(self, request, analysis_id=None):
        """Display the analysis results"""

        if not analysis_id:
            analysis_id = request.session.get('analysis_id')
        
        if not analysis_id:
            messages.error(request, 'No analysis results found.')
            return redirect('analyzer:upload')
        
        try:
            analysis = get_object_or_404(ResumeAnalysis, id=analysis_id)
            
            context = {
                'analysis': analysis,
                'job_posting': analysis.job_posting,
                'matching_count': len(analysis.matching_keywords),
                'missing_count': len(analysis.missing_keywords),
                'score_class': self._get_score_class(analysis.ats_score),
                'similarity_class': self._get_score_class(analysis.semantic_similarity)
            }
            
            return render(request, self.template_name, context)
            
        except Exception as e:
            messages.error(request, f'Error displaying results: {str(e)}')
            return redirect('analyzer:upload')
    
    def _get_score_class(self, score):
        """Get CSS class based on score"""
        if score >= 80:
            return 'success'
        elif score >= 60:
            return 'warning'
        else:
            return 'danger'

class AnalysisHistoryView(View):
    """Display history of all analyses"""
    
    template_name = 'analyzer/history.html'
    
    def get(self, request):
        """Show paginated list of all analyses"""
        analyses_list = ResumeAnalysis.objects.all().order_by('-created_at')
        
        paginator = Paginator(analyses_list, 20)  # 20 analyses per page
        page_number = request.GET.get('page')
        analyses = paginator.get_page(page_number)
        
        context = {
            'analyses': analyses,
            'total_analyses': analyses_list.count()
        }
        
        return render(request, self.template_name, context)
