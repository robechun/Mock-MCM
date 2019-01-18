class Customer:
    checkout_time_hour = 0
    field_of_vision = 3  # for simplicity make it odd number

    def __init__(self, checkout_time_hour):
        self.checkout_time_hour = checkout_time_hour

    # Available lanes are given to you.
    # Choose the one with the shortest wait time
    # return: chosen lane
    def choose_register(self, randomStart, registerArray):
        # print("within choose_register")
        # print("randomstart is: {}".format(randomStart))
        diff = int((self.field_of_vision - 1) / 2)
        arrayLength = len(registerArray.registers)

        # print("diff is: {}".format(diff))
        # print("arrayLength is: {}".format(arrayLength))
        if randomStart - diff < 0:
            possible = registerArray.registers[0:self.field_of_vision]
        elif randomStart + diff + 1 > arrayLength:
            possible = registerArray.registers[arrayLength -
                                               self.field_of_vision:arrayLength]
        else:
            possible = registerArray.registers[randomStart-diff:randomStart+diff+1]
        
        # print("before error")
        # print(possible)
        possible = list(filter(lambda p: p.open, possible))
        # print(possible)

        chosen = None
        found = False
        # If all are closed, find the closest one that's open
        if len(possible) == 0:
            i = randomStart
            j = 0

            while (i-j >= 0 or i+j < arrayLength):
                if found:
                    break
                if i+j < arrayLength and registerArray.registers[i+j].open:
                    found = True
                    chosen = registerArray.registers[i+j]
                if i-j >= 0 and registerArray.registers[i-j].open:
                    found = True
                    chosen = registerArray.registers[i-j]

                j += 1

            if not found:
                raise Exception("No possible register for customer. Random start: {}, i: {}, j: {}".format(randomStart, i, j))
        else:
            chosen = min(possible, key=lambda reg: reg.current_wait)

        # print(chosen)
        return chosen

    def __str__(self):
        return "Customer checkout time in hours:{}".format(self.checkout_time_hour)


# registerArray -> choose random spot -> give closest x lanes to "choose_lane"
# -> return lane chosen -> enqueue into Register

# TODO: customers come in parallel sometimes and not at other times (staggered)
