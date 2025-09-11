from mateRequest import mateRequest

def mateRequestTest():

    while True:
        print("=== Menu ===")
        print("1. New request\n2. Accept request\n3. Cancel request\n4. Decline request\n5.End Program")
        
        choice = input("Choose an option: ")

        if choice == "1":
            print("New request\n-------")
            user1 = input("Enter username of request sender: ")
            user2 = input("Enter the username of the receiver: ")

            newRequest = mateRequest(user1, user2)
            print("Request sent. Status: ", newRequest.print_request(user1, user2))

        elif choice == "2":
            print("Accept request\n-------")
            user1 = input("Enter username of request sender: ")
            user2 = input("Enter the username of the receiver: ")

            accRequest = mateRequest.load_request(user1, user2)
            accRequest.accept_request(user1, user2)
            print("Request accepted. Status: ", accRequest.print_request(user1, user2))

        elif choice == "3":
            print("Cancel request\n-------")
            user1 = input("Enter username of request sender: ")
            user2 = input("Enter the username of the receiver: ")

            canRequest = mateRequest.load_request(user1, user2)
            canRequest.cancel_request(user1, user2)
            print("Request canceled. Status: ", canRequest.print_request(user1, user2))

        elif choice == "4":
            print("Decline request\n-------")
            user1 = input("Enter username of request sender: ")
            user2 = input("Enter the username of the receiver: ")

            decRequest = mateRequest.load_request(user1, user2)
            decRequest.decline_request(user1, user2)
            print("Request declined. Status: ", decRequest.print_request(user1, user2))

        elif choice == "5":
            print("Ending program...")
            break
        else:
            print("Invalid input")
    
        

        

        




    



mateRequestTest()