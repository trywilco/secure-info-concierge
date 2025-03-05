import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.llm_service import LLMService

def test_llm_model():
    print("Initializing LLM Service with Azure OpenAI...")
    
    # Set Azure OpenAI credentials - replace with your actual values
    os.environ["AZURE_OPENAI_ENDPOINT"] = "YOUR_AZURE_ENDPOINT"
    os.environ["AZURE_OPENAI_API_KEY"] = "YOUR_API_KEY"
    os.environ["AZURE_OPENAI_DEPLOYMENT"] = "YOUR_DEPLOYMENT_NAME"
    
    llm_service = LLMService()
    
    # Test financial queries
    test_queries = [
        "What's my current account balance?",
        "How can I improve my credit score?",
        "What are the best investment options for retirement?",
        "Can you explain how mortgage rates work?"
    ]
    
    for query in test_queries:
        print("\n" + "="*50)
        print(f"Query: {query}")
        response = llm_service.generate_response(query)
        print(f"Response: {response}")
        print("="*50)
    
    # Test with context
    context = """
    Account Summary:
    Checking Account: $2,543.87
    Savings Account: $15,789.23
    Credit Card Balance: $432.19
    Last Transaction: Coffee Shop - $4.50 on 2023-03-04
    """
    
    query_with_context = "How much money do I have in my accounts?"
    print("\n" + "="*50)
    print(f"Query with context: {query_with_context}")
    response = llm_service.generate_response(query_with_context, context)
    print(f"Response with context: {response}")
    print("="*50)

if __name__ == "__main__":
    test_llm_model()
