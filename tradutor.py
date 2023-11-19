from deep_translator import GoogleTranslator
from flask import Flask, render_template, request

app = Flask(__name__)


def tradutor(idioma_padrao, idioma_traduzido, texto):
    texto_traduzido = GoogleTranslator(source=idioma_padrao, target=idioma_traduzido)
    traducao = texto_traduzido.translate(texto)

    return traducao


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        idioma_padrao = request.form.get("idioma_padrao")
        idioma_traduzido = request.form.get("idioma_traduzido")
        texto_a_traduzir = request.form.get("texto_a_traduzir")

        texto = tradutor(idioma_padrao, idioma_traduzido, texto_a_traduzir)

        return render_template("index.html", texto=texto )

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
