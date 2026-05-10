import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
    flash
)

from werkzeug.utils import secure_filename

from config import Config
from utils.pem_converter import convert_to_pem_der

app = Flask(__name__)
app.config.from_object(Config)

# Création automatique des dossiers
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERSION_FOLDER'], exist_ok=True)


def allowed_file(filename):

    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower()
        in app.config['ALLOWED_EXTENSIONS']
    )


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():

    # Vérifie si un fichier est envoyé
    if 'file' not in request.files:

        flash('Aucun fichier sélectionné')
        return redirect(url_for('index'))

    file = request.files['file']

    # Vérifie si le nom du fichier est vide
    if file.filename == '':

        flash('Aucun fichier sélectionné')
        return redirect(url_for('index'))

    # Vérifie si extension autorisée
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        # Chemin du fichier uploadé
        upload_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        # Sauvegarde du fichier
        file.save(upload_path)

        print(f"Fichier uploadé : {upload_path}")

        # Conversion PEM <-> DER
        output_file = convert_to_pem_der(
            upload_path,
            app.config['CONVERSION_FOLDER']
        )

        print(f"Fichier converti : {output_file}")

        # Vérifie si conversion réussie
        if output_file and os.path.exists(output_file):

            return render_template(
                'result.html',
                filename=os.path.basename(output_file)
            )

        else:

            flash('Erreur lors de la conversion')
            return redirect(url_for('index'))

    flash('Type de fichier non autorisé')
    return redirect(url_for('index'))


@app.route('/download/<filename>')
def download(filename):

    # Chemin absolu du fichier converti
    path = os.path.abspath(
        os.path.join(
            app.config['CONVERSION_FOLDER'],
            filename
        )
    )

    print(f"Téléchargement : {path}")

    # Vérifie si le fichier existe
    if not os.path.exists(path):

        return f"Fichier introuvable : {path}"

    # Téléchargement
    return send_file(
        path,
        as_attachment=True
    )


if __name__ == '__main__':

    app.run(debug=True)