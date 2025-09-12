from .utils.resume_analyzer import ResumeAnalyzer

def create_resume_processor():
    """Factory function to create analyzer"""
    return ResumeAnalyzer()

# For backward compatibility
class ResumeProcessor:
    def __init__(self):
        self.analyzer = ResumeAnalyzer()
    
    def process_resume(self, resume_file_path, job_description):
        """Delegate to new analyzer"""
        return self.analyzer.analyze_resume(resume_file_path, job_description)
