import json
import requests,os
from supabase import create_client,SupabaseException,Client
from dotenv import load_dotenv
from models import (
    EggProductionLogs as EggProductionLogModel,
    ExpenseRequest,
    FeedLog as FeedLogModel,
    Flock as FlockModel,
    HealthLog as HealthLogModel,
    InventoryItem,
    InventoryTransaction,
    MortalityLog as MortalityLogModel,
    Sale,
    User,
    WeightLog as WeightLogModel,
    ResponseModel,
    Action
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
                endpoint, data=data , headers={"Content-Type": "application/json"}, 
            )
            print("response from post request",response.json())

            response.raise_for_status()
            return ResponseModel(**response.json())
        except requests.exceptions.RequestException as e:
            return ResponseModel(status="error", single=None, body=None, error=str(e))

    def makeGetRequest(self, endpoint: str) -> ResponseModel:
        try:
            response = requests.get(endpoint, )
            print("response from get request",response.json())

            response.raise_for_status()
            return ResponseModel(**response.json())
        except requests.exceptions.RequestException as e:
            return ResponseModel(status="error", single=None, body=None, error=str(e))

    def makeDeleteRequest(self, endpoint: str) -> ResponseModel:
        try:
            response = requests.delete(endpoint,)
            print("response from delete request..",response.json())
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



    # ________ RETRIEVING FCR DATA__________

   
    def getFlockFCR(self, flock_id: int = None) -> ResponseModel:
        if flock_id:
            return self.makeDatabaseRequest(tableName="flock_fcr", method="select", filterCol="flock_id", filterVal=flock_id)
        return self.makeDatabaseRequest(tableName="flock_fcr", method="select")

  


    # _______________Handling DATA___________


                        ########_____________Egg Production____________

    def EggProductionLogs(
        self,
        log: EggProductionLogModel = None,
        logs: list[EggProductionLogModel] = None,
        action: Action = Action.ADD_SINGLE,
        deleteId: int = None,
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(
                    endpoint=f"{self.digifarm_server_url}/eggs/addLog",
                    data=log.model_dump_json(exclude_none=True),
                )
            case Action.SELECT:
                return self.makeGetRequest(
                    endpoint=f"{self.digifarm_server_url}/eggs/getLogs",
                )
            case Action.DELETE_BY_ID:
                if not deleteId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null Id not Allowed")
                return self.makeDeleteRequest(
                    endpoint=f"{self.digifarm_server_url}/eggs/deleteLogById/{deleteId}",
                )
            case Action.ADD_BUNCH:
                if not logs:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(
                    endpoint=f"{self.digifarm_server_url}/eggs/addLogs",
                    data=json.dumps([egg_log.model_dump(exclude_none=True) for egg_log in logs]),
                )




##_________________Expenses__________________
    def ExpenseLogs(
        self,
        log: ExpenseRequest = None,
        logs: list[ExpenseRequest] = None,
        action: Action = Action.ADD_SINGLE,
        deleteId: int = None,
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(
                    endpoint=f"{self.digifarm_server_url}/expenses/addLog",
                    data=log.model_dump_json(exclude_none=True),
                )
            case Action.SELECT:
                return self.makeGetRequest(
                    endpoint=f"{self.digifarm_server_url}/expenses/getAllLogs",
                )
            case Action.DELETE_BY_ID:
                if not deleteId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null Id not Allowed")
                return self.makeDeleteRequest(
                    endpoint=f"{self.digifarm_server_url}/expenses/deleteLogById/{deleteId}",
                )
            case Action.DELETE:
                return self.makeDeleteRequest(
                    endpoint=f"{self.digifarm_server_url}/expenses/deleteAllLogs",
                )
            case Action.ADD_BUNCH:
                if not logs:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(
                    endpoint=f"{self.digifarm_server_url}/expenses/addLogs",
                    data=json.dumps([expense.model_dump(exclude_none=True) for expense in logs]),
                )






#_____________________Health Logs______________

    def HealthLog(
        self,
        log: HealthLogModel = None,
        logs: list[HealthLogModel] = None,
        action: Action = Action.ADD_SINGLE,
        deleteId: int = None,
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(
                    endpoint=f"{self.digifarm_server_url}/health/addLog",
                    data=log.model_dump_json(exclude_none=True),
                )
            case Action.SELECT:
                return self.makeGetRequest(
                    endpoint=f"{self.digifarm_server_url}/health/getAllLogs",
                )
            case Action.DELETE_BY_ID:
                if not deleteId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null Id not Allowed")
                return self.makeDeleteRequest(
                    endpoint=f"{self.digifarm_server_url}/health/deleteLogById/{deleteId}",
                )
            case Action.ADD_BUNCH:
                if not logs:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(
                    endpoint=f"{self.digifarm_server_url}/health/addLogs",
                    data=json.dumps([health_log.model_dump(exclude_none=True) for health_log in logs]),
                )





#_____________FeedLogs___________________ endppoints=[ 'getLogs,addLog,addLogs,editLog,deleteLog']

    def FeedLog(
        self,
        log: FeedLogModel = None,
        logs: list[FeedLogModel] = None,
        action: Action = Action.ADD_SINGLE,
        deleteId:int=None
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/feeds/addLog", data=log.model_dump_json(exclude_none=True))
            case Action.SELECT:
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/feeds/getLogs")
            case Action.ADD_BUNCH:
                if not logs:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/feeds/addLogs", data=json.dumps([feed.model_dump(exclude_none=True) for feed in logs]))
            case Action.UPDATE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/feeds/editLog", data=log.model_dump_json(exclude_none=True))
            case Action.DELETE:
                if not deleteId:
                    return ResponseModel(status="Rejected",single=None,body=None,error="Must provide an id of item to delete")
                return self.makeDeleteRequest(endpoint=f"{self.digifarm_server_url}/feeds/deleteLogById/{deleteId}")





#____________WeightLogs_______________endpoint=["getAllLogs,getLogById/{id},addLog,deleteLogById/{id},deleteAllLogs"]

    def WeightLog(
        self,
        log: WeightLogModel = None,
        logs: list[WeightLogModel] = None,
        action: Action = Action.ADD_SINGLE,
        logId: int = None,
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/weight/addLog", data=log.model_dump_json(exclude_none=True))
            case Action.SELECT:
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/weight/getAllLogs")
            case Action.SELECT_BY_ID:
                if not logId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null Id not Allowed")
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/weight/getLogById/{logId}")
            case Action.ADD_BUNCH:
                if not logs:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/weight/addLogs", data=json.dumps([w_log.model_dump(exclude_none=True) for w_log in logs]))
            case Action.DELETE_BY_ID:
                if not logId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null Id not Allowed")
                return self.makeDeleteRequest(endpoint=f"{self.digifarm_server_url}/weight/deleteLogById/{logId}")
            case Action.DELETE:
                return self.makeDeleteRequest(endpoint=f"{self.digifarm_server_url}/weight/deleteAllLogs")






#______________________MortalityLogs____________endpoints=['getAllLogs,addLog,addLogs']

    def MortalityLog(
        self,
        log: MortalityLogModel = None,
        logs: list[MortalityLogModel] = None,
        action: Action = Action.ADD_SINGLE,
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/mortality/addLog", data=log.model_dump_json(exclude_none=True))
            case Action.SELECT:
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/mortality/getAllLogs")
            case Action.ADD_BUNCH:
                if not logs:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/mortality/addLogs", data=json.dumps([mortality.model_dump(exclude_none=True) for mortality in logs]))





#________________inventory items_______enpoints=['getAllLogs,addLog,addLogs,updateLog,deleteLog']
    def InventoryItemLog(
        self,
        item: InventoryItem = None,
        items: list[InventoryItem] = None,
        action: Action = Action.ADD_SINGLE,
        deleteId:int=None
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not item:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/inventory/addLog", data=item.model_dump_json(exclude_none=True))
            case Action.SELECT:
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/inventory/getAllLogs")
            case Action.ADD_BUNCH:
                if not items:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/inventory/addLogs", data=json.dumps([inventory_item.model_dump(exclude_none=True) for inventory_item in items]))
            case Action.UPDATE:
                if not item:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/inventory/updateLog", data=item.model_dump_json(exclude_none=True))
            case Action.DELETE:
                if not deleteId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null ID not Allowed")

                return self.makeDeleteRequest(endpoint=f"{self.digifarm_server_url}/inventory/deleteLogById/{deleteId}")




#__________Inventory Transaction_____________enpoint=['getAllLogs,addLog,addLogs,updateLog,deleteLog']
    def InventoryTransactionLog(
        self,
        transaction: InventoryTransaction = None,
        transactions: list[InventoryTransaction] = None,
        action: Action = Action.ADD_SINGLE,
        deleteId=None
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not transaction:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/transactions/addLog", data=transaction.model_dump_json(exclude_none=True))
            case Action.SELECT:
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/transactions/getAllLogs")
            case Action.ADD_BUNCH:
                if not transactions:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/transactions/addLogs", data=json.dumps([item.model_dump(exclude_none=True) for item in transactions]))
            case Action.UPDATE:
                if not transaction:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/transactions/updateLog", data=transaction.model_dump_json(exclude_none=True))
            case Action.DELETE:
                if not deleteId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null ID not Allowed")

                return self.makeDeleteRequest(endpoint=f"{self.digifarm_server_url}/transactions/deleteLogById/{deleteId}")





##____________Sales Logs__________endpoint=[''addLog,addLogs,updateLog,deleteLog,getLogs']

    def SalesLog(
        self,
        log: Sale = None,
        logs: list[Sale] = None,
        action: Action = Action.ADD_SINGLE,
        deleteId:int=None
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/sales/addLog", data=log.model_dump_json(exclude_none=True))
            case Action.SELECT:
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/sales/getLogs")
            case Action.ADD_BUNCH:
                if not logs:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/sales/addLogs", data=json.dumps([sale.model_dump(exclude_none=True) for sale in logs]))
            case Action.UPDATE:
                if not log:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/sales/updateLog", data=log.model_dump_json(exclude_none=True))
            case Action.DELETE:
                if not deleteId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null ID not Allowed")

                return self.makeDeleteRequest(endpoint=f"{self.digifarm_server_url}/sales/deleteLogById/{deleteId}")



    #_____________Flock Logs_________endpoints=['getAllLogs,getLogById/{flockId},addLog,deleteLogById/{flockId},deleteAllLogs']

    def Flock(
        self,
        flock: FlockModel = None,
        action: Action = Action.ADD_SINGLE,
        flockId: int = None,
    ) -> ResponseModel:
        match action:
            case Action.ADD_SINGLE:
                if not flock:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null body not Allowed")
                return self.makePostRequest(endpoint=f"{self.digifarm_server_url}/flock/addLog", data=flock.model_dump_json(exclude_none=True))
            case Action.SELECT:
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/flock/getAllLogs")
            case Action.SELECT_BY_ID:
                if not flockId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null Id not Allowed")
                return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/flock/getLogById/{flockId}")
            case Action.DELETE_BY_ID:
                if not flockId:
                    return ResponseModel(status="Rejected", single=None, body=None, error="Null Id not Allowed")
                return self.makeDeleteRequest(endpoint=f"{self.digifarm_server_url}/flock/deleteLogById/{flockId}")
            case Action.DELETE:
                return self.makeDeleteRequest(endpoint=f"{self.digifarm_server_url}/flock/deleteAllLogs")


