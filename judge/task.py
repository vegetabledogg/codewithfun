# from celery.decorators import task
from judge.models import Submission, Lesson
from accounts.models import Profile
import subprocess
import os

class Container:
    def create_container(self, image, memory_limit):
        try:
            temp = subprocess.check_output(['docker', 'run', '-it', '-m', memory_limit, '-d', image])
        except Exception as exc:
            print('ERROR: returncode = %d' % (exc.returncode))
            print('ERROR: %s' % (exc.output.decode(encoding='utf-8')))
        temp = temp.decode(encoding='utf-8')
        self.container_id = temp[:len[temp] - 1]

    def copy_local2container(self, local_path, container_path):
        subprocess.call(['docker', 'cp', local_path, '{}:/{}'.format(self.container_id, container_path)])

    def copy_container2local(self, container_path, local_path):
        subprocess.call(['docker', 'cp', '{}:/{}'.format(self.container_id, container_path), local_path])

    def execute(command):
        return subprocess.call(['docker', 'execute'].extend(command))

    def stop(self):
        subprocess.call(['docker', 'stop', self.container_id])

# @task(name='evaluateSubmission')
def evaluate_submission(submission_id):
    try:
        submission = Submission.object.get(pk=submission_id)
    except:
        print('ERROR: submission with id = %d not found' % (submission_id))
    lesson = submission.lesson
    username = submission.submitter.user.username
    input_filename = lesson.inputfile.name.split('/')[1]
    memory_limit = str(lesson.memory_limit)
    time_limit = str(lesson.time_limit)
    language = lesson.language
    user_output_filename = '{}.{}.output'.format(username, submission_id)
    user_output_filepath = 'useroutput/{}'.format(user_output_filename)

    container = Container()
    container.create_container('ubuntu:16.04')
    container.copy_local2container(lesson.inputfile.name, input_filename)

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
        container.copy_local2container(src_filepath, src_filename)
        compile_status = container.execute([compiler, src_filename, '-o', exe_filename, '>>', user_output_filename, '2>&1'])
        if compile_status != 0:
            container.copy_container2local(user_output_filename, user_output_filepath)  
            submission.status = 'CE'
            # submission.result
            submission.save()
        else:
            exe_status = container.execute(['timeout', time_limit, './{}'.format(exe_filename), '<', input_filename, '>>', user_output_filename, '2>&1'])
            container.copy_container2local(user_output_filename, user_output_filepath)  
            if exe_status == 124:
                submission.status = 'TL'
                # submission.result
                submission.save()
            elif exe_status != 0:
                submission.status = 'RE'
                # submission.result
                submission.save()
            else: 
                diff = subprocess.call(['diff', lesson.outputfile.name, user_output_filepath])
                if not diff:
                    submission.status = 'AC'
                    # submission.result
                    submission.save()
                else:
                    submission.status = 'WA'
                    # submission.result
                    submission.save()
    elif language == 'Python':
        src_filename = '{}.{}.py'.format(username, submission)
        src_filepath = 'submissions/{}'.format(src_filename)
        srcfile = open(src_filepath, 'w+')
        print(submission.code, file=srcfile)
        srcfile.close()
        container.copy_local2container(src_filepath, src_filename)
        exe_status = container.execute(['timeout', time_limit, 'python3', src_filename, '<', input_filename, '>>', user_output_filename, '2>&1'])
        container.copy_container2local(user_output_filename, user_output_filepath)
        if exe_status == 124:
            submission.status = 'TL'
            # submission.result
            submission.save()
        elif exe_status != 0:
            submission.status = 'RE'
            # submission.result
            submission.save()
        else:
            diff = subprocess.call(['diff', lesson.outputfile.name, user_output_filepath])
            if not diff:
                submission.status = 'AC'
                # submission.result
                submission.save()
            else:
                submission.status = 'WA'
                submission.save()

    os.remove(src_filepath)
    os.remove(user_output_filepath)
    container.stop()
