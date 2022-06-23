import csv
from hashmap import HashMap
from package import Package

hash_map = HashMap()
low_priority_packages = []  # No deadline
medium_priority_packages = []  # 10:30 delivery time deadline
high_priority_packages = []  # 9:00 delivery time deadline


# Imports the package date from package_info.csv, converts the data into Package objects and inserts those
# objects into the hashmap and into different lists based on the Package's priority
# O(n)
def import_data():
    with open('package_info.csv') as csv_file1:
        package_info_csv = list(csv.reader(csv_file1, delimiter=','))

    for row in package_info_csv:
        key = row[0]
        location_number = row[1]  # For compatibility with distance table
        address = row[2]
        city = row[3]
        state = row[4]
        zipcode = row[5]
        deadline = row[6]
        weight = row[7]
        notes = row[8]
        new_package = Package(key, location_number, address, city, state, zipcode, deadline, weight, notes)
        hash_map.add(key, new_package)
        prioritize_package(new_package)


# Prioritizes each package
# O(1)
def prioritize_package(package):
    if '9:00' in package.deadline:
        high_priority_packages.append(package)
        package.priority = 1
    elif '10:30' in package.deadline:
        medium_priority_packages.append(package)
        package.priority = 2
    else:
        low_priority_packages.append(package)
        package.priority = 3


def get_hash_map():
    return hash_map


def get_low_priority_packages():
    return low_priority_packages


def get_medium_priority_packages():
    return medium_priority_packages


def get_high_priority_packages():
    return high_priority_packages


def get_all_unassigned_packages():
    unassigned_packages = high_priority_packages + medium_priority_packages + low_priority_packages
    return unassigned_packages
