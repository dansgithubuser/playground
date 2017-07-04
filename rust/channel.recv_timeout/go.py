import os, subprocess
subprocess.check_call('rustc main.rs', shell=True)
subprocess.check_call(os.path.join('.', 'main'), shell=True)
