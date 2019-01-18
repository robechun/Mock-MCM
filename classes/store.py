from register import RegisterArray
from customer import Customer

import plotly

import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go


class Store:
    # TODO: does this even matter since ppl are approaching the
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
    # for i in range(0, 15):
        # registerArray.registers[i].open_register()

    expected_number_of_customers_in_hour = customers_per_hour
    average_per_minute = expected_number_of_customers_in_hour / 60

    # how many people enter the store every minute
    # calculated by doing a poisson distribution
    # TODO: for actual use, need to know how many PEOPLE go to the store.
    for i in range(0, 60):
        sample = np.random.poisson(average_per_minute)

        # Get a random time for how long it takes to do groeries
        # via normal distribution
        # This has a figure from data -- avg time per week thing

        # TODO: have to find a good standard deviation
        average_time_in_grocery_store_min = 20
        standard_dev = 10

        durations = np.random.normal(average_time_in_grocery_store_min,
                                     standard_dev, sample)
        customers = list(map(lambda duration: Customer(duration), durations))

        # TODO: figure out how to incorporate open/closed registers

        # For each customer, choose a register
        for customer in customers:
            chosenReg = customer.choose_register(
                        np.random.randint(0, registerArraySize),
                        registerArray)
            registerArray.enqueue(customer, chosenReg)

        while (not registerArray.isFinished()):
            registerArray.tick(False)

    print("----end----")
    print("TickCount: {}".format(registerArray.tickCount))

    return registerArray.tickCount


if __name__ == '__main__':
    print("starting program...")
    # test()

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

    sim_setups = [
            {
                "people": 100000,
                "pattern": [1, 3, 5, 7, 9],
                "lanes": 15
            },
            {
                "people": 100000,
                "pattern": [1, 2, 3, 4, 5],
                "lanes": 15
            },
            {
                "people": 100000,
                "pattern": [2, 3, 4, 5, 6],
                "lanes": 15
            },
            {
                "people": 100000,
                "pattern": [5, 6, 7, 8, 9],
                "lanes": 15
            },
            {
                "people": 100000,
                "pattern": [1, 4, 7, 11, 14],
                "lanes": 15
            }
        ]

    result = []
    # Run simulations
    for setup in sim_setups:
        tickCount = 0
        for i in range(0, num_of_sims):
            tickCount += sim(setup['people'], setup['pattern'], setup['lanes'])

        avgTickCount = tickCount / num_of_sims
        result.append({"pattern": setup['pattern'], "result": avgTickCount})

    # Transform to be able to graph
    X = list(map(lambda item: item['pattern'], result))
    X = list(map(lambda item: ', '.join(map(str, item)), X))
    X = list(map(lambda item: "pattern: " + item, X))

    Y = list(map(lambda item: item['result'], result))

    print("X is {}\nY is {}".format(X, Y))

    data = [go.Bar(x=X, y=Y)]

    py.plot(data, filename='basic-bar')

    print(result)
