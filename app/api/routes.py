from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from app.auth.jwt import get_current_user, User
from app.database.db_manager import (
    get_client_data, log_user_query, get_account_balance, 
    get_recent_transactions, get_user_query_history, get_spending_analysis
)
from app.models.llm_service import LLMService
import json

router = APIRouter()
llm_service = LLMService()

# Store previous queries for semantic similarity search
previous_queries = []

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
    
    # Simple intent-based response generation
    if "balance" in query.lower():
        accounts = await get_account_balance(current_user.username)
        if accounts:
            accounts_info = "\n".join([f"{account['account_type'].capitalize()} account ending in {account['account_number'][-4:]}: ${account['balance']:.2f}" for account in accounts])
            context = f"Account Information:\n{accounts_info}"
        else:
            context = "No account information available."
    elif "transaction" in query.lower() or "spend" in query.lower():
        transactions = await get_recent_transactions(current_user.username, 5)
        if transactions:
            trans_info = "\n".join([f"{t['transaction_date'].split()[0]} - {t['description']} - ${t['amount']:.2f} ({t['transaction_type']})" for t in transactions])
            context = f"Recent Transactions:\n{trans_info}"
        else:
            context = "No recent transactions found."
    else:
        # For other queries, get general information
        data_items = await get_client_data(intent_tag, 3) if intent_tag else []
        context = "\n\n".join([item['info'] for item in data_items]) if data_items else ""
    
    # Generate response using LLM
    response = llm_service.generate_response(query, context)
    
    return QueryResponse(response=response)

# User endpoints
@router.get("/users/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users/history")
async def get_query_history(current_user: User = Depends(get_current_user)):
    """Get the user's query history"""
    history = await get_user_query_history(current_user.username)
    return {"history": history}

@router.get("/users/accounts")
async def get_user_accounts(current_user: User = Depends(get_current_user)):
    """Get the user's financial accounts"""
    accounts = await get_account_balance(current_user.username)
    return {"accounts": accounts}

@router.get("/users/transactions")
async def get_user_transactions(limit: int = 10, current_user: User = Depends(get_current_user)):
    """Get the user's recent transactions"""
    transactions = await get_recent_transactions(current_user.username, limit)
    return {"transactions": transactions}

@router.get("/users/spending-analysis")
async def get_user_spending_analysis(days: int = 30, current_user: User = Depends(get_current_user)):
    """Get spending analysis for the user"""
    analysis = await get_spending_analysis(current_user.username, days)
    return analysis
