import os
from flask import Flask, render_template_string, send_from_directory, jsonify, request

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Fall Detection Server</title></head>
<body style="font-family: Arial; text-align: center; padding-top: 50px;">
    <h2>Fall Detection Server is Running!</h2>
    <p>Uploaded Images:</p>
    {% for img in images %}
        <div style="margin: 10px;">
            <img src="{{ url_for('uploaded_file', filename=img) }}" width="300" style="border-radius: 8px;">
        </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    images = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_PAGE, images=images)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/images', methods=['GET'])
def get_images():
    images = os.listdir(UPLOAD_FOLDER)
    image_urls = [f"http://{request.host}/uploads/{img}" for img in images]
    return jsonify({"images": image_urls})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)