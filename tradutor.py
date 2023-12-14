from deep_translator import GoogleTranslator
from flask import Flask, render_template, request
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "simple"})


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

        # Gera uma chave única para a combinaçao de idiomas e texto
        chave_cache = f"{idioma_padrao}_{idioma_traduzido}_{texto_a_traduzir}"
        # Tenta obter o resultado do cache:
        texto = cache.get(chave_cache)

        if texto is None:
            # Se não estiver no cache, realiza a traduçao:
            texto = tradutor(idioma_padrao, idioma_traduzido, texto_a_traduzir)
            # Armazena o resultado no cache por um tempo definido(5min, nesse caso):
            cache.set(chave_cache, texto, timeout=300)

        return render_template("index.html", texto=texto)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
