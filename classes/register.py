class Register:
    cost_per_hour = 15  # cost per hour for each lane should actually be same
    current_wait = 0
    open = False

    def __init__(self, open):
        self.open = open

    # open and close register for available checkout
    def close_register(self):
        self.open = False

    # open and close register for available checkout
    def open_register(self):
        self.open = True

    # Add customer to queue by adding their checkout-time
    def enqueue(self, customer):
        self.current_wait += customer.checkout_time_hour

    # counter to reduce current_wait (by unit of time)
    def tick(self):
        # print("tick")
        # print(self.current_wait)
        if self.current_wait > 0:
            self.current_wait -= 1

    def __str__(self):
        return str("Current Wait: {}, Open: {}".format(self.current_wait, self.open))


class RegisterArray:
    registers = []
    tickCount = 0
    done = False

    def __init__(self, size):
        self.registers = [Register(False) for x in range(0, size)]

    # Add to the "array" in which represents ALL registers
    # Open & closed
    # TODO: prob dont need
    def addRegister(self, register):
        self.registers.append(register)

    def enqueue(self, customer, chosen):
        chosen.enqueue(customer)

    def tick(self, unconditional):
        # In cases where theres no customers in queue but are not fulfilled in
        # pool
        if unconditional:
            list(map(lambda x: x.tick(), self.registers))
            self.tickCount += 1
            return

        # Check to see if all lines are clear.
        done = list(filter(lambda x: x.current_wait <= 0, self.registers))
        if len(done) == len(self.registers):
            print("DONE!")
            self.done = True
            return

        # Tick each register
        list(map(lambda x: x.tick(), self.registers))
        self.tickCount += 1

    def isFinished(self):
        return self.done

    def __str__(self):
        toReturn = ""
        for i in range(0, len(self.registers)):
            toReturn += "Register {}: ".format(i) + self.registers[i].__str__() + "\n"

        return toReturn
