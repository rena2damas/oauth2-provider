from flask import current_app

from src.services.oauth2.client import OAuth2ClientService
from src.services.role import RoleService
from src.services.scope import ScopeService
from src.services.user import UserService


def seed():
    # Seed Scopes
    if not ScopeService.find_by():
        current_app.logger.info('* Seeding scopes *')
        ScopeService.create(name='view:profile',
                            description='View profile information')
        current_app.logger.info('... Scopes seeded.')

    # Seed Roles
    if not RoleService.find_by():
        current_app.logger.info('* Seeding roles *')
        RoleService.create(name='Admin', description='Role for administrative purposes.')
        RoleService.create(name='User', description='Default user role. Every user should belong to this role.')
        RoleService.create(name='Developer', description='Role for developers. Granting this role, allows the user to '
                                                         'create new clients.')

        # Add scopes to roles
        RoleService.add_scope(role_name='Admin', scope_name='view:profile')
        RoleService.add_scope(role_name='User', scope_name='view:profile')

        current_app.logger.info('... Roles seeded.')

    # Seed Users
    if not UserService.find_by():
        current_app.logger.info('* Seeding users *')

        # Admin
        UserService.create(username='admin')
        UserService.add_role(username='admin', role_name='Admin')
        UserService.add_role(username='admin', role_name='User')
        UserService.add_role(username='admin', role_name='Developer')

        # Test
        UserService.create(username='test')
        UserService.add_role(username='test', role_name='User')

        current_app.logger.info('... Users seeded.')

    # Seed dummy client app
    if not OAuth2ClientService.find_by():
        current_app.logger.info('* Seeding OAuth2 clients *')

        # Admin
        OAuth2ClientService.create(
            resource_owner_id=UserService.find_by(username='admin', fetch_one=True).id,
            client_metadata={
                'client_name': 'dummy',
                'client_uri': '',
                'grant_types': [
                    'authorization_code',
                    'implicit',
                    'password',
                    'refresh_token',
                    'client_credentials'
                ],
                'redirect_uris': [
                    '/api/support/client/callback'
                ],
                'response_types': [
                    'code',
                    'token'
                ],
                'scope': 'openid test',
                'token_endpoint_auth_method': 'client_secret_basic'
            }
        )

        current_app.logger.info('... OAuth2 Clients seeded.')
