import sys
import subprocess

if __name__ == "__main__":
    try:
        executable = sys.argv[1]
        input_filename = sys.argv[2]
        output_filename = sys.argv[3]
        tl = sys.argv[4]
    except IndexError:
        sys.exit(-1)

    input_file = open(input_filename, "r")
    output_file = open(output_filename, "w+")
    returncode = 0
    try:
        subprocess.check_output(["timeout", tl, "./{}".format(executable)], stdin=input_file, stderr=output_file)
    except Exception as exc:
        returncode = exc.returncode
        print(exc.output.decode('utf-8'))
    print(returncode)
    f = open('returncode', 'w+')
    print(returncode, file=f)
    f.close()
    input_file.close()
    output_file.close()
