for dataset in "anatomy" "restaurant" "doremus" "person" "SPIMBENCH_small-2019" "SPIMBENCH_large-2016"
do
    python3.8 ./linking.py --suffix $dataset
    python3.8 ./drawer.py --suffix $dataset
done
