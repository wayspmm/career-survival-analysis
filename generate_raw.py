import numpy as np
import pandas as pd
import random
import datetime as dt
import sys

OUT = sys.argv[1]
rng = np.random.default_rng(2026)
random.seed(2026)

OBS_START, OBS_END, SIM_END = 1885, 1913, 1916

DEPTS = ['паровозный', 'вагонный', 'кузнечный', 'путь', 'контора']
DEPT_NAME = {'паровозный': ['паровозный цех', 'Паровозн. цех', 'паровозные мастерские', 'паровоз. цехъ'],
             'вагонный': ['вагонный цех', 'вагонн. цех', 'Вагонный цехъ', 'вагонные мастерские'],
             'кузнечный': ['кузнечный цех', 'кузнечн. цех', 'Кузница', 'кузнечный цехъ'],
             'путь': ['служба пути', 'Служба пути', 'сл. пути', '3-й участок пути', '5-й участок пути'],
             'контора': ['контора', 'Контора мастерских', 'канцелярия', 'контора упр.']}
DEPT_ACC = {'паровозный': 'в паровозный цех', 'вагонный': 'в вагонный цех', 'кузнечный': 'в кузнечный цех',
            'путь': 'в службу пути', 'контора': 'в контору'}

# (nom, instr, gen) по уровням 0..5
POS = {
    'паровозный': [('ученик', 'учеником', 'ученика'), ('подручный', 'подручным', 'подручного'),
                   ('слесарь', 'слесарем', 'слесаря'), ('старший слесарь', 'старшим слесарем', 'старшего слесаря'),
                   ('помощник мастера', 'помощником мастера', 'помощника мастера'), ('мастер', 'мастером', 'мастера')],
    'вагонный': [('ученик', 'учеником', 'ученика'), ('подручный', 'подручным', 'подручного'),
                 ('плотник', 'плотником', 'плотника'), ('старший плотник', 'старшим плотником', 'старшего плотника'),
                 ('помощник мастера', 'помощником мастера', 'помощника мастера'), ('мастер', 'мастером', 'мастера')],
    'кузнечный': [('ученик', 'учеником', 'ученика'), ('молотобоец', 'молотобойцем', 'молотобойца'),
                  ('кузнец', 'кузнецом', 'кузнеца'), ('старший кузнец', 'старшим кузнецом', 'старшего кузнеца'),
                  ('помощник мастера', 'помощником мастера', 'помощника мастера'), ('мастер', 'мастером', 'мастера')],
    'путь': [('чернорабочий', 'чернорабочим', 'чернорабочего'), ('путевой рабочий', 'путевым рабочим', 'путевого рабочего'),
             ('старший рабочий', 'старшим рабочим', 'старшего рабочего'), ('артельный староста', 'артельным старостой', 'артельного старосты'),
             ('помощник дорожного мастера', 'помощником дорожного мастера', 'помощника дорожного мастера'),
             ('дорожный мастер', 'дорожным мастером', 'дорожного мастера')],
    'контора': [('писец', 'писцом', 'писца'), ('конторщик', 'конторщиком', 'конторщика'),
                ('старший конторщик', 'старшим конторщиком', 'старшего конторщика'), ('счетовод', 'счетоводом', 'счетовода'),
                ('помощник бухгалтера', 'помощником бухгалтера', 'помощника бухгалтера'), ('бухгалтер', 'бухгалтером', 'бухгалтера')],
}
POS_ABBR = {'слесарь': ['слес.', 'слесарь 2 разр.', 'слесарь 1 разр.'], 'старший слесарь': ['ст. слесарь', 'старш. слесарь'],
            'помощник мастера': ['пом. мастера', 'помощн. мастера'], 'чернорабочий': ['чернораб.'], 'путевой рабочий': ['путев. рабочий', 'рабочий'],
            'конторщик': ['контор.'], 'старший конторщик': ['ст. конторщик'], 'помощник бухгалтера': ['пом. бухгалтера'],
            'дорожный мастер': ['дор. мастер'], 'помощник дорожного мастера': ['пом. дор. мастера'], 'кузнец': ['кузн.'],
            'подручный': ['подруч.', 'подручный слесаря'], 'молотобоец': ['молотоб.'], 'старший кузнец': ['ст. кузнец']}

