from register import RegisterArray
from customer import Customer

import plotly

import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go


class Store:
    # registers at random?
    aisles = 0

    def __init__(self, num_of_aisles, registerArray):
        self.aisles = num_of_aisles
        self.registers = registerArray

    def __str__(self):
        toRet = "store test!!!\n"
        toRet += self.registers.__str__()
        return toRet


def test():
    # r1 = Register(True)
    # r2 = Register(True)

    c1 = Customer(40)
    c2 = Customer(20)

    array = RegisterArray(5)
    print(array.registers[0])
    array.registers[0].open = True
    array.registers[3].open = True
    array.registers[4].open = True
    array.registers[0].enqueue(c1)
    array.registers[3].enqueue(c2)

    # TODO: AND CUSTOMER POOL ISNT EMPTY
    while (not array.isFinished()):
        array.tick()

    print(array.tickCount)

    # array.addRegister(r1)
    # array.addRegister(r2)

    s = Store(10, array)
    print(s)


    # print(r1)
    # print(r2)
    print(c1)
    print(c2)


def sim(customers_per_hour, open_registers, register_array_size):
    # print("Running simulation with:\n \
            # Expected customers per hour: {}\n \
            # Open Registers: {}\n \
            # Register Array Size: {}\n".format(customers_per_hour,
                # open_registers, register_array_size))

    registerArraySize = register_array_size
    registerArray = RegisterArray(registerArraySize)
    for number in open_registers:
        registerArray.registers[number].open_register()

    expected_number_of_customers_in_hour = customers_per_hour
    average_per_minute = expected_number_of_customers_in_hour / 60

    # how many people enter the store every minute
    # calculated by doing a poisson distribution

    avg_checkout_time = 2
    # TODO: have to find a good standard deviation
    standard_dev = 0.5
    customer_actual_time = 0
    for i in range(0, 60):
        sample = np.random.poisson(average_per_minute)

        # Get a random time for how long it takes to do groeries
        # via normal distribution
        # This has a figure from data -- avg time per week thing


        durations = np.random.normal(avg_checkout_time,
                                     standard_dev, sample)
        customers = list(map(lambda duration: Customer(duration), durations))

        # For each customer, choose a register
        for customer in customers:
            chosenReg = customer.choose_register(
                        np.random.randint(0, registerArraySize),
                        registerArray)
            registerArray.enqueue(customer, chosenReg)
            customer_actual_time += customer.actual_time_to_checkout

        registerArray.tick(False)

    while (not registerArray.isFinished()):
        registerArray.tick(False)

    customer_avg_time = customer_actual_time / expected_number_of_customers_in_hour 
    print("----end----")
    print("TickCount: {}".format(registerArray.tickCount))
    print("Customer avg time checkout: {}".format(customer_avg_time))

    return {"tickCount": registerArray.tickCount, "customer_avg":
            customer_avg_time}


def find_max_registers(expected_customers, acceptable_time):
    acceptable_found = False

    # run 40 times so that you eliminate error
    num_sims = 40
    arraySize = 1
    while (not acceptable_found):
        count = 0

        for i in range(0, num_sims):
            count += sim(expected_customers, np.arange(arraySize),
            arraySize)['customer_avg']

        actual = count/num_sims
        # print("count/num_sims for arraySize {} is {}".format(arraySize, actual))
        if actual <= acceptable_time:
            print("Found!")
            return arraySize

        arraySize += 1


def run_sample_sims():
    tickCount = 0
    num_of_sims = 10
    # Run same simulation 100 times
    # for i in range(0, num_of_sims):
        # tickCount += sim(100000, [1, 3, 5, 7, 9], 15)
    # 13052 for above

    # for i in range(0, num_of_sims):
        # tickCount += sim(100000, [1,2,3,4,5], 15)
    # 19907 for above

    # for i in range(0, num_of_sims):
        # tickCount += sim(100000, [5,6,7,8,9], 15)
    # 12026 for above

    avgTickCount = tickCount / num_of_sims

    # ---------- START -------------- #
    sim_setups = [
            {
                "people": 500,
                "pattern": [1, 3, 5, 7, 9],
                "lanes": 15
            },
            {
                "people": 500,
                "pattern": [1, 2, 3, 4, 5],
                "lanes": 15
            },
            {
                "people": 500,
                "pattern": [2, 3, 4, 5, 6],
                "lanes": 15
            },
            {
                "people": 500,
                "pattern": [5, 6, 7, 8, 9],
                "lanes": 15
            },
            {
                "people": 500,
                "pattern": [1, 4, 7, 11, 14],
                "lanes": 15
            }
        ]

    result = []
    # Run simulations
    for setup in sim_setups:
        tickCount = 0
        for i in range(0, num_of_sims):
            tickCount += sim(setup['people'], setup['pattern'],
                    setup['lanes'])['tickCount']

        avgTickCount = tickCount / num_of_sims
        result.append({"pattern": setup['pattern'], "result": avgTickCount})

    # Transform to be able to graph
    X = list(map(lambda item: item['pattern'], result))
    X = list(map(lambda item: ', '.join(map(str, item)), X))
    X = list(map(lambda item: "pattern: " + item, X))

    Y = list(map(lambda item: item['result'], result))

    print("X is {}\nY is {}".format(X, Y))

    data = [go.Bar(x=X, y=Y)]

    py.plot(data, filename='basic-bar2')

    print(result)


def max_reg_sims():
    accept_time = 5
    result = []

    for i in range(100, 520, 30):
        result.append([i, find_max_registers(i, accept_time)])

    X = list(map(lambda item: item[0], result))
    Y = list(map(lambda item: item[1], result))

    data = [go.Bar(x=X, y=Y)]
    py.plot(data, filename='max_register')


if __name__ == '__main__':
    print("starting program...")
    # max_reg_sims()
    # find_max_registers(400, 5)
    run_sample_sims()


# TickCount is how long to service EVERYONE in one hour
