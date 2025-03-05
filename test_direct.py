#!/usr/bin/env python3
from openai import AzureOpenAI

def test_azure_openai():
    """Test Azure OpenAI API connection and response generation"""
    
    # Hardcoded Azure OpenAI credentials for testing
    azure_endpoint = "https://wilco-ai.openai.azure.com"
    api_key = "fec412fcb1f14812b7416e74ae7c0f6b"
    deployment_name = "gpt-4o-mini"
    api_version = "2025-01-01-preview"
    
    print(f"Azure OpenAI endpoint: {azure_endpoint}")
    print(f"Using deployment: {deployment_name}")
    print(f"Using API version: {api_version}")
    
    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )
        
        # Test a single query
        query = "What's my current account balance?"
        print("\n" + "="*50)
        print(f"Query: {query}")
        
        # Call Azure OpenAI API
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a secure financial information concierge. Provide helpful, accurate, and concise responses about financial information."},
                {"role": "user", "content": f"Answer this financial question: {query}"}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=0.95
        )
        
        # Extract and print the response
        if response.choices and len(response.choices) > 0:
            response_text = response.choices[0].message.content
            print(f"Response: {response_text}")
        else:
            print("No response received.")
        
        print("="*50)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_azure_openai()
