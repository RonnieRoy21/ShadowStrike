import requests,os
from supabase import create_client,SupabaseException,Client
from dotenv import load_dotenv
from models import (
    EggProductionLogs,
    ExpenseRequest,
    FeedLog,
    Flock,
    HealthLog,
    InventoryItem,
    InventoryTransaction,
    MortalityLog,
    Sale,
    User,
    WeightLog,
    ResponseModel
)


load_dotenv()



class DigiFarm:
    def __init__(self):
        self.supabase: Client = create_client(
            supabase_key=os.getenv("digifarm_secret"),
            supabase_url=os.getenv("digifarm_url"),
        )
        self.digifarm_server_url = os.getenv("digifarm_server_url")

    def makePostRequest(self, endpoint: str, data) -> ResponseModel:
        try:
            response = requests.post(
                endpoint, data=data, headers={"Content-Type": "application/json"}, 
            )
            response.raise_for_status()
            return ResponseModel(**response.json())
        except requests.exceptions.RequestException as e:
            return ResponseModel(status="error", single=None, body=None, error=str(e))

    def makeGetRequest(self, endpoint: str) -> ResponseModel:
        try:
            response = requests.get(endpoint, )
            response.raise_for_status()
            return ResponseModel(**response.json())
        except requests.exceptions.RequestException as e:
            return ResponseModel(status="error", single=None, body=None, error=str(e))

    def makeDeleteRequest(self, endpoint: str) -> ResponseModel:
        try:
            response = requests.delete(endpoint,)
            response.raise_for_status()
            return ResponseModel(**response.json())
        except requests.exceptions.RequestException as e:
            return ResponseModel(status="error", single=None, body=None, error=str(e))
        
    def makeDatabaseRequest(
        self,
        tableName: str,
        method: str,
        selects: str = "*",
        filterCol: str = None,
        filterVal: int | str | float = None,
        updateJson: str = None,
    ) -> ResponseModel:
        try:
            match str(method).lower().strip():
                case "select":
                    if filterCol and filterVal:
                        data = self.supabase.from_(tableName).select(selects).eq(filterCol, filterVal).execute().data
                    else:
                        data = self.supabase.from_(tableName).select(selects).execute().data
                    return ResponseModel(status="success", single=None, body=data, error=None)
                case "update":
                    if filterCol and filterVal:
                        data = self.supabase.from_(tableName).update(updateJson).eq(filterCol, filterVal).execute().data
                        return ResponseModel(status="success", single=None, body=data, error=None)
                    return ResponseModel(status="error", single=None, body=None, error="Can't update without filterCol and filterVal")
                case "delete":
                    if filterCol and filterVal:
                        data = self.supabase.from_(tableName).delete(selects).eq(filterCol, filterVal).execute().data
                        return ResponseModel(status="success", single=None, body=data, error=None)
                    return ResponseModel(status="error", single=None, body=None, error="Can't delete without filterCol and filterVal")
                case "insert":
                    data = self.supabase.from_(tableName).insert(selects).execute().data
                    return ResponseModel(status="success", single=None, body=data, error=None)
        except SupabaseException as se:
            return ResponseModel(status="error", single=None, body=None, error=se.message)
        except Exception as e:
            return ResponseModel(status="error", single=None, body=None, error=str(e))

    # ________1. RETRIEVING DATA__________

    def getFlocks(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/flock/getAllLogs")
    def getFlockFCR(self, flock_id: int = None) -> ResponseModel:
        if flock_id:
            return self.makeDatabaseRequest(tableName="flock_fcr", method="select", filterCol="flock_id", filterVal=flock_id)
        return self.makeDatabaseRequest(tableName="flock_fcr", method="select")

    def getEggProductionLogs(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/eggs/getLogs")

    def getExpenses(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/expenses/getAllLogs")

    def getHealthLogs(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/health/getAllLogs")

    def getFeedLogs(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/feeds/getLogs")

    def getWeightLogs(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/weight/getAllLogs")

    def getMortalityLogs(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/mortality/getAllLogs")

    def getInventoryItems(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/inventory/getAllLogs")

    def getInventoryTransactions(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/transactions/getAllLogs")

    def getSales(self) -> ResponseModel:
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/sales/getLogs")

    def getUsers(self) -> ResponseModel:
        return self.makeDatabaseRequest(tableName="users", method="select")

    # 2._______________INSERTING DATA___________

    def addEggProductionLogs(self, log: EggProductionLogs) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/eggs/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addExpenseLogs(self, log: ExpenseRequest) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/expenses/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addHealthLog(self, log: HealthLog) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/health/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addFeedLog(self, log: FeedLog) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/feeds/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addWeightLog(self, log: WeightLog) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/weight/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addMortalityLog(self, log: MortalityLog) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/mortality/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addInventoryItem(self, item: InventoryItem) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/inventory/addLog",
            data=item.model_dump_json(exclude_none=True),
        )

    def addInventoryTransaction(self, transaction: InventoryTransaction) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/transactions/addLog",
            data=transaction.model_dump_json(exclude_none=True),
        )

    def addSalesLog(self, log: Sale) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/sales/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addUser(self, user: User) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/users/addLog",
            data=user.model_dump_json(exclude_none=True),
        )

    def addNewFlock(self, flock: Flock) -> ResponseModel:
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/flock/addLog",
            data=flock.model_dump_json(exclude_none=True),
        )
    def deleteWeightLog(self, id: int) -> ResponseModel:
        return self.makeDeleteRequest(
            endpoint=f"{self.digifarm_server_url}/weight/deleteLogById/{id}"
        )

    def deleteAllWeightLogs(self) -> ResponseModel:
        return self.makeDeleteRequest(
            endpoint=f"{self.digifarm_server_url}/weight/deleteAllLogs"
        )