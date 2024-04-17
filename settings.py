yolo_weights = '/media/dmitry/disk/ru_num/models/bestR6.pt'
ocr_weights = '/media/dmitry/disk/ru_num/models/mod.h5'
direct_weights = '/media/dmitry/disk/ru_num/models/in_out.h5'

source = 'rtsp://admin:Qwerty123@31.28.6.27:566/ISAPI/Streaming/Channels/104'
boxes = [68, 194, 1782, 1080]
lines = [408, 925]
postgre = dict(database='numbers', user='postgres', password='postgres', host='localhost')