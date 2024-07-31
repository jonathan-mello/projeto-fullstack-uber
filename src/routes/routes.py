from fastapi import APIRouter, Depends, HTTPException, Query
from src.database.connection import get_db, UberManagement, UberManagementReceipts
from sqlalchemy.orm import Session
from sqlalchemy import join, update
from fastapi.responses import FileResponse
import os

router = APIRouter()


@router.get("/", response_class=FileResponse)
def root():
    file_path = os.path.join(os.path.dirname(__file__), "..", "templates", "index.html")
    return FileResponse(file_path)


@router.get("/add", response_class=FileResponse)
def addDay():
    file_path = os.path.join(os.path.dirname(__file__), "..", "templates", "add.html")
    return FileResponse(file_path)


@router.get("/update", response_class=FileResponse)
def updateDay():
    file_path = os.path.join(
        os.path.dirname(__file__), "..", "templates", "update.html"
    )
    return FileResponse(file_path)


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

    data_uber_receipts = req.get("receipt")
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


@router.get("/api/v1/uber/consult")
def query_data(db: Session = Depends(get_db)):
    dados = (
        db.query(UberManagement)
        .join(
            UberManagementReceipts,
            UberManagement.receipt_id == UberManagementReceipts.id,
        )
        .all()
    )

    results = []
    for dado in dados:

        cost_by_gasoline = (
            dado.kilometer / dado.average_comsuption * dado.liter_gasoline_value
        )
        rent = (670 / 1250) * float(dado.kilometer)
        total_cost_by_kilometer = (rent + float(cost_by_gasoline)) / float(
            dado.kilometer
        )
        total_cost = rent + float(cost_by_gasoline)

        total_receipt_by_kilometer = (
            dado.receipt.uber_value
            + dado.receipt.pop_99_value
            + dado.receipt.promotions
            + dado.receipt.run_outside
        ) / dado.kilometer
        profit_day = (
            float(
                dado.receipt.uber_value
                + dado.receipt.pop_99_value
                + dado.receipt.promotions
                + dado.receipt.run_outside
            )
            - total_cost
        )
        profit_hour = profit_day / float(dado.worked_hours)
        profit_by_kilometer = (
            float(total_receipt_by_kilometer) - total_cost_by_kilometer
        )
        total_receipt = dado.receipt.uber_value + dado.receipt.pop_99_value + dado.receipt.promotions + dado.receipt.run_outside

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
                "cost_by_gasoline": cost_by_gasoline,
                "rent": rent,
                "total_cost_by_kilometer": total_cost_by_kilometer,
                "total_cost": total_cost,
            },
            "receipts": {
                "uber_value": dado.receipt.uber_value,
                "pop_99_value": dado.receipt.pop_99_value,
                "promotions": dado.receipt.promotions,
                "run_outside": dado.receipt.run_outside,
                "total_receipt_by_kilometer": total_receipt_by_kilometer,
                "total_receipt": total_receipt
            },
            "profit": {
                "day": profit_day,
                "hour": profit_hour,
                "profit_by_kilometer": profit_by_kilometer,
            },
        }
        results.append(result)

    return results


@router.delete("/api/v1/uber/delete")
def delete(id: int = Query(...), db: Session = Depends(get_db)):
    itemManagement = db.query(UberManagement).filter(UberManagement.id == id).first()
    if itemManagement:
        db.delete(itemManagement)
        db.commit()
        db.close()

    itemReceipt = (
        db.query(UberManagementReceipts).filter(UberManagementReceipts.id == itemManagement.receipt_id).first()
    )
    if itemReceipt:
        db.delete(itemReceipt)
        db.commit()
        db.close()
        return {"message": "Item deletado com sucesso!"}
    else:
        raise HTTPException(status_code=404, details="Item not found")


@router.get("/api/v1/uber/getday")
def getDay(id: int, db: Session = Depends(get_db)):
    dados = (
        db.query(UberManagement)
        .join(
            UberManagementReceipts,
            UberManagement.receipt_id == UberManagementReceipts.id,
        )
        .all()
    )


    results = []
    for dado in dados:
        result = {
            "day": dado.day,
            "weekday": dado.weekday,
            "kilometer": dado.kilometer,
            "balance_kilometer": dado.balance_kilometer,
            "average_cumsuption": dado.average_comsuption,
            "liter_gasoline_value": dado.liter_gasoline_value,
            "worked_hours": dado.worked_hours,
            "prejudice": dado.prejudice,
            "receipt": {
                "uber_value": dado.receipt.uber_value,
                "pop_99_value": dado.receipt.pop_99_value,
                "promotions": dado.receipt.promotions,
                "run_outside": dado.receipt.run_outside,
            },
        }

        results.append(result)


    query = db.query(UberManagement)
    query = query.filter(UberManagement.id == id)
    get_day = query.all()

    return get_day



@router.put("/api/v1/uber/update")
async def updateDay(id: int, req: dict, db: Session = Depends(get_db)):
    management = db.query(UberManagement).filter(UberManagement.id == id).first()
    if not management:
        raise HTTPException(status_code=404, detail="Item não encontrado!")

    receipt = (
        db.query(UberManagementReceipts)
        .filter(UberManagementReceipts.id == management.receipt_id)
        .first()
    )
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt não encontrado!")

    management.day = req.get("day", management.day)
    management.weekday = req.get("weekday", management.weekday)
    management.kilometer = req.get("kilometer", management.kilometer)
    management.balance_kilometer = req.get(
        "balance_kilometer", management.balance_kilometer
    )
    management.average_comsuption = req.get(
        "average_comsuption", management.average_comsuption
    )
    management.liter_gasoline_value = req.get(
        "liter_gasoline_value", management.liter_gasoline_value
    )
    management.worked_hours = req.get("worked_hours", management.worked_hours)
    management.prejudice = req.get("prejudice", management.prejudice)

    receipt_data = req.get("receipt")
    if receipt_data:
        receipt.uber_value = receipt_data.get("uber_value", receipt.uber_value)
        receipt.pop_99_value = receipt_data.get("pop_99_value", receipt.pop_99_value)
        receipt.promotions = receipt_data.get("promotions", receipt.promotions)
        receipt.run_outside = receipt_data.get("run_outside", receipt.run_outside)

    db.commit()
    db.refresh(management)
    db.refresh(receipt)

    return {"message": "Dados atualizados com sucesso!"}
