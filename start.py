from detect import load_model, run
try:
    from settings import yolo_weights, source, boxes, lines
except Exception as e:
    print('Нет файла настроек с весами для yolo')
    yolo_weights = ''
    source = ''
    boxes = []
    lines = []


model = load_model(weights=yolo_weights)
try:
    run(model=model, source=source, save_crop=True, nosave=True, boxes=boxes, lines=lines)
except Exception as e:
    print(e.__class__.__name__)


