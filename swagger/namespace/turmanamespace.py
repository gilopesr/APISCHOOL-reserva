from flask_restx import Namespace, Resource, fields
from turma.modelTurmas import Turma,TurmaNaoEncontrada,turma_por_id, getTurma, apaga_tudo, createTurma, deleteTurma, atualizarTurma, atualizarParcialTurma

turma_ns = Namespace("turma", description="Dados relacionados as tumas")

turma_model = turma_ns.model("Turma", {
    "nome": fields.String(required=True, description="Nome da turma"),
    "professor": fields.String(required=True, description="Professor Responsavel")
})

turma_output_model = turma_ns.model("turmaOutput", {
    "id": fields.Integer(description="ID da turma"),
    "nome": fields.String(description="Nome da turma"),
    "professor": fields.String(required=True, description="Professor Responsavel")
})

@turma_ns.route("/")
class TurmaResource(Resource):
    @turma_ns.marshal_list_with(turma_output_model)
    def get(self):
        """Lista todas as turmas"""
        return getTurma()

    @turma_ns.expect(turma_model)
    def post(self):
        """Cria uma nova turma"""
        data = turma_ns.payload
        response, status_code = createTurma(data)
        return response, status_code

@turma_ns.route("/<int:id_turma>")
class TurmaIdResource(Resource):
    @turma_ns.marshal_with(turma_output_model)
    def get(self, id_turma):
        """Obtém uma turma por ID"""
        return turma_por_id(id_turma)

    @turma_ns.expect(turma_model)
    def put(self, id_turma):
        """Atualiza uma turma por ID"""
        data = turma_ns.payload
        atualizarParcialTurma(id_turma, data)
        return data, 200

    def delete(self, id_turma):
        """Exclui uma turma por ID"""
        deleteTurma(id_turma)
        return {"message": "turma excluída com sucesso"}, 200