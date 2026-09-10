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
)


load_dotenv()



class DigiFarm:
    def __init__(self):

        self.supabase:Client=create_client(supabase_key=os.getenv("digifarm_secret"),supabase_url=os.getenv("digifarm_url"))
        self.digifarm_server_url=os.getenv("digifarm_server_url")
        print(self.digifarm_server_url)





    def makePostRequest(self, endpoint: str, data):
        try:
            response = requests.post(endpoint, json=data, timeout=10)  # json= not data=
            response.raise_for_status()  # raise on 4xx/5xx instead of silently continuing
            return response.json()
        except requests.exceptions.RequestException as e:
            # log this properly, not jst return args
            raise RuntimeError(f"POST to {endpoint} failed: {e}") from e

    
    def makeGetRequest(self, endpoint: str):
        try:
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"GET to {endpoint} failed: {e}") from e

    

    def makeDatabaseRequest(self,tableName:str,method:str,selects:str="*",filterCol:str=None,filterVal:int | str | float =None,updateJson:str=None):
        try:
            match str(method).lower().strip():
                case "select":
                    if filterCol and filterVal:
                        return self.supabase.from_(tableName).select(selects).eq(filterCol,filterVal).execute().data
                    return self.supabase.from_(tableName).select(selects).execute().data
                case "update":
                    if filterCol and filterVal:
                        return self.supabase.from_(tableName).update(updateJson).eq(filterCol,filterVal).execute().data
                    return "Can't Update without specifying row and column to update"
                case "delete":
                    if filterCol and filterVal:
                        return self.supabase.from_(tableName).delete(selects).eq(filterCol,filterVal).execute().data
                    return "Can't Delete without specifying row and column to delete"
                case "insert":
                    return self.supabase.from_(tableName).insert(selects).execute().data

        except SupabaseException as se:
            return se.message
        except Exception as e:
            return e.args



## ________1. RETRIEVING DATA__________

    def getFlocks(self):
        return self.makeGetRequest(endpoint=f"{self.digifarm_server_url}/flock/getAllLogs")

    def getEggProductionLogs(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/eggs/getLogs"
        )

    def getExpenses(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/expenses/getAllLogs"
        )

    def getHealthLogs(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/health/getAllLogs"
        )

    def getFeedLogs(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/feeds/getLogs"
        )

    def getWeightLogs(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/weight/getAllLogs"
        )

    def getMortalityLogs(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/mortality/getAllLogs"
        )

    def getInventoryItems(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/inventory/getAllLogs"
        )

    def getInventoryTransactions(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/transactions/getAllLogs"
        )

    def getSales(self):
        return self.makeGetRequest(
            endpoint=f"{self.digifarm_server_url}/sales/getLogs"
        )

    def getUsers(self):
        return self.makeDatabaseRequest(tableName="users",method="select")


# 2._______________INSERTING DATA___________

    def addEggProductionLogs(self, log:EggProductionLogs):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/eggs/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addExpenseLogs(self, log:ExpenseRequest):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/expenses/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addHealthLog(self, log:HealthLog):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/health/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addFeedLog(self, log:FeedLog):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}feeds/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addWeightLog(self, log:WeightLog):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/weight/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addMortalityLog(self, log:MortalityLog):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/mortality/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addInventoryItem(self, item:InventoryItem):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/inventory/addLog",
            data=item.model_dump_json(exclude_none=True),
        )

    def addInventoryTransaction(self, transaction:InventoryTransaction):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/transactions/addLog",
            data=transaction.model_dump_json(exclude_none=True),
        )

    def addSalesLog(self, log:Sale):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/sales/addLog",
            data=log.model_dump_json(exclude_none=True),
        )

    def addUser(self, user:User):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/users/addLog",
            data=user.model_dump_json(exclude_none=True),
        )

    def addNewFlock(self, flock:Flock):
        return self.makePostRequest(
            endpoint=f"{self.digifarm_server_url}/flock/addLog",
            data=flock.model_dump_json(exclude_none=True),
        )
