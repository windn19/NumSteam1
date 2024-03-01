from detect import load_model, run
try:
    from settings import yolo_weights, source
except Exception as e:
    print('Нет файла настроек с весами для yolo')
    yolo_weights = ''
    source = ''


if __name__ == '__main__':
    model = load_model(weights=yolo_weights)
    try:
        run(model=model, source=source, save_crop=True, nosave=True)
    except Exception as e:
        print(e.__class__.__name__)


