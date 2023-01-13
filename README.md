# FastAPI_Event2All

---

API em desenvolvimento com FastAPI, os endpoints do projeto Event2All que foram realizados anteriormente com TypeOrm estão sendo reconstruídos. 

Deploy realizado no Google Cloud (Docker -> PostgreSQL e Artifact Registry)

Alguns endpoints já disponíbilizados no Google Cloud - Swagger/FastAPI: `https://event2all-api-2-ezjia6ekrq-uc.a.run.app/docs`

---
## Como usar localmente essa API:
Pré-requisitos: Python(3.9) e Docker/Postgres.

  1) Após clonar o repositório, instalar todas as dependências -> `dependencies.py`
  2) Iniciar o postgres no docker pelo terminal, exemplo -> `docker run -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 postgres`
  3) Realizar as `migrations` (Alembic) com os comando -> `alembic revision -m "01"` + `alembic upgrade head`
  4) Rodar a API pelo arquivo `main.py`
  
  Obs.: Para acessar o swagger do fastapi é necessário acrescentar `.../docs` ao final do https. 
  
---

## :page_with_curl: Documentação

A documentação da API desenvolvida até o momento encontra-se em: `https://event2all-api-2-ezjia6ekrq-uc.a.run.app/docs`


---


## :keyboard: Desenvolvedor participante
 
[<sub>Danilo Freitas</sub>](https://github.com/danilojpfreitas)  

