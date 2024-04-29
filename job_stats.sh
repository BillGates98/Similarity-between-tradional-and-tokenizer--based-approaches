# for dataset in "SPIMBENCH_small-2019" "restaurant" "doremus" "person"
# for dataset in "anatomy" "restaurant" "doremus" "person" "SPIMBENCH_small-2019"
# for dataset in "UOBM_small-2016" "anatomy" "restaurant" "doremus" "person" "SPIMBENCH_small-2019" "SPIMBENCH_large-2016"
for dataset in "anatomy" "restaurant" "doremus" "person" "SPIMBENCH_small-2019" "SPIMBENCH_large-2016"
do
    python3.8 ./statistic.py --suffix $dataset
done
