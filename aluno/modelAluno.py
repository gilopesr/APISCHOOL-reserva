# dici = {
#     "alunos":[
#         {"id":1,"nome":"Joao"},
#         {"id":2,"nome":"Maria"},
#         {"id":3,"nome":"Pedro"}
#     ] 
# }

from config import db

class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))


    turma = db.relationship("Turma", back_populates="alunos")
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome}
    

class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise  AlunoNaoEncontrado("Aluno não encontrado")
    return aluno.to_dict()

def get_alunos():
    alunos = Aluno.query.all()
    print(alunos)
    return [aluno.to_dict() for aluno in alunos]


def apaga_tudo():
    try:
        db.session.query(Aluno).delete()
        db.session.commit()
        return "message: Banco de dados resetado"
    except Exception as e:
        db.session.rollback()
        return f"Erro ao resetar o banco de dados: {e}"


def create_aluno(id, nome):
    if not id or not nome:
        return {'erro': 'Parâmetro obrigatório ausente'}

    if not isinstance(id, int) or id <= 0:
        return {'erro': 'O id deve ser um número inteiro'}

    if not isinstance(nome, str):
        return {'erro': 'O nome deve ser uma string'}

    aluno_existente = Aluno.query.get(id)
    if aluno_existente:
        return {'erro': 'id ja utilizada'}

    novo_aluno = Aluno(id=id, nome=nome)
    db.session.add(novo_aluno)
    db.session.commit()

    return novo_aluno.to_dict()


def atualizarAluno(id_aluno, nome=None, body_id=None):
    try:
        aluno_encontrado = Aluno.query.get(id_aluno)
        if aluno_encontrado is None:
            raise AlunoNaoEncontrado("Aluno não encontrado")

        if nome is None:
            if body_id is None or body_id == id_aluno:
                return 'erro: aluno sem nome', None

        if nome is not None and not isinstance(nome, str):
            return 'erro: O nome deve ser uma string', None

        if body_id is not None and not isinstance(body_id, int):
            return 'erro: O id deve ser um número inteiro', None
        
        if body_id != id_aluno:
                aluno_com_id_conflict = Aluno.query.get(body_id)
                if aluno_com_id_conflict:
                    return 'erro: ID de aluno já existe'
                aluno_encontrado.id = body_id
        if nome:
            aluno_encontrado.nome = nome
        db.session.commit()

        return "mensagem: aluno atualizado com sucesso", aluno_encontrado.to_dict()
    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None
    
def atualizarParcialAluno(id_aluno,dados):
    try:
        aluno_encontrado = Aluno.query.get(id_aluno)
        if aluno_encontrado is None:
            raise AlunoNaoEncontrado("Aluno não encontrado")

        for chave, valor in dados.items():
            if hasattr(aluno_encontrado, chave):
                setattr(aluno_encontrado, chave, valor)

        db.session.commit()
        return "mensagem: Turma atualizada com sucesso", aluno_encontrado.to_dict()

    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None
    
def deleteAluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado("Aluno não encontrado")
    db.session.delete(aluno)
    db.session.commit()
    return 'mensagem: Aluno deletado com sucesso', aluno
    
