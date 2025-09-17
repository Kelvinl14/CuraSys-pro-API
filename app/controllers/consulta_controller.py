# -*- coding: utf-8 -*-
from app.models.consulta import Consulta
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.extensions import db
from datetime import datetime

def listar_consultas():
    """
    function to list all consultas
    :return: consulta list
    """
    try:
        return Consulta.query.all()
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao listar consultas: {str(e)}")

def consulta_id(id):
    """
    function to get a consulta by ID
    :param id: consulta identifier
    :return: consulta by ID
    """
    try:
        consultas = Consulta.query.get(id)
        if not consultas:
            raise Exception("Consulta não encontrada")
        return consultas
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar consultas: {str(e)}")

def criar_consulta(data):
    """
    function to create new consulta
    :param data: my database
    :return: consulta
    """
    try:
        # Validar dados obrigatorios
        campos_obrigatorios = ['data_consulta', 'hora_consulta', 'paciente_id', 'medico_id']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                raise Exception(f"Campo obrigatório faltando: {campo}")

        # Converter data_consulta se for string
        if isinstance(data['data_consulta'], str):
            try:
                data['data_consulta'] = datetime.strptime(data['data_consulta'], '%d-%m-%Y').date()
            except ValueError:
                raise Exception("Formato de data inválido. Use DD-MM-YYYY")

        # Converter hora_consulta se for string
        if isinstance(data['hora_consulta'], str):
            try:
                data['hora_consulta'] = datetime.strptime(data['hora_consulta'], '%H:%M').time()
            except ValueError:
                raise Exception("Formato de hora inválido. Use HH:MM")

        nova_consulta = Consulta(
            data_consulta=data['data_consulta'],
            hora_consulta=data['hora_consulta'],
            paciente_id=data['paciente_id'],
            medico_id=data['medico_id'],
            descricao=data.get('descricao')
        )
        db.session.add(nova_consulta)
        db.session.commit()
        return nova_consulta
    except IntegrityError as e:
        db.session.rollback()
        raise Exception(f"Erro de integridade ao criar consulta: {str(e)}")
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao criar consulta: {str(e)}")


def atualizar_consulta(id, data):
    """
    function to update consulta
    :param id: consulta identifier
    :param data: my database
    :return: consulta updated
    """
    try:
        consulta = Consulta.query.get(id)
        if not consulta:
            raise Exception("Consulta não encontrada")

        # Atualizar campos permitidos
        campos_permitidos = ['data_consulta', 'hora_consulta', 'status', 'descricao', 'paciente_id', 'medico_id']
        for campo in campos_permitidos:
            if campo in data:
                if campo == 'data_consulta' and isinstance(data[campo], str):
                    try:
                        data[campo] = datetime.strptime(data[campo], '%d-%m-%Y').date()
                    except ValueError:
                        raise Exception("Formato de data inválido. Use DD-MM-YYYY")
                if campo == 'hora_consulta' and isinstance(data[campo], str):
                    try:
                        data[campo] = datetime.strptime(data[campo], '%H:%M').time()
                    except ValueError:
                        raise Exception("Formato de hora inválido. Use HH:MM")
                setattr(consulta, campo, data[campo])

        db.session.commit()
        return consulta
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao atualizar consulta: {str(e)}")

def deletar_consulta(id):
    """
    Function to delete a consulta from the database.
    :param id: Identifier of the consulta to be deleted.
    :return: True if the consulta was successfully deleted.
    :raises Exception: If there is an error during the deletion process.
    """
    try:
        consulta = Consulta.query.get(id)
        if not consulta:
            raise Exception("Consulta não encontrada")

        db.session.delete(consulta)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao deletar consulta: {str(e)}")

def listar_consultas_por_paciente(paciente_id):
    """
    Function to list all consultas for a specific paciente.
    :param paciente_id: Identifier of the paciente.
    :return: List of consultas for the specified paciente.
    :raises Exception: If there is an error during the retrieval process.
    """
    try:
        consultas = Consulta.query.filter_by(paciente_id=paciente_id).all()
        return consultas
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao listar consultas por paciente: {str(e)}")

def listar_consultas_por_medico(medico_id):
    """
    Function to list all consultas for a specific medico.
    :param medico_id: Identifier of the medico.
    :return: List of consultas for the specified medico.
    :raises Exception: If there is an error during the retrieval process.
    """
    try:
        consultas = Consulta.query.filter_by(medico_id=medico_id).all()
        return consultas
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao listar consultas por medico: {str(e)}")