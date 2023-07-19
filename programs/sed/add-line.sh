cp rsyslog rsyslog.test
sed -i '/weekly/a \\tmaxsize 100k' rsyslog.test
sed -i '/daily/a \\tmaxsize 100k' rsyslog.test
cat rsyslog.test
echo -e '\ndiff:'
diff rsyslog rsyslog.test
