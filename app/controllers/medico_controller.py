# -*- coding: utf-8 -*-
from app.models.medico import Medico
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.extensions import db
from datetime import datetime

def listar_medicos():
    """
    function to list all doctors
    :return: doctor list
    """
    try:
        return Medico.query.all()
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao listar pacientes: {str(e)}")

def medico_id(id):
    """
    function to get a doctor by ID
    :param id: doctor identifier
    :return: doctor by ID
    """
    try:
        medicos = Medico.query.get(id)
        if not medicos:
            raise Exception("Paciente não encontrado")
        return medicos
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar medicos: {str(e)}")

def criar_medico(data):
    """
    function to create new doctor
    :param data: my database
    :return: doctor
    """
    try:
        # Validar dados obrigatorios
        campos_obrigatorios = ['nome', 'data_nascimento', 'cpf']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                raise Exception(f"Campo obrigatório faltando: {campo}")

        # Verifica de cpf já existe
        if Medico.query.filter_by(cpf=data['cpf']).first():
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

        medico = Medico(**data)
        db.session.add(medico)
        db.session.commit()
        return medico

    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"erro ao criar paciente: {str(e)}")
    except ValueError:
        raise Exception("Formato de data inválido. Use YYYY-MM-DD")

def atualizar_medico(id, data):
    """
    function to update doctor
    :param id: doctor identifier
    :param data: database
    :return: doctor update by ID
    """
    try:
        medico = medico_id(id)

        # Verifica de cpf já existe
        if Medico.query.filter_by(cpf=data['cpf']).first():
            raise Exception("CPF já cadastrado")

        # Converter data_nascimento se for string
        if 'data_nascimento' in data and isinstance(data['data_nascimento'], str):
            try:
                data['data_nascimento'] = datetime.strptime(data['data_nascimento'], '%d-%m-%Y').date()
            except ValueError:
                raise Exception("Formato de data inválido. Use DD-MM-YYYY")

        # Atualizar campos do medico
        campos_permitidos = ['nome', 'data_nascimento', 'cpf', 'telefone', 'email']
        for key, value in data.items():
            if key in campos_permitidos and hasattr(medico, key):
                setattr(medico, key, value)

        db.session.commit()
        return medico

    except IndexError:
        db.session.rollback()
        raise Exception("Medico não encontrado")
    except IntegrityError:
        db.session.rollback()
        raise Exception("Erro de integridade: possível duplicação de CPF")
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao atualizar pacientes: {str(e)}")

def deletar_medico(id):
    """
    Function to delete a doctor from the database.
    :param id: Identifier of the doctor to be deleted.
    :return: True if the doctor was successfully deleted.
    :raises Exception: If there is an error during the deletion process.
    """
    try:
        medico = medico_id(id)
        db.session.delete(medico)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao deletar paciente: {str(e)}")

def medico_nome(nome):
    """
    function to get doctor by name
    :param nome: doctor's name
    :return: doctor by name
    """
    try:
        if not nome or len(nome.strip()) < 2:
            raise Exception("O nome deve ter pelo menos 2 caracteres")

        return Medico.query.filter(Medico.nome.ilike(f"%{nome}%")).all()
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar medicos: {str(e)}")

def medico_cpf(cpf):
    """
    function to get doctor by CPF
    :return: doctor by CPF
    """
    try:
        if not cpf:
            raise Exception("CPF não fornecido")

        cpf_limpo = cpf.replace('.', '').replace('-', '')
        if not (cpf_limpo.isdigit() and len(cpf_limpo) == 11):
            raise Exception("CPF inválido. Deve conter 11 dígitos numéricos.")

        paciente = Medico.query.filter_by(cpf=cpf_limpo).first()
        if not paciente:
            raise Exception("Medicos não encontrado com o CPF fornecido")

        return paciente

    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar medicos por CPF: {str(e)}")

def medico_crm(crm):
    """
    function to get doctor by CRM
    :return: doctor by CRM
    """
    try:
        if not crm:
            raise Exception("CRM não fornecido")

        medico = Medico.query.filter_by(crm=crm).first()
        if not medico:
            raise Exception("Medico não encontrado com o CRM fornecido")

        return medico

    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar medicos por CRM: {str(e)}")

def medico_especialidade(especialidade):
    """
    function to get doctors by specialty
    :return: doctors by specialty
    """
    try:
        if not especialidade or len(especialidade.strip()) < 3:
            raise Exception("A especialidade deve ter pelo menos 3 caracteres")

        medicos = Medico.query.filter(Medico.especialidade.ilike(f"%{especialidade}%")).all()
        if not medicos:
            raise Exception("Nenhum medico encontrado com a especialidade fornecida")

        return medicos

    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar medicos por especialidade: {str(e)}")