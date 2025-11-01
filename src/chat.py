from .retrieval import retrieve
from .prompt_gen import build_prompt
from .config import GEMINI_API_KEY, MODEL, TOP_K
from .formatter import create_professional_summary
from google import genai
import datetime

# Initialize the GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

# Session state management
conversation_state = {
    "file_name": None,
    "conversation_history": [],
    "session_id": None,
    "start_time": None,
    "status": "inactive"  # inactive, active, finalized
}


def start_new_conversation(file_name: str):
    """
    Start a BRAND NEW conversation for a new file.
    This is called AFTER the previous conversation has been finalized.
    
    Args:
        file_name (str): Name of the newly uploaded file
    """
    global conversation_state
    
    # Create new session
    session_id = f"{file_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    conversation_state = {
        "file_name": file_name,
        "conversation_history": [],
        "session_id": session_id,
        "start_time": datetime.datetime.now().isoformat(),
        "status": "active"
    }
    
    print(f"✨ NEW CONVERSATION STARTED")
    print(f"   File: {file_name}")
    print(f"   Session ID: {session_id}")
    print(f"   Status: ACTIVE")
    print(f"   History: EMPTY (fresh start)")


def finalize_conversation(file_name: str) -> str:
    """
    Gracefully finalize the current conversation with Gemini.
    Creates a summary and properly closes the session.
    
    Args:
        file_name (str): Name of the file being finalized
        
    Returns:
        str: Summary message of the finalized conversation
    """
    global conversation_state
    
    if conversation_state["status"] != "active":
        print("ℹ️  No active conversation to finalize")
        return "No active conversation"
    
    history_count = len(conversation_state["conversation_history"])
    duration = "unknown"
    
    if conversation_state.get("start_time"):
        start = datetime.datetime.fromisoformat(conversation_state["start_time"])
        end = datetime.datetime.now()
        duration_seconds = (end - start).total_seconds()
        duration = f"{int(duration_seconds // 60)} minutes"
    
    # Create finalization summary
    summary = {
        "file_name": file_name,
        "session_id": conversation_state["session_id"],
        "total_exchanges": history_count,
        "duration": duration,
        "status": "finalized",
        "finalized_at": datetime.datetime.now().isoformat()
    }
    
    # Optional: Generate AI summary of the conversation
    if history_count > 0:
        try:
            summary_prompt = f"""This conversation about {file_name} is ending. 
It had {history_count} exchanges over {duration}. 
Provide a brief 1-sentence summary of what was discussed."""
            
            response = client.models.generate_content(model=MODEL, contents=summary_prompt)
            summary["ai_summary"] = response.text.strip() if response.text else "Summary unavailable"
        except Exception as e:
            print(f"⚠️  Could not generate AI summary: {e}")
            summary["ai_summary"] = "Summary generation failed"
    else:
        summary["ai_summary"] = "No exchanges in this conversation"
    
    # Mark as finalized
    conversation_state["status"] = "finalized"
    
    print(f"🔚 CONVERSATION FINALIZED")
    print(f"   File: {file_name}")
    print(f"   Exchanges: {history_count}")
    print(f"   Duration: {duration}")
    print(f"   Summary: {summary['ai_summary']}")
    
    return summary


def query_portfolio(user_query: str, top_k: int = TOP_K, is_new_session: bool = False) -> str:
    """
    Query portfolio using RAG with conversation management.
    
    - Each file has its own isolated conversation
    - History is ONLY from current active session
    - When new file uploaded, previous conversation is finalized first
    
    Args:
        user_query (str): User question
        top_k (int): Number of chunks to retrieve
        is_new_session (bool): True if this is first query after new file upload
        
    Returns:
        str: AI-generated answer
    """
    global conversation_state
    
    # Ensure we have an active session
    if conversation_state["status"] != "active":
        print("⚠️  No active session - cannot process query")
        return "Error: No active conversation session. Please upload a file first."
    
    # Log session info for new sessions
    if is_new_session:
        print(f"\n🆕 FIRST QUERY OF NEW SESSION")
        print(f"   File: {conversation_state['file_name']}")
        print(f"   Session: {conversation_state['session_id']}")
        print(f"   History: {len(conversation_state['conversation_history'])} exchanges")
    
    # Retrieve relevant chunks from CURRENT file
    chunks = retrieve(user_query, top_k)
    if not chunks:
        return "No relevant information found in the portfolio."

    # Convert chunks to strings
    string_chunks = [c[0] if isinstance(c, tuple) else c for c in chunks]

    # Build prompt with CURRENT session history ONLY
    prompt = build_contextual_prompt(
        user_query, 
        string_chunks, 
        conversation_state["conversation_history"],
        conversation_state["file_name"]
    )

    # Generate response
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        answer = response.text.strip() if response.text else "No response generated."
        
        # Store in CURRENT session history
        conversation_state["conversation_history"].append({
            "user": user_query,
            "assistant": answer,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Manage context window - keep last 10 exchanges
        if len(conversation_state["conversation_history"]) > 10:
            conversation_state["conversation_history"] = \
                conversation_state["conversation_history"][-10:]
        
        exchange_num = len(conversation_state["conversation_history"])
        print(f"💬 Exchange #{exchange_num} recorded in current session")

        return create_professional_summary(answer)

    except Exception as e:
        print(f"❌ Error generating response: {e}")
        return f"Error generating response: {e}"


def build_contextual_prompt(user_query: str, chunks: list, history: list, file_name: str) -> str:
    """
    Build prompt with conversation context from CURRENT session only.
    
    Args:
        user_query (str): Current question
        chunks (list): Retrieved chunks from current file
        history (list): History from CURRENT session ONLY
        file_name (str): Current file name for context
        
    Returns:
        str: Formatted prompt
    """
    # Base prompt from existing function
    base_prompt = build_prompt(user_query, chunks)
    
    # Add session context if history exists
    if history and len(history) > 0:
        context = f"\n\n=== Conversation Context (Current File: {file_name}) ===\n"
        context += f"This is an ongoing conversation about {file_name}.\n"
        context += f"Previous exchanges in THIS session:\n\n"
        
        # Include last 5 exchanges
        for idx, exchange in enumerate(history[-5:], 1):
            context += f"Exchange {idx}:\n"
            context += f"User: {exchange['user']}\n"
            context += f"You: {exchange['assistant']}\n\n"
        
        context += f"=== Current Question ===\n"
        
        # Combine with base prompt
        enhanced_prompt = f"{base_prompt}\n{context}\nUser: {user_query}\n\nAnswer:"
        return enhanced_prompt
    
    return base_prompt


def get_session_status():
    """
    Get current session status and statistics
    
    Returns:
        dict: Session information
    """
    return {
        "file_name": conversation_state.get("file_name"),
        "session_id": conversation_state.get("session_id"),
        "status": conversation_state.get("status"),
        "exchanges": len(conversation_state.get("conversation_history", [])),
        "start_time": conversation_state.get("start_time"),
        "active": conversation_state.get("status") == "active"
    }


def get_conversation_summary():
    """
    Get a summary of the current conversation
    
    Returns:
        dict: Conversation summary
    """
    history = conversation_state.get("conversation_history", [])
    
    if not history:
        return {"message": "No conversation history"}
    
    topics = [ex["user"] for ex in history]
    
    return {
        "file_name": conversation_state.get("file_name"),
        "total_exchanges": len(history),
        "topics_discussed": topics,
        "session_status": conversation_state.get("status")
    }

