# api/admin_api.py
from fastapi import APIRouter, HTTPException,Depends
from app.schemas.node_prompt import UpdatePromptRequest, PromptResponse
from app.crud.edit_prompt import get_db_prompt, upsert_db_prompt, delete_db_prompt
from app.config.prompt import DEFAULT_PROMPTS
from app.api.auth import admin_required
router = APIRouter(prefix="/admin", tags=["Prompt Chatbot"])

@router.get("/get-prompt/{node_id}", response_model=PromptResponse)
def read_prompt(node_id: str,current_admin: dict = Depends(admin_required)):
    #เช็ค jwt ด้วย
    db_data = get_db_prompt(node_id)
    
    if db_data:
        return {"node_id": node_id, "messages": db_data["messages"]}
    
    default = DEFAULT_PROMPTS.get(node_id)
    if not default:
        raise HTTPException(status_code=404, detail="Node prompt not found")
    
    return {
        "node_id": node_id, 
        "messages": [
            {"role": "system", "content": default["system"]},
            {"role": "human", "content": default["human"]}
        ]
    }

@router.post("/update-prompt")
def update_prompt(payload: UpdatePromptRequest,current_admin: dict = Depends(admin_required)):

    data = payload.model_dump()
    upsert_db_prompt(data)
    return {"status": "success", "message": "บันทึกสำเร็จ"}

@router.get("/reset-prompt/{node_id}")
def reset_prompt(node_id: str,current_admin: dict = Depends(admin_required)):

    delete_db_prompt(node_id)
    
    default = DEFAULT_PROMPTS.get(node_id) #ใช้promptค่าเริ่มต้น
    if not default:
        raise HTTPException(status_code=404, detail="Default prompt not found")
        
    return {
        "system": default["system"],
        "human": default["human"]
    }