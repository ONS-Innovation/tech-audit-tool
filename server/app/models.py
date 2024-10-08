# from flask_restx import fields, Model

# class NestedField(Model):
#     name = fields.String(required=True, description="Name of the item")

# class ProjectModel(Model):
#     project_name = fields.String(required=True, description="The name of the project")
#     project_long_name = fields.String(required=True, description="The long name of the project")
#     contact_email = fields.String(required=True, description="The contact email for the project")
#     owner_email = fields.String(required=True, description="The owner's email for the project")
#     doc_link = fields.String(required=False, description="Link to the project documentation")
#     IDE_arr = fields.List(fields.Nested(NestedField), required=False, description="List of IDEs used in the project")
#     lang_frame_arr = fields.List(fields.Nested(NestedField), required=False, description="List of languages and frameworks used in the project")
#     misc_arr = fields.List(fields.Nested(NestedField), required=False, description="Miscellaneous information about the project")
