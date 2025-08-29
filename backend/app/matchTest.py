from MatchEngine import getMatches

def matchTest():
    
    user = input("Enter username to find matches: ")

    matches = getMatches(user)

    print(matches)



matchTest()