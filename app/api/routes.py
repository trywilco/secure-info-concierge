from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from app.auth.jwt import get_current_user, User
from app.database.db_manager import (
    get_client_data, log_user_query, get_account_balance, 
    get_recent_transactions
)
from app.models.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@router.post("/secure-query", response_model=QueryResponse)
async def secure_query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    query = request.query
    
    # Determine intent using LLM
    intent_tag = llm_service.interpret_user_intent(query)
    
    # Log the query in background
    background_tasks.add_task(log_user_query, current_user.username, query, intent_tag)
    
    # Fetch context based on intent
    context = await get_context_for_intent(intent_tag, current_user.username)
    
    # Generate response using LLM
    response = llm_service.generate_response(query, context)
    
    return QueryResponse(response=response)

async def get_context_for_intent(intent_tag: str, username: str) -> str:
    if intent_tag == "account_balance":
        accounts = await get_account_balance(username)
        if accounts:
            accounts_info = "\n".join([f"{account['account_type'].capitalize()} account {account['account_number']}: ${account['balance']:.2f}" for account in accounts])
            return f"Account Information:\n{accounts_info}"
        else:
            return "No account information available."
            
    elif intent_tag in ["transaction_history", "spending_analysis"]:
        transactions = await get_recent_transactions(username, 5)
        if transactions:
            trans_info = "\n".join([f"{t['transaction_date'].split()[0]} - {t['description']} - ${t['amount']:.2f} ({t['transaction_type']})" for t in transactions])
            return f"Recent Transactions:\n{trans_info}"
        else:
            return "No recent transactions found."
            
    else:
        # For other queries, get general information
        data_items = await get_client_data(intent_tag) if intent_tag else []
        return "\n\n".join([item['info'] for item in data_items]) if data_items else ""

# User endpoints
@router.get("/users/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
