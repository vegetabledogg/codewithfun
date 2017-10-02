import subprocess
import os
import sys

input_filename = 'testin.input'
memory_limit = '8m'
time_limit = '10'
language = sys.argv[1]
input_filename = 'testin.input'
input_filepath = './{}'.format(input_filename)
user_output_filename = 'usertestout.output'
user_output_filepath = './{}'.format(user_output_filename)
user_outputfile = open('./err.out', 'a')

os.chdir('/Users/yunanlong/Desktop/codewithfun/judge/test')

container_id = subprocess.check_output(["docker", "run", "-it", "-m", memory_limit, "-d", "test:v1"])
container_id = container_id.decode('utf-8')
print(container_id)
container_id = container_id[:len(container_id) - 1]

subprocess.call(["docker", "cp", input_filepath, "{}:/{}".format(container_id, input_filename)])

if language == 'C' or language == 'C++':
    if language == 'C':
        src_filename = 'testcode.c'
        compiler = 'gcc'
    elif language == 'C++':
        src_filename = 'testcode.cpp'
        compiler = 'g++'
    src_filepath = './{}'.format(src_filename)
    exe_filename = 'testexe.out'
    subprocess.call(["docker", "cp", src_filepath, "{}:/{}".format(container_id, src_filename)])
    compile_status = subprocess.call(['docker', 'exec', container_id, compiler, src_filename, '-o', exe_filename], stderr=user_outputfile)
    if compile_status != 0:  
        print('CE')
    else:
        subprocess.call(["docker", "cp", './run.py', "{}:/run.py".format(container_id)])
        exe_status = subprocess.call(['docker', 'exec', container_id, 'python3', 'run.py', exe_filename, input_filename, user_output_filename, time_limit])  
        subprocess.call(["docker", "cp", "{}:/{}".format(container_id, user_output_filename), user_output_filepath])
        if exe_status == 124:
            print('TL')
        elif exe_status != 0:
            print('RE')
        else: 
            diff = subprocess.call(['diff', './testout.output', user_output_filepath])
            if not diff:
                print('AC')
            else:
                print('WA')
elif language == 'Python':
    src_filename = 'testcode.py'
    src_filepath = './{}'.format(src_filename)
    subprocess.call(["docker", "cp", src_filepath, "{}:/{}".format(container_id, src_filename)])
    subprocess.call(["docker", "cp", './runpy.py', "{}:/runpy.py".format(container_id)])
    exe_status = subprocess.call(['docker', 'exec', container_id, 'python3', 'runpy.py', src_filename, input_filename, user_output_filename, time_limit])
    subprocess.call(["docker", "cp", "{}:/{}".format(container_id, user_output_filename), user_output_filepath])
    if exe_status == 124:
        print('TL')
    elif exe_status != 0:
        print('RE')
    else:
        diff = subprocess.call(['diff', './testout.output', user_output_filepath])
        if not diff:
            print('AC')
        else:
            print('WA')
