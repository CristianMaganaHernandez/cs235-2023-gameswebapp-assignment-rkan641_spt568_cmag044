
import csv
import os

from games.domainmodel.model import User


# Uncommented for now
# class UserDataCSVWriter:
#
#     def __init__(self, filename):
#         self.__filename = filename
#
#     def write_csv_file(self, user: User):
#         if not os.path.exists(self.__filename):
#             print(f"path {self.__filename} does not exist!")
#             return
#
#         with open(self.__filename, 'w', encoding='utf-8-sig') as file:
#             writer = csv.DictWriter(file)
#             username, password = user.username, user.password
#             writer.writerow({'username': username, 'password': password})
#
#
