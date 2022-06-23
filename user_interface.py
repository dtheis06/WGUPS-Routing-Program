import datetime
from algorithm import *

# Welcome menu that appears in the console when you first start the program
# o(n)
from truck import Truck


def menu():
    print()
    print("Welcome to the Western Governors University Parcel Service's Package Information System")
    print()
    repeated_menu()


# Part of the menu that appears at launch and repeated again after the program did what the user intended.
# O(n)
def repeated_menu():
    print("Pick an option from the choices below")
    print()
    print("[1] Option 1: View the status and information of a package")
    print("[2] Option 2: View the status and information of all packages")
    print("[3] Option 3: Exit")
    print()
    option = int(input("Enter the option number: "))
    if option == 1:
        option_1()
        repeated_menu()
    if option == 2:
        option_2()
        repeated_menu()
    if option == 3:
        quit()


# When you select option one, this method runs
# O(n^2)
def option_1():
    key = input("Enter the key of the package: ")
    truck1, truck2, truck3 = algorithm()
    h = get_hash_map()
    package = h.get(int(key))
    print("")
    print("")
    print("Miles Traveled:")
    print("Truck 1: " + str(truck1.miles) + " miles")
    print("Truck 2: " + str(truck2.miles) + " miles")
    print("Truck 3: " + str(truck3.miles) + " miles")
    print("Total  : " + str(truck1.miles + truck2.miles + truck3.miles) + " miles")
    print("")
    print("PACKAGE INFORMATION")
    print("Key: " + package.key)
    print("Address: " + package.address)
    print("City: " + package.city)
    print("State: " + package.state)
    print("Zipcode: " + package.zip)
    print("Deadline: " + package.deadline)
    print("Weight: " + package.weight)
    print("Notes: " + package.notes)
    print("Status: " + package.status)
    print(package.delivery_time)
    print()


# When you select option 2, this method runs.
# O(n^2)
def option_2():
    flag = 0
    more_deliveries = False
    h = get_hash_map()
    truck1, truck2, truck3 = algorithm()
    hash_it = iter(h)
    for i in range(40):
        package = next(hash_it)
        if not package.on_time:
            flag = 1
        if "Delivered" not in package.status:
            more_deliveries = True
        print("Package " + str(
            package.key) + ": " + package.address + ", " + package.city + ", " + package.zip + ", " + "Deadline: " + package.deadline + ", Weight: " + package.weight + "oz" + ", Notes: " + package.notes + " Status: " + package.status)
    print("")
    if flag == 0 and not more_deliveries:
        print("ALL PACKAGES DELIVERED ON SCHEDULE!")
    elif flag == 0 and more_deliveries:
        print("ALL PACKAGES CURRENTLY ON TIME")
    elif flag == 1:
        print("A package was not delivered on time")
    print("")
    print("Miles Traveled:")
    print("Truck 1: " + str(truck1.miles) + " miles")
    print("Truck 2: " + str(truck2.miles) + " miles")
    print("Truck 3: " + str(truck3.miles) + " miles")
    print("Total distance traveled  : " + str(truck1.miles + truck2.miles + truck3.miles) + " miles")


# This part of the algorithm runs unless option 3 is chosen
# O(n^2)
def algorithm():
    time_input = input("Enter the time in the following format(HH:mm): ")
    time = datetime.datetime.strptime(time_input, "%H:%M")
    hours = time.hour
    minutes = time.minute
    date_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hours, minutes))
    import_data()
    truck1 = Truck("Truck 1")
    truck2 = Truck("Truck 2")
    truck3 = Truck("Truck 3")
    sort_packages_with_notes(truck1)
    sort_packages_with_notes(truck2)
    sort_packages_with_notes(truck3)
    fill_truck(truck1, date_time)
    set_time_truck3(truck3)
    fill_truck(truck3, date_time)
    set_time_truck2(truck2)
    fill_truck(truck2, date_time)
    return truck1, truck2, truck3

# Test Run
# menu()
