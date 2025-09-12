from .extract_utils import extract_text_from_file
from .nlp_processor import NLPProcessor
import logging

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    def __init__(self):
        self.nlp_processor = NLPProcessor()

    def analyze_resume(self, resume_file_path, job_description):
        """Main analysis method - returns results immediately"""
        try:
            # Step 1: Extract text
            logger.info("Extracting text from resume...")
            resume_text = extract_text_from_file(resume_file_path)
            
            if not resume_text:
                raise ValueError("Could not extract text from resume")
            
            # Step 2: Process keywords
            logger.info("Processing keywords...")
            resume_keywords = self.nlp_processor.extract_keywords(resume_text)
            job_keywords = self.nlp_processor.extract_keywords(job_description)
            
            # Step 3: Match keywords
            logger.info("Matching keywords...")
            matching_keywords, missing_keywords = self.match_keywords(job_keywords, resume_keywords)
            
            # Step 4: Calculate similarity
            logger.info("Computing semantic similarity...")
            semantic_similarity = self.nlp_processor.compute_semantic_similarity(job_description, resume_text)
            
            # Step 5: Calculate ATS score
            logger.info("Calculating ATS score...")
            ats_score = self.calculate_ats_score(matching_keywords, job_keywords, semantic_similarity)
            
            # Step 6: Extract entities
            logger.info("Extracting named entities...")
            names, emails, phones = self.nlp_processor.extract_named_entities(resume_text)
            
            # Step 7: Generate feedback
            logger.info("Generating feedback...")
            feedback = self.generate_feedback(ats_score, matching_keywords, missing_keywords, semantic_similarity)
            
            logger.info("Analysis completed successfully!")
            
            return {
                'resume_text': resume_text,
                'ats_score': ats_score,
                'semantic_similarity': semantic_similarity * 100,  # Convert to percentage
                'matching_keywords': matching_keywords,
                'missing_keywords': missing_keywords,
                'applicant_name': names[0] if names else None,
                'email': emails[0] if emails else None,
                'phone_number': phones[0] if phones else None,
                'feedback': feedback,
                'status': 'completed'
            }
        
        except Exception as e:
            logger.error(f"Resume analysis failed: {str(e)}")
            return {
                'resume_text': '',
                'ats_score': 0.0,
                'semantic_similarity': 0.0,
                'matching_keywords': [],
                'missing_keywords': [],
                'applicant_name': None,
                'email': None,
                'phone_number': None,
                'feedback': f"Analysis failed: {str(e)}",
                'status': 'failed'
            }

    def match_keywords(self, job_keywords, resume_keywords):
        """Match job and resume keywords"""
        job_set = set(job_keywords)
        resume_set = set(resume_keywords)
        matching = list(job_set & resume_set)
        missing = list(job_set - resume_set)
        return matching, missing

    def calculate_ats_score(self, matching_keywords, job_keywords, semantic_similarity):
        """Calculate final ATS score"""
        try:
            total_job_keywords = len(job_keywords) if job_keywords else 1
            keyword_score = len(matching_keywords) / total_job_keywords
            
            semantic_score = max(0.0, min(1.0, semantic_similarity))
            
            # 70% keywords, 30% semantic similarity
            ats_score = (keyword_score * 0.7) + (semantic_score * 0.3)
            return min(100.0, ats_score * 100)  # Return as percentage
        
        except Exception as e:
            logger.error(f"ATS score calculation error: {str(e)}")
            return 0.0

    def generate_feedback(self, ats_score, matching_keywords, missing_keywords, semantic_similarity):
        """Generate user feedback"""
        feedback = []
        
        if ats_score < 30:
            feedback.append("Your resume needs significant improvement to match this job.")
        elif ats_score < 60:
            feedback.append("Your resume is moderately aligned with the job requirements.")
        else:
            feedback.append("Your resume is well-aligned with the job requirements!")
        
        if len(matching_keywords) > 0:
            feedback.append(f"Great! You have {len(matching_keywords)} matching keywords.")
        
        if len(missing_keywords) > 0:
            feedback.append(f"Consider adding these keywords: {', '.join(missing_keywords[:5])}.")
        
        if semantic_similarity < 0.3:
            feedback.append("Try to better align your experience with job requirements.")
        
        return " ".join(feedback)
