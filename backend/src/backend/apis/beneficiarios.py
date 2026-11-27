from fastapi import APIRouter, HTTPException
from backend.database import get_conn
from backend.models import BeneficiarioIn, BeneficiarioOut

router = APIRouter(prefix="/beneficiarios", tags=["Beneficiarios"])


def _row(row) -> BeneficiarioOut:
    return BeneficiarioOut(**dict(row))


@router.get("", response_model=list[BeneficiarioOut])
def listar():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM beneficiarios ORDER BY nom").fetchall()
    return [_row(r) for r in rows]


@router.post("", response_model=BeneficiarioOut, status_code=201)
def crear(b: BeneficiarioIn):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO beneficiarios (nom,dni,dir,nac,mail,est) VALUES (?,?,?,?,?,?)",
            (b.nom, b.dni, b.dir, b.nac, b.mail, b.est),
        )
        row = conn.execute("SELECT * FROM beneficiarios WHERE id=?", (cur.lastrowid,)).fetchone()
    return _row(row)


@router.put("/{id}", response_model=BeneficiarioOut)
def actualizar(id: int, b: BeneficiarioIn):
    with get_conn() as conn:
        conn.execute(
            "UPDATE beneficiarios SET nom=?,dni=?,dir=?,nac=?,mail=?,est=? WHERE id=?",
            (b.nom, b.dni, b.dir, b.nac, b.mail, b.est, id),
        )
        row = conn.execute("SELECT * FROM beneficiarios WHERE id=?", (id,)).fetchone()
    if not row:
        raise HTTPException(404, "Beneficiario no encontrado")
    return _row(row)


@router.delete("/{id}", status_code=204)
def eliminar(id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM beneficiarios WHERE id=?", (id,))