BASE_WAGE = {'w': [96, 180, 300, 420, 600, 960], 'p': [144, 204, 276, 384, 540, 900], 'c': [180, 300, 420, 540, 720, 1140]}

SURN = ('Иванов Петров Сидоров Кузнецов Смирнов Попов Васильев Соколов Михайлов Новиков Фёдоров Морозов Волков Алексеев '
        'Лебедев Семёнов Егоров Павлов Козлов Степанов Николаев Орлов Андреев Макаров Никитин Захаров Зайцев Соловьёв '
        'Борисов Яковлев Григорьев Романов Воробьёв Сергеев Кудрявцев Фролов Александров Дмитриев Королёв Гусев Киселёв '
        'Ильин Максимов Поляков Сорокин Виноградов Ковалёв Белов Медведев Антонов Тарасов Жуков Баранов Филиппов Комаров '
        'Давыдов Беляев Герасимов Богданов Осипов Сидорчук Матвеев Титов Марков Миронов Крылов Куликов Карпов Власов '
        'Мельников Денисов Гаврилов Тихонов Казаков Афанасьев Данилов Савельев Тимофеев Фомин Чернов Абрамов Мартынов '
        'Ефимов Федотов Щербаков Назаров Калинин Исаев Чернышёв Быков Маслов Родионов Коновалов Лазарев Воронин Климов '
        'Филатов Пономарёв Голубев Кузьмин Лукин Ершов Ширяев Дорофеев Горбунов Рыжов Пахомов Субботин Мухин Селиванов').split()
NAMES = 'Иван Пётр Николай Василий Алексей Михаил Фёдор Григорий Семён Яков Андрей Дмитрий Степан Павел Егор Тимофей Илья Кузьма Матвей Сергей Александр Афанасий Прокофий Никифор Емельян'.split()

GUB = ['Саратовская губ.', 'Сарат. губ.', 'Пензенская губ.', 'Пенз. губ.', 'Тамбовская губ.', 'Симбирская губ.', 'Самарская губ.',
       'Рязанская губ.', 'Тульская губ.', 'Воронежская губ.', 'г. Саратов', 'Саратов', 'Аткарский уезд', 'Петровский у.', 'Вольский уезд']

SOSL = {'крестьяне': ['крестьянин', 'крест.', 'из крестьян', 'Крестьянин', 'крестьянинъ', 'кр-н'],
        'мещане': ['мещанин', 'мещ.', 'из мещан', 'Мещанин', 'мещанинъ'],
        'прочие': ['из солдатских детей', 'цеховой', 'из купцов', 'сын чиновника', 'из духовного звания', 'личный почётный гражданин']}
EDU = {0: ['неграмотен', 'неграм.', 'не обучался', 'безграмотный'],
       1: ['грамотен', 'домашнее', 'обучался дома', 'читает и пишет'],
       2: ['сельская школа', 'церковно-приходская школа', 'ц.-пр. школа', 'земская школа', 'нач. народное училище'],
       3: ['городское училище', 'уездное училище', 'гор. уч-ще', 'двухклассное училище'],
       4: ['техническое училище', 'ремесленное училище', 'железнодорожное техническое училище', 'ж.д. технич. уч-ще', 'реальное училище']}

MONTH_GEN = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
MONTH_NOM = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']


def logit(x):
    return 1 / (1 + np.exp(-x))


def period_exit(y):
    e = 0.0
    if y in (1891, 1892):
        e += 0.35
    if 1900 <= y <= 1903:
        e += 0.3
    if y == 1905:
        e += 1.1
    if y == 1906:
        e += 0.6
    if y >= 1909:
        e -= 0.1
    return e


