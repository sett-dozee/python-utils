import time
from random import randrange, choice
import numpy as np

# Structure : event, timestamp, eventValue, eventDescription, MSB, LSB
max_events = 53
max_eventValue = 10
max_eventDescription = 86
msb = 0
lsb = 0

valid_ranges_eventVal = {0 : {"VAL" : [0, 2], "DES" : [0, 12]},
                         1 : {"VAL" : [0, 3], "DES" : [0, 11]},
                         3 : {"DES" : [0, 5]},
                         4 : {"VAL" : [0, 2]},
                         5 : {"VAL" : [0, 2]},
                         6 : {"VAL" : [0, 2]},
                         7 : {"VAL" : [0, 2]},
                         8 : {"VAL" : [0, 4]},
                         9 : {"VAL" : [0, 2]},
                         10 : {"VAL" : [0, 4]},
                         11 : {"VAL" : [0, 4]},
                         12 : {"VAL" : [0, 4]},
                         13 : {"VAL" : [0, 4]},
                         14 : {"VAL" : [0, 2]},
                         16 : {"VAL" : [0, 2]},
                         17 : {"VAL" : [0, 2]},
                         18 : {"VAL" : [0, 2], "DES" : [0, 13]},
                         19 : {"VAL" : [0, 2], "DES" : [0, 86]},
                         20 : {"VAL" : [0, 3]},
                         21 : {"VAL" : [0, 2]},
                         22 : {"VAL" : [0, 7], "DES" : [0, 15]},
                         26 : {"VAL" : [0, 10]},
                         28 : {"VAL" : [0, 4]},
                         30 : {"VAL" : [0, 4]},
                         39 : {"VAL" : [0, 3]},
                         41 : {"VAL" : [0, 4]},
                         42 : {"VAL" : [0, 5]},
                         43 : {"VAL" : [0, 2]},
                         44 : {"VAL" : [0, 6]},
                         45 : {"VAL" : [0, 6]},
                         46 : {"VAL" : [0, 6]},
                         47 : {"VAL" : [0, 6]},
                         # 52 : {"VAL" : [0, 4]},
                         }


def method_finder(classname):

    non_magic_class = []

    class_methods = dir(classname)

    for m in class_methods:

        if m.startswith('__'):

            continue

        else:

            non_magic_class.append(m)

    return non_magic_class


