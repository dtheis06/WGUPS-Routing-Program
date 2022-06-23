import datetime

from csv_reader import *
from datetime import timedelta

high_priority_packages = get_high_priority_packages()
medium_priority_packages = get_medium_priority_packages()
low_priority_packages = get_low_priority_packages()
next_location = 0


# If a package has a note disallowing it from being on a truck, the package will be added to the truck's restricted_packages list
# O(n^2)
def sort_packages_with_notes(truck):
    if "Truck 1" in truck.name or "Truck 3" in truck.name:
        for package in get_all_unassigned_packages():
            if "truck 2" in package.notes or "Wrong" in package.notes:
                truck.restricted_packages.append(package)
            elif "Truck 1" in truck.name and "Delayed" in package.notes:
                truck.restricted_packages.append(package)
            elif "Truck 1" in truck.name and "with" in package.notes:
                for word in package.notes.replace(",", "").split():
                    if word.isdigit():
                        for package2 in get_all_unassigned_packages():
                            if int(package2.key) == int(word):
                                truck.linked_packages.append(package2)
                truck.linked_packages.append(package)


# Removes packages that are already in the truck.packages list from the truck.linked_packages list
# O(n^2)
def remove_packages_already_in_truck_from_linked(truck):
    for package1 in truck.linked_packages:
        for package2 in truck.packages:
            if int(package1.key) == int(package2.key):
                truck.linked_packages.remove(package1)
    for package1 in truck.linked_packages:  # Repeated because for some reason it didn't do the job 100% the first time.
        for package2 in truck.packages:
            if int(package1.key) == int(package2.key):
                truck.linked_packages.remove(package1)
    truck.linked_packages = list(dict.fromkeys(truck.linked_packages))


# Adds the linked_package to the truck.packages list at the index before the closest package to the linked_package is located
# O(n)
def add_linked_package_to_closest_package(linked_package, truck):
    lowest_distance = 999
    lowest_package = None
    lowest_index = None
    for i in range(len(truck.packages) - 1):
        distance = distance_calculator(truck.packages[i].location_number, linked_package.location_number)
        if distance < lowest_distance:
            lowest_distance = distance
            lowest_package = truck.packages[i]
            lowest_index = i
    if truck.packages[-1].key != truck.packages[-2].key:
        if truck.packages[-1].priority == 2:
            medium_priority_packages.append(truck.packages[-1])
        else:
            low_priority_packages.append(truck.packages[-1])
        truck.packages.pop()
        truck.packages.insert(lowest_index, linked_package)
    elif truck.packages[-3].key != truck.packages[-2].key and truck.packages[-3].key != truck.packages[-4].key:
        if truck.packages[-3].priority == 2:
            medium_priority_packages.append(truck.packages[-3])
        else:
            low_priority_packages.append(truck.packages[-3])
        truck.packages.pop(-3)
        truck.packages.insert(lowest_index + 1, linked_package)
    else:
        if truck.packages[-4].priority == 2:
            medium_priority_packages.append(truck.packages[-4])
        else:
            low_priority_packages.append(truck.packages[-4])
        truck.packages.pop(-4)
        truck.packages.insert(lowest_index + 1, lowest_package)


# Checks if a package is on the truck's restricted_packages list
# O(n)
def restricted_package_check(package1, truck):
    flag = False
    for package2 in truck.restricted_packages:
        if package1.key == package2.key:
            flag = True
    return flag


# Calculate the distance between location_number1 and location_number2 by checking distance_table.csv
# O(1)
def distance_calculator(location_number1, location_number2):
    with open('distance_table.csv') as file2:
        distance_table_csv = list(csv.reader(file2, delimiter=','))
    if int(location_number1) < int(location_number2):
        distance = float(distance_table_csv[int(location_number2)][int(location_number1)])
    else:
        distance = float(distance_table_csv[int(location_number1)][int(location_number2)])
    return distance


# Gets the closest priority package to the truck's current location
# O(n)
def get_closest_package(truck):
    next_package = None
    array_of_packages = []
    if len(high_priority_packages) > 0:
        array_of_packages = high_priority_packages
    elif len(medium_priority_packages) > 0:
        array_of_packages = medium_priority_packages
    elif len(low_priority_packages) > 0:
        array_of_packages = low_priority_packages
    lowest_distance = 999
    global next_location
    for package1 in array_of_packages:
        package1_distance = distance_calculator(package1.location_number, truck.current_location)
        if package1_distance < lowest_distance and not (restricted_package_check(package1, truck)):
            lowest_distance = package1_distance
            next_location = package1.location_number
            next_package = package1
    return next_package


