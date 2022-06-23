import datetime


# Truck Class
class Truck:

    def __init__(self, name):
        self.miles = 0
        self.current_location = 0  # 0 = Hub. This value is determined from the distance_table.csv (row 1 = 0, row 2 = 1.. etc)
        self.packages = []  # Packages that will be delivered by the truck in the order they are indexed.
        self.time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))
        self.start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))  # To see if truck is out for delivery
        self.bunch = []  # Packages in the bunch are packages on the way to a priority package's location, including the priority package.
        self.restricted_packages = []  # Packages that cannot be on a truck
        self.linked_packages = []  # Packages that have to be included on a truck
        self.name = name
