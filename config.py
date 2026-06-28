"""
Configuration for the feedback classifier
Defines categories and keywords for both rule-based and ML training
"""

# Define feedback categories
CATEGORIES = [
    "Technical Support",
    "Billing",
    "Feedback"
]

# Keywords for each category (used for rule-based matching and ML training)
KEYWORDS = {
    "Technical Support": [
        # Bug and error related
        "bug", "crash", "error", "broken", "not working", "failed", "exception",
        "error message", "glitch", "malfunction", "stops", "freeze", "hangs",
        "loading", "timeout", "connection", "network", "slow", "lag", "lag",
        
        # Feature and functionality related
        "feature", "function", "doesn't work", "unable", "can't", "cannot",
        "fails", "missing", "installation", "setup", "install", "uninstall",
        "update", "upgrade", "version", "compatibility", "plugin", "extension",
        
        # Device and platform related
        "device", "app", "application", "software", "system", "mobile", "desktop",
        "windows", "mac", "linux", "ios", "android", "browser", "chrome", "safari",
        
        # Help and guidance related
        "help", "how to", "tutorial", "guide", "documentation", "manual", "support",
        "support team", "technical support", "troubleshoot", "fix", "resolve",
        "solution", "workaround", "issue", "problem", "debug"
    ],
    
    "Billing": [
        # Payment and transaction related
        "payment", "charge", "billing", "invoice", "bill", "price", "cost",
        "fee", "subscription", "paid", "purchase", "order", "transaction",
        "money", "refund", "refund", "discount", "coupon", "promo",
        
        # Account and plan related
        "account", "plan", "upgrade", "downgrade", "cancel", "subscription",
        "premium", "free", "trial", "pricing", "tier", "monthly", "annual",
        "credit card", "payment method", "renewal", "auto-renew",
        
        # Issues and complaints
        "overcharge", "duplicate charge", "wrong amount", "unexpected charge",
        "billing error", "payment failed", "declined", "charge dispute",
        "refund status", "invoice issue", "receipt", "billing inquiry",
        "payment issue", "financial", "expense", "cost", "expensive"
    ],
    
    "Feedback": [
        # Positive feedback
        "great", "excellent", "awesome", "amazing", "wonderful", "fantastic",
        "perfect", "love", "like", "good", "happy", "satisfied", "impressed",
        "helpful", "easy", "simple", "smooth", "intuitive", "user friendly",
        
        # Suggestions and improvements
        "suggestion", "improve", "improvement", "feature request", "idea", "thought",
        "better", "could be", "should have", "nice to have", "would like",
        "recommend", "recommendation", "opinion", "comment", "feedback", "input",
        
        # Neutral observations
        "experience", "interface", "design", "layout", "appearance", "look",
        "feel", "performance", "speed", "reliability", "quality", "service",
        
        # Negative feedback
        "bad", "poor", "disappointing", "disappointed", "unhappy", "unsatisfied",
        "confusing", "difficult", "complicated", "unclear", "messy", "weak",
        "not satisfied", "expectation", "expected", "complaint", "issue"
    ]
}

# Optional: Additional configuration parameters
CONFIG = {
    "rule_based": {
        "keyword_weight": 0.6,
        "similarity_weight": 0.4,
        "min_confidence": 0.1
    },
    "ml_based": {
        "max_features": 1000,
        "ngram_range": (1, 2),
        "min_confidence": 0.3
    }
}
