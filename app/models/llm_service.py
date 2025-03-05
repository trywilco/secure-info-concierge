import re
import os
import logging
from openai import AzureOpenAI
from app.config.credentials_service import CredentialsService

logger = logging.getLogger(__name__)

class LLMService:
    """Service for generating responses using Azure OpenAI"""
    
    def __init__(self):
        """Initialize the Azure OpenAI service"""
        logger.info("Initializing LLM Service with Azure OpenAI...")
        
        try:
            # Initialize credentials service
            self.credentials_service = CredentialsService()
            credentials = self.credentials_service.get_credentials()
            
            # Extract credentials
            self.azure_endpoint = credentials["base_url"]
            self.api_key = credentials["api_key"]
            self.deployment_name = credentials["deployment_name"]
            self.api_version = credentials["api_version"]
            
            # Log Azure OpenAI configuration
            logger.info(f"Azure OpenAI endpoint configured: {self.azure_endpoint}")
            logger.info(f"Using deployment: {self.deployment_name}")
            logger.info(f"Using API version: {self.api_version}")
            
            # Initialize Azure OpenAI client
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
    
    def generate_response(self, query, context=None, transaction_history=None):
        """Generate a response to the user query using Azure OpenAI"""
        # Sanitize the query
        sanitized_query = self._sanitize_input(query)
        
        # Prepare system message with financial context
        system_message = "You are a secure financial information concierge. "
        system_message += "Provide helpful, accurate, and concise responses about financial information. "
        system_message += "Never reveal sensitive information unless explicitly authorized. "
        
        # Add context if available
        if context:
            # Check if context is a dictionary (user_data) or a string
            if isinstance(context, dict):
                # Handle dictionary context (user_data)
                context_str = "\nUser Information:\n"
                for key, value in context.items():
                    if key != 'password' and key != 'password_hash':
                        context_str += f"{key}: {value}\n"
                system_message += f"\nHere is the relevant context for the user:\n{context_str}"
            else:
                # Handle string context
                system_message += f"\nHere is the relevant context for the user:\n{context}"
        
        # Add transaction history if available
        if transaction_history:
            tx_context = "\nRecent Transactions:\n"
            for tx in transaction_history[:5]:  # Limit to 5 most recent
                tx_context += f"{tx['date']} - {tx['description']}: ${tx['amount']}\n"
            system_message += f"\n{tx_context}"
        
        try:
            # Call Azure OpenAI API
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": sanitized_query}
                ],
                temperature=0.7,
                max_tokens=256,
                top_p=0.95
            )
            
            # Extract and return the response
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
            # Use Azure OpenAI to classify intent
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
            
            # Extract the response
            if response.choices and len(response.choices) > 0:
                classification = response.choices[0].message.content.strip()
                
                # Find the best matching label
                best_label = None
                for label in candidate_labels:
                    if label.lower() in classification.lower():
                        best_label = label
                        break
                
                # If no match found, use the first label
                if not best_label and candidate_labels:
                    best_label = candidate_labels[0]
                
                print(f"Classified intent: {best_label}")
                return {
                    'label': best_label,
                    'score': 0.9  # Placeholder score
                }
            else:
                return None
        except Exception as e:
            print(f"Error classifying intent: {str(e)}")
            return None
    
    def interpret_user_intent(self, query):
        """Interpret the user's intent from their query"""
        # Define common financial intents
        intents = [
            "account_balance",
            "transaction_history",
            "spending_analysis",
            "budget_advice",
            "investment_advice",
            "general_question"
        ]
        
        try:
            # Use Azure OpenAI to classify intent
            result = self.classify_intent(query, intents)
            if result:
                return result['label']
            else:
                # Default fallback intent
                return "general_question"
        except Exception as e:
            print(f"Error interpreting user intent: {str(e)}")
            return "general_question"
    
    def _sanitize_input(self, text):
        """Sanitize user input to remove potential harmful content"""
        if not text:
            return ""
        
        # Remove any potential SQL injection or script tags
        sanitized = re.sub(r'[<>]|script|SELECT|INSERT|UPDATE|DELETE|DROP|UNION|--', '', text, flags=re.IGNORECASE)
        
        # Limit length
        max_length = 1000
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
