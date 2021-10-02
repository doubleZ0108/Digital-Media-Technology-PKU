import cv2

# 读取原视频
cap = cv2.VideoCapture("video.MOV")

# fps = round(cap.get(cv2.CAP_PROP_FPS))
# print('origin fps: ', fps)
# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# print('origin size: ', size)

# 设置输出尺寸和帧率
size = (320, 240)
fps = 15

# 使用VideoWriter_fourcc视频编解码器写出yuv格式视频
videoWriter = cv2.VideoWriter("video-opencv.yuv", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

# 读如第一帧判断视频读取成功与否
if cap.isOpened():
    ret, frame = cap.read()
else:
    ret = False

while ret:
    # 设置输出帧率和尺寸
    frame = cv2.resize(frame, size)
    videoWriter.write(frame)
    ret, frame = cap.read()

cap.release()
