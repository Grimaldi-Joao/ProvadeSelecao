from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/test_db")

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    cnpj = Column(String, unique=True, nullable=False, index=True)
    endereco = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    
    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa", cascade="all, delete-orphan")

class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    periodicidade = Column(String, nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    
    empresa = relationship("Empresa", back_populates="obrigacoes")

# Criar conexão com banco
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar tabelas com Alembic
Base.metadata.create_all(bind=engine)
