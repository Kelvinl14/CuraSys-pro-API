# -*- coding: utf-8 -*-
from app.models.exame import Exame
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.extensions import db
from datetime import datetime

def listar_exames():
    """
    function to list all exams
    :return: exam list
    """
    try:
        return Exame.query.all()
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao listar exames: {str(e)}")

def exame_id(id):
    """
    function to get an exam by ID
    :param id: exam identifier
    :return: exam by ID
    """
    try:
        exame = Exame.query.get(id)
        if not exame:
            raise Exception("Exame não encontrado")
        return exame
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar exame: {str(e)}")

def criar_exame(data):
    """
    function to create new exam
    :param data: my database
    :return: exam
    """
    try:
        # Validar dados obrigatorios
        campos_obrigatorios = ['tipo', 'data_exame', 'resultado', 'consulta_id']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                raise Exception(f"Campo obrigatório faltando: {campo}")

        # Converter data_exame se for string
        if isinstance(data['data_exame'], str):
            try:
                data['data_exame'] = datetime.strptime(data['data_exame'], '%d-%m-%Y').date()
            except ValueError:
                raise Exception("Formato de data inválido. Use DD-MM-YYYY")

        novo_exame = Exame(
            tipo=data['tipo'],
            data_exame=data['data_exame'],
            resultado=data['resultado'],
            consulta_id=data['consulta_id']
        )
        db.session.add(novo_exame)
        db.session.commit()
        return novo_exame
    except IntegrityError as e:
        db.session.rollback()
        raise Exception(f"Erro de integridade ao criar exame: {str(e)}")
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao criar exame: {str(e)}")

def atualizar_exame(id, data):
    """
    function to update an exam
    :param id: exam identifier
    :param data: my database
    :return: exam
    """
    try:
        exame = Exame.query.get(id)
        if not exame:
            raise Exception("Exame não encontrado")

        # Atualizar campos se presentes nos dados
        if 'tipo' in data:
            exame.tipo = data['tipo']
        if 'data_exame' in data:
            if isinstance(data['data_exame'], str):
                try:
                    exame.data_exame = datetime.strptime(data['data_exame'], '%d-%m-%Y').date()
                except ValueError:
                    raise Exception("Formato de data inválido. Use DD-MM-YYYY")
            else:
                exame.data_exame = data['data_exame']
        if 'resultado' in data:
            exame.resultado = data['resultado']
        if 'consulta_id' in data:
            exame.consulta_id = data['consulta_id']

        db.session.commit()
        return exame
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao atualizar exame: {str(e)}")

def deletar_exame(id):
    """
    function to delete an exam
    :param id: exam identifier
    :return: message
    """
    try:
        exame = Exame.query.get(id)
        if not exame:
            raise Exception("Exame não encontrado")

        db.session.delete(exame)
        db.session.commit()
        return {"message": "Exame deletado com sucesso"}
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao deletar exame: {str(e)}")


def listar_exames_paciente(id_paciente):
    """
    function to list exams by patient ID
    :param id_paciente: patient identifier
    :return: exam list by patient ID
    """
    try:
        exames = Exame.query.join(Exame.consulta).filter_by(id_paciente=id_paciente).all()
        return exames
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao listar exames do paciente: {str(e)}")

def upload_arquivo_exame(id, arquivo_path):
    """
    function to upload exam file
    :param id: exam identifier
    :param arquivo_path: path to the exam file
    :return: exam with updated file path
    """
    try:
        exame = Exame.query.get(id)
        if not exame:
            raise Exception("Exame não encontrado")

        exame.arquivo_exame = arquivo_path
        db.session.commit()
        return exame
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao fazer upload do arquivo do exame: {str(e)}")