import sys, os

pipe_command_path = "/tmp/servmond_command"
pipe_result_path = "/tmp/servmond_result"

if not os.path.exists(pipe_command_path) or not os.path.exists(pipe_result_path):
    print("Daemon not running!")
    exit(1)

pipe_command = open(pipe_command_path, 'w')
pipe_result = open(pipe_result_path, 'r')

pipe_command.write("kernel\n")
print(pipe_result.read())