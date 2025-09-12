from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

@method_decorator(csrf_exempt, name='dispatch')
class AnalysisAPIView(View):
    """API endpoint for AJAX analysis requests"""
    
    def post(self, request):
        """Handle AJAX analysis requests"""
        try:
            data = json.loads(request.body)
            job_description = data.get('job_description')
            
            if not job_description:
                return JsonResponse({
                    'success': False,
                    'error': 'Job description is required'
                }, status=400)
            
            # This could be expanded for API-based analysis
            return JsonResponse({
                'success': True,
                'message': 'Analysis completed',
                'data': {
                    'job_description_length': len(job_description)
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    def get(self, request):
        """Handle GET requests for API documentation"""
        return JsonResponse({
            'message': 'ATS Analyzer API',
            'endpoints': {
                'POST /api/analyze/': 'Submit analysis request'
            }
        })
