import spacy
import re
from sentence_transformers import SentenceTransformer, util
import logging

logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Error initializing NLP models: {str(e)}")
            raise

    def extract_keywords(self, text, include_skills=True):
        """Extract keywords using spaCy"""
        if not text:
            return set()
        
        try:
            doc = self.nlp(text.lower())
            keywords = set()
            
            for token in doc:
                if token.is_stop or token.is_punct or token.is_space:
                    continue
                if token.pos_ in ['NOUN', 'PROPN', 'VERB']:
                    keywords.add(token.lemma_)
            
            if include_skills:
                skill_keywords = self.extract_skill_entities(doc)
                keywords.update(skill_keywords)
            
            return keywords
        
        except Exception as e:
            logger.error(f"Keyword extraction error: {str(e)}")
            return set()

    def extract_skill_entities(self, doc):
        """Extract technology skills"""
        tech_patterns = [
            r'\b(?:python|java|javascript|react|angular|vue|node|django|flask|sql|mongodb|aws|azure|docker|kubernetes|git)\b',
            r'\b(?:machine learning|data science|artificial intelligence|deep learning|nlp|computer vision)\b',
            r'\b(?:html|css|bootstrap|tailwind|jquery|typescript|php|ruby|c\+\+|c#|go|rust)\b'
        ]
        
        skills = set()
        text_lower = doc.text.lower()
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            skills.update(matches)
        
        return skills

    def extract_named_entities(self, text):
        """Extract names, emails, phones"""
        if not text:
            return [], [], []
        
        try:
            doc = self.nlp(text)
            
            # Extract names
            names = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
            
            # Extract emails
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text, re.IGNORECASE)
            
            # Extract phone numbers
            phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
            phones = re.findall(phone_pattern, text)
            
            return names, emails, phones
        
        except Exception as e:
            logger.error(f"Entity extraction error: {str(e)}")
            return [], [], []

    def compute_semantic_similarity(self, text1, text2):
        """Calculate semantic similarity"""
        try:
            if not text1 or not text2:
                return 0.0
            
            embedding1 = self.similarity_model.encode(text1, convert_to_tensor=True)
            embedding2 = self.similarity_model.encode(text2, convert_to_tensor=True)
            
            similarity = util.pytorch_cos_sim(embedding1, embedding2)
            return float(similarity.item())
        
        except Exception as e:
            logger.error(f"Similarity calculation error: {str(e)}")
            return 0.0
