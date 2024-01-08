python3 out-err.py \    # run this command
	> out-err.txt \ # put stdout into this file
	2>&1            # and put stderr where stdout is going

# these ideas DON'T work:
# cmd > out-err.txt 2> out-err.txt
# cmd 2>&1 > out-err.txt