# Adds lesser priority packages on the way from the truck's current location to the next higher priority package to truck.bunch
# Also the next package will be added to the bunch
# The packages in the bunch will be in the order they will be delivered.
# O(n)
def check_for_less_priority_packages_nearby(truck):
    all_packages = get_all_unassigned_packages()
    next_package = get_closest_package(truck)
    for package in all_packages:
        distance_to_current_location = distance_calculator(package.location_number, truck.current_location)
        distance_to_next_location = distance_calculator(package.location_number, next_location)
        current_to_next_distance = distance_calculator(next_package.location_number, truck.current_location)
        if package.location_number != next_package.location_number and distance_to_current_location + distance_to_next_location <= (
                current_to_next_distance * 1.05) and not (restricted_package_check(package, truck)):
            truck.bunch.append(package)
        elif package.location_number == next_location and not (
                restricted_package_check(package, truck)) and package.key != next_package.key:
            truck.bunch.insert(len(truck.bunch), package)
    truck.bunch.append(next_package)


# Add current bunch of packages to truck.packages and reset the bunch to allow for a new bunch if there's more room on the truck
# O(n^2)
def add_bunch(truck):
    if len(truck.bunch) > 0:
        last_package = truck.bunch[(len(truck.bunch) - 1)].location_number
        truck.current_location = last_package
    while len(truck.bunch) + len(truck.packages) > 16:  # If adding the bunch will make the truck have > 16 packages
        truck.bunch.pop()  # Remove packages until it'll be <= 16
    if len(truck.bunch) > 0:
        for package in truck.bunch:  # Adds each package in the bunch to the truck.packages list
            truck.packages.append(package)
            remove_from_priority_package_list(package)  # This method alone is #O(n)
    truck.bunch.clear()


# Removes the bunch_package from its priority package list
# O(n)
def remove_from_priority_package_list(bunch_package):
    if bunch_package.priority == 1:
        for high_priority_package in high_priority_packages:
            if high_priority_package.key == bunch_package.key:
                high_priority_packages.remove(high_priority_package)
    elif bunch_package.priority == 2:
        for medium_priority_package in medium_priority_packages:
            if medium_priority_package.key == bunch_package.key:
                medium_priority_packages.remove(medium_priority_package)
    elif bunch_package.priority == 3:
        for low_priority_package in low_priority_packages:
            if low_priority_package.key == bunch_package.key:
                low_priority_packages.remove(low_priority_package)


# Adds packages that are on the way back to the hub
# O(n)
def return_to_hub(truck):
    all_packages = get_all_unassigned_packages()
    for package in all_packages:
        if len(truck.bunch) + len(truck.packages) < 16:
            distance_to_current_location = distance_calculator(package.location_number, truck.current_location)
            distance_to_hub = distance_calculator(package.location_number, 0)
            current_to_hub = distance_calculator(truck.current_location, 0)
            if distance_to_current_location + distance_to_hub <= (
                    current_to_hub * 1.05) and not restricted_package_check(package, truck):
                truck.bunch.append(package)


# Fills the truck with packages in the order they will be delivered. (index 0 is delivered first)
# O(n^2)
def fill_truck(truck, time):
    global next_location
    while len(truck.packages) + len(truck.bunch) < 15 and len(get_all_unassigned_packages()) > 0:
        check_for_less_priority_packages_nearby(truck)
        add_bunch(truck)
    return_to_hub(truck)
    add_bunch(truck)
    if len(truck.linked_packages) > 0:
        remove_packages_already_in_truck_from_linked(truck)
        for package in truck.linked_packages:
            add_linked_package_to_closest_package(package, truck)
            priority = package.priority
            if priority == 2:
                medium_priority_packages.remove(package)
            elif priority == 3:
                low_priority_packages.remove(package)
    calculate_miles_and_time(truck, time)
    truck.current_location = 0
    next_location = 0
    empty_truck(truck)


# Calculates the miles added and time added for each delivery
# O(n)
def calculate_miles_and_time(truck, time):
    first_package_distance = distance_calculator(truck.packages[0].location_number, 0)
    time_add(truck, first_package_distance)
    if truck.time < time:
        truck.miles += first_package_distance
    update_delivery_status(0, time, truck)
    for i in range(1, len(truck.packages) - 1):
        distance = distance_calculator(truck.packages[i].location_number, truck.packages[i - 1].location_number)
        time_add(truck, distance)
        if truck.time < time:
            truck.miles += distance
        update_delivery_status(i, time, truck)
    last_delivery_distance = distance_calculator(truck.packages[-1].location_number, truck.packages[-2].location_number)
    if truck.time < time:
        truck.miles += last_delivery_distance
    time_add(truck, last_delivery_distance)
    update_delivery_status(len(truck.packages) - 1, time, truck)
    distance_back_to_hub = distance_calculator(truck.packages[-1].location_number, 0)
    time_add(truck, distance_back_to_hub)
    if truck.time < time:
        truck.miles += distance_back_to_hub


