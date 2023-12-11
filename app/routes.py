from flask import render_template, request, redirect, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image as PILImage, ImageOps
from app import app, db
from app.models import Image
import os
import hashlib

@app.route('/', methods=['GET', 'POST'])
def index():
  """
  Render the index page and handle image upload.
  """
  if request.method == 'POST':
    image_file = request.files['image']
    if image_file:
      filename = secure_filename(image_file.filename)
      upload_folder = current_app.config['UPLOAD_FOLDER']
      if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
      filepath = os.path.join(upload_folder, filename)
      image_file.save(filepath)

      image_hash = hashlib.blake2b(open(filepath, 'rb').read()).hexdigest()

      existing_image = Image.query.filter_by(image_hash=image_hash).first()
      if existing_image:
        return redirect(url_for('display_image', image_hash=image_hash))

      thumbnail_path = generate_thumbnail(filepath, image_hash)

      new_image = Image(image_hash=image_hash, image_name=filename, thumbnail_path=thumbnail_path)
      db.session.add(new_image)
      db.session.commit()

      return redirect(url_for('display_image', image_hash=image_hash))

  return render_template('upload.html')


def generate_thumbnail(image_path, image_hash):
  """
  Generate and save a thumbnail for the given image.
  """
  size = (256, 256)
  thumbnail_dir = current_app.config['THUMBNAIL_FOLDER']
  thumbnail_path = os.path.join(thumbnail_dir, f'{image_hash}.jpg')

  try:
    img = PILImage.open(image_path)
    img.thumbnail(size, PILImage.LANCZOS)
    img.save(thumbnail_path, "JPEG")
    return thumbnail_path
  except IOError:
    print("Cannot create thumbnail for", image_path)
    return None

@app.route('/image/<image_hash>')
def display_image(image_hash):
  """
  Display the image with the given image hash.
  """
  image = Image.query.filter_by(image_hash=image_hash).first()
  if image:
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.image_name)
    thumbnail_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], f'{image_hash}.jpg')
    return render_template('display_image.html', image_path=image_path, image=image, thumbnail_path=thumbnail_path)
  return 'Image not found', 404

@app.route('/image/<image_hash>/download')
def download_image(image_hash):
  """
  Download the image with the given image hash.
  """
  image = Image.query.filter_by(image_hash=image_hash).first()
  if image:
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], image.image_name)
  return 'Image not found', 404

@app.route('/image/<image_hash>/thumbnail')
def download_thumbnail(image_hash):
  """
  Download the thumbnail of the image with the given image hash.
  """
  image = Image.query.filter_by(image_hash=image_hash).first()
  if image:
    return send_from_directory(current_app.config["THUMBNAIL_FOLDER"], f'{image_hash}.jpg')
  return 'Image not found', 404
