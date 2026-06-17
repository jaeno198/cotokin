"""
Utilitário para corrigir senhas em texto puro no banco.

Uso:
  python fix_senhas.py                     # lista usuários com senha inválida
  python fix_senhas.py <email> <nova_senha> # redefine a senha de um usuário
"""
import sys
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from config import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
engine = create_engine(settings.database_url)


def is_hash_valido(h: str) -> bool:
    try:
        pwd.identify(h)
        return True
    except Exception:
        return False


def listar_invalidos():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, nome, email, hashed_password FROM usuarios")).fetchall()

    print(f"{'ID':<5} {'Email':<35} {'Status'}")
    print("-" * 60)
    for r in rows:
        status = "OK (bcrypt)" if is_hash_valido(r[3]) else "INVALIDO (texto puro ou outro formato)"
        print(f"{r[0]:<5} {r[2]:<35} {status}")


def redefinir_senha(email: str, nova_senha: str):
    novo_hash = pwd.hash(nova_senha)
    with engine.connect() as conn:
        result = conn.execute(
            text("UPDATE usuarios SET hashed_password = :h WHERE email = :e"),
            {"h": novo_hash, "e": email},
        )
        conn.commit()
        if result.rowcount == 0:
            print(f"Usuário '{email}' não encontrado.")
        else:
            print(f"Senha de '{email}' atualizada com sucesso.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        listar_invalidos()
    elif len(sys.argv) == 3:
        redefinir_senha(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python fix_senhas.py [email nova_senha]")
