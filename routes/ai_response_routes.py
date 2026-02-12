from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import ChatHistory, User, Conversation
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse, ChatMessage, ConversationSchema
from utils.deps import get_current_user
from datetime import datetime
from typing import List, Optional

router = APIRouter()

@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get response from AI model, save to history, manage conversation."""
    try:
        conversation_id = request.conversation_id
        
        # New Conversation?
        if conversation_id is None:
            new_conv = Conversation(
                user_id=current_user.id,
                title=request.message[:30], # Simple title from first message
                created_at=datetime.utcnow()
            )
            db.add(new_conv)
            db.commit()
            db.refresh(new_conv)
            conversation_id = new_conv.id
        else:
            # Verify ownership
            conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
            if not conv:
                raise HTTPException(status_code=404, detail="Conversation not found or access denied")

        # Save User Message
        user_msg = ChatHistory(
            conversation_id=conversation_id,
            role="user",
            content=request.message,
            timestamp=datetime.utcnow()
        )
        db.add(user_msg)
        
        # Get Response
        response_text = get_completion(request.message, request.system_prompt)
        
        # Save AI Message
        ai_msg = ChatHistory(
            conversation_id=conversation_id,
            role="assistant",
            content=response_text,
            timestamp=datetime.utcnow()
        )
        db.add(ai_msg)
        
        db.commit()

        return AIResponse(response=response_text, conversation_id=conversation_id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations", response_model=List[ConversationSchema])
def get_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all conversations for current user."""
    return db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.created_at.desc()).all()

@router.get("/history/{conversation_id}", response_model=List[ChatMessage])
def get_conversation_history(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get messages for a specific conversation."""
    # Verify ownership
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    history = db.query(ChatHistory).filter(ChatHistory.conversation_id == conversation_id).order_by(ChatHistory.timestamp.asc()).all()
    return history

@router.delete("/conversation/{conversation_id}")
def delete_conversation(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a conversation and its messages."""
    # Verify ownership
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")
    
    try:
        # Delete messages first due to FK constraints if any (though Cascade would be better)
        db.query(ChatHistory).filter(ChatHistory.conversation_id == conversation_id).delete()
        db.delete(conv)
        db.commit()
        return {"message": "Conversation deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
