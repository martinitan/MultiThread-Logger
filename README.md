# MultiThread-Logger

This Repo Is a work in progress library for a logging tool to be used on multi-threaded projects in python. 

The goal of this tool is collect log data from many threads and create a single logfile which is ordered in a linear time. 

The log data will be managed through shared memory. A persistent thread will handle ordering and saving the log data to the logfile.

WIP documentation found at https://docs.google.com/document/d/1ruY6W8oYo5NYqHy7JW1HHzXsUsheJmmQk22SUhV3YAo/edit?usp=sharing
