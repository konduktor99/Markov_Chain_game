
import numpy as np
import pandas

#przygotowanie danych ukazujących zmiany macierzy przejciaw każdej rundzie
#preparing  data of transition matrix changes
def prepareDiagnosticStats():

    possiblePairsAbbr = ['r_r','r_p','r_s','p_r','p_p','p_s','s_r','s_p','s_s']
    
    separator ='-----------------------------------------------------------------'
    expected = f'Choice expected by algorithm: {estimatedUserChoice}'
    transition = f'Actual situation: {currPair} --> {nextPair}'
    prettyPrintedMatrix =pandas.DataFrame(transitionMatrix, possiblePairsAbbr, possiblePairsAbbr)
    matrix = 'Numerators matrix after probability adjustment: \n' + prettyPrintedMatrix.to_string()
    
    return separator +'\n'+ expected +'\n'+ transition +'\n'+ matrix +'\n'+ separator + '\n'
   

#wczytywanie i walidacja wyboru gracza
#user's choice reading and validation
def loadUserChoice ():          
    
    global roundCounter
    roundCounter+=1
    print(f'\n--({roundCounter})--')

    while True:
        global userChoice
        userChoice= input('ENTER YOUR CHOICE. \n')
        userChoice=userChoice.lower()
        if(userChoice != 'paper' and userChoice != 'rock' and userChoice != 'scissors' and userChoice != 'r' and userChoice != 'p' and userChoice != 's'):
            print('THE CHOICE IS INCORRECT. ENTER ANOTHER ONE. (Correct: rock, paper, scissors, r, p, s)')
            continue
        else: 
            break
        
    userChoice = 'paper' if userChoice=='p' else  userChoice
    userChoice = 'rock' if userChoice=='r' else  userChoice
    userChoice = 'scissors' if userChoice=='s' else  userChoice
  
    
    
    
#Złączenie uprzednio wczytanych wyborów gracza i komputera    
#merging user's and computer's choices read before
def mergeChoices (aiChoice,userChoice):      
    print(f'\nYOUR CHOICE: {userChoice}')
    print(f'CPU\'s CHOICE: {aiChoice}') 
    return f'{aiChoice}_{userChoice}'
    

#przyznawanie punktów na podstawie wyborów gracza i komputera
#summarizing user's and computer's points basing on choices after the single round
def sumPoints():                
    global userPoints, aiPoints
    
    if (userChoice=='paper' and aiChoice=='scissors') or (userChoice=='scissors' and aiChoice=='rock') or (userChoice=='rock' and aiChoice=='paper'):
        aiPoints+=1
        userPoints-=1
    elif userChoice != aiChoice :

        aiPoints-=1
        userPoints+=1
    print( f'YOU: {userPoints} CPU: {aiPoints}')
    
#wczytywanie i walidacja docelowej liczby punktów
#reading and validating the target score
def readTargetPoints():
    global targetPoints
    while True:
        try:
            targetPoints = int(input('ENTER TARGET SCORE \n'))
        except ValueError:
            print('YOU HAVE TO ENTER NUMERIC VALUE')
            continue
        if targetPoints <=0:
            print('YOU HAVE TO ENTER POSITIVE VALUE')
            continue
        else:
            break 
        
#wczytanie decyzji gracza czy algorytm ma korzystać z macierzy wyuczonej w poprzedniej rozgrywce
#reading user's decision whether transition matrix from previous game is used
def readDecisionIfPreviousLearning():
    while True:
         decision = input('DO YOU WANT TO PLAY WITH PREVIOUSLY LEARNED CPU? TYPE yes/no (y/n). \n')
         decision=decision.lower()
        
         if decision !='y' and decision !='n' and decision !='yes' and decision !='no':
             print('YOU HAVE TO TYPE yes/no (y/n).')
             continue
         else:
             decision = 'y' if decision=='yes' else  decision
             decision = 'n' if decision=='no' else  decision
             break 
         print(decision)
    return True if decision=='y' else False
         
#wczytanie ostatniej pary z poprzedniej gry znajdującej się w ostatniej linii pliku i usunięcie tej linii z pliku
# reading and removing the last pair from previous game being the last line of the file          
def popPairFromPreviousGame():
    global currPair, fileModelName
    with open(fileModelName,'r+') as f:
       lines = f.readlines()
       f.seek(0)
       currPair=lines.pop()
       print(currPair)
       for l in lines:
           f.write(l)
           f.truncate()
       



