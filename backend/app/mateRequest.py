from pymongo import MongoClient

uri = "mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLYLINKED"]
students = db["STUDENTS"]
courses = db["COURSES"]
requests = db["MATE_REQUESTS"]


class mateRequest():
    def __init__(self, sender, receiver, status = "pending"):
        self.sender = sender
        self.receiver = receiver
        self.status = status

        if not students.find_one({"userName": sender}):
            print("__init__: Could not find userName of sender")
        elif not students.find_one({"userName": receiver}):
            print("__init__: Could not find userName of receiver")

        else: 
            request = requests.find_one({"sender": sender, "receiver": receiver, "status": status})
            viceVersa = requests.find_one({"sender": receiver, "receiver": sender, "status": status})

            if(request):
                requestStatus = request["status"]
                print("Request already exists. Status of request: ", requestStatus)

            elif(viceVersa):
                self.accept_request(receiver, sender)
                # requests.update_one(
                #     {"sender": receiver, "receiver": sender},
                #     {"$set": {"status": "accepted"}}
                # )
                print("Mutually requested. Auto accepted ClassMates successfully")  

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
        if self.check_user(sender) is False:
            return False
        if self.check_user(receiver) is False:
            return False
        
        request_status = self.check_status(sender, receiver)

        if request_status is False:
            print("accept_request: Pending request does not exist")
            return False
        elif request_status == "pending":
            requests.update_one(
                {"sender": sender, "receiver": receiver, "status": "pending"},
                {"$set": {"status": "accepted"}}
            )
            students.update_one(
                {"userName": receiver},
                {"$pull": {"mateRequests": sender}}
            )
            students.update_one(
                {"userName": sender},
                {"$addToSet": {"classMates": receiver}}
            )
            students.update_one(
                {"userName": receiver},
                {"$addToSet": {"classMates": sender}}
            )
            print("Added ClassMates Successfully")
            return True
        else:
            print("accept_request: Unknown status: ", request_status)
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
        if self.check_user(sender) is False:
            return False
        if self.check_user(receiver) is False:
            return False

        request_status = self.check_status(sender, receiver)
        if request_status is False:
            print("decline_request: Pending request does not exist")
            return False

        elif request_status == "pending":
            requests.update_one(
                {"sender": sender, "receiver": receiver, "status": "pending"},
                {"$set": {"status": "declined"}}
            )
            students.update_one(
                {"userName": receiver},
                {"$pull": {"mateRequests": sender}}
                )
            print("decline_request: Request declined successfully")
            return True
        else:
            print("decline_request: Unknown request status: ", request_status)
            return False

    def check_status(self, sender, receiver):
        request_doc = requests.find_one({"sender": sender, "receiver": receiver, "status": "pending"})
        
        if request_doc is None:
            print("check_request: No pending request exists")
            return False
        else:
            return request_doc["status"]

    def cancel_request(self, sender, receiver):
        if self.check_user(sender) is False:
            return False
        if self.check_user(receiver) is False:
            return False
        
        request_status = self.check_status(sender, receiver)

        if request_status is False:
            print("cancel_request: Request does not exist")
            return False
        elif request_status == "pending":
            requests.update_one(
                {"sender": sender, "receiver": receiver, "status": "pending"},
                {"$set": {"status": "canceled"}}
            )
            students.update_one(
                {"userName": receiver},
                {"$pull": {"mateRequests": sender}}
            )
            print("cancel_request: Canceled request successfully")
            return True
        else:
            print("cancel_request: Unknown request status: ", request_status)
            return False
        
    def print_request(self, sender, receiver):
        request_doc = self.check_status(sender, receiver)

        if not request_doc:
            return None
        
        return request_doc     
    
    def check_user(self, userToCheck):
        user = students.find_one({"userName": userToCheck})

        if user :
            return True
        else:
            print("check_user: Could not find userToCheck")
            return False



    # static method to allow a request to be loaded from the MATE_REQUESTS database collection without creating new student
    @classmethod
    def load_request(cls, sender, receiver):
        request_doc = requests.find_one({"sender": sender, "receiver": receiver})

        if not request_doc:
            print("Request does not exist")
            return None
            
        request = cls.__new__(cls)
        
        request.sender = request_doc["sender"]
        request.receiver = request_doc["receiver"]
        request.status = request_doc["status"]

        return request
    