# Changes package information based on when the package is delivered/expected to be delivered
# O(1)
def update_delivery_status(i, time, truck):
    h = get_hash_map()
    a_key = truck.packages[i].key
    if truck.time <= time:
        h.get(a_key).delivery_time = truck.time
        check_on_time(truck, i)
        h.get(a_key).status = "Delivered by: " + truck.name + " " + on_time_print(truck.packages[i]) + " at " + str(h.get(a_key).delivery_time)
        # truck.packages[i].delivery_time = "Delivered at: " + str(truck.time) + " by: " + truck.name
        # truck.packages[i].status = "Delivered"
    elif truck.start_time > time:
        h.get(a_key).delivery_time = ""
        # truck.packages[i].delivery_time = "Expected to be delivered at: " + str(truck.time)
    elif truck.time > time:
        h.get(a_key).delivery_time = ""
        h.get(a_key).status = "En route on: " + truck.name
        # truck.packages[i].delivery_time = "Expected to be delivered at: " + str(truck.time)
        # truck.packages[i].status = "En route on: " + truck.name

# Returns as a string if the package was delivered on time
# O(1)
def on_time_print(package):
    if package.on_time:
        return "on time"
    else:
        return "not on time"

# Checks to see if a package was delivered on time. If not, it changes the package's on_time value to False
# O(1)
def check_on_time(truck, i):
    if truck.packages[i].priority == 1:
        if truck.packages[i].delivery_time > datetime.datetime.combine(datetime.date.today(), datetime.time(9, 0)):
            truck.packages[i].on_time = False
    elif truck.packages[i].priority == 2:
        if truck.packages[i].delivery_time > datetime.datetime.combine(datetime.date.today(), datetime.time(10, 30)):
            truck.packages[i].on_time = False


# Empties all packages from truck.packages
# O(n)
def empty_truck(truck):
    truck.packages.clear()


# Calculates and adds the time traveled to truck.time
# O(n)
def time_add(truck, distance):
    minutes = distance * 3
    seconds = distance * 20
    time_change = timedelta(minutes=minutes, seconds=seconds)
    new_time = truck.time + time_change
    truck.time = new_time


# Gets all packages that are currently unassigned to a truck
# O(1)
def get_all_unassigned_packages():
    unassigned_packages = high_priority_packages + medium_priority_packages + low_priority_packages
    return unassigned_packages


# Sets truck 2's time to 10:30(Truck 2's starting point)
# O(1)
def set_time_truck2(truck2):
    time_change = timedelta(hours=2, minutes=30)
    new_time = truck2.time + time_change
    truck2.time = new_time
    truck2.start_time = new_time


# Sets truck 3's time to 9:05(Truck 3's starting point)
# 0(1)
def set_time_truck3(truck3):
    time_change = timedelta(hours=1, minutes=5)
    new_time = truck3.time + time_change
    truck3.time = new_time
    truck3.start_time = new_time

# def sort_hash_map():
#     h = get_hash_map()
#     temp = []
#     hash_it = iter(h)
#     for i in range(40):
#         package = next(hash_it)
#         temp.append(package)
#         h.delete(i)
#     temp.sort(key=lambda x: int(x.key))
#     for package in temp:
#         h.add(package.key, package)

# # Test stuff
#
# import_data()
# h = get_hash_map()
# # h.print()
# temp = []
# hash_it = iter(h)
# package1 = Package(41,2,1,1,1,1,1,1,1)
# temp.append(package1)
# for i in range(40):
#     package = next(hash_it)
#     temp.append(package)
#     h.delete(i)
# temp.sort(key=lambda x: int(x.key))
# for package in temp:
#     h.add(package.key, package)
# h.print()
# key = str(3)
# print(h.get(key).key)
# # hash_it = iter(h)
# # for i in range(40):
# #     print(next(hash_it).key)
# truck1 = Truck("truck1")
# truck2 = Truck("truck2")
# truck3 = Truck("truck3")
# sort_packages_with_notes(truck1)
# sort_packages_with_notes(truck2)
# sort_packages_with_notes(truck3)
# fill_truck(truck1)
# print("-------Truck 1 IDs-------------")
# for package in truck1.packages:
#     print(package.key)
# set_time_truck3(truck3)
# fill_truck(truck3)
# print("---------Truck 3 IDs-------------")
# for package in truck3.packages:
#     print(package.key)
# set_time_truck2(truck2, truck1)
# fill_truck(truck2)
# print("---------Truck 2 IDs-------------")
# for package in truck2.packages:
#     print(package.key)
# # print("truck1 miles: " + str(truck1.miles))
# # print("truck2 miles: " + str(truck2.miles))
# # print("truck3 miles: " + str(truck3.miles))
# # print(str(truck1.miles + truck2.miles + truck3.miles))
# # print("done")
