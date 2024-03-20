from collections import Counter
from datetime import datetime
import json
import logging
import logging.config
import re
import os


number_lat = re.compile(r'[ABEKMHOPCTYX_]\d{3}[ABEKMHOPCTYX_]{2}\d{2,3}|[ABEKMHOPCTYX_]{2}\d{5,6}')
num_lat = re.compile(r'[ABEKMHOPCTYX_]\d{3}[ABEKMHOPCTYX_]{2}|[ABEKMHOPCTYX_]{2}\d{5,6}')
number_by = re.compile(r'\d{4}[A-Z]{2}-\d')
number_by1 = re.compile(r'\d?\w{3}\d{3,4}')
number_by2 = re.compile(r'\d{2}\w{2}\d{3}')
number_lat1 = re.compile(r'\w{2}\d{5}')
number_lat2 = re.compile(r'\w{2}\d{4}\w')
number_tj = re.compile(r'\d{5}\w{3}')
# logging.config.fileConfig('file.conf')
log = logging.getLogger('file1')


def prepare1(source):
    # with open('list.json', mode='w', encoding='utf8') as f:
    #     json.dump({'result': source}, f, ensure_ascii=False)
    log.info(source)
    # words2 = source[1]
    # words = map(str.upper, map(lambda x: x.replace(' ', ''), source))
    words = list(map(lambda x: x.replace('[UNK]', '_'), source))
    source_ = ' '.join(words)
    # source_dop = ' '.join(source[1])
    # res0 = num_lat.findall(source_dop)
    res = number_lat.findall(source_)
    res1 = number_by.findall(source_ )
    res2 = number_by1.findall(source_)
    res3 = number_by2.findall(source_)
    res4 = number_lat1.findall(source_)
    res5 = number_lat2.findall(source_)
    res6 = number_tj.findall(source_)
    if not res:
        log.info('По иностранным шаблонам')
        out = Counter(res1 + res2 + res3 + res4 + res5 + res6)
        num_reg = ''
    else:
        log.info('Российский номер')
        out = Counter(res)
        # out1 = Counter(res0)
        num_reg = max(out.keys(), key=lambda x: out[x])
        log.info(f'\n{out}\n{num_reg}')
    log.info(f'Результат: {source}\n{out}')
    try:
        if num_reg:
            num = max(filter(lambda x: num_reg in x, out.keys()), key=lambda x: out[x])
        else:
            num = max(out.keys(), key=lambda x: out[x])
        return num
    except Exception as e:
        log.error(e.__class__.__name__, exc_info=False)
        return None


def replace_char(arr: list) -> list:
    for ch, char in [('0', 'O'), ('4', 'A'), ('8', 'B')]:
        arr.extend([it.replace(ch, char).replace(' ', '').upper() for it in arr])
    for num, word in enumerate(arr):
        if word[-4:].isdigit():
            arr[num] = word[:-4] + word[-3:]
    return arr


if __name__ == '__main__':
    # print(replace_char(['Ho480k1799', '104860k799', '24300h']))
    # python detect.py - -weights bestR5.pt - -source rtsp: // admin: Qwerty123 @ 31.28.6.27: 566 / ISAPI / Streaming / Channels / 104 --save-crop --nosave --boxes 68 194 1782 1080 --lines 348 925
    s = 'B824XP___ B824XP___ B824XP___ B24XO 2AXP B24X0 B2AX0 24XP B24x0 B2AXO K824XP790 K824XP790 K824XP790 P2EYPHP KO24XEK KO2AXEK P2EYphp Ko2aXek KO24Xek'
    s = s.split()
    print(prepare1(s))