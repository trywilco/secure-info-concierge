#!/usr/bin/env python3
from app.models.llm_service import LLMService

def test_intent_interpretation():
    """Test the interpret_user_intent method of LLMService"""
    
    # Initialize LLM service
    llm_service = LLMService()
    
    # Test financial queries
    test_queries = [
        "What's my current account balance?",
        "How do I set up a budget?",
        "What are the best investment strategies for retirement?",
        "Show me my recent transactions",
        "Can you analyze my spending patterns?",
        "What's the best way to save for a house?"
    ]
    
    # Test intent interpretation
    print("\n=== Testing Intent Interpretation ===")
    for query in test_queries:
        print(f"\nQuery: {query}")
        intent = llm_service.interpret_user_intent(query)
        print(f"Interpreted intent: {intent}")

if __name__ == "__main__":
    test_intent_interpretation()
