slave214="6 12 14 16 18 22 23 28"
slave215="32 50 54 181 182 300 458 1462"
slave216="1501 4534 23381 40499 40670 40983 1590"

cd ../..
host_name=$(hostname)
for d in ${!host_name}; do
  nohup python -m benchmarks.bdas_time_cv -s plain -t 1800 -d $d >$d.txt 2>&1 &
done

logs_dir="half_plain_best_logs"
if [ ! -d "$logs_dir" ]; then
  mkdir $logs_dir
fi

mv [[:digit:]]*.txt $logs_dir
