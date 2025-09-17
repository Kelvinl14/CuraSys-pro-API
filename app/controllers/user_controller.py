# -*- coding: utf-8 -*-
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.extensions import db
import re
from datetime import datetime


def listar_usuarios():
    """
    function to list all users
    :return: user list
    """
    try:
        return User.query.all()
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao listar usuários: {str(e)}")

def usuario_id(id):
    """
    function to get a user by ID
    :param id: user identifier
    :return: user by ID
    """
    try:
        usuario = User.query.get(id)
        if not usuario:
            raise Exception("Usuário não encontrado")
        return usuario
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar usuário: {str(e)}")

def criar_usuario(data):
    """
    function to create new user
    :param data: my database
    :return: user
    """
    try:
        # Validar dados obrigatorios
        campos_obrigatorios = ['username', 'email', 'password']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                raise Exception(f"Campo obrigatório faltando: {campo}")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            raise Exception("Email inválido")

        # Verifica de username ou email já existe
        if User.query.filter_by(username=data['username']).first():
            raise Exception("Username já cadastrado")
        if User.query.filter_by(email=data['email']).first():
            raise Exception("Email já cadastrado")

        usuario = User(
            username=data['username'],
            email=data['email'],
        )
        usuario.set_password(data['password'])
        db.session.add(usuario)
        db.session.commit()
        return usuario
    except IntegrityError as e:
        db.session.rollback()
        raise Exception(f"Erro de integridade ao criar usuário: {str(e)}")
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao criar usuário: {str(e)}")

def atualizar_usuario(id, data):
    """
    function to update user
    :param id: user identifier
    :param data: my database
    :return: updated user
    """
    try:
        usuario = User.query.get(id)
        if not usuario:
            raise Exception("Usuário não encontrado")

        # Atualizar campos permitidos
        campos_permitidos = ['username', 'email', 'password']
        for campo in campos_permitidos:
            if campo in data and data[campo]:
                if campo == 'username' and data['username'] != usuario.username:
                    if User.query.filter_by(username=data['username']).first():
                        raise Exception("Username já cadastrado")
                if campo == 'email' and data['email'] != usuario.email:
                    if User.query.filter_by(email=data['email']).first():
                        raise Exception("Email já cadastrado")
                setattr(usuario, campo, data[campo])

        db.session.commit()
        return usuario
    except IntegrityError as e:
        db.session.rollback()
        raise Exception(f"Erro de integridade ao atualizar usuário: {str(e)}")
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao atualizar usuário: {str(e)}")

def deletar_usuario(id):
    """
    function to delete user
    :param id: user identifier
    :return: None
    """
    try:
        usuario = User.query.get(id)
        if not usuario:
            raise Exception("Usuário não encontrado")

        db.session.delete(usuario)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao deletar usuário: {str(e)}")

def usuario_username(username):
    """
    function to get a user by username
    :param username: user username
    :return: user by username
    """
    try:
        usuario = User.query.filter_by(username=username).first()
        if not usuario:
            raise Exception("Usuário não encontrado")
        return usuario
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar usuário: {str(e)}")

def usuario_email(email):
    """
    function to get a user by email
    :param email: user email
    :return: user by email
    """
    try:
        usuario = User.query.filter_by(email=email).first()
        if not usuario:
            raise Exception("Usuário não encontrado")
        return usuario
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar usuário: {str(e)}")

def autenticar_usuario(username, password):
    """
    function to authenticate user
    :param username: user username
    :param password: user password
    :return: authenticated user
    """
    try:
        usuario = User.query.filter_by(username=username).first()
        if not usuario or not usuario.check_password(password):
            raise Exception("Credenciais inválidas")
        return usuario
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao autenticar usuário: {str(e)}")

def alterar_senha(id, nova_senha):
    """
    function to change user password
    :param id: user identifier
    :param nova_senha: new password
    :return: user with updated password
    """
    try:
        usuario = User.query.get(id)
        if not usuario:
            raise Exception("Usuário não encontrado")

        usuario.password = nova_senha  # Assumindo que a senha será hashada no setter do modelo
        db.session.commit()
        return usuario
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao alterar senha do usuário: {str(e)}")

def resetar_senha(email, nova_senha):
    """
    function to reset user password by email
    :param email: user email
    :param nova_senha: new password
    :return: user with updated password
    """
    try:
        usuario = User.query.filter_by(email=email).first()
        if not usuario:
            raise Exception("Usuário não encontrado")

        usuario.password = nova_senha  # Assumindo que a senha será hashada no setter do modelo
        db.session.commit()
        return usuario
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao resetar senha do usuário: {str(e)}")
