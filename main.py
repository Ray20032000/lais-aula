from flask import Flask, render_template, request, redirect
from datetime import date, timedelta

app = Flask(__name__)

livros = []

@app.route('/')
def index():
    return render_template("index.html", livros=livros)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    livros.append({
        'titulo': titulo,
        'autor': autor,
        'emprestado': False,
        'data_devolucao': None
    })
    return redirect('/')

@app.route('/emprestar/<int:idx>')
def emprestar(idx):
    hoje = date.today()
    livros[idx]['emprestado'] = True
    livros[idx]['data_devolucao'] = hoje + timedelta(days=7)
    return redirect('/')

@app.route('/devolver/<int:idx>')
def devolver(idx):
    hoje = date.today()
    data_dev = livros[idx]['data_devolucao']
    multa = 0
    if hoje > data_dev:
        dias_atraso = (hoje - data_dev).days
        multa = 10 + (10 * 0.01 * dias_atraso)  # R$10 + 1% ao dia
    else:
        dias_atraso = 0
    livros[idx]['emprestado'] = False
    livros[idx]['data_devolucao'] = None
    return render_template("index.html", livros=livros, multa=round(multa, 2), dias_atraso=dias_atraso)

if __name__ == '__main__':
    app.run(debug=True)