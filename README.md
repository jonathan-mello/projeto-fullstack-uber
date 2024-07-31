1 -> iniciar o projeto em python, utilizando sql alchemy com postgres e fast api []

2 ->  criar um docker compose, para subir a imagem do banco de dados []

3 -> criar 2 tabelas no banco []

4 -> criar conexao com o banco de dados

5 -> criar um endpoint []

POST http://localhost:3000/api/v1/uber/management

request:

{
    "date": "2024-01-25",
    "weekday": "Quinta-Feira",
    "kilometer": 237,
    "balance_kilometer": 787,
    "average_comsuption": 12.9,
    "liter_gasoline_value": 5.08,
    "worked_hours": 9.5,
    "prejudice": 10,
    "acquisitions": {
        "uber_value": 245.19,
        "99_pop_value": 90.53,
        "promotions": 67.78,
        "run_outside": 56.90
    }
}

Fluxo: ao receber a request, devemos salvar esses valores no banco, os valores do objeto receipts, serão salvos na tabela
uber_management_receipts, e entao, após salvar, vamos utilizar o id do registro feito e iremos salvar os valores do objeto principal, juntamente com o aquisition_id, na tabela uber_management

6 -> criar um endpoint []

GET http://localhost:3000/api/v1/uber/aquisitions

response:

{
    "uber_managements": [
        {
            "id": 1,
            "date": "2024-01-25",
            "weekday": "Quinta-Feira",
            "kilometer": 237,
            "balance_kilometer": 787,
            "average_comsuption": 12.9,
            "worked_hours": 9.5,
            "prejudice": 10,
            "receipt_id": 1,
            "costs": {
                "liter_gasoline_value": 5.08,
                "cost_by_gasoline": 106.10,
                "rent": 161.45,
                "total_cost_by_kilometer": 0.88,
                "total_cost": 220.74
            },
            "receipts": {
                "id": 1,
                "uber_value": 245.19,
                "99_pop_value": 90.53,
                "promotions": 67.78,
                "run_outside": 56.90,
                "total_receipt_by_kilometer": 1.74,
                "total_receipt": 300
            },
            "profit": {
                "day": 171.40,
                "hour": 13.18,
                "profit_by_kilometer": 0.74
            }
        },
        {
            "id": 2,
            "date": "2024-01-26",
            "weekday": "Sexta-Feira",
            "kilometer": 237,
            "balance_kilometer": 787,
            "average_comsuption": 12.9,
            "worked_hours": 9.5,
            "prejudice": 10,
            "receipt_id": 2,
            "costs": {
                "liter_gasoline_value": 5.08,
                "cost_by_gasoline": 106.10,
                "rent": 161.45,
                "total_cost_by_kilometer": 0.88,
                "total_cost": 220.74
            },
            "receipts": {
                "id": 2,
                "uber_value": 245.19,
                "99_pop_value": 90.53,
                "promotions": 67.78,
                "run_outside": 56.90,
                "total_receipt_by_kilometer": 1.74,
                "total_receipt": 300
            },
            "profit": {
                "day": 171.40,
                "hour": 13.18,
                "profit_by_kilometer": 0.74
            }
        }
    ]
}

Fluxo: Esse endpoint, irá buscar todos os registros do banco (ou seja, todos os registros de uber_management e consequentemente os registros de uber_management_receipts), de cada dia, e então para cada dia será feito todos os calculos, de media, lucro, etc e então irá retornar os valores consolidados.
