import json
from datetime import datetime
from flask import Flask, jsonify, request, abort, url_for

app = Flask(__name__)

biblioteca_livros = {
    1: {
        "id": 1, "titulo": "Clean Architecture", "isbn": "978-0134494166",
        "ano_publicacao": 2017, "disponivel": True, "autor_id": 1
    },
    2: {
        "id": 2, "titulo": "The Pragmatic Programmer", "isbn": "978-0201616224",
        "ano_publicacao": 1999, "disponivel": False, "autor_id": 2
    },
    3: {
        "id": 3, "titulo": "Refactoring", "isbn": "978-0134757599",
        "ano_publicacao": 2018, "disponivel": True, "autor_id": 3
    }
}
cadastro_autores = {
    1: {"id": 1, "nome": "Robert C. Martin"},
    2: {"id": 2, "nome": "Andrew Hunt"},
    3: {"id": 3, "nome": "Martin Fowler"}
}
registro_emprestimos = {
    123: {"id": 123, "livro_id": 2, "status": "ATIVO"}
}


def obter_detalhes_autor(identificador_autor):
    return cadastro_autores.get(identificador_autor)

def adicionar_links_hateoas(volume_livro):
    identificador_livro = volume_livro['id']
    volume_livro['_links'] = [
        {"rel": "self", "href": url_for('get_livro', livro_id=identificador_livro, _external=True), "method": "GET"},
        {"rel": "update", "href": url_for('update_livro', livro_id=identificador_livro, _external=True), "method": "PUT"},
        {"rel": "delete", "href": url_for('delete_livro', livro_id=identificador_livro, _external=True), "method": "DELETE"}
    ]
    if volume_livro['disponivel']:
        volume_livro['_links'].append(
            {"rel": "emprestar", "href": "/emprestimos", "method": "POST"}
        )
    else:
        identificador_emprestimo = next((eid for eid, emp in registro_emprestimos.items() if emp['livro_id'] == identificador_livro and emp['status'] == 'ATIVO'), None)
        if identificador_emprestimo:
            volume_livro['_links'].append(
                {"rel": "devolver", "href": f"/emprestimos/{identificador_emprestimo}/devolucao", "method": "PUT"}
            )
    return volume_livro

def expandir_livro(volume_livro):
    copia_livro = volume_livro.copy()
    identificador_autor = copia_livro.pop('autor_id', None)
    if identificador_autor:
        copia_livro['autor'] = obter_detalhes_autor(identificador_autor)
    return adicionar_links_hateoas(copia_livro)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "erro": "Recurso não encontrado", "codigo": 404,
        "timestamp": datetime.utcnow().isoformat() + "Z", "caminho": request.path
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "erro": "Requisição inválida", "mensagem": error.description, "codigo": 400,
        "timestamp": datetime.utcnow().isoformat() + "Z", "caminho": request.path
    }), 400

@app.route('/livros', methods=['GET'])
def get_livros():
    lista_livros = list(biblioteca_livros.values())
    nome_autor = request.args.get('autor')
    string_disponivel = request.args.get('disponivel')
    if nome_autor:
        id_autor_encontrado = next((aid for aid, autor in cadastro_autores.items() if nome_autor.lower() in autor['nome'].lower()), None)
        if id_autor_encontrado:
            lista_livros = [livro for livro in lista_livros if livro['autor_id'] == id_autor_encontrado]
    if string_disponivel is not None:
        valor_disponivel = string_disponivel.lower() == 'true'
        lista_livros = [livro for livro in lista_livros if livro['disponivel'] == valor_disponivel]
    ordenar_por = request.args.get('sort', 'id')
    direcao_ordem = request.args.get('order', 'asc')
    if ordenar_por in ['id', 'titulo', 'ano_publicacao']:
        lista_livros.sort(key=lambda x: x[ordenar_por], reverse=(direcao_ordem == 'desc'))
    numero_pagina = request.args.get('page', 1, type=int)
    tamanho_pagina = request.args.get('size', 10, type=int)
    indice_inicio = (numero_pagina - 1) * tamanho_pagina
    indice_fim = indice_inicio + tamanho_pagina
    lista_paginada = lista_livros[indice_inicio:indice_fim]
    resultado = [expandir_livro(livro) for livro in lista_paginada]
    return jsonify(resultado)

@app.route('/livros/<int:livro_id>', methods=['GET'])
def get_livro(livro_id):
    volume_livro = biblioteca_livros.get(livro_id)
    if not volume_livro:
        abort(404)
    return jsonify(expandir_livro(volume_livro))

@app.route('/livros', methods=['POST'])
def create_livro():
    dados_entrada = request.get_json()
    if not dados_entrada or 'titulo' not in dados_entrada or 'autor_id' not in dados_entrada:
        abort(400, description="Dados incompletos. 'titulo' e 'autor_id' são obrigatórios.")
    if dados_entrada['autor_id'] not in cadastro_autores:
        abort(400, description=f"Autor com id {dados_entrada['autor_id']} não existe.")
    novo_identificador = max(biblioteca_livros.keys()) + 1
    novo_volume = {
        'id': novo_identificador, 'titulo': dados_entrada['titulo'], 'isbn': dados_entrada.get('isbn', ''),
        'ano_publicacao': dados_entrada.get('ano_publicacao'), 'disponivel': dados_entrada.get('disponivel', True),
        'autor_id': dados_entrada['autor_id']
    }
    biblioteca_livros[novo_identificador] = novo_volume
    return jsonify(expandir_livro(novo_volume)), 201

@app.route('/livros/<int:livro_id>', methods=['PUT'])
def update_livro(livro_id):
    if livro_id not in biblioteca_livros:
        abort(404)
    dados_atualizacao = request.get_json()
    if not dados_atualizacao:
        abort(400, description="Nenhum dado fornecido para atualização.")
    if 'autor_id' in dados_atualizacao and dados_atualizacao['autor_id'] not in cadastro_autores:
         abort(400, description=f"Autor com id {dados_atualizacao['autor_id']} não existe.")
    volume_existente = biblioteca_livros[livro_id]
    volume_existente.update(dados_atualizacao)
    biblioteca_livros[livro_id] = volume_existente
    return jsonify(expandir_livro(volume_existente))

@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def delete_livro(livro_id):
    if livro_id not in biblioteca_livros:
        abort(404)
    del biblioteca_livros[livro_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)