class EVENT_GENERATOR():
    def __init__(self):
        self.events = self.EVENTS(self)
        self.all_events = []
        self.all_valid_events = []

        def create_all_possible_events():
            timestamp = int(time.time())
            print(f"Timestamp start : {timestamp}")
            all_events = []
            total_events_created = 0
            print("Creating all possible events")
            for event in range(0, max_events):
                for eventValue in range(0, max_eventValue):
                    for eventDescription in range(0, max_eventDescription + 1):
                        event_string = f"{event},{timestamp},{eventValue}," + \
                                       f"{eventDescription},0,0\n"
                        timestamp += 1
                        total_events_created += 1
                        all_events.append(event_string)

            print(f"Created = {total_events_created}")
            self.all_events = all_events

        def create_all_possible_valid_events():
            timestamp = int(time.time())
            print(f"Timestamp start : {timestamp}")
            all_events = []
            total_events_created = 0
            print("Creating all possible valid events")
            for event in range(0, max_events + 1):
                if event in valid_ranges_eventVal.keys():
                    if "VAL" in valid_ranges_eventVal[event].keys():
                        eventVal_min = valid_ranges_eventVal[event]["VAL"][0]
                        eventVal_max = valid_ranges_eventVal[event]["VAL"][1]
                    else:
                        eventVal_min = 0
                        eventVal_max = 10
                else:
                    eventVal_min = 0
                    eventVal_max = 10
                if event in valid_ranges_eventVal.keys():
                    if "DES" in valid_ranges_eventVal[event].keys():
                        eventDesc_min = valid_ranges_eventVal[event]["DES"][0]
                        eventDesc_max = valid_ranges_eventVal[event]["DES"][1]
                    else:
                        eventDesc_min = 0
                        eventDesc_max = 86
                else:
                    eventDesc_min = 0
                    eventDesc_max = 86
                for eventValue in range(eventVal_min, eventVal_max):
                    for eventDescription in range(eventDesc_min, eventDesc_max):
                        event_string = f"{event},{timestamp},{eventValue}," + \
                                       f"{eventDescription},0,0\n"
                        timestamp += 1
                        total_events_created += 1
                        all_events.append(event_string)
            print(f"Created = {total_events_created}")
            self.all_valid_events = all_events

        create_all_possible_events()
        create_all_possible_valid_events()
        self.events.methods = method_finder(EVENT_GENERATOR.EVENTS)

    def generate_random_10_digit_number():
        num = ""
        for i in range(0, 10):
            digit = randrange(10)
            num += str(digit)
        return num

    def put_all_possible_events_in_file(self, filename, number=-1):
        file = open(filename, "a")
        total = len(self.all_events)
        event_written = 0
        for i in range(0, total):
            selected = randrange(0, len(self.all_events))
            event = self.all_events[selected]
            timestamp = str(int(time.time()))
            event = event.split(",", 1)[0] + "," + timestamp + "," + \
                event.split(",", 2)[2]
            print(self.all_events[selected])
            self.all_events.pop(selected)
            file.write(event)
            event_written += 1
            if event_written == number:
                break
        file.close()

    def put_valid_events_in_file(self, filename, number=-1):
        file = open(filename, "a")
        total = len(self.all_valid_events)
        event_written = 0
        for i in range(0, total):
            selected = randrange(0, len(self.all_valid_events))
            event = self.all_valid_events[selected]
            timestamp = str(int(time.time()))
            event = event.split(",", 1)[0] + "," + timestamp + "," + \
                event.split(",", 2)[2]
            self.all_valid_events.pop(selected)
            file.write(event)
            event_written += 1
            if event_written == number:
                break
        print(f"Valid events created = {event_written}")
        file.close()

    def put_events_different_types_in_file(self, filename, total_events_to_create):
        file = open(filename, "a")
        event_written = 0
        functions = [self.events.create_empty_line_event,
                     self.events.create_crlf_event,
                     self.events.create_event_with_invalid_characters,
                     self.events.create_random_event_from_given_ranges,
                     self.events.get_an_event_from_all_possible_integer_events
                     ]
        weights = [1/100, 1/100, 2/100, 4/100, 92/100]

        file = open(filename, "a")
        while event_written < total_events_to_create:
            selected_func = np.random.choice(functions, 1, p=weights)[0]
            print(selected_func)
            event_string = selected_func()
            file.write(event_string)
            event_written += 1
        file.close()
        print(f"Finished writing events to file {filename}")


    class EVENTS():
        def __init__(self, ev_g):
            self.ev_g = ev_g

        def create_empty_line_event(self):
            return "\n"

        def create_crlf_event(self):
            return "\r\n"

        def create_event_with_invalid_characters(self, invalid_only=False):
            ascii_ranges = [[0, 9], [11, 12], [14, 47],
                            [58, 64], [91, 96],
                            [123, 127]]
            full_range = [0, 127]
            length = randrange(1, 50)
            current = 0
            event_string = ""
            while current < length:
                if invalid_only:
                    range_selected = randrange(len(ascii_ranges))
                    ascii_picked = randrange(ascii_ranges[range_selected][0],
                                             ascii_ranges[range_selected][1] + 1)
                else:
                    ascii_picked = randrange(full_range[0],
                                             full_range[1] + 1)
                character = chr(ascii_picked)
                event_string += character
                current += 1
            return event_string

        def create_random_event_from_given_ranges(self,
                                                  max_events=53,
                                                  max_eventValue=111,
                                                  max_eventDescription=86,
                                                  randomize_timestamp=False):
            timestamp = int(time.time())
            print(f"Timestamp start : {timestamp}")

            event = randrange(max_events + 1)
            eventValue = randrange(max_eventValue + 1)
            eventDescription = randrange(max_eventDescription + 1)
            if randomize_timestamp:
                timestamp = self.ev_g.generate_random_10_digit_number()
            else:
                timestamp += 1
            event_string = f"{event},{timestamp},{eventValue}," + \
                           f"{eventDescription},0,0\n"
            return event_string

        def get_an_event_from_all_possible_integer_events(self):
            selected = randrange(0, len(self.ev_g.all_events))
            return self.ev_g.all_events[selected]


if __name__ == "__main__":
    event_generator = EVENT_GENERATOR()
    event_generator.put_all_possible_events_in_file("events.txt", -1)
    # event_generator.put_valid_events_in_file("events.txt", -1)
