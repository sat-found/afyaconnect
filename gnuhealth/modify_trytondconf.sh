f=/opt/gnuhealth/etc/trytond.conf
l=$(grep -n '\[web\]' $f | sed -e 's/:.*//')
mv $f tmp
sed "$l aroot=/home/node/sao" tmp > $f
cat >> $f <<'EOF'
num_proxies = 1
cors =
    http://localhost:8090
    http://127.0.0.1:8090
    http://localhost:8091
    http://127.0.0.1:8091
EOF
sed -i 's/#list = True/list = True/' $f
grep -A 12 '\[web\]' $f
