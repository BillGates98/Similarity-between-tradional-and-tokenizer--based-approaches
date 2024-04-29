# for dataset in "SPIMBENCH_small-2019" "restaurant" "doremus" "person"
# for dataset in "anatomy" "restaurant" "doremus" "person" "SPIMBENCH_small-2019"
# for dataset in "UOBM_small-2016" "anatomy" "restaurant" "doremus" "person" "SPIMBENCH_small-2019" "SPIMBENCH_large-2016"
for dataset in "person"
do
    python3.8 ./linking.py --suffix $dataset
    python3.8 ./drawer.py --suffix $dataset
done
