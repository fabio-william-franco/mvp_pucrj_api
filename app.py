from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError


from model import Session, Trabalhador, Tarefa, Custo, Atribuicao, Especialidade, TrabalhadorEspecialidade
from services import process_assignments
from logger import logger
from schemas import *
from flask_cors import CORS



info = Info(title="API de Atribuição", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
trabalhador_tag = Tag(name="Trabalhador", description="Gerenciamento de trabalhadores")
tarefa_tag = Tag(name="Tarefa", description="Gerenciamento de tarefas")
custo_tag = Tag(name="Custo", description="Gerenciamento de custos")
atribuicao_tag = Tag(name="Atribuição", description="Gerenciamento de atribuições")
especialidade_tag = Tag(name="Especialidade", description="Gerenciamento de especialidades")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

# Endpoints para Especialidade
@app.post('/especialidade', tags=[especialidade_tag],
          responses={"200": EspecialidadeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_especialidade(form: EspecialidadeSchema):
    """Adiciona uma nova Especialidade."""
    especialidade = Especialidade(nome=form.nome)
    logger.debug(f"Adicionando especialidade: '{especialidade.nome}'")
    try:
        session = Session()
        session.add(especialidade)
        session.commit()
        return {"id": especialidade.id, "nome": especialidade.nome}, 200
    except IntegrityError:
        error_msg = "Especialidade já cadastrada."
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Erro ao cadastrar especialidade."
        logger.error(f"Erro: {e}")
        return {"message": error_msg}, 400
    
@app.put('/especialidade/edit', tags=[especialidade_tag],
         responses={"200": EspecialidadeViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def edit_especialidade(form: EspecialidadeSchema):
    """Edita o nome de uma especialidade existente."""
    session = Session()
    try:
        especialidade = session.query(Especialidade).filter_by(id=form.id).first()
        if not especialidade:
            return {"message": "Especialidade não encontrada."}, 404
        
        especialidade.nome = form.nome  
        session.commit()
        return {"id": especialidade.id, "nome": especialidade.nome}, 200
    except Exception as e:
        session.rollback()
        error_msg = "Erro ao editar especialidade."
        logger.error(f"Erro: {e}")
        return {"message": error_msg}, 400



@app.get('/especialidades', tags=[especialidade_tag],
         responses={"200": ListagemEspecialidadesSchema, "404": ErrorSchema})
def get_especialidades():
    """Lista todas as Especialidades cadastradas."""
    logger.debug("Coletando especialidades")
    session = Session()
    especialidades = session.query(Especialidade).all()
    if not especialidades:
        return {"especialidades": []}, 200

    return {
        "especialidades": [{"id": e.id, "nome": e.nome} for e in especialidades]
    }, 200



@app.post('/trabalhador', tags=[trabalhador_tag],
          responses={"200": TrabalhadorViewSchema, "422": ErrorSchema})
def add_trabalhador(form: TrabalhadorSchema):
    """
    Adiciona um novo Trabalhador com especialidades associadas.
    """
    session = Session()
    try:
        
        nome = form.nome
        especialidades_nomes = form.especialidades_nomes

        
        trabalhador = Trabalhador(nome=nome)
        session.add(trabalhador)
        session.flush()  

       
        for especialidade_nome in especialidades_nomes:
            
            especialidade = session.query(Especialidade).filter_by(nome=especialidade_nome).first()
            if not especialidade:
                especialidade = Especialidade(nome=especialidade_nome)
                session.add(especialidade)
                session.flush()

            
            trabalhador_especialidade = TrabalhadorEspecialidade(
                trabalhador_id=trabalhador.id,
                especialidade_id=especialidade.id
            )
            session.add(trabalhador_especialidade)

        session.commit()

        
        return {
            "id": trabalhador.id,
            "nome": trabalhador.nome,
            "especialidades": [{"id": te.especialidade.id, "nome": te.especialidade.nome}
                               for te in trabalhador.especialidades]
        }, 200

    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao cadastrar trabalhador: {e}")
        return {"message": "Erro ao cadastrar trabalhador."}, 500



@app.get('/trabalhadores', tags=[trabalhador_tag],
         responses={"200": ListagemTrabalhadoresSchema, "404": ErrorSchema})
def get_trabalhadores():
    """Lista todos os Trabalhadores com suas Especialidades pelo nome."""
    logger.debug("Coletando trabalhadores")
    session = Session()

    
    trabalhadores = session.query(Trabalhador).all()

    
    if not trabalhadores:
        return {"trabalhadores": []}, 200

    
    result = []
    for trabalhador in trabalhadores:
        
        especialidades = [
            {"id": te.especialidade.id, "nome": te.especialidade.nome}
            for te in trabalhador.especialidades
        ]
        
        result.append({
            "id": trabalhador.id,
            "nome": trabalhador.nome,
            "especialidades": especialidades
        })

    return {"trabalhadores": result}, 200


@app.delete('/trabalhador', tags=[trabalhador_tag],
            responses={"200": TrabalhadorDelSchema, "404": ErrorSchema})
def del_trabalhador(query: TrabalhadorBuscaSchema):
    """Deleta um Trabalhador pelo nome informado."""
    trabalhador_nome = unquote(query.nome)
    logger.debug(f"Deletando trabalhador: {trabalhador_nome}")
    session = Session()
    count = session.query(Trabalhador).filter(Trabalhador.nome == trabalhador_nome).delete()
    session.commit()
    if count:
        return {"message": "Trabalhador removido", "nome": trabalhador_nome}, 200
    else:
        error_msg = "Trabalhador não encontrado."
        return {"message": error_msg}, 404
    

@app.put('/trabalhador/edit', tags=[trabalhador_tag],
         responses={"200": TrabalhadorViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def edit_trabalhador(form: TrabalhadorSchema):
    """Edita o nome e as especialidades de um trabalhador existente."""
    session = Session()
    try:
        
        trabalhador = session.query(Trabalhador).filter_by(id=form.id).first()
        if not trabalhador:
            return {"message": "Trabalhador não encontrado."}, 404

       
        trabalhador.nome = form.nome

        
        especialidades_validas = session.query(Especialidade.id).filter(Especialidade.id.in_(form.especialidades_ids)).all()
        especialidades_validas_ids = [e.id for e in especialidades_validas]

        
        ids_invalidos = set(form.especialidades_ids) - set(especialidades_validas_ids)
        if ids_invalidos:
            return {"message": f"IDs de especialidades inválidos: {list(ids_invalidos)}"}, 400

       
        trabalhador.especialidades.clear()
        for especialidade_id in especialidades_validas_ids:
            trabalhador_especialidade = TrabalhadorEspecialidade(
                trabalhador_id=trabalhador.id,
                especialidade_id=especialidade_id
            )
            session.add(trabalhador_especialidade)

        session.commit()
        return {
            "id": trabalhador.id,
            "nome": trabalhador.nome,
            "especialidades": [{"id": e.especialidade.id, "nome": e.especialidade.nome} for e in trabalhador.especialidades]
        }, 200
    except Exception as e:
        session.rollback()
        error_msg = "Erro ao editar trabalhador."
        logger.error(f"Erro: {e}")
        return {"message": error_msg}, 400



@app.post('/tarefa', tags=[tarefa_tag],
          responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tarefa(form: TarefaSchema):
    """Adiciona uma nova Tarefa à base de dados."""
    
    tarefa = Tarefa(nome=form.nome, especialidade_id=form.especialidade_id)
    logger.debug(f"Adicionando tarefa: '{tarefa.nome}'")

    try:
        
        session = Session()
        session.add(tarefa)
        session.commit()

        
        especialidade = session.query(Especialidade).filter_by(id=form.especialidade_id).first()
        if not especialidade:
            return {"message": "Especialidade não encontrada."}, 400

        logger.debug(f"Tarefa adicionada: '{tarefa.nome}'")
        
        return {
            "id": tarefa.id,
            "nome": tarefa.nome,
            "especialidade": {
                "id": especialidade.id,
                "nome": especialidade.nome
            }
        }, 200

    except IntegrityError:
        
        error_msg = "Tarefa de mesmo nome já existe."
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.nome}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        
        error_msg = "Erro ao salvar nova tarefa."
        logger.error(f"Erro ao adicionar tarefa '{tarefa.nome}': {e}")
        return {"message": error_msg}, 400


@app.delete('/tarefa', tags=[tarefa_tag],
            responses={"200": TarefaDelSchema, "404": ErrorSchema})
def del_tarefa(query: TarefaBuscaSchema):
    """Deleta uma Tarefa pelo nome informado."""
    tarefa_nome = unquote(query.nome)
    logger.debug(f"Deletando tarefa: {tarefa_nome}")
    session = Session()
    count = session.query(Tarefa).filter(Tarefa.nome == tarefa_nome).delete()
    session.commit()
    if count:
        return {"message": "Tarefa removida", "nome": tarefa_nome}, 200
    else:
        error_msg = "Tarefa não encontrada."
        return {"message": error_msg}, 404


@app.get('/tarefas', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas():
    """Lista todas as Tarefas cadastradas."""
    logger.debug("Coletando tarefas")
    session = Session()
    tarefas = session.query(Tarefa).all()
    if not tarefas:
        return {"tarefas": []}, 200
    return apresenta_tarefas(tarefas), 200


# Endpoints para Custo
@app.post('/custo', tags=[custo_tag],
          responses={"200": CustoViewSchema, "400": ErrorSchema})
def add_custo(form: CustoSchema):
    """
    Adiciona um novo custo à base de dados.
    """
    session = Session()
    try:
        
        custo = Custo(
            trabalhador_id=form.trabalhador_id,
            tarefa_id=form.tarefa_id,
            custo=form.custo
        )
        session.add(custo)
        session.commit()

       
        trabalhador = session.query(Trabalhador).filter_by(id=form.trabalhador_id).first()
        tarefa = session.query(Tarefa).filter_by(id=form.tarefa_id).first()

        
        return {
            "id": custo.id,
            "trabalhador": trabalhador.nome if trabalhador else "Desconhecido",
            "tarefa": tarefa.nome if tarefa else "Desconhecida",
            "custo": custo.custo
        }, 200

    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao adicionar custo: {e}")
        return {"message": "Erro ao salvar novo custo."}, 400



@app.delete('/custo', tags=[custo_tag],
            responses={"200": CustoDelSchema, "404": ErrorSchema})
def del_custo(query: CustoIdSchema):
    """
    Deleta um Custo pelo id.
    """
    session = Session()

    try:
        # Buscar o custo a ser deletado pelo ID
        custo = session.query(Custo).filter(Custo.id == query.id).first()

        if custo:
            session.delete(custo)
            session.commit()
            return {
                "message": "Custo removido com sucesso.",
                "id": custo.id
            }, 200
        else:
            return {"message": "Custo não encontrado."}, 404
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao deletar custo: {e}")
        return {"message": "Erro ao deletar custo."}, 400



@app.get('/custos', tags=[custo_tag],
         responses={"200": ListagemCustosSchema, "404": ErrorSchema})
def get_custos():
    """
    Lista todos os custos cadastrados com descrições detalhadas.
    """
    logger.debug("Coletando custos")
    session = Session()
    custos = session.query(Custo).all()

    if not custos:
        return {"custos": []}, 200

    
    result = []
    for custo in custos:
        trabalhador = session.query(Trabalhador).filter_by(id=custo.trabalhador_id).first()
        tarefa = session.query(Tarefa).filter_by(id=custo.tarefa_id).first()
        result.append({
            "id": custo.id,
            "trabalhador": trabalhador.nome if trabalhador else "Desconhecido",
            "tarefa": tarefa.nome if tarefa else "Desconhecida",
            "custo": custo.custo
        })

    return {"custos": result}, 200



# Endpoints para Atribuição
@app.post('/atribuicao', tags=[atribuicao_tag],
          responses={"200": AtribuicaoViewSchema, "400": ErrorSchema})
def add_atribuicao(form: AtribuicaoSchema):
    """Adiciona uma nova atribuição à base de dados."""
    atribuicao = Atribuicao(custo_id=form.custo_id)
    logger.debug(f"Adicionando atribuicao com custo_id: {form.custo_id}")
    try:
        session = Session()
        session.add(atribuicao)
        session.commit()
        logger.debug("Adicionada atribuição com sucesso")
        return {"id": atribuicao.id, "custo_id": atribuicao.custo_id, "data_insercao": atribuicao.data_insercao}, 200
    except Exception as e:
        error_msg = "Erro ao salvar nova atribuição."
        logger.error(f"Erro ao adicionar atribuição: {e}")
        return {"message": error_msg}, 400



@app.delete('/atribuicao', tags=[atribuicao_tag],
            responses={"200": AtribuicaoDelSchema, "404": ErrorSchema})
def del_atribuicao(query: AtribuicaoSchema):
    """Deleta uma Atribuição pelo trabalhador_id e tarefa_id."""
    session = Session()
    count = session.query(Atribuicao).filter(
        Atribuicao.trabalhador_id == query.trabalhador_id,
        Atribuicao.tarefa_id == query.tarefa_id
    ).delete()
    session.commit()

    if count:
        return {"message": "Atribuição removida."}, 200
    else:
        error_msg = "Atribuição não encontrada."
        return {"message": error_msg}, 404


@app.get('/atribuicoes', tags=[atribuicao_tag],
         responses={"200": ListagemAtribuicoesSchema, "404": ErrorSchema})
def get_atribuicoes():
    """Lista todas as Atribuições cadastradas."""
    logger.debug("Coletando atribuições")
    session = Session()
    atribuicoes = session.query(Atribuicao).all()
    if not atribuicoes:
        return {"atribuicoes": []}, 200
    return apresenta_atribuicoes(atribuicoes), 200


@app.get('/atribuicoes_detalhadas', tags=[atribuicao_tag],
         responses={"200": ListagemAtribuicoesSchema, "404": ErrorSchema})
def get_atribuicoes_detalhadas():
    """
    Retorna todas as atribuições detalhadas com informações do custo associado.
    """
    session = Session()
    atribuicoes = session.query(Atribuicao).all()

    if not atribuicoes:
        return {"atribuicoes": []}, 200

    
    resultado = []
    for atribuicao in atribuicoes:
        custo = session.query(Custo).get(atribuicao.custo_id)

        
        if custo:
            trabalhador = session.query(Trabalhador).get(custo.trabalhador_id)
            tarefa = session.query(Tarefa).get(custo.tarefa_id)

            resultado.append({
                "atribuicao_id": atribuicao.id,
                "data_insercao": atribuicao.data_insercao,
                "trabalhador": trabalhador.nome if trabalhador else None,
                "tarefa": tarefa.nome if tarefa else None,
                "custo": custo.custo
            })

    return {"atribuicoes": resultado}, 200


from flask import jsonify

@app.post('/process_assignments', tags=[atribuicao_tag],
          responses={"200": ListagemAtribuicoesSchema, "400": ErrorSchema})
def process_assignments_endpoint():
    """Processa as atribuições e retorna os resultados."""
    try:
        session = Session()
        process_assignments(session)
        atribuicoes = session.query(Atribuicao).all()
        result = []
        for atribuicao in atribuicoes:
            custo = session.query(Custo).get(atribuicao.custo_id)
            if custo:
                trabalhador = session.query(Trabalhador).get(custo.trabalhador_id)
                tarefa = session.query(Tarefa).get(custo.tarefa_id)
                result.append({
                    "atribuicao_id": atribuicao.id,
                    "data_insercao": atribuicao.data_insercao,
                    "trabalhador": trabalhador.nome if trabalhador else None,
                    "tarefa": tarefa.nome if tarefa else None,
                    "custo": custo.custo
                })
        return jsonify({"atribuicoes": result}), 200
    except Exception as e:
        error_msg = "Erro ao processar atribuições."
        logger.error(f"Erro ao processar atribuições: {e}")
        return {"message": error_msg}, 400



