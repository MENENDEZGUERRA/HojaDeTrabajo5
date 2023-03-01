import simpy
from random import randint
#This code will change for adding process time 

class Process():

    def __init__(self,initialTime,finalTime):
        self.instructions = randint(1,10)
        self.memory = randint(1,10)
        self.initialTime = initialTime
        self.finalTime = finalTime

class System:
    
    def __init__(self,ram,cpuInstructions):
        self.ram = ram
        self.cpuInstructions = cpuInstructions

    #Method returns an array of n procedures.
    def generateProcess(self,proceduresQt):
        proceduresList = []

        for i in range(proceduresQt):
            newProcess = Process(0,0)
            #print(str(i+1),". OBJ: "+str(newProcess),"MEMORY GEN: "+str(newProcess.memory))
            proceduresList.append(newProcess)
        #print(proceduresList)
        return proceduresList

def RunSystem(env,ram,cpuInstructions,interval,processQt):
    mainSystem = System(ram,cpuInstructions)
    
    SystemProcedures = mainSystem.generateProcess(processQt) #This will be defaultly the waiting as well
    RAM_queue = []
    proceduresTimes = []

    while True:
        for i in range(interval):
            print("YILED 1")
            print("=====================")
            print("RAM: "+str(mainSystem.ram))

            try:
                print("Process memory: "+str(SystemProcedures[0].memory))
                print("Process instructions: "+str(SystemProcedures[0].instructions))

                if SystemProcedures[0].memory <= mainSystem.ram:
                    print("Process taken at: "+str(env.now))
                    SystemProcedures[0].initialTime = env.now
                    print("Process initial time: "+str(SystemProcedures[0].initialTime))
                    mainSystem.ram = mainSystem.ram - SystemProcedures[0].memory
                    RAM_queue.append(SystemProcedures[0])
                    SystemProcedures.pop(0)
                    print("RAM: "+str(mainSystem.ram))
                else:
                    print("Process could not be taken at: "+str(env.now))
            except:
                pass



        yield env.timeout(1) #READY QUEUE SET

        for i in range(interval):

            print("YIELD 2")

            try:
                processRunning = RAM_queue[0]

                print("===============")
                print("Instructions: "+str(processRunning.instructions))
                print("INSTRUCTIONS RUNABLE: "+str(mainSystem.cpuInstructions))

                if processRunning.instructions <= mainSystem.cpuInstructions:
                    print("PROCEDURE DONE")
                    print("Process succesfully completed at: "+str(env.now))
                    processRunning.finalTime = env.now
                    print("Process initial time: "+str(processRunning.initialTime))
                    print("Final process time: "+str(processRunning.finalTime))

                    runTime = processRunning.finalTime - processRunning.initialTime
                    print("Total process time: "+str(runTime))

                    proceduresTimes.append(runTime)
                    mainSystem.ram = mainSystem.ram + processRunning.memory
                    print("RAM: "+str(mainSystem.ram))
                    #Process might now feel free to go
                    RAM_queue.pop(0)

                else:
                    print("Process could not be completed at: "+str(env.now))
                    processRunning.instructions = processRunning.instructions - mainSystem.cpuInstructions
                    print("Restant instructions: "+str(processRunning.instructions))
                    #SystemProcedures.append(processRunning)
            except:
                pass

        if mainSystem.ram == 100:
            print("Process done")
            print(proceduresTimes)
            print(len(proceduresTimes))
            print("STADISTICS")
            #proceduresTimes list contains all data of the time that each process has taken.
            break
        yield env.timeout(1)

env = simpy.Environment()
#def RunSystem(env,ram,cpuInstructions,interval,processQt):
env.process(RunSystem(env,100,3,5,200))
env.run() #Until