def period_promo(y):
    e = 0.0
    if 1896 <= y <= 1899:
        e += 0.25
    if 1900 <= y <= 1903:
        e -= 0.3
    if y in (1905, 1906):
        e -= 0.35
    if y >= 1909:
        e += 0.25
    return e


def exit_logit(p, y):
    t = y - p['hire_y']
    tb = [-1.0, -1.55, -1.95, -2.3, -2.45, -2.6, -2.7, -2.75, -2.8, -2.85, -2.9][min(t, 10)]
    x = tb - 0.22 * p['level']
    x += 0.38 * (p['sosl'] == 'крестьяне') - 0.12 * p['edu']
    x += -1.3 * np.log(p['m'])
    x += 0.09 * min(max(p['yil'] - 4, 0), 8)
    age = y - p['birth']
    if age >= 52:
        x += 0.13 * (age - 52)
    if age < 18:
        x += 0.2
    x += {'путь': 0.35, 'контора': -0.25}.get(p['dept'], 0)
    x += 0.15 * p['transfers'] if p['transfers'] <= 2 else 0.3
    x += period_exit(y)
    return x


def promo_logit(p, y):
    lv, yil = p['level'], p['yil']
    if lv >= 5:
        return -99
    if lv == 0:
        x = [-3.0, -1.1, 0.0, 0.4, 0.6][min(yil, 4)]
    else:
        x = [None, -1.7, -2.3, -3.0, -3.4][lv] + 0.28 * min(yil, 4) - 0.08 * max(yil - 7, 0)
        x += 0.3 * max(p['edu'] - 1, 0) * (lv >= 2)
    x += -0.2 * (p['sosl'] == 'крестьяне') + 0.5 * np.log(p['m'])
    age = y - p['birth']
    if age > 50:
        x -= 0.6
    x += period_promo(y)
    return x


def make_person(pid, hire_y, initial=False):
    dept = rng.choice(DEPTS, p=[0.3, 0.22, 0.13, 0.25, 0.10])
    if dept == 'контора':
        sosl = rng.choice(['крестьяне', 'мещане', 'прочие'], p=[0.35, 0.45, 0.20])
        edu = int(rng.choice([1, 2, 3, 4], p=[0.15, 0.35, 0.35, 0.15]))
    else:
        sosl = rng.choice(['крестьяне', 'мещане', 'прочие'], p=[0.68, 0.27, 0.05])
        edu = int(rng.choice([0, 1, 2, 3, 4], p=[0.22, 0.25, 0.33, 0.13, 0.07]))
    r = rng.random()
    if dept in ('путь',):
        level = 0 if r < 0.75 else 1
    elif dept == 'контора':
        level = 0 if r < 0.6 else 1
    else:
        level = 0 if r < 0.45 else (1 if r < 0.8 else 2)
    if level == 0 and dept not in ('путь', 'контора'):
        age = int(rng.integers(14, 19))
    else:
        age = int(np.clip(rng.normal(25 + 3 * level, 6), 16, 48))
    m = float(np.exp(rng.normal(0, 0.14)))
    return dict(pid=pid, hire_y=hire_y, dept=dept, sosl=sosl, edu=edu, level=level, birth=hire_y - age,
                m=m, yil=0, transfers=0, events=[], active=True, exit_y=None)


def rand_date(y, frac_from=0.0):
    start = dt.date(y, 1, 1).toordinal()
    end = dt.date(y, 12, 31).toordinal()
    s = int(start + frac_from * (end - start))
    return dt.date.fromordinal(int(rng.integers(s, end + 1)))


def wage_of(p, y):
    base = BASE_WAGE[{'контора': 'c', 'путь': 'p'}.get(p['dept'], 'w')][p['level']]
    infl = 1 + 0.012 * max(y - 1897, 0)
    return base * p['m'] * infl


