from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory
import os
import subprocess
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'drk_super_secret_key'  # Change this in production

# Base directory setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, 'tools', 'posts')

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # If it's a directory, try to serve its index.html (e.g. /insights -> /insights/index.html)
    full_path = os.path.join(BASE_DIR, path)
    if os.path.isdir(full_path):
        if os.path.exists(os.path.join(full_path, 'index.html')):
            return send_from_directory(full_path, 'index.html')
            
    # Serve the requested file if it exists
    if os.path.exists(full_path):
        return send_from_directory(BASE_DIR, path)
        
    return "Not Found", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login no longer required, redirecting directly to write
    return redirect('/write')

@app.route('/logout')
def logout():
    return redirect('/write')

import json

CATEGORIES_FILE = os.path.join(BASE_DIR, 'tools', 'categories.json')

def load_categories():
    if os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_categories(cats):
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(cats, f, indent=2)

@app.route('/write')
def write():
    categories = load_categories()
    return render_template('write.html', categories=categories)

@app.route('/api/categories', methods=['POST'])
def add_category():
    new_cat = request.json.get('category')
    if new_cat:
        cats = load_categories()
        if new_cat not in cats:
            cats.append(new_cat)
            save_categories(cats)
        return jsonify({'success': True, 'categories': cats})
    return jsonify({'error': 'Missing category'}), 400

@app.route('/api/categories', methods=['DELETE'])
def delete_category():
    cat_to_del = request.json.get('category')
    if cat_to_del:
        cats = load_categories()
        if cat_to_del in cats:
            cats.remove(cat_to_del)
            save_categories(cats)
        return jsonify({'success': True, 'categories': cats})
    return jsonify({'error': 'Missing category'}), 400

@app.route('/api/publish', methods=['POST'])
def publish():
    data = request.json
    title = data.get('title')
    categories = data.get('categories', [])  # It's a list now
    description = data.get('description', '')
    thumbnail = data.get('thumbnail', '')
    content = data.get('content', '')
    
    if not title or not content:
        return jsonify({'success': False, 'error': 'Title and content are required'})
        
    # Create filename from title
    filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + '.md'
    filepath = os.path.join(POSTS_DIR, filename)
    
    # Current date in ISO format
    date_str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    # Format categories (join them if multiple, or just take the first for backward compatibility with build_post.py if needed)
    # Actually build_post.py expects a string. We can join them with commas: "Gaming, Pet"
    category_str = ", ".join(categories) if categories else "General"
    
    # Build markdown frontmatter
    md_content = f"""---
title: "{title.replace('"', "'")}"
date: "{date_str}"
category: "{category_str}"
thumbnail: "{thumbnail}"
description: "{description.replace('"', "'").replace(chr(10), ' ')}"
---

{content}
"""
    
    
    # Save the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # Run the builder script
    build_script = os.path.join(BASE_DIR, 'tools', 'build_post.py')
    try:
        subprocess.run(['python', build_script], cwd=BASE_DIR, check=True, capture_output=True)
        return jsonify({'success': True, 'message': 'Post published and website rebuilt successfully!'})
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'error': f'Build failed: {e.stderr.decode("utf-8")}'})

import uuid
from werkzeug.utils import secure_filename

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # Create unique filename
    ext = os.path.splitext(file.filename)[1]
    filename = f"img_{uuid.uuid4().hex[:8]}{ext}"
    
    # Save to assets/images/posts/
    upload_dir = os.path.join(BASE_DIR, 'assets', 'images', 'posts')
    os.makedirs(upload_dir, exist_ok=True)
    
    file.save(os.path.join(upload_dir, filename))
    
    # Return the URL that will be used in the markdown
    image_url = f"/assets/images/posts/{filename}"
    return jsonify({'url': image_url})

if __name__ == '__main__':
    # Make sure templates folder exists
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    app.run(port=5001, debug=True)
