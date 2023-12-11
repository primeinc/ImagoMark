# app/models.py

from app import app, db

class Image(db.Model):
    image_hash = db.Column(db.String, primary_key=True)
    image_name = db.Column(db.String)
    date_added = db.Column(db.DateTime)
    file_size = db.Column(db.Integer)
    dimensions = db.Column(db.String)
    version = db.Column(db.String)
    metadata_type = db.Column(db.String)
    metadata_json = db.Column(db.String)
    model_hash = db.Column(db.String)
    lora_hash = db.Column(db.String)
    number_of_steps = db.Column(db.Integer)
    sampler = db.Column(db.String)
    cfg_value = db.Column(db.Float)
    thumbnail_path = db.Column(db.String)

class Path(db.Model):
    path_id = db.Column(db.Integer, primary_key=True)
    image_hash = db.Column(db.String, db.ForeignKey('image.image_hash'))
    file_path = db.Column(db.String)

class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String)
    parent_tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'))

class ImageTag(db.Model):
    image_hash = db.Column(db.String, db.ForeignKey('image.image_hash'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True)

class TagTemplate(db.Model):
    template_id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String)
    template_description = db.Column(db.String)

class TemplateTag(db.Model):
    template_id = db.Column(db.Integer, db.ForeignKey('tag_template.template_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True)
    order_index = db.Column(db.Integer)
    
# Create the database tables
with app.app_context():
#   db.drop_all()
  db.create_all()