def exit_reason(p, y):
    age = y - p['birth']
    opts = [('по прошению', 0.55), ('за нетрезвое поведение', 0.08), ('за неисправность по службе', 0.07),
            ('по болезни', 0.06), ('за прогулы', 0.05)]
    if age > 50:
        opts += [('умер', 0.25), ('с пенсией за выслугою лет', 0.25 if p['level'] >= 3 else 0.05)]
    else:
        opts += [('умер', 0.03)]
    if y in (1905, 1906):
        opts += [('за участие в забастовке', 0.45)]
    if 1900 <= y <= 1903 or y in (1891, 1892):
        opts += [('по сокращению штатов', 0.25)]
    w = np.array([o[1] for o in opts])
    return opts[rng.choice(len(opts), p=w / w.sum())][0]


def simulate(p):
    y = p['hire_y']
    hd = rand_date(y)
    p['hire_date'] = hd
    p['events'].append(('hire', hd, p['level'], p['dept'], wage_of(p, y)))
    p['history'] = {}
    frac = (hd.toordinal() - dt.date(y, 1, 1).toordinal()) / 365
    first = True
    while y <= SIM_END:
        if not first:
            p['history'][y] = (p['level'], p['dept'], wage_of(p, y))
        scale = (1 - frac) if first else 1.0
        pe = logit(exit_logit(p, y)) * scale
        pp = logit(promo_logit(p, y)) * scale
        pt = (0.025 if p['dept'] != 'контора' else 0.008) * scale
        r = rng.random()
        if r < pe:
            d = rand_date(y, frac if first else 0)
            p['events'].append(('exit', d, p['level'], p['dept'], exit_reason(p, y)))
            p['active'] = False
            p['exit_y'] = y
            return p
        elif r < pe + pp and p['level'] < 5:
            d = rand_date(y, frac if first else 0)
            p['level'] += 1
            p['yil'] = 0
            p['m'] *= float(np.exp(rng.normal(0.02, 0.05)))
            p['events'].append(('promo', d, p['level'], p['dept'], wage_of(p, y)))
        elif r < pe + pp + pt and p['level'] >= 1:
            d = rand_date(y, frac if first else 0)
            if p['dept'] == 'контора':
                pass
            else:
                newd = rng.choice([x for x in DEPTS if x not in ('контора', p['dept'])])
                if newd == 'путь' and p['level'] == 0:
                    newd = 'паровозный'
                p['dept'] = newd
                p['transfers'] += 1
                p['events'].append(('transfer', d, p['level'], p['dept'], wage_of(p, y)))
            p['yil'] += 1
        else:
            p['yil'] += 1
        if not first or frac < 0.5:
            pass
        if rng.random() < 0.18:
            p['m'] *= float(np.exp(rng.normal(0.03, 0.04)))
            p['events'].append(('wage', rand_date(y), p['level'], p['dept'], wage_of(p, y)))
        if rng.random() < 0.05:
            p['events'].append(('award', rand_date(y), p['level'], p['dept'], None))
        if rng.random() < 0.06:
            p['events'].append(('leave', rand_date(y), p['level'], p['dept'], None))
        if rng.random() < 0.03:
            p['events'].append(('fine', rand_date(y), p['level'], p['dept'], None))
        first = False
        y += 1
    return p


people = []
pid = 1
# старый состав: нанятые до начала наблюдения, в архив попадают только те, кто дожил до 1885
for y in range(1860, 1885):
    n = rng.poisson(55 + 2.5 * (y - 1860))
    for _ in range(n):
        p = simulate(make_person(pid, y, True))
        pid += 1
        if p['exit_y'] is None or p['exit_y'] >= 1885:
            people.append(p)
