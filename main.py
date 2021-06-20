import os
import cv2
import numpy
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import uuid

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = "dafasdfef"


@app.route('/', methods=["POST", "GET"])
def inicio():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('Pedido feito não possui ficheiro.')
            return redirect(url_for("inicio"))

        file = request.files['file']
        if file.filename == '':
            flash('Nenhum ficheiro selecionado')
            return redirect(url_for("inicio"))

        if file and not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            flash('Formato do ficheiro não é suportado. Use apenas PNG, JPG ou JPEG')
            return redirect(url_for("inicio"))

        # img = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
        nome = str(uuid.uuid1()).replace("-", "")
        # cv2.imwrite("tmp/" + nome + ".png", img)  # Guarda a imagem
        file.save("tmp/" + nome + ".png")
        return redirect("/foto/" + nome)

    else:
        return render_template("index.html", fotos=["a", "b"])


@app.route('/img<string:nomeImg>')  # Obtem Imagem
def mostraImagem(nomeImg):
    if os.path.exists("tmp/" + nomeImg + ".png"):
        return send_from_directory("tmp/", nomeImg + ".png")
    else:
        return redirect(url_for("inicio"))


@app.route('/foto/<string:nomeImg>')  # Pagina da imagem
def paginaImagem(nomeImg):
    if os.path.exists("tmp/" + nomeImg + ".png"):
        return render_template("foto.html", ligacao=nomeImg)
    else:
        return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
