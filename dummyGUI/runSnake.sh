#!/bin/bash
python3 snakeio_driver.py -i 4 -o 1 -h 2 -l 0 &
python3 snakeio_driver.py -i 4 -o 1 -h 2 -l 1 &
python3 snakeio_driver.py -i 4 -o 1 -h 3 -l 2 &