from django.urls import path
from .views import ResumeUploadView, ProcessResumeView
from .views import ResultsView, AnalysisHistoryView
from .views import AnalysisAPIView

app_name = 'analyzer'

urlpatterns = [
    path('', ResumeUploadView.as_view(), name='upload'),
    path('process/', ProcessResumeView.as_view(), name='process_resume'),
    path('results/', ResultsView.as_view(), name='results'),
    path('results/<int:analysis_id>/', ResultsView.as_view(), name='results_detail'),
    path('history/', AnalysisHistoryView.as_view(), name='history'),
    path('api/analyze/', AnalysisAPIView.as_view(), name='api_analyze'),
]
