"""
Classification implementations for customer feedback
Supports both rule-based and machine learning approaches
"""

from abc import ABC, abstractmethod
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import re


class Classifier(ABC):
    """Abstract base class for classifiers"""
    
    @abstractmethod
    def classify(self, feedback: str) -> tuple:
        """
        Classify feedback into a category
        Returns: (category, confidence_score)
        """
        pass


class RuleBasedClassifier(Classifier):
    """
    Rule-based classifier using keyword matching and TF-IDF similarity
    Simple, interpretable, and doesn't require training data
    """
    
    def __init__(self, keywords: dict, categories: list):
        """
        Initialize rule-based classifier
        
        Args:
            keywords: Dict mapping category -> list of keywords
            categories: List of valid categories
        """
        self.keywords = keywords
        self.categories = categories
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self._prepare_keyword_vectors()
    
    def _prepare_keyword_vectors(self):
        """Prepare TF-IDF vectors for keyword sets"""
        # Create keyword documents
        keyword_docs = [' '.join(keywords) for keywords in self.keywords.values()]
        
        # Fit vectorizer and transform
        self.keyword_vectors = self.vectorizer.fit_transform(keyword_docs)
    
    def _preprocess(self, text: str) -> str:
        """Preprocess feedback text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
        return text.strip()
    
    def _calculate_keyword_match_score(self, feedback: str, keywords: list) -> float:
        """Calculate match score based on keyword presence"""
        feedback_words = set(feedback.split())
        keyword_set = set(keywords)
        
        if not keyword_set:
            return 0.0
        
        matches = len(feedback_words & keyword_set)
        return matches / len(keyword_set)
    
    def classify(self, feedback: str) -> tuple:
        """
        Classify feedback using keyword matching
        Returns: (category, confidence_score)
        """
        preprocessed = self._preprocess(feedback)
        
        # Calculate scores for each category
        scores = {}
        for category, keywords in self.keywords.items():
            score = self._calculate_keyword_match_score(preprocessed, keywords)
            scores[category] = score
        
        # Calculate TF-IDF similarity
        try:
            feedback_vector = self.vectorizer.transform([preprocessed])
            from sklearn.metrics.pairwise import cosine_similarity
            
            similarities = {}
            for idx, category in enumerate(self.categories):
                similarity = cosine_similarity(feedback_vector, 
                                              self.keyword_vectors[idx:idx+1])[0][0]
                similarities[category] = similarity
            
            # Combine keyword match and TF-IDF scores (60% / 40%)
            combined_scores = {}
            for category in self.categories:
                combined = (scores.get(category, 0) * 0.6 + 
                           similarities.get(category, 0) * 0.4)
                combined_scores[category] = combined
        
        except:
            combined_scores = scores
        
        # Get best match
        if not combined_scores or max(combined_scores.values()) == 0:
            # Default to first category if no match
            best_category = self.categories[0]
            confidence = 0.33  # Equal confidence if no keywords match
        else:
            best_category = max(combined_scores, key=combined_scores.get)
            confidence = min(combined_scores[best_category], 1.0)
        
        return best_category, confidence


class MLClassifier(Classifier):
    """
    Machine learning-based classifier using Naive Bayes
    Learns from training data for better accuracy
    """
    
    def __init__(self, categories: list):
        """
        Initialize ML classifier
        
        Args:
            categories: List of valid categories
        """
        self.categories = categories
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english', 
                                     max_features=1000, ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        self.is_trained = False
    
    def train_from_keywords(self, keywords: dict):
        """
        Train classifier using keyword data
        Expands keywords into synthetic training examples
        
        Args:
            keywords: Dict mapping category -> list of keywords
        """
        # Create training data from keywords
        training_texts = []
        training_labels = []
        
        for category, keyword_list in keywords.items():
            # Use keywords as training data
            training_texts.extend(keyword_list)
            training_labels.extend([category] * len(keyword_list))
        
        if training_texts:
            self.pipeline.fit(training_texts, training_labels)
            self.is_trained = True
    
    def train(self, texts: list, labels: list):
        """
        Train classifier with custom training data
        
        Args:
            texts: List of feedback strings
            labels: List of corresponding category labels
        """
        self.pipeline.fit(texts, labels)
        self.is_trained = True
    
    def classify(self, feedback: str) -> tuple:
        """
        Classify feedback using trained ML model
        Returns: (category, confidence_score)
        """
        if not self.is_trained:
            raise ValueError("Classifier must be trained before use")
        
        # Get prediction and probability
        prediction = self.pipeline.predict([feedback])[0]
        probabilities = self.pipeline.predict_proba([feedback])[0]
        confidence = max(probabilities)
        
        return prediction, confidence
