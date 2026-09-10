from typing import Optional

from pydantic import BaseModel
from datetime import date
from uuid import uuid4

class ResponseModel(BaseModel):
    status:str
    single:object | None
    body:list[object] | None
    error:str | None


class ExpenseRequest(BaseModel):
    id:Optional[int]=None
    recorded_by:str
    flock_id:int
    amount:int
    category:str
    expense_date:str
    description:str

class Flock(BaseModel):
    id: Optional[int] = None
    batch_code:str=uuid4().hex
    breed:str
    purpose:str
    start_date:date=date.today()
    initial_count:int
    current_count:int
    status:str
    created_by:str
    created_at:date=date.today()

class EggProductionLogs(BaseModel):
    id:Optional[int]=None
    flock_id:int
    log_date:date
    eggs_collected:int
    eggs_broken:int
    notes:str
    recorded_by:str
    created_at:date=date.today()

class WeightLog(BaseModel):
    id :Optional[int]=None
    flock_id:int
    sample_size:int
    total_weight_kg:int
    avg_weight_kg:float
    log_date:date=date.today()
    recorded_by:str

class FeedLog(BaseModel):
    id:Optional[int]=None
    flock_id:int
    feed_item_id:int
    quantity_kg:int
    cost:int
    recorded_by:str
    log_date:date=date.today()

class HealthLog(BaseModel):
    id:Optional[int]=None
    flock_id:int
    recorded_by:str
    event_type:str
    medication_name:str
    dosage:str
    notes:str
    event_date:date=date.today()

class MortalityLog(BaseModel):
    id: Optional[int]=None
    flock_id: int
    deaths_count: int
    log_date: date=date.today()
    cause: str
    notes: str
    recorded_by: str


class InventoryTransaction(BaseModel):
    id: Optional[int]=None
    item_id: int
    quantity: int
    transaction_date: date=date.today()
    reference_note: str
    transaction_type: str

class InventoryItem(BaseModel):
    id: Optional[int]=None
    quantity_on_hand: int
    reorder_threshold: int=10
    item_name: str
    category: str
    unit: str="kg"
    last_updated: date=date.today()


class User(BaseModel):
    id: Optional[str]=None
    name: str
    email: str
    role: str
    created_at: date=date.today()


class Sale(BaseModel):
    id: Optional[int]=None
    flock_id: int
    quantity: int
    unit_price: int
    total_amount: int
    amount_paid: int
    product_type: str
    buyer_name: str
    buyer_contact: str
    payment_status: str
    recorded_by: str
    sale_date: date=date.today()