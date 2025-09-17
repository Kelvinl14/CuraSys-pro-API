# -*- coding: utf-8 -*-
from app.models.paciente import Paciente
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.extensions import db
from datetime import datetime

def listar_pacientes():
    """
    function to list all patients
    :return: patient list
    """
    try:
        return Paciente.query.all()
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao listar pacientes: {str(e)}")

def paciente_id(id):
    """
    function to get a patient by ID
    :param id: patient identifier
    :return: patient by ID
    """
    try:
        paciente = Paciente.query.get(id)
        if not paciente:
            raise Exception("Paciente não encontrado")
        return paciente
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar paciente: {str(e)}")

def criar_paciente(data):
    """
    function to create new patient
    :param data: my database
    :return: patient
    """
    try:
        # Validar dados obrigatorios
        campos_obrigatorios = ['nome', 'data_nascimento', 'cpf']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                raise Exception(f"Campo obrigatório faltando: {campo}")

        # Verifica de cpf já existe
        if Paciente.query.filter_by(cpf=data['cpf']).first():
            raise Exception("CPF já cadastrado")

        # Converter data_nascimento se for string
        if isinstance(data['data_nascimento'], str):
            try:
                data['data_nascimento'] = datetime.strptime(data['data_nascimento'], '%d-%m-%Y').date()
            except ValueError:
                raise Exception("Formato de data inválido. Use DD-MM-YYYY")


        # Validar CPF (apenas números e 11 dígitos)
        cpf = data['cpf'].replace('.', '').replace('-', '')
        if not (cpf.isdigit() and len(cpf) == 11):
            raise Exception("CPF inválido. Deve conter 11 dígitos numéricos.")
        data['cpf'] = cpf

        paciente = Paciente(**data)
        db.session.add(paciente)
        db.session.commit()
        return paciente

    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"erro ao criar paciente: {str(e)}")
    except ValueError:
        raise Exception("Formato de data inválido. Use YYYY-MM-DD")

def atualizar_paciente(id, data):
    """
    function to update patient
    :param id: patient identifier
    :param data: database
    :return: patient update by ID
    """
    try:
        paciente = paciente_id(id)

        # Verifica de cpf já existe
        if Paciente.query.filter_by(cpf=data['cpf']).first():
            raise Exception("CPF já cadastrado")

        # Converter data_nascimento se for string
        if 'data_nascimento' in data and isinstance(data['data_nascimento'], str):
            try:
                data['data_nascimento'] = datetime.strptime(data['data_nascimento'], '%d-%m-%Y').date()
            except ValueError:
                raise Exception("Formato de data inválido. Use DD-MM-YYYY")

        # Atualizar campos do paciente
        campos_permitidos = ['nome', 'data_nascimento', 'cpf', 'telefone', 'email']
        for key, value in data.items():
            if key in campos_permitidos and hasattr(paciente, key):
                setattr(paciente, key, value)

        db.session.commit()
        return paciente

    except IndexError:
        db.session.rollback()
        raise Exception("Paciente não encontrado")
    except IntegrityError:
        db.session.rollback()
        raise Exception("Erro de integridade: possível duplicação de CPF")
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao atualizar pacientes: {str(e)}")

def deletar_paciente(id):
    """
    Function to delete a patient from the database.

    :param id: Identifier of the patient to be deleted.
    :return: True if the patient was successfully deleted.
    :raises Exception: If there is an error during the deletion process.
    """
    try:
        paciente = paciente_id(id)
        db.session.delete(paciente)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao deletar paciente: {str(e)}")

def paciente_nome(nome):
    """
    function to get patient by name
    :param nome: patient's name
    :return: patient by name
    """
    try:
        if not nome or len(nome.strip()) < 2:
            raise Exception("O nome deve ter pelo menos 2 caracteres")

        return Paciente.query.filter(Paciente.nome.ilike(f"%{nome}%")).all()
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar pacientes: {str(e)}")

def paciente_cpf(cpf):
    """
    function to get patient by CPF
    :return: patient by CPF
    """
    try:
        if not cpf:
            raise Exception("CPF não fornecido")

        cpf_limpo = cpf.replace('.', '').replace('-', '')
        if not (cpf_limpo.isdigit() and len(cpf_limpo) == 11):
            raise Exception("CPF inválido. Deve conter 11 dígitos numéricos.")

        paciente = Paciente.query.filter_by(cpf=cpf_limpo).first()
        if not paciente:
            raise Exception("Paciente não encontrado com o CPF fornecido")

        return paciente

    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar paciente por CPF: {str(e)}")