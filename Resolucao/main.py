from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestão de Empresas e Obrigações Acessórias", description="API para gerenciar empresas e obrigações fiscais", version="1.0")

# Endpoints para Empresa
@app.post("/empresas/", response_model=schemas.Empresa, summary="Criar nova empresa")
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = models.Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=List[schemas.Empresa], summary="Listar todas as empresas")
def read_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Empresa).offset(skip).limit(limit).all()

@app.get("/empresas/{empresa_id}", response_model=schemas.Empresa, summary="Obter detalhes de uma empresa")
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

@app.put("/empresas/{empresa_id}", response_model=schemas.Empresa, summary="Atualizar dados de uma empresa")
def update_empresa(empresa_id: int, empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    for key, value in empresa.dict().items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.delete("/empresas/{empresa_id}", summary="Deletar uma empresa")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    db.delete(empresa)
    db.commit()
    return {"detail": "Empresa deletada com sucesso"}

# Endpoints para ObrigacaoAcessoria
@app.post("/obrigacoes/", response_model=schemas.ObrigacaoAcessoria, summary="Criar nova obrigação acessória")
def create_obrigacao(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.dict())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/", response_model=List[schemas.ObrigacaoAcessoria], summary="Listar todas as obrigações acessórias")
def read_obrigacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ObrigacaoAcessoria).offset(skip).limit(limit).all()

@app.get("/obrigacoes/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria, summary="Obter detalhes de uma obrigação acessória")
def read_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    return obrigacao

@app.delete("/obrigacoes/{obrigacao_id}", summary="Deletar uma obrigação acessória")
def delete_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    
    db.delete(obrigacao)
    db.commit()
    return {"detail": "Obrigação deletada com sucesso"}
