from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@127.0.0.1/empresa'
db = SQLAlchemy(app)

class Setor(db.Model):
    id_setor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
def __str__(self):
        return f'Setor {self.nome}'


class Cargo(db.Model):
    id_cargo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    

def __str__(self):
        return f'Cargo{self.nome}'    

           
class Funcionario(db.Model):
    id_funcionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primeiro_nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    status_funcionario = db.Column(db.Integer, nullable=False)    
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id_setor'), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id_cargo'), nullable=False)
    setor = db.relationship('Setor', backref=db.backref('funcionarios', lazy=True))
    cargo = db.relationship('Cargo', backref=db.backref('funcionarios', lazy=True))

    def __str__(self):
        return f'Funcionario {self.primeiro_nome}'
    
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')
   
@app.route('/cadastro_setor', methods=['GET', 'POST'])
def cadastro_setor():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_setor = Setor(nome=nome)
        db.session.add(novo_setor)
        db.session.commit()
        return redirect(url_for('cadastro_setor'))
    return render_template('setor.html')

@app.route('/cadastro_funcionario', methods=['GET', 'POST'])
def cadastro_funcionario():
    setores = Setor.query.all()
    cargos = Cargo.query.all()
    
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome'].capitalize()
        sobrenome = request.form['sobrenome'].capitalize()
        data_admissao = request.form['data_admissao']
        status_funcionario = request.form.get('status_funcionario', False)
        id_setor = request.form['id_setor']
        id_cargo = request.form['id_cargo']

        novo_funcionario = Funcionario(
            primeiro_nome=primeiro_nome, 
            sobrenome=sobrenome, 
            data_admissao=data_admissao, 
            status_funcionario=status_funcionario,
            id_setor=id_setor,
            id_cargo=id_cargo
        )

        db.session.add(novo_funcionario)
        db.session.commit()
        return redirect(url_for('cadastro_funcionario'))
    
    return render_template('funcionario.html', setores=setores, cargos=cargos,)


@app.route('/cadastro_cargo', methods=['GET', 'POST'])
def cadastro_cargo():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_cargo = Cargo(nome=nome)
        db.session.add(novo_cargo)
        db.session.commit()
        return redirect(url_for('cadastro_cargo'))
    return render_template('cargo.html')

@app.route('/visualizar_funcionarios')
def visualizar_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('visualizar_funcionarios.html', funcionarios=funcionarios)

@app.route('/excluir_funcionario/<int:id_funcionario>', methods=['POST'])
def excluir_funcionario(id_funcionario):
    funcionario = Funcionario.query.get(id_funcionario)
    if funcionario:
        db.session.delete(funcionario)
        db.session.commit()
    return redirect(url_for('visualizar_funcionarios'))

@app.route('/voltar', methods=['GET'])
def voltar():
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)