"""
@File    :   t.py
@Time    :   2023/09/18 18:02:25
@Author  :   glx 
@Version :   1.0
@Contact :   18095542g@connect.polyu.hk
@Desc    :   test algorithm
"""

# here put the import lib

from solver import *
import ortools_solver
import logging
import os

logging.basicConfig(
    filename="algorithm.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


list_dir = os.listdir("data")
for file in list_dir:
    # file_location = r"./data/ks_4_0"
    file_location = os.path.join("./data", file)
    with open(file_location, "r") as input_data_file:
        input_data = input_data_file.read()
    # parse the input
    lines = input_data.split("\n")

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))
    t = len(items)
    # if len(items) > 99:
    #     continue
    # print(dp_solver(items, capacity))
    values = dp_solver(items, capacity)[0]
    logging.info(
        f"problem scale: {len(items)} \n Algorithm: dp solver \n result: {values}"
    )

    values = ortools_solver.ortools_solver(items, capacity)[0]
    logging.info(
        f"problem scale: {len(items)} \n Algorithm: ortools solver \n result: {values}"
    )
    # break
    # print(ortools_solver.ortools_solver(items, capacity))
