#!/usr/bin/bash


# =====[ DEFINE IMPORTANT VARIABLES ]===== #
export CURRENT_WORKSPACE=$(pwd)
export PHANTOMJS_DRIVER=$HOME/Driver/phantomjs
export DATA=$CURRENT_WORKSPACE/data/
export CONFIG=$CURRENT_WORKSPACE/config/


# =====[ DOWNLOAD LINKS ]================= #
phantomjs="https://cdn.glitch.com/c16f71ef-e58b-4291-89f3-62975c2ebc7f%2Fphantomjs?v=1594230459325"
yolo_config="https://cdn.glitch.com/c16f71ef-e58b-4291-89f3-62975c2ebc7f%2Fyolov3-face.cfg?v=1586632897107"
yolo_weights="https://cdn.glitch.com/c16f71ef-e58b-4291-89f3-62975c2ebc7f%2Fyolov3-wider_16000.weights?v=1586632996143"


# =====[ DEFINE SOME FUNCTIONS ]========== #
count_files () {
    local folder=$1
    local sum=0
    for file in $(ls $folder); do
        sum=$(($sum + 1))
    done
    echo $sum
}


# =====[ CHECK PHANTOMJS DRIVER ]========= #
if [ -f "$PHANTOMJS_DRIVER" ]; then
    echo "[✓] PhantomJs was installed."
else
    echo "[!] PhantomJs driver was not found!"
    echo "[?] try to download PhantomJs driver ..."
    mkdir ~/Driver/
    wget $phantomjs -O $PHANTOMJS_DRIVER
    echo "[✓] saved to $PHANTOMJS_DRIVER."
fi


# =====[ CHECK DATA FOLDER ]============== #
if [ -d "$DATA" ]; then
    echo "[✓] data folder existed."
else
    echo "[!] data folder was not found!"
    mkdir data
    echo "[✓] created data folder."
fi


# =====[ CHECK YOLO CONFIG FILES ]======== #
if [ $(count_files $CONFIG) -ne 0 ]; then
    echo "[✓] config files were downloaded!"
else
    echo "[!] config files were not found!"
    echo "[?] try to download config files."
    wget $yolo_config  -O $CONFIG/yolov3-face.cfg
    echo "    [✓] Downloaded yolov3-face.cfg"
    wget $yolo_weights -O $CONFIG/yolov3-wider_16000.weights
    echo "    [✓] Downloaded yolov3-wider_16000.weights"
fi

# ======================================== #