#wybór ruchu komputera na podstawie macierzy przejscia
#selecting computer choice basing on transition matrix
def setAiChoice():
    global aiChoice, currRowIndex, estimatedUserChoice
    
    currRowIndex = possibleChoicesPairs.index(currPair)
    currRow=transitionMatrix[currRowIndex]
    
    
    denominatorForCurrRow = sum(currRow)
    currRowProbs=np.divide(currRow,denominatorForCurrRow)                  #prawdopodobienstwa w rzędzie macierzy wyliczane dzieląc wszystkie elementy przez ich sume
   
    
    estimatedPair = np.random.choice(possibleChoicesPairs,p=currRowProbs)  #wybór komórki pary spodziewanej na podstawie prawdopodobienstw w danym rzędzie
    
    estimatedUserChoice= (estimatedPair.split('_'))[1]                     #wyłuskanie spodziewanego wyboru gracza z danej pary
   
    
    if estimatedUserChoice =='paper':
        aiChoice = 'scissors'
    elif estimatedUserChoice =='scissors':
        aiChoice = 'rock'
    else:
        aiChoice = 'paper'
        
#aktualizacja licznika w komórce danego przejscia między parami w macierzy przejscia - aktualizacja łańcucha markova 
#updating the numerator in transition matrix cell associated with current and next pair of choices - markov chain update     
def updateTransitionMatrixNumerators():
    updateParamColumnIndex=possibleChoicesPairs.index(nextPair)
    transitionMatrix[currRowIndex][updateParamColumnIndex]+=1



def main():
    global roundCounter, aiChoice, userChoice, userPoints, aiPoints,transitionMatrix,possibleChoicesPairs, currPair, nextPair, fileModelName
    fileResult = open("markov_events.txt", "w")
    fileModelName ="markov_model.txt"
    roundCounter=0
    userPoints = 0
    aiPoints = 0
    possibleResults = ['rock', 'paper', 'scissors']
    possibleChoicesPairs = ['rock_rock','rock_paper','rock_scissors','paper_rock','paper_paper','paper_scissors','scissors_rock','scissors_paper','scissors_scissors']
    acc='w'
    
    
    
    
    readTargetPoints()    
    fileResult.write(f'|TARGET SCORE: {targetPoints}|\n')
    
    
     #Jesli gracz tak zdecydował, wczytywane są parametry łańcucha Markova z pliku z poprzedniej gry,
     #w przeciwnym wypadku tworzona jest nowa macierz i pobierana pierwsza para zagrań.
     
    if  readDecisionIfPreviousLearning():
       popPairFromPreviousGame()
       transitionMatrix=np.loadtxt(fileModelName) 
       acc='a'
    else:   
       transitionMatrix = [[1 for x in range(9)] for y in range(9)] 
       loadUserChoice()
       aiChoice=np.random.choice(possibleResults)
       currPair=mergeChoices(aiChoice,userChoice)
       sumPoints()
       fileResult.write(f'\n({roundCounter}) -- CPU\'s choice: {aiChoice}, User\'s choice: {userChoice} -- CPU: {aiPoints}, User: {userPoints}')
      

    fileModelEvo = open("markov_model_evo.txt", acc)
       
    
    
    
    #main loop
    while userPoints != targetPoints and aiPoints != targetPoints:
    
    
        setAiChoice()      
        loadUserChoice()
        sumPoints()
        nextPair=mergeChoices(aiChoice,userChoice)
       
        fileResult.write(f'\n({roundCounter}) -- CPU\'s choice: {aiChoice}, User\'s choice: {userChoice} -- CPU: {aiPoints}, User: {userPoints}')
       
        updateTransitionMatrixNumerators()
        
        fileModelEvo.write(prepareDiagnosticStats())
         
        currPair=nextPair
        
            
                    
    
    if userPoints == targetPoints:
        print('!!!  YOU WON THE GAME  !!!')
        fileResult.write('\nUSER WINS')
    else:
        print('!!!  AI WON THE GAME :)  !!!')
        fileResult.write('\nCPU WINS')
        
        
    np.savetxt("markov_model.txt", transitionMatrix,'%2.f')
    with open(fileModelName,'a+') as f:
        f.write(currPair)
        
    fileResult.close()  
    fileModelEvo.close()  
  
    
  
if __name__ == "__main__":
    main()
        
    
    