for y in range(1885, SIM_END + 1):
    lam = 140 * 1.025 ** (y - 1885)
    if 1896 <= y <= 1899:
        lam *= 1.45
    if 1900 <= y <= 1903:
        lam *= 0.75
    if y in (1905, 1906):
        lam *= 1.15
    if y >= 1909:
        lam *= 1.2
    for _ in range(rng.poisson(lam)):
        people.append(simulate(make_person(pid, y)))
        pid += 1

print('people', len(people))

# перенумерация табельных номеров как в архиве (не подряд)
ids = rng.choice(np.arange(1, 30000), size=len(people), replace=False)
ids.sort()
for p, i in zip(people, ids):
    p['tab'] = int(i)
    p['fio'] = f"{rng.choice(SURN)} {rng.choice(NAMES)[0]}. {rng.choice(NAMES)[0]}."


def old_orth(s):
    out = []
    for w in s.split(' '):
        if len(w) > 1 and w[-1] in 'бвгджзклмнпрстфхцчшщ':
            w = w + 'ъ'
        w = w.replace('ие', 'іе').replace('ия', 'ія').replace('ии', 'іи')
        w = w.replace('определ', 'опредѣл').replace('Определ', 'Опредѣл').replace('смерт', 'смерт').replace('след', 'слѣд')
        out.append(w)
    return ' '.join(out)


def fmt_date(d):
    r = rng.random()
    y = d.year
    if rng.random() < 0.004:
        s = str(y)
        y_bad = s[0] + s[2] + s[1] + s[3] if rng.random() < 0.5 else s[0] + s[1] + s[3] + s[2]
        return f"{d.day:02d}.{d.month:02d}.{y_bad}"
    if r < 0.45:
        return f"{d.day:02d}.{d.month:02d}.{y}"
    if r < 0.63:
        return f"{d.day} {MONTH_GEN[d.month - 1]} {y}" + (' г.' if rng.random() < 0.4 else '')
    if r < 0.73:
        return d.isoformat()
    if r < 0.83:
        return f"{MONTH_NOM[d.month - 1]} {y}"
    if r < 0.88:
        return f"{y}" + (' г.' if rng.random() < 0.5 else '')
    if r < 0.94:
        return f"{d.day}/{d.month}/{str(y)[2:]}"
    if r < 0.97:
        return f"{d.day:02d}.{d.month:02d}.{y}  "
    return rng.choice(['', '—', 'н/д'])


def fmt_wage(w, level, dept):
    if w is None or rng.random() < 0.07:
        return rng.choice(['', '', '—', 'без сод.']) if w is None else ''
    r = rng.random()
    if dept != 'контора' and level <= 3 and r < 0.35:
        day = round(w / 280 * 20) / 20
        rub, kop = int(day), int(round((day - int(day)) * 100))
        if rub > 0 and kop == 0:
            return f"{rub} р. в день"
        return f"{rub} р. {kop} к. в день" if rub > 0 else f"{kop} к. в день"
    if r < 0.6:
        return f"{round(w / 12)} р. в мес."
    if r < 0.8:
        return f"{int(round(w))} р."
    if r < 0.92:
        return f"{int(round(w))} руб. в год"
    return f"{int(round(w))}"


def tab_fmt(t):
    r = rng.random()
    if r < 0.6:
        return str(t)
    if r < 0.75:
        return f"{t:05d}"
    if r < 0.9:
        return f"№ {t}"
    return f" {t} "


def pos_text(dept, level, form):
    return POS[dept][level][form]


def pos_raw(dept, level):
    nom = POS[dept][level][0]
    if nom in POS_ABBR and rng.random() < 0.35:
        nom = rng.choice(POS_ABBR[nom])
    if rng.random() < 0.15:
        nom = nom.capitalize()
    if rng.random() < 0.05:
        return ''
    return nom


