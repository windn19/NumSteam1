import datetime
import json
import logging.config
import sqlite3
from os.path import join
from pathlib import Path

from models_pe import Numbers, db
from prepare import prepare1

# from detect import run
BASEDIR = Path(__file__).parents[1]
print(BASEDIR)
# logging.config.fileConfig('file.conf')
log = logging.getLogger('file1')


def similarity_text(text, old_text):
    amound = min(len(text), len(old_text))
    if not amound:
        return False
    unequal = len([text[i] for i in range(amound) if text[i] != old_text[i]])
    if unequal > 1:
        log.info('Несходство строк')
        return False
    return True


def add_row(res, text, img=None, crop=None, cam_name='test_cam1', timeout=10):
    date = datetime.datetime.now()
    log.info(str(date))
    res1 = json.dumps({'result': res})
    log.info(f'Был получен - {text}')
    # prior = Numbers.select().where(Numbers.cam_name == cam_name).order_by(Numbers.datetime.desc()).limit(1)[0]
    try:
        prior = Numbers.select().where(Numbers.cam_name == cam_name).get()
        date_old, text_old, res_old = prior.datetime, prior.num, prior.res
        log.info(f'Старый текст - {text_old}')
        res_old = json.loads(res_old)['result']
    except Exception as e:
        log.info(e.__class__.__name__)
        text_old, res_old = '', []
        date_old = str(date - datetime.timedelta(seconds=60))
        log.info(date_old)
    log.info(f'{text} == {text_old}')
    if similarity_text(text, text_old):
        log.info('Обновление базы')
        res.extend(res_old)
        text = prepare1(res)
        log.info(f'Новый текст - {text}')
        res1 = json.dumps({'result': res})
        # print('Here')
        prior.num, prior.res, prior.crop, prior.image = text, res1, crop, img
        prior.save()
    else:
        log.info(Numbers.create(datetime=date, num=text, crop=crop, image=img, res=res1, cam_name=cam_name))
        log.info(f'Добавлено в базу - камера {cam_name} -> {text}')
    db.close()


def create_table():
    conn = sqlite3.connect(join(BASEDIR, 'base.db'))
    cur = conn.cursor()
    with open('create.sql') as f:
        text = f.read()

    cur.executescript(text)
    conn.commit()
    print('Create')
    cur.close()
    conn.close()


def read_all():
    conn = sqlite3.connect(join(BASEDIR, 'base.db'))
    cur = conn.cursor()
    cur.execute('select datetime, num, res from base where cam_name=? order by datetime desc limit 1;',
                (cam_name,))
    date_old, text_old, res_old = cur.fetchone()
    n = 1
    # result = [('test_cam1', row[0]) for row in cur.fetchall()]
    # print(result)
    # cur.executemany('''
    #     update base
    #     set cam_name=?
    #     where datetime=?
    # ''', result)
    # conn.commit()
    print('Read')
    cur.close()
    conn.close()


if __name__ == '__main__':
    print(similarity_text('O486OK799', 'O648CK799'))
