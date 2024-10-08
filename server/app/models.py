from flask_restx import fields

from .extensions import api 

class Project:
    def __init__(self):
        self.user_model = api.model('User', {
            'email': fields.String(required=True, description="User email"),
            'roles': fields.List(fields.String, required=True, description="Roles of the user")
        })

        self.architecture_model = api.model('Architecture', {
            'hosting': fields.Nested(api.model('Hosting', {
                'type': fields.String(required=True, description="Type of hosting"),
                'detail': fields.List(fields.String, required=False, description="Details of hosting")
            })),
            'database': fields.Nested(api.model('Database', {
                'main': fields.String(required=True, description="Main database"),
                'others': fields.List(fields.String, required=False, description="Other databases")
            })),
            'languages': fields.Nested(api.model('Languages', {
                'main': fields.String(required=True, description="Main language"),
                'others': fields.List(fields.String, required=False, description="Other languages")
            })),
            'frameworks': fields.Nested(api.model('Frameworks', {
                'main': fields.String(required=True, description="Main framework"),
                'others': fields.List(fields.String, required=False, description="Other frameworks")
            })),
            'CICD': fields.Nested(api.model('CICD', {
                'main': fields.String(required=True, description="Main CICD tool"),
                'others': fields.List(fields.String, required=False, description="Other CICD tools")
            })),
            'infrastructure': fields.Nested(api.model('Infrastructure', {
                'main': fields.String(required=True, description="Main infrastructure tool"),
                'others': fields.List(fields.String, required=False, description="Other infrastructure tools")
            }))
        })

        self.project_model = api.model('Project', {
            'user': fields.List(fields.Nested(self.user_model), required=True, description="List of users"),
            'details': fields.Nested(api.model('Details', {
                'name': fields.String(required=True, description="Project name"),
                'short_name': fields.String(required=True, description="Short name of the project"),
                'documentation_link': fields.String(required=False, description="Link to the project documentation")
            })),
            'developed': fields.List(fields.Raw, required=True, description="Development details"),
            'source_control': fields.List(fields.String, required=True, description="Source control platforms"),
            'architecture': fields.Nested(self.architecture_model, required=True, description="Architecture details")
        })

    def get_project_model(self):
        return self.project_model