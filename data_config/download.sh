CONFIG_FILE="https://cdn.glitch.com/c16f71ef-e58b-4291-89f3-62975c2ebc7f%2Fyolov3-face.cfg?v=1586632897107"
WEIGHTS_FILE="https://cdn.glitch.com/c16f71ef-e58b-4291-89f3-62975c2ebc7f%2Fyolov3-wider_16000.weights?v=1586632996143"

wget -q $CONFIG_FILE  -O yolov3-face.cfg
wget -q $WEIGHTS_FILE -O yolov3-wider_16000.weights