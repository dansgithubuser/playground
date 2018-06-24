import subprocess

cmd='python -m package'
print('=====running '+cmd+'=====')
subprocess.check_call(cmd.split())

print('=====importing package and calling run=====')
import package
package.run()
