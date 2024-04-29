for dataset in "anatomy" "restaurant" "doremus" "person" "SPIMBENCH_small-2019" "SPIMBENCH_large-2016"
do
    python3.8 ./statistic.py --suffix $dataset
done
