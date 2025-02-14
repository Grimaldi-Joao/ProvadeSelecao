from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str  # mensal, trimestral, anual

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    empresa_id: int

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa_id: int

    class Config:
        from_attributes = True

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int
    obrigacoes: List[ObrigacaoAcessoria] = []

    class Config:
        from_attributes = True
