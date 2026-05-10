import os
import subprocess


def convert_to_pem_der(input_path, output_folder):

    filename = os.path.basename(input_path)

    name, ext = os.path.splitext(filename)

    ext = ext.lower()

    try:

        # PEM -> DER
        if ext == '.pem':

            output_file = os.path.join(
                output_folder,
                f"{name}.der"
            )

            command = [
                'openssl',
                'x509',
                '-outform',
                'DER',
                '-in',
                input_path,
                '-out',
                output_file
            ]

        # DER -> PEM
        elif ext == '.der':

            output_file = os.path.join(
                output_folder,
                f"{name}.pem"
            )

            command = [
                'openssl',
                'x509',
                '-inform',
                'DER',
                '-in',
                input_path,
                '-out',
                output_file
            ]

        else:
            return None

        # Exécution OpenSSL
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        print("STDOUT :", result.stdout)
        print("STDERR :", result.stderr)

        # Vérifie erreurs
        if result.returncode != 0:

            return None

        # Vérifie si fichier créé
        if not os.path.exists(output_file):

            return None

        return output_file

    except Exception as e:

        print("Erreur :", e)

        return None