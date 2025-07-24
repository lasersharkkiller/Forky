 # input images are 3840x2160 wxh
 
yolo detect train \
     model=yolov8n.pt \
     data=data.yaml \
     epochs=30 \
     imgsz=640 \
     batch=4
