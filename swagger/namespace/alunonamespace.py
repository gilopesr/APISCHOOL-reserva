from flask_restx import Namespace, Resource, fields
from aluno.modelAluno import AlunoNaoEncontrado, aluno_por_id, get_alunos, create_aluno, apaga_tudo, atualizarAluno, atualizarParcialAluno, deleteAluno

alunos_ns = Namespace("alunos", description="Dados relacionados aos alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno")
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(description="Nome do aluno")
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return get_alunos()

    @alunos_ns.expect(aluno_model)
    def post(self):
        """Cria um novo aluno"""
        data = alunos_ns.payload
        response, status_code = create_aluno(data)
        return response, status_code

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        return aluno_por_id(id_aluno)

    @alunos_ns.expect(aluno_model)
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        data = alunos_ns.payload
        atualizarParcialAluno(id_aluno, data)
        return data, 200

    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        deleteAluno(id_aluno)
        return {"message": "Aluno excluído com sucesso"}, 200