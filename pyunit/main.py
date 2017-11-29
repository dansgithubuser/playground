import subprocess
subprocess.check_call(['python', '-m', 'unittest', 'pyunit'])
subprocess.check_call(['python', '-m', 'unittest', 'pyunit.TestPlay1'])
subprocess.check_call(['python', '-m', 'unittest', 'pyunit.TestPlay1.test_1'])
