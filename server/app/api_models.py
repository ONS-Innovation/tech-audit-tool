# ns_models.py
from flask_restx import fields
from .extensions import api  # Import the shared ns instance

def get_project_model():
    from .resources import ns

    # Define all models globally
    user_model = ns.model('User', {
        'email': fields.String(required=True, description="User email"),
        'roles': fields.List(fields.String, required=True, description="Roles of the user")
    })

    architecture_model = ns.model('Architecture', {
        'hosting': fields.Nested(ns.model('Hosting', {
            'type': fields.String(required=True, description="Type of hosting"),
            'detail': fields.List(fields.String, required=False, description="Details of hosting")
        })),
        'database': fields.Nested(ns.model('Database', {
            'main': fields.String(required=True, description="Main database"),
            'others': fields.List(fields.String, required=False, description="Other databases")
        })),
        'languages': fields.Nested(ns.model('Languages', {
            'main': fields.String(required=True, description="Main language"),
            'others': fields.List(fields.String, required=False, description="Other languages")
        })),
        'frameworks': fields.Nested(ns.model('Frameworks', {
            'main': fields.String(required=True, description="Main framework"),
            'others': fields.List(fields.String, required=False, description="Other frameworks")
        })),
        'CICD': fields.Nested(ns.model('CICD', {
            'main': fields.String(required=True, description="Main CICD tool"),
            'others': fields.List(fields.String, required=False, description="Other CICD tools")
        })),
        'infrastructure': fields.Nested(ns.model('Infrastructure', {
            'main': fields.String(required=True, description="Main infrastructure tool"),
            'others': fields.List(fields.String, required=False, description="Other infrastructure tools")
        }))
    })

    details_model = ns.model('Details', {
            'name': fields.String(required=True, description="Project name"),
            'short_name': fields.String(required=True, description="Short name of the project"),
            'documentation_link': fields.String(required=False, description="Link to the project documentation")
     })

    # Project Model
    project_model = ns.model('Project', {
        'user': fields.List(fields.Nested(user_model), required=True, description="List of users"),
        'details': fields.List(fields.Nested(details_model), required=True, description="Details of project"),
        'developed': fields.List(fields.Raw, required=True, description="Development details"),
        'source_control': fields.List(fields.String, required=True, description="Source control platforms"),
        'architecture': fields.Nested(architecture_model, required=True, description="Architecture details")
    })

    return project_model

