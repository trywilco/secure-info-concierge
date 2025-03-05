import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.llm_service import LLMService

def test_phi2_performance():
    print("Testing Phi-2 model performance...")
    
    # Sample financial queries for testing
    test_queries = [
        "What's the best way to improve my credit score?",
        "How do I create a budget for my monthly expenses?",
        "What are the pros and cons of different retirement accounts?",
        "How can I protect myself from financial fraud?"
    ]
    
    # Initialize LLM service
    start_time = time.time()
    llm_service = LLMService()
    init_time = time.time() - start_time
    print(f"Model initialization time: {init_time:.2f} seconds")
    
    # Test response generation
    total_time = 0
    for i, query in enumerate(test_queries):
        print(f"\nQuery {i+1}: {query}")
        
        # Measure response time
        start_time = time.time()
        response = llm_service.generate_response(query)
        query_time = time.time() - start_time
        total_time += query_time
        
        print(f"Response: {response}")
        print(f"Generation time: {query_time:.2f} seconds")
        print("-" * 50)
    
    avg_time = total_time / len(test_queries)
    print(f"\nAverage response time: {avg_time:.2f} seconds")
    print(f"Total test time: {total_time:.2f} seconds")

if __name__ == "__main__":
    test_phi2_performance()
