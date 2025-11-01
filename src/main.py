from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import hashlib
import datetime

from .convert import pdf_to_txt
from .embedding import main as embed_main
from .chat import query_portfolio, finalize_conversation, start_new_conversation
from .retrieval import _load_resources, reset_for_new_file, reload_resources
from .config import RESUME_PATH, INDEX_PATH

app = FastAPI(title="AI Portfolio Assistant")

# === Allow CORS for local frontend ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Track current session with file hash ===
current_session = {
    "file_name": None,
    "file_hash": None,
    "upload_timestamp": None,
    "conversation_active": False
}

# === Store finalized conversations history ===
conversation_archive = []


def get_file_hash(file_path: str) -> str:
    """Generate hash of file content to detect if it's truly a new file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def archive_old_conversation():
    """
    Archive the current conversation before starting a new one.
    Stores it in conversation_archive for potential future reference.
    """
    if current_session.get("conversation_active") and current_session.get("file_name"):
        archived_conv = {
            "file_name": current_session["file_name"],
            "file_hash": current_session["file_hash"],
            "start_time": current_session["upload_timestamp"],
            "end_time": datetime.datetime.now().isoformat(),
            "status": "finalized"
        }
        conversation_archive.append(archived_conv)
        print(f"📦 Archived conversation for: {current_session['file_name']}")
        print(f"📚 Total archived conversations: {len(conversation_archive)}")


# === On startup: load portfolio base knowledge ===
@app.on_event("startup")
async def startup_event():
    try:
        _load_resources()
        print("✅ Portfolio base data loaded.")
    except Exception as e:
        print(f"⚠️ Could not preload portfolio data: {e}")


@app.post("/chat")
async def chat_with_cv(
    message: str = Form(...), 
    file: UploadFile = File(None),
    format_type: str = Form("clean")  # Options: 'clean', 'html', 'structured'
):
    """
    Handles chat with conversation lifecycle management:
    
    When NEW file uploaded:
    1️⃣ FINALIZE current conversation with Gemini (graceful closure)
    2️⃣ Archive old conversation metadata
    3️⃣ Clean up old file data (FAISS, resume text)
    4️⃣ Process new file (convert, embed)
    5️⃣ START NEW conversation with Gemini (fresh session)
    6️⃣ Process first query with new context
    
    When SAME file:
    - Continue existing conversation with history
    """
    try:
        file_changed = False
        finalization_message = None
        
        if file:
            pdf_path = f"data/{file.filename}"
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

            # Save uploaded file
            with open(pdf_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            
            # Check if this is actually a NEW file
            new_file_hash = get_file_hash(pdf_path)
            
            if new_file_hash != current_session.get("file_hash"):
                file_changed = True
                print(f"\n{'='*60}")
                print(f"📄 NEW FILE DETECTED: {file.filename}")
                print(f"{'='*60}")
                
                # Step 1: FINALIZE the old conversation gracefully
                if current_session.get("conversation_active"):
                    old_file = current_session.get("file_name", "previous file")
                    print(f"🔚 Finalizing conversation for: {old_file}")
                    
                    finalization_summary = finalize_conversation(old_file)
                    finalization_message = finalization_summary
                    
                    # Archive the old conversation
                    archive_old_conversation()
                    
                    print(f"✅ Conversation finalized and archived")
                else:
                    print(f"ℹ️  No active conversation to finalize")
                
                # Step 2: RESET retrieval system (unload old index & chunks)
                print(f"\n🔄 Resetting retrieval system...")
                reset_for_new_file()
                
                # Step 3: Clean up old file data
                if os.path.exists(INDEX_PATH):
                    os.remove(INDEX_PATH)
                    print("🧹 Old FAISS index deleted")

                if os.path.exists(RESUME_PATH):
                    os.remove(RESUME_PATH)
                    print("🧹 Old resume text deleted")

                # Step 4: Process NEW file
                print(f"\n🔄 Processing new file: {file.filename}")
                pdf_to_txt(pdf_path, RESUME_PATH)
                embed_main()
                print("✅ New CV converted and indexed")
                if os.path.exists(pdf_path):
                 os.remove(pdf_path)   
                # Step 5: RELOAD retrieval resources with new file data
                print(f"\n📥 Loading new file data into retrieval system...")
                reload_resources()
                print("✅ New retrieval data loaded")

                # Step 6: START NEW conversation session
                print(f"\n✨ Starting NEW conversation for: {file.filename}")
                start_new_conversation(file.filename)
                
                # Step 7: Update session tracking
                current_session["file_name"] = file.filename
                current_session["file_hash"] = new_file_hash
                current_session["upload_timestamp"] = datetime.datetime.now().isoformat()
                current_session["conversation_active"] = True
                
                print(f"{'='*60}")
                print(f"✅ NEW SESSION READY")
                print(f"{'='*60}\n")
                
            else:
                print(f"ℹ️  Continuing conversation with: {file.filename}")

        # Query Gemini
        reply = query_portfolio(message, is_new_session=file_changed)
        
        # Build response
        response_data = {
            "reply": reply,
            "new_session": file_changed,
            "current_file": current_session.get("file_name")
        }
        
        # Include finalization message if there was one
        if finalization_message:
            response_data["previous_session_summary"] = finalization_message
            response_data["note"] = "Previous conversation has been finalized and archived"
        
        return JSONResponse(response_data)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/finalize")
async def finalize_current_conversation():
    """
    Manually finalize the current conversation without uploading a new file.
    Useful for explicitly ending a session.
    """
    try:
        if not current_session.get("conversation_active"):
            return JSONResponse({
                "message": "No active conversation to finalize",
                "status": "no_action"
            })
        
        file_name = current_session.get("file_name")
        summary = finalize_conversation(file_name)
        archive_old_conversation()
        
        current_session["conversation_active"] = False
        
        return JSONResponse({
            "message": f"Conversation finalized for: {file_name}",
            "summary": summary,
            "status": "finalized"
        })
    except Exception as e:
        print(f"❌ Error finalizing: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/session")
async def get_session():
    """
    Get current session information
    """
    return JSONResponse({
        "current_file": current_session.get("file_name"),
        "file_hash": current_session.get("file_hash"),
        "upload_timestamp": current_session.get("upload_timestamp"),
        "conversation_active": current_session.get("conversation_active", False),
        "has_active_session": current_session.get("file_name") is not None,
        "archived_conversations_count": len(conversation_archive)
    })


@app.get("/history")
async def get_conversation_history():
    """
    Get archive of all finalized conversations
    """
    return JSONResponse({
        "archived_conversations": conversation_archive,
        "total_count": len(conversation_archive)
    })


@app.get("/diagnostics")
async def get_diagnostics():
    """
    Get comprehensive system diagnostics including retrieval stats
    """
    from .retrieval import get_retrieval_stats
    from .chat import get_session_status
    
    retrieval_stats = get_retrieval_stats()
    chat_status = get_session_status()
    
    return JSONResponse({
        "session": {
            "current_file": current_session.get("file_name"),
            "file_hash": current_session.get("file_hash"),
            "conversation_active": current_session.get("conversation_active"),
            "upload_timestamp": current_session.get("upload_timestamp")
        },
        "chat_state": chat_status,
        "retrieval_system": retrieval_stats,
        "archives": {
            "total_finalized_conversations": len(conversation_archive)
        },
        "files": {
            "index_exists": os.path.exists(INDEX_PATH),
            "resume_exists": os.path.exists(RESUME_PATH)
        }
    })


@app.get("/history")
async def get_conversation_history():
    """
    Get archive of all finalized conversations
    """
    return JSONResponse({
        "archived_conversations": conversation_archive,
        "total_count": len(conversation_archive)
    })


@app.post("/clear-all")
async def clear_all():
    """
    Clear everything including archives
    """
    try:
        if current_session.get("conversation_active"):
            finalize_conversation(current_session.get("file_name"))
            archive_old_conversation()
        
        current_session["file_name"] = None
        current_session["file_hash"] = None
        current_session["upload_timestamp"] = None
        current_session["conversation_active"] = False
        
        # Optionally clear archives
        # conversation_archive.clear()
        
        print("🧹 All sessions cleared")
        
        return JSONResponse({
            "message": "All sessions cleared successfully",
            "archived_count": len(conversation_archive)
        })
    except Exception as e:
        print(f"❌ Error clearing: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

