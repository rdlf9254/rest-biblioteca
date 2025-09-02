# API para Gestão de Biblioteca Digital - dac

## 1. Visão Geral

Esta é uma API RESTful projetada para a administração completa de uma biblioteca digital. A solução permite o controle de livros, o gerenciamento de autores e o registro de empréstimos, oferecendo uma interface programática clara e consistente para interações com o sistema.

### Principais Funcionalidades

- **Gerenciamento de Livros**: CRUD completo (Criar, Ler, Atualizar, Deletar) para o acervo de livros
- **Controle de Autores**: Cadastro e manutenção de informações sobre os autores
- **Registro de Empréstimos**: Sistema para registrar e consultar empréstimos de livros a usuários

## 2. Primeiros Passos

Siga as instruções abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.8+
- Pipenv

### Instalação

1. Clone o repositório:

2. Acesse o diretório do projeto:
   ```bash
   cd rest-biblioteca
   ```

3. Instale as dependências com o Pipenv:
   ```bash
   pipenv install
   ```

4. Ative o ambiente virtual:
   ```bash
   pipenv shell
   ```

5. Para iniciar o servidor da API em modo de desenvolvimento, utilize o comando:

```bash
python app.py
```

Por padrão, a API estará acessível em `http://127.0.0.1:5000`.

## 3. Endpoints da API

A seguir, a lista dos principais endpoints disponíveis.

### Recursos de Livros (`/livros`)

- **GET** `/livros` - Retorna uma lista com todos os livros do acervo
- **GET** `/livros/{id}` - Busca um livro específico pelo seu ID
- **POST** `/livros` - Adiciona um novo livro ao acervo
- **PUT** `/livros/{id}` - Atualiza os dados de um livro existente
- **DELETE** `/livros/{id}` - Remove um livro do acervo

### Recursos de Autores (`/autores`)

- **GET** `/autores` - Retorna uma lista com todos os autores cadastrados
- **GET** `/autores/{id}` - Busca um autor específico pelo seu ID
- **POST** `/autores` - Adiciona um novo autor
- **PUT** `/autores/{id}` - Atualiza os dados de um autor

### Recursos de Empréstimos (`/emprestimos`)

- **GET** `/emprestimos` - Lista todos os empréstimos registrados
- **POST** `/emprestimos` - Cria um novo registro de empréstimo