rows = []
staff = []
LOST_LISTS = {1893, 1906}
for p in people:
    unrecorded_exit = p['exit_y'] is not None and rng.random() < 0.075
    prev_lvl = None
    for ev in sorted(p['events'], key=lambda e: e[1]):
        kind, d, lvl, dept, extra = ev
        if d.year < 1885 and kind in ('award', 'leave', 'fine') and rng.random() < 0.6:
            continue
        if kind == 'exit' and unrecorded_exit:
            continue
        sal = ''
        if kind == 'hire':
            v = rng.choice(['Определён', 'определён на службу', 'принят', 'Зачислен', 'определен'])
            txt = f"{v} {pos_text(dept, lvl, 1)}" + (f" {DEPT_ACC[dept]}" if rng.random() < 0.7 else '')
            sal = fmt_wage(extra, lvl, dept)
        elif kind == 'promo':
            r = rng.random()
            if r < 0.5:
                txt = f"назначен {pos_text(dept, lvl, 1)}"
            elif r < 0.8:
                txt = f"переведён на должность {pos_text(dept, lvl, 2)}"
            else:
                txt = f"утверждён в должности {pos_text(dept, lvl, 2)}"
            sal = fmt_wage(extra, lvl, dept)
        elif kind == 'transfer':
            txt = rng.choice(['переведён', 'Переведен', 'перемещён']) + f" {DEPT_ACC[dept]}" + rng.choice(['', ' тем же званием', ' на ту же должность'])
            sal = fmt_wage(extra, lvl, dept)
        elif kind == 'wage':
            txt = rng.choice(['прибавлено жалованье', 'Назначено жалованье', 'жалованье увеличено', 'прибавка к жалованью'])
            sal = fmt_wage(extra, lvl, dept)
        elif kind == 'award':
            txt = rng.choice(['награждён серебряной медалью «За усердие»', 'объявлена благодарность начальника мастерских',
                              'выдано денежное награждение 10 р.', 'награжден наградными 15 руб.'])
        elif kind == 'leave':
            txt = rng.choice(['уволен в отпуск на 28 дней', 'уволен в отпуск по болезни', 'уволен в отпуск на 2 мес. по домашним обстоятельствам',
                              'увольнен в отпуск на 14 дн.', 'отпуск 1 мес.'])
        elif kind == 'fine':
            txt = rng.choice(['оштрафован на 3 р. за прогул', 'оштрафован за опоздание', 'сделан выговор', 'вычтено из жалованья 2 р. за порчу инструмента'])
        elif kind == 'exit':
            reason = extra
            if reason == 'умер':
                txt = rng.choice(['умер', 'Исключён из списков за смертью', 'исключен за смертью', 'умре'])
            elif reason == 'с пенсией за выслугою лет':
                txt = rng.choice(['уволен с пенсией за выслугою лет', 'уволен в отставку с пенсией', 'вышел на пенсию'])
            else:
                txt = rng.choice(['уволен', 'Уволен', 'уволен со службы', 'увол.']) + ' ' + reason
                if rng.random() < 0.05:
                    txt = rng.choice(['выбыл', 'рассчитан', 'Рассчитан по прошению'])
        if d.year < 1918 and rng.random() < (0.55 if d.year < 1900 else 0.25):
            txt = old_orth(txt)
        if rng.random() < 0.1:
            txt = txt.lower()
        if rng.random() < 0.05:
            txt = '  ' + txt
        dept_raw = '' if rng.random() < 0.12 else rng.choice(DEPT_NAME[dept])
        pr = pos_raw(dept, lvl) if kind not in ('award', 'leave', 'fine') or rng.random() < 0.3 else ''
        fond = f"Ф. {rng.choice([187, 187, 187, 421])}. Оп. {rng.choice([1, 2, 2, 3])}. Д. {rng.integers(1, 900)}. Л. {rng.integers(1, 300)}" + (' об.' if rng.random() < 0.3 else '')
        note = ''
        rr = rng.random()
        if rr < 0.03:
            note = 'текст частично утрачен'
        elif rr < 0.05:
            note = 'зачёркнуто'
        elif rr < 0.07:
            note = 'см. приказ'
        elif rr < 0.08:
            note = 'по старому стилю'
        rows.append(dict(tab=tab_fmt(p['tab']), date_raw=fmt_date(d), text=txt, dept=dept_raw, position=pr, salary=sal, source=fond, note=note))
    # ведомости личного состава на 1 января
    for y in range(1885, 1915):
        if y in LOST_LISTS or y not in p['history']:
            continue
        if rng.random() < 0.012:
            continue
        lvl, dept, w = p['history'][y]
        fio = p['fio'] if rng.random() > 0.15 else old_orth(p['fio'])
        staff.append(dict(year=y, tab_no=f"{p['tab']}" if rng.random() < 0.8 else f"таб. {p['tab']}", fio=fio,
                          position=pos_raw(dept, lvl), shop=rng.choice(DEPT_NAME[dept]), salary_year=str(int(round(w))) if rng.random() > 0.05 else ''))

