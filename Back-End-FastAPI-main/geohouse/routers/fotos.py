from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil, os, uuid
 
from config import settings
from database import get_db
from models import FotoImovel, Imovel
from schemas.foto import FotoCreate, FotoRead, FotoUpdate

router = APIRouter(prefix="/imoveis/{imovel_id}/fotos", tags=["Fotos"])

UPLOAD_DIR = settings.upload_dir
 
 
# ──────────────────────────────────────────────
# Helper: valida imóvel
# ──────────────────────────────────────────────
 
def _get_imovel_or_404(imovel_id: int, db: Session) -> Imovel:
    imovel = db.get(Imovel, imovel_id)
    if not imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imóvel {imovel_id} não encontrado",
        )
    return imovel
 
 
# ──────────────────────────────────────────────
# GET /imoveis/{imovel_id}/fotos — lista fotos do imóvel
# ──────────────────────────────────────────────
 
@router.get(
    "/",
    response_model=List[FotoRead],
    summary="Lista todas as fotos de um imóvel",
)
def listar_fotos(imovel_id: int, db: Session = Depends(get_db)):
    """Endpoint público — retorna fotos ordenadas pelo campo `ordem`."""
    _get_imovel_or_404(imovel_id, db)
    return (
        db.query(FotoImovel)
        .filter(FotoImovel.imovel_id == imovel_id)
        .order_by(FotoImovel.ordem)
        .all()
    )
 
 
# ──────────────────────────────────────────────
# POST /imoveis/{imovel_id}/fotos/upload — faz upload de arquivo
# ──────────────────────────────────────────────
 
@router.post(
    "/upload",
    response_model=FotoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Faz upload de uma foto para o imóvel (Administrador/Corretor)",
)
def upload_foto(
    imovel_id: int,
    file:      UploadFile = File(..., description="Arquivo de imagem (jpg, png, webp)"),
    descricao: Optional[str] = Form(None),
    ordem:     int           = Form(0),
    capa:      bool          = Form(False),
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    """
    Salva o arquivo em disco (ou substitua por S3/GCS)
    e registra a URL no banco vinculada ao imóvel.
    """
    _get_imovel_or_404(imovel_id, db)
 
    # Valida extensão
    extensoes_permitidas = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in extensoes_permitidas:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato inválido. Use JPG, PNG ou WEBP.",
        )
 
    # Gera nome único e salva
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = file.filename.rsplit(".", 1)[-1]
    nome_arquivo = f"{uuid.uuid4().hex}.{ext}"
    caminho = os.path.join(UPLOAD_DIR, nome_arquivo)
 
    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
 
    url = f"/{UPLOAD_DIR}/{nome_arquivo}"  # troque pela URL pública do seu storage
 
    # Se marcada como capa, desmarca as demais
    if capa:
        db.query(FotoImovel).filter(FotoImovel.imovel_id == imovel_id).update({"capa": False})
 
    foto = FotoImovel(
        imovel_id=imovel_id,
        url=url,
        descricao=descricao,
        ordem=ordem,
        capa=capa,
    )
    db.add(foto)
    db.commit()
    db.refresh(foto)
    return foto
 
 
# ──────────────────────────────────────────────
# POST /imoveis/{imovel_id}/fotos — vincula URL externa
# ──────────────────────────────────────────────
 
@router.post(
    "/",
    response_model=FotoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Vincula uma URL de foto já hospedada ao imóvel (Administrador/Corretor)",
)
def criar_foto_por_url(
    imovel_id: int,
    payload: FotoCreate,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    """Útil quando as imagens já estão em um CDN ou storage externo."""
    _get_imovel_or_404(imovel_id, db)
 
    if payload.capa:
        db.query(FotoImovel).filter(FotoImovel.imovel_id == imovel_id).update({"capa": False})
 
    foto = FotoImovel(
        imovel_id=imovel_id,
        url=payload.url,
        descricao=payload.descricao,
        ordem=payload.ordem,
        capa=payload.capa,
    )
    db.add(foto)
    db.commit()
    db.refresh(foto)
    return foto
 
 
# ──────────────────────────────────────────────
# PATCH /imoveis/{imovel_id}/fotos/{foto_id} — atualiza ordem/capa
# ──────────────────────────────────────────────
 
@router.patch(
    "/{foto_id}",
    response_model=FotoRead,
    summary="Atualiza descrição, ordem ou capa de uma foto (Administrador/Corretor)",
)
def atualizar_foto(
    imovel_id: int,
    foto_id:   int,
    payload:   FotoUpdate,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    foto = db.query(FotoImovel).filter(
        FotoImovel.id == foto_id,
        FotoImovel.imovel_id == imovel_id,
    ).first()
 
    if not foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Foto {foto_id} não encontrada para o imóvel {imovel_id}",
        )
 
    # Se está redefinindo a capa, desmarca as outras antes
    if payload.capa:
        db.query(FotoImovel).filter(FotoImovel.imovel_id == imovel_id).update({"capa": False})
 
    dados = payload.model_dump(exclude_unset=True)
    for campo, valor in dados.items():
        setattr(foto, campo, valor)
 
    db.commit()
    db.refresh(foto)
    return foto
 
 
# ──────────────────────────────────────────────
# DELETE /imoveis/{imovel_id}/fotos/{foto_id} — remove
# ──────────────────────────────────────────────
 
@router.delete(
    "/{foto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove uma foto do imóvel (Administrador/Corretor)",
)
def deletar_foto(
    imovel_id: int,
    foto_id:   int,
    db: Session = Depends(get_db),
    # _: Usuario = Depends(require_role("Administrador", "Corretor")),
):
    foto = db.query(FotoImovel).filter(
        FotoImovel.id == foto_id,
        FotoImovel.imovel_id == imovel_id,
    ).first()
 
    if not foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Foto {foto_id} não encontrada para o imóvel {imovel_id}",
        )
 
    # Remove arquivo local se existir
    if foto.url.startswith(f"/{UPLOAD_DIR}/") or foto.url.startswith("/uploads/fotos/"):
        caminho = foto.url.lstrip("/")
        if os.path.exists(caminho):
            os.remove(caminho)
 
    db.delete(foto)
