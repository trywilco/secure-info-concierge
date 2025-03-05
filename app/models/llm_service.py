import re
import logging
from openai import AzureOpenAI
from app.config.credentials_service import CredentialsService
from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

logger = logging.getLogger(__name__)

class LLMService:
    """Service for generating responses using Azure OpenAI"""
    
    def __init__(self):
        """Initialize the Azure OpenAI service"""
        logger.info("Initializing LLM Service with Azure OpenAI...")
        
        try:
            self.credentials_service = CredentialsService()
            credentials = self.credentials_service.get_credentials()
            
            self.azure_endpoint = credentials["base_url"]
            self.api_key = credentials["api_key"]
            self.deployment_name = credentials["deployment_name"]
            self.api_version = credentials["api_version"]
            
            self.client = AzureOpenAI(
                azure_endpoint=self.azure_endpoint,
                api_key=self.api_key,
                api_version=self.api_version
            )
            logger.info("Azure OpenAI client initialized successfully")
            
        except ValueError as e:
            logger.error(f"Configuration error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error initializing Azure OpenAI client: {str(e)}")
            raise
    
    def generate_response(self, query, context=None):
        system_message = "You are a secure financial information concierge. "
        system_message += "Provide helpful, accurate, and concise responses about financial information. "
        system_message += "Never reveal sensitive information unless explicitly authorized. "
        
        if context:
            system_message += f"\nHere is the relevant context for the user:\n{context}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=256,
                top_p=0.95
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "I'm sorry, I couldn't generate a response. Please try again."
                
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"I'm sorry, there was an error processing your request: {str(e)}"
    
    def classify_intent(self, query, candidate_labels):
        """Classify the intent of the user query using Azure OpenAI"""
        try:
            prompt = f"Classify the following query into one of these categories: {', '.join(candidate_labels)}\n\nQuery: {query}\n\nCategory:"
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that classifies user queries into predefined categories. Respond only with the exact category name."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=20
            )
            
            if response.choices and len(response.choices) > 0:
                classification = response.choices[0].message.content.strip()
                
                best_label = None
                for label in candidate_labels:
                    if label.lower() in classification.lower():
                        best_label = label
                        break
                
                if not best_label and candidate_labels:
                    best_label = candidate_labels[0]
                
                print(f"Classified intent: {best_label}")
                return best_label
            else:
                return None
        except Exception as e:
            print(f"Error classifying intent: {str(e)}")
            return None
    
    def interpret_user_intent(self, query):
        """Interpret the user's intent from their query"""
        intents = [
            "account_balance",
            "transaction_history",
            "spending_analysis",
            "budget_advice",
            "investment_advice",
            "general_question"
        ]
        
        try:
            result = self.classify_intent(query, intents)
            if result:
                return result
            else:
                return "general_question"
        except Exception as e:
            print(f"Error interpreting user intent: {str(e)}")
            return "general_question"
