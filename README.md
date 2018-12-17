# Trabalho AB1.1

A company database manager that uses information from www.transparencia.gov.br to see if the companies are in the CNEP (Cadastro Nacional de Empresas Punidas).

## Getting Started

These instructions will show how to get the project running in a local machine.

### Prerequisites

This project was written in Python 3.7 and uses the Flask and Connexion web frameworks as well as Swagger to build and document the API.

To handle some HTTP requests, the appropriately named Requests module was used.

### Installing Dependencies

The easiest way to install the dependencies is using pip.

#### Requests

```
pip install requests
```

#### Flask

```
pip install flask
```

#### Connexion

```
pip install connexion
```

To see the swagger documentation UI, an aditional package have to be installed as it no longer comes bundled with Connexion.

```
pip install swagger-ui-bundle
```

### Starting the server

The server can be started using the python interpreter.

```
python server.py
```
Once started, the server will listen to the default port 5000. Navegating to **localhost:5000** will show the home.html page, which won't really have much to show. The swagger ui, though, will have the documentation of the API structured in a more organized manner. Just go to **localhost:5000/api/ui**, to see it.
