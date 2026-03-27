from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from . import database, services

# Cria a tabela no Supabase automaticamente ao ligar
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def task_process(sub_id: int, db: Session):
    sub = db.query(database.SBARSubmission).filter(database.SBARSubmission.id == sub_id).first()
    if sub:
        feedback = services.analyze_sbar(sub.situation, sub.background, sub.assessment, sub.recommendation)
        sub.ai_feedback = feedback
        db.commit()
        services.send_email(sub.student_email, feedback, sub.situation, sub.background, sub.assessment, sub.recommendation)

@app.post("/api/sbar")
def submit(sbar: database.SBARCreate, bg: BackgroundTasks, db: Session = Depends(database.get_db)):
    nova_sub = database.SBARSubmission(**sbar.model_dump())
    db.add(nova_sub)
    db.commit()
    db.refresh(nova_sub)
    bg.add_task(task_process, nova_sub.id, db)
    return {"message": "Enviado! Aguarde o feedback no e-mail."}

@app.get("/api/results")
def list_results(db: Session = Depends(database.get_db)):
    return db.query(database.SBARSubmission).all()

# Rotas para abrir as páginas HTML
@app.get("/")
def index(): return FileResponse("frontend/index.html")

@app.get("/dashboard")
def dash(): return FileResponse("frontend/results.html")

# Monta a pasta frontend para carregar CSS/JS se precisar
app.mount("/static", StaticFiles(directory="frontend"), name="static")