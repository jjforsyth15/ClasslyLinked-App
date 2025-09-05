from pymongo import MongoClient
import bcrypt

uri = "mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLYLINKED"]
students = db["STUDENTS"]
courses = db["COURSES"]
requests = db["MATE_REQUESTS"]


def mateRequest():
    def __init__(self, sender, receiver, status = "pending"):
        self.sender = sender
        self.receiver = receiver
        self.status = status

        request = requests.find_one({"sender": sender, "receiver": receiver})

        if(request):
            requestStatus = request["status"]
            print("Request already exists. Status of request: ", requestStatus)

        viceVersa = request.find_one({"sender": receiver, "receiver": sender})

        if(viceVersa):
            accept_request(receiver, sender)
            # requests.update_one(
            #     {"sender": receiver, "receiver": sender},
            #     {"$set": {"status": "accepted"}}
            # )
            print("Mutually requested. Auto accepting ClassMates")  
        else:
            requests.insert_one({
                "sender": sender,
                "receiver": receiver,
                "status": status
            })
            students.update_one(
                {"userName": receiver},
                {"$addToSet": {"mateRequests": sender}}
            )

    def accept_request(self, sender, receiver):
        request_doc = requests.find_one({"sender": sender, "receiver": receiver})

        if request_doc is None:
            print("Request does not exist")
            return False
        request_status = request_doc["status"]

        if request_status == "accepted":
            print("Users are already ClassMates")
            return False
        elif request_status == "declined":
            print("Receiver declined request")
            return False
        elif request_status == "canceled":
            print("Sender cancelled request")
            return False
        elif request_status == "pending":
            requests.update_one(
                {"sender": sender, "receiver": receiver},
                {"$set": {"status": "accepted"}}
            )
            students.update_one(
                {"userName": receiver},
                {"$pull": {"mateRequests": sender}}
            )
            print("Added ClassMates Successfully")
            return True
        else:
            print("Unknown status: ", request_status)
            return False

    # def accept_mate(self, sender, receiver):
    #     request_doc = requests.find_one({"sender": sender, "receiver": receiver})

    #     if request_doc is None:
    #         print("ClassMate request does not exist")
    #         return False
    #     request_status = request_doc["status"]

    #     if request_status == "accepted":
    #         print("Users are already ClassMates")
    #         return False
    #     elif request_status == "declined":
    #         print("Receiver declined request")
    #         return False
    #     elif request_status == "canceled":
    #         print("Sender cancelled request")
    #         return False
    #     elif request_status == "pending":
    #         students.update_one(
    #             {"userName": sender},
    #             {"$addToSet": {"classMates": receiver}}
    #         )
    #         students.update_one(
    #             {"userName": receiver},
    #             {"$addToSet": {"classMates": sender}}
    #         )
    #         requests.update_one(
    #             {"sender": sender, "receiver": receiver},
    #             {"$set": {"status": "accepted"}}
    #         )
    #         print("Added ClassMate sucessfully")
    #         return True
    #     else:
    #         print("Unknown status: ", request_status)
    #         return False

    def decline_request(self, sender, receiver):
        request_doc = requests.find_one({"sender": sender, "receiver": receiver})

        if request_doc is None:
            print("Request does not exist")
            return False
        request_status = request_doc["status"]

        if request_status == "pending":
            requests.update_one(
                {"sender": sender, "receiver": receiver},
                {"$set": {"status": "declined"}}
            )
            students.update_one(
                {"userName": receiver},
                {"$pull": {"mateRequests": sender}}
                )

    def check_status(self, sender, receiver):
        request_doc = requests.find_one({"sender": sender, "receiver": receiver})
        
        if request_doc is None:
            print("Request does not exist")
            return False
        else:
            return request_doc["status"]

    def cancel_request(self, sender, receiver):
        request_status = check_status(sender, receiver)

        if request_status is False:
            print("Request does not exist")
            return False
        
        requests.update_one(
            {"sender": sender, "receiver": receiver},
            {"$set": {"status": "canceled"}}
        )
        students.update_one(
            {"userName": receiver},
            {"$pull": {"mateRequests": sender}}
        )
        print("Canceled request successfully")
        return True
        

    # static method to allow a request to be loaded from the MATE_REQUESTS database collection without creating new student
    @classmethod
    def load_request(cls, sender, receiver):
        request_doc = requests.find_one({"sender": sender, "receiver": receiver})

        if not request_doc:
            return None
        
        request = cls.__new__(cls)
        
        request.sender = request_doc["sender"]
        request.receiver = request_doc["receiver"]
        request.status = request_doc["status"]

        return request