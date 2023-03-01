import simpy
import random
import numpy as np

# Configuración de la simulación
RANDOM_SEED = 42
RAM_CAPACITY = 100
CPU_SPEED = 1
INSTRUCTIONS_PER_CYCLE = 3
WAITING_PROBABILITY = 0.5
NUM_PROCESSES = [25, 50, 100, 150, 200]
# num_processes = [25, 50, 100, 150, 200]

# Clase para el proceso
class Process:
    def __init__(self, id, env, RAM, CPU):
        self.id = id
        self.env = env
        self.RAM = RAM
        self.CPU = CPU
        self.memory_required = random.randint(1, 10)
        self.instructions_remaining = random.randint(1, 10)
        self.waiting_time = 0
        self.start_time = 0

    # Método que ejecuta el proceso
    def run(self):
        # Esperar a que haya suficiente RAM disponible
        yield self.RAM.get(self.memory_required)
        # Esperar a que haya CPU disponible
        with self.CPU.request() as req:
            yield req
            self.start_time = self.env.now
            while self.instructions_remaining > 0:
                # Ejecutar instrucciones
                cycles = min(self.instructions_remaining, INSTRUCTIONS_PER_CYCLE)
                yield self.env.timeout(cycles / CPU_SPEED)
                self.instructions_remaining -= cycles
                # Decidir qué hacer después de ejecutar las instrucciones
                if self.instructions_remaining == 0:
                    self.RAM.put(self.memory_required)
                    print(f"Proceso {self.id} terminado en tiempo {self.env.now}")
                else:
                    self.decide_next()

    # Método que decide qué hacer después de ejecutar las instrucciones
    def decide_next(self):
        # Generar un número al azar para decidir qué hacer
        x = random.uniform(0, 1)
        if x <= WAITING_PROBABILITY:
            self.waiting_time += 1
            self.env.process(self.wait())
        else:
            self.env.process(self.ready())

    # Método que espera en la cola de waiting
    def wait(self):
        print(f"Proceso {self.id} esperando en waiting en tiempo {self.env.now}")
        yield self.env.timeout(1)
        self.env.process(self.ready())

    # Método que vuelve a ready
    def ready(self):
        print(f"Proceso {self.id} en cola de ready en tiempo {self.env.now}")
        yield self.env.timeout(1)
        self.env.process(self.run())


# Función que simula el sistema con el número de procesos dado
def simulate(num_processes):
    env = simpy.Environment()
    random.seed(RANDOM_SEED)
    RAM = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
    CPU = simpy.Resource(env, capacity=1)
    processes = [Process(i, env, RAM, CPU) for i in range(num_processes)]
    for p in processes:
        env.process(p.run())
        #env.process(num_processes(env, RAM)) 
        #env.process(new_process(env, RAM)
    env.run(until=100)
    return [p.waiting_time for p in processes]


#RANDOM_SEED = 42
#RAM_CAPACITY = 100
INSTRUCTION_COUNT = 10
#INSTRUCTION_CYCLES = 3

# Función que genera nuevos procesos con una distribución exponencial
def generate_process(env, RAM, CPU):
    pid = 0
    while True:
        # Generar el tiempo de llegada del próximo proceso
        inter_arrival = random.expovariate(1/10)
        yield env.timeout(inter_arrival)

        # Crear un nuevo proceso
        pid += 1
        process_memory = random.randint(1, 10)

        env.process(process_life_cycle(env, pid, process_memory, RAM, CPU))

# Función que simula el ciclo de vida de un proceso
def process_life_cycle(env, pid, memory, RAM, CPU):
    # El proceso llega al sistema operativo pero debe esperar que se le asigne memoria RAM
    yield RAM.get(memory)

    # Si hay memoria disponible puede pasar al estado de ready. En caso contrario permanece haciendo cola, esperando por memoria.
    print(f"Tiempo {env.now:.2f}: Proceso {pid} ha solicitado {memory} de memoria RAM")

    # El proceso está listo para correr pero debe esperar que lo atienda el CPU
    with CPU.request() as request:
        yield request

        # El CPU atiende al proceso por un tiempo limitado, suficiente para realizar solamente 3 instrucciones
        while True:
            # Obtener la cantidad de instrucciones que quedan por realizar
            instructions_left = INSTRUCTION_COUNT - env.now

            # Ejecutar instrucciones
            if instructions_left >= INSTRUCTIONS_PER_CYCLE:
                yield env.timeout(1)
                instructions_left -= INSTRUCTIONS_PER_CYCLE
            elif instructions_left > 0:
                yield env.timeout(instructions_left)
                instructions_left = 0

            # Si se han completado todas las instrucciones, el proceso pasa al estado Terminated y sale del sistema
            if instructions_left == 0:
                print(f"Tiempo {env.now:.2f}: Proceso {pid} ha completado su ejecución")
                RAM.put(memory)
                return

            # Al dejar el CPU se genera un número entero al azar entre 1 y 2
            io_operation = random.randint(1, 2)

            # Si es 1 entonces pasa a la cola de Waiting para hacer operaciones de I/O (entrada/salida)
            if io_operation == 1:
                print(f"Tiempo {env.now:.2f}: Proceso {pid} está realizando una operación de I/O")
                yield env.timeout(1)
                print(f"Tiempo {env.now:.2f}: Proceso {pid} ha regresado de la operación de I/O")

            # Si es 2 entonces se dirige nuevamente a la cola de Ready
            else:
                print(f"Tiempo {env.now:.2f}: Proceso {pid} regresa al estado Ready")
                return

### BORRAR ESTO ###

# Función que realiza la simulación para una cantidad dada de procesos
def run_simulation(num_processes):
    env = simpy.Environment()
    ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
    cpu = simpy.Resource(env, capacity=1)
    io = simpy.Resource(env, capacity=1)
    env.process(generate_process(env, ram, cpu))
    env.run(until=num_processes * 10)

# Establecer la semilla aleatoria
random.seed(RANDOM_SEED)

# Ejecutar la simulación para cada cantidad de procesos
for num in NUM_PROCESSES:
    #run_simulation(num)
    simulate(num)