# сироты: записи по номерам, которых нет в формулярах
for _ in range(150):
    t = int(rng.integers(30000, 31000))
    rows.append(dict(tab=str(t), date_raw=fmt_date(rand_date(int(rng.integers(1885, 1914)))), text=rng.choice(['прибавлено жалованье', 'определён подручным', 'уволен по прошению']),
                     dept='', position='', salary='', source='Ф. 421. Оп. 3. Д. 12. Л. 4', note='номер не читается' if rng.random() < 0.5 else ''))

rec = pd.DataFrame(rows)
# копии послужного списка: точные дубли и копии с другой записью даты
dup_exact = rec.sample(frac=0.018, random_state=1)
dup_copy = rec.sample(frac=0.02, random_state=2).copy()
dup_copy['source'] = dup_copy['source'].str.replace('Ф. 187', 'Ф. 421', regex=False)
dup_copy['note'] = 'копия'
rec = pd.concat([rec, dup_exact, dup_copy], ignore_index=True)
rec = rec.sample(frac=1, random_state=3).reset_index(drop=True)
rec.insert(0, 'rec_id', np.arange(1, len(rec) + 1))
rec.to_csv(f'{OUT}/service_records.csv', index=False)

form = []
for p in people:
    r = rng.random()
    b = p['birth']
    if r < 0.55:
        br = str(b)
    elif r < 0.7:
        br = f"{b} г."
    elif r < 0.78:
        br = f"ок. {b}"
    elif r < 0.85:
        br = f"{rng.integers(1, 28)}.{rng.integers(1, 13):02d}.{b}"
    elif r < 0.9:
        br = f"{p['hire_y'] - b} лет на {p['hire_y']} г."
    elif r < 0.93:
        br = str(b)[2:]
    else:
        br = ''
    sosl = rng.choice(SOSL[p['sosl']]) if rng.random() > 0.04 else ''
    edu = rng.choice(EDU[p['edu']]) if rng.random() > 0.09 else ''
    form.append(dict(tab_no=p['tab'], fio=p['fio'], born=br, estate=sosl, education=edu, origin=rng.choice(GUB) if rng.random() > 0.06 else ''))
form = pd.DataFrame(form)
form = pd.concat([form, form.sample(frac=0.01, random_state=5)]).sample(frac=1, random_state=6)
form.to_csv(f'{OUT}/formulary.csv', index=False)

st = pd.DataFrame(staff)
st = st.sample(frac=1, random_state=7)
st.to_csv(f'{OUT}/staff_lists.csv', index=False)
print(rec.shape, form.shape, st.shape)

# истинная история для проверки (в репозиторий не идёт)
truth = pd.DataFrame([dict(tab=p['tab'], hire_y=p['hire_y'], exit_y=p['exit_y'], dept0=p['dept'], sosl=p['sosl'], edu=p['edu'], birth=p['birth']) for p in people])
truth.to_csv(f'/home/claude/gen/truth.csv', index=False)
