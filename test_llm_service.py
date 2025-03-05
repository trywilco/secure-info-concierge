#!/usr/bin/env python3
from app.models.llm_service import LLMService

def test_llm_service():
    """Test the LLMService class with Azure OpenAI integration"""
    
    # Initialize LLM service
    llm_service = LLMService()
    
    # Test financial queries
    test_queries = [
        "What's my current account balance?",
        "How do I set up a budget?",
        "What are the best investment strategies for retirement?"
    ]
    
    # Sample user data for testing
    user_data = {
        "name": "John Doe",
        "account_number": "XXXX-XXXX-1234",
        "account_type": "Checking",
        "balance": "$5,432.10"
    }
    
    # Sample transaction history for testing
    transaction_history = [
        {"date": "2023-05-01", "description": "Grocery Store", "amount": "45.67"},
        {"date": "2023-05-03", "description": "Gas Station", "amount": "35.50"},
        {"date": "2023-05-05", "description": "Online Shopping", "amount": "120.99"}
    ]
    
    # Test generate_response
    print("\n=== Testing LLM Response Generation ===")
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = llm_service.generate_response(query, context=user_data, transaction_history=transaction_history)
        print(f"Response: {response}")
    
    # Test intent classification
    print("\n=== Testing Intent Classification ===")
    candidate_labels = ["account_inquiry", "financial_advice", "transaction_history", "customer_support"]
    for query in test_queries:
        print(f"\nQuery: {query}")
        intent = llm_service.classify_intent(query, candidate_labels)
        if intent:
            print(f"Classified as: {intent['label']} (score: {intent['score']})")
        else:
            print("Classification failed")

if __name__ == "__main__":
    test_llm_service()
