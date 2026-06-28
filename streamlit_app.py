"""
AI-Powered Customer Feedback Classifier - Streamlit Version
Deploy to Streamlit Cloud for a live shareable link!
"""

import streamlit as st
from classifiers import RuleBasedClassifier, MLClassifier
from config import KEYWORDS, CATEGORIES
import pandas as pd

# Page config
st.set_page_config(
    page_title="🤖 AI Feedback Classifier",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1em;
        padding: 10px 20px;
    }
    .success-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 10px 0;
    }
    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #e7f3ff;
        border: 1px solid #b3d9ff;
        color: #004085;
        margin: 10px 0;
    }
    .category-badge {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px 5px 5px 0;
    }
    .technical {
        background-color: #667eea;
        color: white;
    }
    .billing {
        background-color: #764ba2;
        color: white;
    }
    .feedback {
        background-color: #f093fb;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'rule_classifier' not in st.session_state:
    st.session_state.rule_classifier = RuleBasedClassifier(KEYWORDS, CATEGORIES)
    st.session_state.ml_classifier = MLClassifier(CATEGORIES)
    st.session_state.ml_classifier.train_from_keywords(KEYWORDS)

# Header
st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1>🤖 AI Feedback Classifier</h1>
        <p style='font-size: 1.2em; color: #666;'>
            Automatically categorize customer feedback with AI
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    method = st.radio(
        "🧠 Select Classification Method:",
        ["⚡ Rule-Based (Fast)", "🧠 ML-Based (Smart)"],
        help="Rule-Based: Fast and simple. ML-Based: Better accuracy with varied text."
    )
    
    classifier_type = "rule" if "Rule" in method else "ml"
    
    st.markdown("---")
    
    st.markdown("### 📊 About This App")
    st.info("""
    **Features:**
    - Single feedback classification
    - Batch processing (100+ feedbacks)
    - Real-time results
    - Summary statistics
    
    **Categories:**
    - 📱 Technical Support
    - 💳 Billing
    - 💬 Feedback
    """)
    
    st.markdown("---")
    
    st.markdown("""
    **Made with ❤️ using Streamlit**
    
    [GitHub](https://github.com) | [Twitter](https://twitter.com)
    """)

# Main content - Tabs
tab1, tab2, tab3 = st.tabs(["🎯 Single Feedback", "📊 Batch Processing", "ℹ️ About"])

# TAB 1: Single Feedback
with tab1:
    st.markdown("<div class='info-box'>📝 Classify a single customer feedback instantly</div>", 
                unsafe_allow_html=True)
    
    # Input
    feedback = st.text_area(
        "Enter Customer Feedback:",
        placeholder="Example: The app keeps crashing when I try to upload files...",
        height=100,
        key="single_feedback"
    )
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        classify_btn = st.button("🚀 Classify Feedback", use_container_width=True, key="classify_single")
    
    with col2:
        clear_btn = st.button("🔄 Clear", use_container_width=True, key="clear_single")
    
    if clear_btn:
        st.rerun()
    
    # Classification
    if classify_btn:
        if not feedback.strip():
            st.warning("⚠️ Please enter some feedback!")
        else:
            with st.spinner("🤔 Analyzing feedback..."):
                classifier = st.session_state.rule_classifier if classifier_type == "rule" else st.session_state.ml_classifier
                category, confidence = classifier.classify(feedback)
                
                # Display result
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Feedback:** {feedback}")
                
                with col2:
                    confidence_pct = round(confidence * 100, 2)
                    
                    # Color code by category
                    if category == "Technical Support":
                        badge_class = "technical"
                    elif category == "Billing":
                        badge_class = "billing"
                    else:
                        badge_class = "feedback"
                    
                    st.markdown(f"""
                        <div style='text-align: center; padding: 20px; border-radius: 10px; background: #f8f9fa;'>
                            <h3 style='margin: 0;'>{category}</h3>
                            <h2 style='margin: 10px 0 0 0; color: #667eea;'>{confidence_pct}% confident</h2>
                            <p style='margin: 10px 0 0 0; color: #666;'>Method: {classifier_type.upper()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown(f"<div class='success-box'>✅ Successfully classified!</div>", 
                           unsafe_allow_html=True)

# TAB 2: Batch Processing
with tab2:
    st.markdown("<div class='info-box'>📤 Process multiple feedbacks at once (one per line)</div>", 
                unsafe_allow_html=True)
    
    # Input
    batch_text = st.text_area(
        "Enter Feedbacks (one per line):",
        placeholder="""The app crashes
I was charged twice
Love the new design!
Why is password reset not working?
Great quality product
Why is it so expensive?""",
        height=200,
        key="batch_feedback"
    )
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        process_btn = st.button("⚡ Process Batch", use_container_width=True, key="process_batch")
    
    with col2:
        clear_batch_btn = st.button("🔄 Clear", use_container_width=True, key="clear_batch")
    
    if clear_batch_btn:
        st.rerun()
    
    # Process batch
    if process_btn:
        feedbacks = [f.strip() for f in batch_text.split('\n') if f.strip()]
        
        if not feedbacks:
            st.warning("⚠️ Please enter at least one feedback!")
        else:
            with st.spinner(f"🤔 Processing {len(feedbacks)} feedbacks..."):
                classifier = st.session_state.rule_classifier if classifier_type == "rule" else st.session_state.ml_classifier
                
                results = []
                category_counts = {}
                
                for feedback in feedbacks:
                    category, confidence = classifier.classify(feedback)
                    results.append({
                        'Feedback': feedback,
                        'Category': category,
                        'Confidence': f"{round(confidence * 100, 1)}%"
                    })
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                # Display results table
                st.markdown("### 📋 Results")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
                
                # Summary statistics
                st.markdown("### 📊 Summary Statistics")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "📱 Technical Support",
                        category_counts.get("Technical Support", 0)
                    )
                
                with col2:
                    st.metric(
                        "💳 Billing",
                        category_counts.get("Billing", 0)
                    )
                
                with col3:
                    st.metric(
                        "💬 Feedback",
                        category_counts.get("Feedback", 0)
                    )
                
                # Chart
                st.markdown("### 📈 Distribution")
                
                chart_data = pd.DataFrame({
                    'Category': list(category_counts.keys()),
                    'Count': list(category_counts.values())
                })
                
                st.bar_chart(chart_data.set_index('Category'))
                
                st.markdown(f"<div class='success-box'>✅ Processed {len(feedbacks)} feedbacks successfully!</div>", 
                           unsafe_allow_html=True)

# TAB 3: About
with tab3:
    st.markdown("### 🤖 About AI Feedback Classifier")
    
    st.markdown("""
    This application uses artificial intelligence to automatically categorize 
    customer feedback into three main categories:
    
    #### 📱 Technical Support
    - Bug reports and crashes
    - Feature requests
    - Installation and setup issues
    - Troubleshooting questions
    
    #### 💳 Billing
    - Payment and transaction issues
    - Subscription management
    - Refund requests
    - Pricing concerns
    
    #### 💬 Feedback
    - General comments and opinions
    - Feature suggestions
    - Compliments
    - Constructive criticism
    
    ---
    
    ### ⚡ Classification Methods
    
    **Rule-Based Classifier:**
    - Fast and simple
    - Uses keyword matching and similarity
    - No training required
    - Good for clear, keyword-rich feedback
    
    **ML-Based Classifier (Machine Learning):**
    - Uses Naive Bayes algorithm
    - Learns patterns from keywords
    - Better accuracy with varied text
    - Great for production use
    
    ---
    
    ### 🛠️ Technology Stack
    
    - **Frontend:** Streamlit
    - **Backend:** Python
    - **ML/NLP:** scikit-learn, numpy
    - **Deployment:** Streamlit Cloud
    
    ---
    
    ### 📊 Use Cases
    
    ✅ **Customer Support** - Auto-route tickets to departments
    
    ✅ **Quality Assurance** - Analyze feedback distribution
    
    ✅ **Product Team** - Identify feature requests
    
    ✅ **Sales** - Track customer sentiment
    
    ✅ **Training** - Learn about feedback patterns
    
    ---
    
    ### 🔗 Links
    
    - **GitHub Repository:** [View on GitHub](https://github.com)
    - **Built with:** [Streamlit](https://streamlit.io)
    
    """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Made with ❤️ using Streamlit</p>
        <p>© 2024 AI Feedback Classifier</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 0.9em;'>
    <p>🚀 Powered by Streamlit | 🤖 AI-Powered Feedback Classification</p>
</div>
""", unsafe_allow_html=True)
