# from celery.decorators import task
from judge.models import Submission, Lesson, Testcase
from accounts.models import Profile
from django.core.files import File
import subprocess
import os

# @task(name='evaluate_submission')
def evaluate_submission(submission_id):
    try:
        submission = Submission.objects.get(pk=submission_id)
    except:
        print('ERROR: submission with id = %d not found' % (submission_id))
    # print(submission.id)
    lesson = submission.lesson
    testcase = Testcase.objects.get(lesson=lesson)
    username = submission.submitter.user.username
    input_filename = testcase.inputfile.name.split('/')[1]
    memory_limit = lesson.memory_limit
    time_limit = lesson.time_limit
    language = lesson.language
    user_output_filename = '{}.{}.output'.format(username, submission_id)
    user_output_filepath = 'useroutput/{}'.format(user_output_filename)
    user_errfile = open('useroutput/err.{}'.format(user_output_filename), 'a')

    container_id = subprocess.check_output(["docker", "run", "-it", "-m", memory_limit, "-d", "test:v1"])
    container_id = container_id.decode('utf-8')
    print(container_id)
    container_id = container_id[:len(container_id) - 1]

    subprocess.call(["docker", "cp", testcase.inputfile.name, "{}:/{}".format(container_id, input_filename)])

    if language == 'C' or language == 'C++':
        if language == 'C':
            src_filename = '{}.{}.c'.format(username, submission_id)
            compiler = 'gcc'
        elif language == 'C++':
            src_filename = '{}.{}.cpp'.format(username, submission_id)
            compiler = 'g++'
        src_filepath = 'submissions/{}'.format(src_filename)
        exe_filename = '{}.{}.out'.format(username, submission_id)
        srcfile = open(src_filepath, 'w+')        
        print(submission.code, file=srcfile)
        srcfile.close()
        subprocess.call(["docker", "cp", src_filepath, "{}:/{}".format(container_id, src_filename)])
        if language == 'C':
            compile_status = subprocess.call(['docker', 'exec', container_id, compiler, '-std=c99', src_filename, '-o', exe_filename], stderr=user_errfile)
        elif language == 'C++':
            compile_status = subprocess.call(['docker', 'exec', container_id, compiler, '-std=c99', src_filename, '-o', exe_filename], stderr=user_errfile)
        user_errfile.close()
        if compile_status != 0:
            user_errfile = open('useroutput/err.{}'.format(user_output_filename), 'r')
            result = user_errfile.read(32767)
            submission.result = result 
            submission.status = 'CE'
        else:
            subprocess.call(["docker", "cp", 'run.py', "{}:/run.py".format(container_id)])
            exe_status = subprocess.call(['docker', 'exec', container_id, 'python3', 'run.py', exe_filename, input_filename, user_output_filename, time_limit])  
            print(exe_status)
            subprocess.call(["docker", "cp", "{}:/{}".format(container_id, user_output_filename), user_output_filepath])  
            if exe_status == 124:
                submission.status = 'TL'
            elif exe_status != 0:
                submission.status = 'RE'
            else: 
                diff = subprocess.call(['diff', testcase.outputfile.name, user_output_filepath])
                if not diff:
                    submission.status = 'AC'
                else:
                    submission.status = 'WA'
            user_outputfile = open(user_output_filepath, 'r')
            result = user_outputfile.read(32767)
            submission.result = result
            os.remove(user_output_filepath)
    elif language == 'Python':
        src_filename = '{}.{}.py'.format(username, submission)
        src_filepath = 'submissions/{}'.format(src_filename)
        srcfile = open(src_filepath, 'w+')
        print(submission.code, file=srcfile)
        srcfile.close()
        subprocess.call(["docker", "cp", src_filepath, "{}:/{}".format(container_id, src_filename)])
        subprocess.call(["docker", "cp", 'runpy.py', "{}:/runpy.py".format(container_id)])
        exe_status = subprocess.call(['docker', 'exec', container_id, 'python3', 'runpy.py', src_filename, input_filename, user_output_filename, time_limit])
        subprocess.call(["docker", "cp", "{}:/{}".format(container_id, user_output_filename), user_output_filepath])
        if exe_status == 124:
            submission.status = 'TL'
        elif exe_status != 0:
            submission.status = 'RE'
        else:
            diff = subprocess.call(['diff', testcase.outputfile.name, user_output_filepath])
            if not diff:
                submission.status = 'AC'
            else:
                submission.status = 'WA'
        user_outputfile = open(user_output_filepath, 'r')
        result = user_outputfile.read(32767)
        submission.result = result
        os.remove(user_output_filepath)
    submission.save()
    # sub = Submission.objects.get(pk=submission_id)
    # print(sub.result)
    # print(sub.status)

    os.remove(src_filepath)
    os.remove('useroutput/err.{}'.format(user_output_filename))

    subprocess.call(["docker", "stop", container_id])
