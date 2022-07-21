
slave222="181 182 300 1590"


cd ../..
host_name=$(hostname)
for d in ${!host_name}; do
  nohup python -m benchmarks.bdas_time_cv -s plain -t 14400 -d $d >$d.txt 2>&1 &
done

logs_dir="comp_bdas_4h_plain_best_logs"
if [ ! -d "$logs_dir" ]; then
  mkdir $logs_dir
fi

mv [[:digit:]]*.txt $logs_dir
