#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

def test_azure_openai():
    """Test Azure OpenAI API connection and response generation"""
    
    # Get Azure OpenAI credentials from environment variables
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")
    
    # Validate Azure OpenAI configuration
    if not azure_endpoint or not api_key:
        print("Error: Azure OpenAI endpoint or API key not configured.")
        print("Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables.")
        return
    
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
