import json
from flask_restx import Resource, Namespace, reqparse, fields, abort
from .api_models import get_project_model
# from .models import Project
from .utils import read_data, write_data, read_array_data, write_array_data
from .extensions import api

ns = Namespace('/api/', path="/api/", description="")


parser = reqparse.RequestParser()
parser.add_argument('owner_email', type=str, required=True, help='owner_email is required')

required_param = {'owner_email': 'The email of the project owner'}

def require_owner_email(func):
    def wrapper(*args, **kwargs):
        args = parser.parse_args()
        owner_email = args['owner_email']
        if not owner_email:
            abort(400, description="owner_email is required")
        return func(*args, **kwargs)
    return wrapper

@ns.route("/projects")
@ns.doc(params=required_param)
class Projects(Resource):
    @ns.doc(responses={200: 'Success', 400: 'owner_email is required'})
    @ns.marshal_with(get_project_model(), as_list=True)
    @require_owner_email
    def get(self):
        args = parser.parse_args()
        owner_email = args['owner_email']
        data = read_data()
        user_projects = [proj for proj in data['projects'] if proj["user"][0]['email'] == owner_email]
        return user_projects, 200
    
    @ns.expect(get_project_model())
    @ns.doc(responses={201: 'Created project', 400: 'owner_email is required', 406: 'Missing JSON data', 409: 'Project with the same name and owner already exists'})
    @require_owner_email
    def post(self):
        new_project = ns.payload
        if 'user' not in new_project or 'details' not in new_project or 'email' not in new_project['user'][0] or 'name' not in new_project['details']:
            abort(406, description="Missing JSON data")
        
        data = read_data()
        if any(proj['details']['name'] == new_project['details']['name'] and proj['user'][0]['email'] == new_project['user'][0]['email'] for proj in data['projects']):
            abort(409, description="Project with the same name and owner already exists")
        
        data['projects'].append(new_project)
        write_data(data)
        
        # Check if the language is in the array_data, if not add it
        if 'languages' in new_project["architecture"]:
            array_data = read_array_data()
            languages = []
            if 'main' in new_project["architecture"]['languages']:
                languages.append(new_project["architecture"]['languages']['main'])
            if 'others' in new_project["architecture"]['languages']:
                languages.extend(new_project["architecture"]['languages']['others'])
            if 'languages' not in array_data:
                array_data['languages'] = []
            array_data['languages'] = [lang.lower() for lang in array_data['languages']]
            for language in languages:
                language = language.lower()
                if language not in array_data['languages']:
                    array_data['languages'].append(language)
            write_array_data(array_data)
        
        return new_project, 201


@ns.doc(params=required_param,
responses={200: 'Success', 400: 'owner_email is required', 404: 'Project not found.'})
@ns.route("/projects/<string:project_name>")
class ProjectDetail(Resource):
    @ns.marshal_list_with(get_project_model())
    @require_owner_email
    def get(self, project_name):
        args = parser.parse_args()
        owner_email = args['owner_email']
        data = read_data()
        project = next((proj for proj in data['projects'] if proj["details"]['name'] == project_name and proj["user"][0]['email'] == owner_email), None)
        if not project:
            abort(404, description="Project not found")
        return project, 200




autoCompleteParser = reqparse.RequestParser()
autoCompleteParser.add_argument('type', type=str, required=True, help='type is required')
autoCompleteParser.add_argument('search', type=str, required=True, help='search is required')

@ns.doc(params={'type':'Type of array', 'search':'Search query'}, 
responses={200: 'Success', 400: 'type and search are required', 404: 'No matches found.', 406: 'Invalid type', 411: 'Search query is too long'})
@ns.route("/autocomplete")
class Autocomplete(Resource):
    def get(self):
        args = autoCompleteParser.parse_args()
        search_type = args['type']
        search_query = args['search']

        if not search_type or not search_query:
            abort(400, description="type and search are required")
        
        if search_type not in ['languages', 'IDEs', 'misc']:
            abort(406, description="Invalid type")
        
        if len(search_query) > 16:
            abort(411, description="Search query is too long")
        
        array_data = read_array_data()
        
        if search_type not in array_data:
            abort(406, description=f"Invalid type: {search_type}")
        
        results = [item for item in array_data[search_type] if search_query.lower() in item.lower()]

        if not results:
            abort(404, description="No matches found")
        
        return results, 200