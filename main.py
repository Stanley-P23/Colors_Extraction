from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from extraction import get_most_popular_colors, group_similar_colors, rgb_to_hex

import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create the upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def delete_all_files_in_uploads():
    # Construct the path to the uploads folder
    uploads_folder = os.path.join('static', 'uploads')
    uploads_folder = os.path.normpath(uploads_folder)  # Normalize the path

    # Check if the directory exists
    if os.path.exists(uploads_folder):
        # List all files in the directory
        for filename in os.listdir(uploads_folder):
            file_path = os.path.join(uploads_folder, filename)
            try:
                # Check if it is a file before attempting to delete
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    # If it's a directory, remove it only if it's empty
                    os.rmdir(file_path)
                    print(f"Deleted directory: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The directory {uploads_folder} does not exist.")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():

    delete_all_files_in_uploads()

    return render_template('test.html')


@app.route('/extract', methods=['POST'])
def extract_colors():

    filename = request.form.get('filename')
    details = int(request.form.get('slider1'))
    average = int(request.form.get('slider2'))


    colors = get_most_popular_colors("static/uploads/" + filename, num_colors=details, threshold=average)



    print(details)
    print(average)
    print(colors)

    return render_template('test.html', filename=filename,   similar=colors[0],  similar_rgb=colors[1], details=details,average=average)





@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)


        colors = [False, False]


        # print(colors[1])

        return render_template('test.html', filename=file.filename,   similar=colors[0],  similar_rgb=colors[1], details=50, average=20)


    slider1_value = request.form.get('slider1Value', type=int, default=50)
    slider2_value = request.form.get('slider2Value', type=int, default=15)

    print(slider1_value)
    print(slider2_value)
    return redirect(request.url)







if __name__ == "__main__":
    app.run(debug=True)
