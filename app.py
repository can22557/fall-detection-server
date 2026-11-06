import os
from flask import Flask, request, redirect, url_for, render_template_string, jsonify, send_from_directory

app = Flask(__name__)

# ตั้งค่าโฟลเดอร์สำหรับเก็บรูปภาพที่อัปโหลด
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML หน้าตาเว็บพร้อมฟอร์มเลือกไฟล์อัปโหลด
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Fall Detection Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; text-align: center; background-color: #f4f4f9; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        input[type=file] { margin: 15px 0; }
        input[type=submit] { background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        .gallery { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 20px; }
        .gallery img { width: 150px; height: 150px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Fall Detection Server is Running!</h2>
        
        <!-- ฟอร์มเลือกรูปภาพจากคอม/มือถือ -->
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required>
            <br>
            <input type="submit" value="Upload Image">
        </form>

        <h3>Uploaded Images:</h3>
        <div class="gallery">
            {% for img in images %}
                <img src="/uploads/{{ img }}" alt="Uploaded Image">
            {% else %}
                <p>ยังไม่มีรูปภาพในระบบ</p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML_TEMPLATE, images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('index'))

# ส่งไฟล์รูปภาพให้อ่านผ่าน URL
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API สำหรับให้ Raspberry Pi 5 ดึงรายชื่อภาพ
@app.route('/api/images')
def get_images_api():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    image_urls = [f"/uploads/{f}" for f in files]
    return jsonify({"images": image_urls})

# API สำหรับให้ Raspberry Pi 5 สั่งลบรูปภาพหลังจากแจ้งเตือนเสร็จ
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"status": "success", "message": f"Deleted {filename}"})
    return jsonify({"status": "not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
