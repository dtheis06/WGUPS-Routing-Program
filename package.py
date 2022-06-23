# Package class

class Package:

    def __init__(self, key, location_number, address, city,
                 state, zipcode, deadline, weight, notes):
        self.key = key
        self.location_number = location_number  # The location number gathered from the csv folder (ie 0 = hub)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = 'At Hub'
        self.delivery_time = ""
        self.priority = 0  # Based on deadline. (1->Deadline = 9:00AM, 2->Deadline = 10:30AM, 3->Deadline = EOD)
        self.on_time = True
