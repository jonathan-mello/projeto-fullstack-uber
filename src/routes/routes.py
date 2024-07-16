from fastapi import APIRouter, Depends
from src.database.connection import get_db, UberManagement, UberManagementReceipts
from sqlalchemy.orm import Session
from sqlalchemy import join

router = APIRouter()


@router.get("/")
def root():
    return {"message": "hello world!"}


@router.post("/api/v1/uber/management")
def save_management(req: dict, db: Session = Depends(get_db)):
    day = req.get("day")
    weekday = req.get("weekday")
    kilometer = req.get("kilometer")
    balance_kilometer = req.get("balance_kilometer")
    average_comsuption = req.get("average_comsuption")
    liter_gasoline_value = req.get("liter_gasoline_value")
    worked_hours = req.get("worked_hours")
    prejudice = req.get("prejudice")

    data_uber_receipts = req.get("receipt_id")
    uber_value = data_uber_receipts["uber_value"]
    pop_99_value = data_uber_receipts["pop_99_value"]
    promotions = data_uber_receipts["promotions"]
    run_outside = data_uber_receipts["run_outside"]

    new_uber_management_receipts = UberManagementReceipts(
        uber_value=uber_value,
        pop_99_value=pop_99_value,
        promotions=promotions,
        run_outside=run_outside,
    )
    
    db.add(new_uber_management_receipts)
    db.commit()
    

    new_uber_management = UberManagement(
        day=day,
        weekday=weekday,
        kilometer=kilometer,
        balance_kilometer=balance_kilometer,
        average_comsuption=average_comsuption,
        liter_gasoline_value=liter_gasoline_value,
        worked_hours=worked_hours,
        prejudice=prejudice,
        receipt_id=new_uber_management_receipts.id,
    )


    db.add(new_uber_management)
    db.commit()

    return {"Message": "Dados inseridos com sucesso!"}


@router.get("/api/v1/uber/receipts")
def query_data(db: Session = Depends(get_db)):
    dados = db.query(UberManagement).join(UberManagementReceipts, UberManagement.receipt_id == UberManagementReceipts.id).all()
    
    results = []
    for dado in dados:
        
        cost_by_gasoline = dado.kilometer / dado.average_comsuption * dado.liter_gasoline_value
        rent = (670 / 1250) * float(dado.kilometer)
        total_cost_by_kilometer = (rent + float(cost_by_gasoline)) / float(dado.kilometer)
        total_cost = rent + float(cost_by_gasoline)
        
        total_receipt_by_kilometer = (dado.receipt.uber_value + dado.receipt.pop_99_value + dado.receipt.promotions + dado.receipt.run_outside) / dado.kilometer
        profit_day = float(dado.receipt.uber_value + dado.receipt.pop_99_value + dado.receipt.promotions + dado.receipt.run_outside) - total_cost
        profit_hour = profit_day / float(dado.worked_hours)
        profit_by_kilometer = float(total_receipt_by_kilometer) - total_cost_by_kilometer
        
        result = {
            "id": dado.id,
            "day": dado.day,
            "weekday": dado.weekday,
            "kilometer": dado.kilometer,
            "balance_kilometer": dado.balance_kilometer,
            "average_comsuption": dado.average_comsuption,
            "worked_hours": dado.worked_hours,
            "prejudice": dado.prejudice,
            "receipt_id": dado.receipt_id,
            "costs": {
                "liter_gasoline_value": dado.liter_gasoline_value,
                "cost_by_gasoline": round(cost_by_gasoline, 2),
                "rent": round(rent, 2),
                "total_cost_by_kilometer": round(total_cost_by_kilometer, 2),
                "total_cost": round(total_cost, 2)
            },
            "receipts": {
                "uber_value": dado.receipt.uber_value,
                "pop_99_value": dado.receipt.pop_99_value,
                "promotions": dado.receipt.promotions,
                "run_outside": dado.receipt.run_outside,
                "total_receipt_by_kilometer": round(total_receipt_by_kilometer, 2)
            },
            "profit": {
                "day": round(profit_day, 2),
                "hour": round(profit_hour, 2),
                "profit_by_kilometer": round(profit_by_kilometer, 2)
            }
        }
        results.append(result)
        
    
    return results
    