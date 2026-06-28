#!/usr/bin/env python3
"""
AI-Powered Customer Feedback Classifier
Supports both rule-based and ML-based classification approaches
"""

import sys
import argparse
from classifiers import RuleBasedClassifier, MLClassifier
from config import CATEGORIES, KEYWORDS


def display_banner():
    """Display application banner"""
    print("\n" + "="*60)
    print("AI-Powered Customer Feedback Classifier")
    print("="*60 + "\n")


def interactive_mode(classifier, method):
    """Interactive mode for continuous feedback classification"""
    print(f"Using {method} classifier (type 'quit' to exit)\n")
    
    while True:
        try:
            feedback = input("Enter customer feedback: ").strip()
            
            if feedback.lower() in ['quit', 'exit', 'q']:
                print("Exiting... Thank you!")
                break
            
            if not feedback:
                print("Please enter some feedback.\n")
                continue
            
            category, confidence = classifier.classify(feedback)
            
            print(f"Category: {category}")
            print(f"Confidence: {confidence:.2%}\n")
            
        except KeyboardInterrupt:
            print("\n\nExiting... Thank you!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


def batch_mode(classifier, method, input_file):
    """Batch processing mode from file"""
    print(f"Processing feedback from {input_file} using {method} classifier...\n")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            feedbacks = [line.strip() for line in f if line.strip()]
        
        results = []
        for feedback in feedbacks:
            category, confidence = classifier.classify(feedback)
            results.append({
                'feedback': feedback,
                'category': category,
                'confidence': confidence
            })
        
        # Display results
        for i, result in enumerate(results, 1):
            print(f"{i}. Feedback: {result['feedback']}")
            print(f"   Category: {result['category']} ({result['confidence']:.2%})\n")
        
        # Summary statistics
        print("="*60)
        category_counts = {}
        for result in results:
            cat = result['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        print("Summary Statistics:")
        for cat, count in sorted(category_counts.items()):
            print(f"  {cat}: {count} feedback(s)")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)


def single_classification(classifier, method, feedback):
    """Classify a single feedback string"""
    category, confidence = classifier.classify(feedback)
    
    print(f"\nFeedback: {feedback}")
    print(f"Method: {method}")
    print(f"Category: {category}")
    print(f"Confidence: {confidence:.2%}\n")


def show_info():
    """Display information about categories and implementation"""
    print("\nAvailable Categories:")
    for cat in CATEGORIES:
        print(f"  • {cat}")
    
    print("\nKeyword Examples (Rule-Based Method):")
    for cat, keywords in KEYWORDS.items():
        print(f"  {cat}: {', '.join(keywords[:5])}...")
    
    print("\nImplementation Details:")
    print("  Rule-Based: Uses keyword matching and TF-IDF similarity")
    print("  ML-Based: Uses Naive Bayes classifier with TF-IDF vectorization")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Customer Feedback Classifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with rule-based classifier
  python main.py -m interactive -t rule
  
  # Single feedback classification
  python main.py -c "The app keeps crashing" -t ml
  
  # Batch processing
  python main.py -m batch -f feedbacks.txt -t rule
  
  # Show information
  python main.py --info
        """
    )
    
    parser.add_argument('-m', '--mode', 
                        choices=['interactive', 'batch', 'single'],
                        default='interactive',
                        help='Operation mode (default: interactive)')
    
    parser.add_argument('-t', '--type',
                        choices=['rule', 'ml', 'both'],
                        default='rule',
                        help='Classifier type (default: rule)')
    
    parser.add_argument('-c', '--classify',
                        type=str,
                        help='Single feedback string to classify')
    
    parser.add_argument('-f', '--file',
                        type=str,
                        help='Input file for batch processing')
    
    parser.add_argument('--info',
                        action='store_true',
                        help='Show information about categories and methods')
    
    args = parser.parse_args()
    
    display_banner()
    
    if args.info:
        show_info()
        return
    
    # Initialize classifiers based on type
    classifiers = {}
    if args.type in ['rule', 'both']:
        classifiers['rule'] = RuleBasedClassifier(KEYWORDS, CATEGORIES)
    if args.type in ['ml', 'both']:
        classifiers['ml'] = MLClassifier(CATEGORIES)
    
    # Train ML classifier if needed
    if 'ml' in classifiers:
        print("Initializing ML classifier...")
        classifiers['ml'].train_from_keywords(KEYWORDS)
        print("ML classifier ready.\n")
    
    # Determine primary classifier
    primary_type = args.type if args.type != 'both' else 'rule'
    classifier = classifiers[primary_type]
    
    # Execute based on mode
    if args.mode == 'interactive':
        interactive_mode(classifier, primary_type.upper())
    
    elif args.mode == 'single':
        if not args.classify:
            print("Error: --classify argument required for single mode")
            sys.exit(1)
        single_classification(classifier, primary_type.upper(), args.classify)
    
    elif args.mode == 'batch':
        if not args.file:
            print("Error: --file argument required for batch mode")
            sys.exit(1)
        batch_mode(classifier, primary_type.upper(), args.file)


if __name__ == "__main__":
    main()
