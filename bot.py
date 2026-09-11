import json, os, time, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
def _token():
    t = os.environ.get('TG_TOKEN')
    if t: return t.strip()
    p = os.path.join(BASE, 'config.txt')
    if os.path.exists(p):
        t = open(p, 'r', encoding='utf-8-sig').read().strip()
        if t: return t
    raise SystemExit('ТОКЕН НЕ ЗАДАНИЙ: збережіть токен BotFather у C:\\ua-bot\\config.txt')
TOKEN = _token()
API = 'https://api.telegram.org/bot' + TOKEN
HR_CHAT = int(os.environ.get('HR_CHAT', '0'))  # ID чату кадрів (змінити на свій)

def tg(method, **kw):
    req = urllib.request.Request(API + '/' + method,
        data=json.dumps(kw).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    r = urllib.request.urlopen(req, timeout=90)
    j = json.loads(r.read().decode('utf-8'))
    if not j.get('ok'):
        raise RuntimeError(method + ': ' + str(j.get('description')))
    return j['result']

REGIONS = [
 ('Київ','kyiv'), ('Крим','crimea'), ('Вінниця','vinn'),
 ('Волинь','volyn'), ('Дніпро','dnip'), ('Донецьк','don'),
 ('Запоріжжя','zapor'), ('Закарпаття','zakarp'), ('Івано-Франківськ','ivan'),
 ('Кіровоград','kirov'), ('Київщина','kyivobl'), ('Луганськ','luh'),
 ('Львів','lviv'), ('Миколаїв','nik'), ('Одеса','odesa'),
 ('Полтава','poltava'), ('Рівне','rivne'), ('Суми','sumy'),
 ('Тернопіль','tern'), ('Харків','kharkiv'), ('Херсон','kherson'),
 ('Хмельницький','khmel'), ('Черкаси','cherkasy'), ('Чернігів','chernih'),
 ('Чернівці','cherniv'), ('Севастополь','sevast'),
]
ORGS = {
'kyiv':[('«Безмежний світ»','розвиток і соціалізація дітей з особливими потребами: майстерні, походи, інклюзивні свята',['on-site','distance']),
        ('«Карітас України»','продуктові банки, гарячі обіди та підтримка людей похилого віку',['donation','distance'])],
'crimea':[('«Кримське серце»','відвідування та супровід людей похилого віку, допомога з документами',['on-site','distance']),
          ('«Ай-Петрі»','адаптивний туризм: походи для людей з інвалідністю',['on-site','donation'])],
'vinn':[('«Подільське серце»','підтримка ветеранів та людей похилого віку: відвідування, справи',['on-site','distance']),
        ('«Світло»','збір обладнання для дитячих шпиталів області',['donation','distance'])],
'volyn':[('«Вільне серце»','день-центр для людей похилого віку: обіди, концерти, прогулянки',['on-site','distance']),
         ('«Коріння»','сільські школи: приналежності, спорт, екскурсії для дітей',['on-site','donation'])],
'dnip':[('«Дніпрове добро»','доставка їжі та ліків тим, хто не може вийти з дому',['on-site']),
        ('«Мости»','менторство та кар’єрна підтримка ветеранів і переселенців',['distance','on-site'])],
'don':[('«Східний світ»','підтримка дітей-переселенців: навчання, психологія, гуртки',['on-site','distance']),
       ('«Новий дім»','пошук та облаштування житла для внутрішньо переміщених осіб',['donation','on-site'])],
'zapor':[('«Заря»','дитячі спортивні та творчі табори',['on-site','donation']),
         ('«Січ»','підтримка ветеранів: реабілітація, спортивні секції, менторство',['on-site','distance'])],
'zakarp':[('«Карпатська іскра»','сільські школи та бібліотеки: книжки, приналежності, подорожі',['on-site','donation']),
          ('«Бескид»','адаптивний туризм Карпат для людей з інвалідністю',['on-site','distance'])],
'ivan':[('«Галицьке серце»','прихисток і денне відділення для дітей та родин у складних ситуаціях',['donation','on-site']),
        ('«Солов’ї»','музична терапія для людей похилого віку',['on-site','distance'])],
'kirov':[('«Печенізький дім»','день-центр для людей з інвалідністю: їжа, дозвілля, соціалізація',['on-site','distance']),
         ('«Степові»','прибирання парків та лісів, еко-освіта',['on-site'])],
'kyivobl':[('«Добрий поріг»','день-центр для людей похилого віку: обіди, заняття, відвідування',['on-site','distance']),
           ('«Козацька спадщина»','екскурсії та музеї для ветеранів і родин',['on-site','donation'])],
'luh':[('«Світло на Сході»','підтримка родин-переселенців: навчання, психологія, речі для дітей',['donation','distance']),
       ('«Вугільне серце»','допомога сім’ям шахтарів і ветеранів: обіди, гуртки, відвідування',['on-site','distance'])],
'lviv':[('«Львівське серце»','прихисток для безпритульних та денний центр для людей похилого віку',['donation','on-site']),
        ('«Галицька дитина»','збір коштів на лікування дітей області',['donation','distance'])],
'nik':[('«Южанка»','дитячі гуртки, секції та табірний сезон',['on-site','donation']),
       ('«Портові»','підтримка ветеранів і сімей портовиків: менторство, спорт',['on-site','distance'])],
'odesa':[('«Чорноморська надія»','обладнання та витратні матеріали для обласної лікарні',['donation','distance']),
         ('«Дельта»','спраця Дніпра та морського узбережжя, еко-проєкти',['on-site','donation'])],
}
ORGS.update({
'poltava':[('«Соняшники»','дитячі табори, гуртки та екскурсії для сімей',['on-site','donation']),
           ('«Гетьманське»','культурні екскурсії для людей похилого віку та ветеранів',['on-site','distance'])],
'rivne':[('«Поліське серце»','відвідування, обіди та супровід людей похилого віку',['on-site','distance']),
         ('«Дуброви»','озеленення міста та догляд за парками',['on-site','donation'])],
'sumy':[('«Слобожанщина»','підтримка ветеранів: секції, менторство, відвідування',['on-site','distance']),
        ('«Окунівка»','дитячі майстерні та гуртки для сільських шкіл',['on-site','donation'])],
'tern':[('«Карпатська хата»','облаштування житла для родин переселенців',['donation','on-site']),
        ('«Збруч»','спраця річок і лісів, еко-освіта',['on-site'])],
'kharkiv':[('«Харківське серце»','прихисток і денне відділення для дітей і родин',['donation','on-site']),
           ('«Вовчки-Добро»','підтримка дітей: навчання, психологія, гуртки',['on-site','distance'])],
'kherson':[('«Степ-Добро»','спраця степових екосистем і міських парків',['on-site','donation']),
           ('«Юг»','підтримка ветеранів і родин: менторство, спорт, відвідування',['on-site','distance'])],
'khmel':[('«Поділля-Добро»','день-центр для людей похилого віку: обіди, концерти, прогулянки',['on-site','distance']),
         ('«Кам’янець»','культурні та історичні екскурсії для старшого покоління',['on-site','donation'])],
'cherkasy':[('«Дніпровські пороги»','спраця Дніпра та міських парків, еко-освіта',['on-site','donation']),
            ('«Черкаське серце»','підтримка дітей-переселенців: навчання, психологія, речі',['donation','distance'])],
'chernih':[('«Десна»','спраця річок, парків і лісів області',['on-site','donation']),
           ('«Чернігів-Добро»','відвідування та супровід людей похилого віку',['on-site','distance'])],
'cherniv':[('«Буковинське серце»','день-центр для людей похилого віку та ветеранів',['on-site','distance']),
           ('«Прут»','спраця річок і лісів, еко-проєкти',['on-site','donation'])],
'sevast':[('«Морська надія»','обладнання та витратні матеріали для лікарні міста',['donation','distance']),
          ('«Чорноморці»','підтримка ветеранів флоту та їхніх родин',['on-site','distance'])],
})
PREF = {'g':['on-site','distance'],'y':['distance','on-site'],'o':['distance','donation'],'r':['donation','distance']}
ZTXT = {
 'g':('Хороший стан','🟢',"Енергії вистачає — час на «активну» допомогу: вихід на волонтерський день або акція разом із колективом."),
 'y':('Робочий стан — слідкуйте за навантаженням','🟡',"Легкий стрес. Не форсуйте: підійде формат «на відстані» — менторство, дзвінки, сортування вдома."),
 'o':('Увага: стрес накопичується','🟠',"Час подбати про себе. Почніть з мікрокроків: година на тиждень — і ви вже потрібні."),
 'r':('Критично: ризик вигорання','🔴',"Будьте обережні — ризик вигорання високий. Почніть із найлегшого: донат або онлайн-акція, а головне — візьміть відпустку."),
}
TAGS = {'on-site':'📍 на місці','distance':'🏠 на відстані','donation':'💛 донат'}
STEPS = ['mood','battery','sleep','exhaust','cynic','hours','support','vacation','future']
state = {}
def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

def kb(rows):
    return {'inline_keyboard': rows}

def ask(chat, text, buttons, rows):
    tg('sendMessage', chat_id=chat, text=text, reply_markup=kb(buttons))
    state[chat] = {'step': rows}

def start(chat):
    state[chat] = {'step': 'region'}
    tg('sendMessage', chat_id=chat, text=(
        'Вітаю! Я — бот <b>Перепочинок</b> 🌿\n'
        '10 коротких питань, 3–5 хвилин — і я покажу, як ваша команда тримається цього місяця.\n'
        'Повна анонімність: кадровики бачать лише «температуру колективу».'), parse_mode='HTML')
    tg('sendMessage', chat_id=chat, text='Де ви працюєте?',
       reply_markup=kb([[{'text': l, 'callback_data': 'region:' + c} for l, c in g] for g in chunked(REGIONS, 3)]))

def nxt(chat):
    i = STEPS.index(state[chat]['step'])
    if i + 1 >= len(STEPS): return done(chat)
    state[chat]['step'] = STEPS[i+1]
    Q[state[chat]['step']](chat)

STOPS = {'battery': True}
def q_mood(c):
    tg('sendMessage', chat_id=c, text='Спершу виміряємо температуру. Як ви себе відчуваєте сьогодні?',
       reply_markup=kb([[{'text': m, 'callback_data': 'mood:' + str(i)}] for m, i in zip(['😊','🙂','😐','😕','😫'], range(5))]))
def q_battery(c):
    tg('sendMessage', chat_id=c, text='Оцініть рівень енергії, ніби це заряд телефону: надішліть цифру від 0 до 100.')
def q_sleep(c):
    _q4(c, 'Як часто ви засинаєте, думаючи про роботу?', ['майже ніколи','часом','часто','кожного дня'], 'sleep')
def q_exhaust(c):
    _q5(c, 'Наприкінці дня я відчуваю себе виснаженим, навіть після відпочинку.', 'exhaust')
def q_cynic(c):
    _q5(c, 'Результати моєї роботи здаються мені дедалі менш важливими.', 'cynic')
def q_hours(c):
    _q4(c, 'Скільки годин ви насправді працювали минулого тижня?', ['до 40','41–48','49–56','понад 56'], 'hours')
def q_support(c):
    _q4(c, 'Чи є з ким на роботі поділити завдання?', ['так','важко сказати','ні'], 'support')
def q_vacation(c):
    _q4(c, 'Коли ви востаннє належно відпочивали?', ['цього місяця','до 3 місяців','до пів року','щиро забув'], 'vacation')
def q_future(c):
    _q4(c, 'Останнє. Через 5 років ви все ще хочете працювати в цій сфері?', ['так','мабуть','не знаю','щиро ні'], 'future')

def _q4(c, text, opts, key):
    tg('sendMessage', chat_id=c, text=text,
       reply_markup=kb([[{'text': o, 'callback_data': key + ':' + str(i)}] for o, i in zip(opts, range(len(opts)))]))
def _q5(c, text, key):
    opts = ['1 — зовсім ні','2','3','4','5 — цілком']
    tg('sendMessage', chat_id=c, text=text,
       reply_markup=kb([[{'text': o, 'callback_data': key + ':' + str(i+1)}] for o, i in zip(opts, range(5))]))
Q = {'mood': q_mood, 'battery': q_battery, 'sleep': q_sleep, 'exhaust': q_exhaust,
     'cynic': q_cynic, 'hours': q_hours, 'support': q_support, 'vacation': q_vacation, 'future': q_future}
MONTHS = ['січень','лютий','березень','квітень','травень','червень','липень','серпень','вересень','жовтень','листопад','грудень']
def calc(S):
    vac = S.get('vacation', 0)
    stress = min(100, round((S['sleep']*.35 + (S['exhaust']-1)*.35 + S['hours']*.15 + vac*.15)/3*100))
    burnout = min(100, round(((S['exhaust']-1)*.35 + (S['cynic']-1)*.35 + S['future']*.2 + S['support']*.1)/4*100))
    overall = round(S['battery']*.4 + (100-stress)*.3 + (100-burnout)*.3)
    z = 'g' if overall>=80 else 'y' if overall>=60 else 'o' if overall>=40 else 'r'
    return stress, burnout, overall, z

def done(chat):
    S = state[chat]
    tg('sendChatAction', chat_id=chat, action='typing')
    time.sleep(1.2)
    stress, burnout, overall, z = calc(S)
    title, emoji, advice = ZTXT[z]
    pref = PREF[z]
    scored = sorted(ORGS[S['region']], key=lambda o: -((2 if pref[0] in o[2] else 0) + (1 if pref[1] in o[2] else 0)))
    now = datetime.now()
    lines = ['🌿 <b>Ваш чек-ап — ' + MONTHS[now.month-1] + ' ' + str(now.year) + '</b>',
             emoji + ' <b>' + title + '</b>', '',
             '😰 Стрес: ' + str(stress) + '%',
             '🔥 Ризик вигорання: ' + str(burnout) + '%',
             '🔋 Енергія: ' + str(S['battery']) + '%', '', advice, '',
             '🤝 <b>Кому зараз потрібна допомога у вашому регіоні:</b>']
    for i, (name, desc, tags) in enumerate(scored[:2], 1):
        lines.append(str(i) + ') <b>' + name + '</b> — ' + desc)
        lines.append('   ' + ' · '.join(TAGS[t] for t in tags))
    lines += ['', 'Результат анонімний: для кадрників це просто ще одна точка «температури колективу».']
    tg('sendMessage', chat_id=chat, text='\n'.join(lines), parse_mode='HTML')
    tg('sendMessage', chat_id=chat, text='Наступний крок?',
       reply_markup=kb([[{'text':'✅ Надіслати анонімно','callback_data':'act:send'}],
                         [{'text':'↻ Пройти ще раз','callback_data':'act:again'}]]))
    S['step'] = 'result'
    S['last'] = (now.isoformat(), S['region'], stress, burnout, S['battery'], z)

def save_hr(chat):
    S = state[chat]
    p = os.path.join(BASE, 'results.json')
    rows = []
    if os.path.exists(p):
        try: rows = json.load(open(p, encoding='utf-8'))
        except Exception: rows = []
    rows.append({'ts': S['last'][0], 'region': S['last'][1], 'stress': S['last'][2],
                 'burnout': S['last'][3], 'energy': S['last'][4], 'zone': S['last'][5]})
    json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tg('sendMessage', chat_id=chat, text='Готово! Вашу точку додано до «температури колективу» 📊\nДякую — до зустрічі на наступній каві ☕')

def hr_report(chat):
    p = os.path.join(BASE, 'results.json')
    rows = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []
    if not rows:
        tg('sendMessage', chat_id=chat, text='Температура колективу: відповідей ще немає.'); return
    n = len(rows)
    avg = lambda k: round(sum(r[k] for r in rows)/n)
    zc = {}
    for r in rows: zc[r['zone']] = zc.get(r['zone'], 0) + 1
    zt = {'g':'🟢 ' + str(zc.get('g',0)), 'y':'🟡 ' + str(zc.get('y',0)), 'o':'🟠 ' + str(zc.get('o',0)), 'r':'🔴 ' + str(zc.get('r',0))}
    tg('sendMessage', chat_id=chat, text=(
        '📊 <b>Температура колективу</b> (' + str(n) + ' відповідей)\n'
        '😰 Середній стрес: ' + str(avg('stress')) + '%\n'
        '🔥 Середній ризик вигорання: ' + str(avg('burnout')) + '%\n'
        '🔋 Середня енергія: ' + str(avg('energy')) + '%\n'
        ' '.join(zt.values())), parse_mode='HTML')

def on_message(chat, text):
    t = text.strip()
    if t.startswith('/start') or t.startswith('/restart'):
        return start(chat)
    if t.startswith('/hr'):
        return hr_report(chat)
    S = state.get(chat)
    if S and S.get('step') == 'battery' and t.isdigit() and 0 <= int(t) <= 100:
        S['battery'] = int(t)
        return nxt(chat)
    if S:
        tg('sendMessage', chat_id=chat, text='Оберіть відповідь кнопкою нижче 🙂')

def on_callback(q):
    chat = q['message']['chat']['id']
    data = q.get('data') or ''
    key, _, val = data.partition(':')
    tg('answerCallbackQuery', callback_query_id=q['id'])
    S = state.get(chat)
    if not S:
        print('state empty, auto-restart, chat=' + str(chat))
        return start(chat)
    if key == 'region':
        S['region'] = val; S['step'] = 'mood'; return q_mood(chat)
    if key == 'act':
        return save_hr(chat) if val == 'send' else start(chat)
    if key in Q:
        S[key] = int(val)
        return nxt(chat)

def _http_keepalive():
    port = os.environ.get('PORT')
    if not port:
        print('http keep-alive: off (no PORT env)'); return
    import http.server, threading
    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'ok')
        def log_message(self, *a): pass
    srv = http.server.HTTPServer(('0.0.0.0', int(port)), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print('http keep-alive: listening on :' + port)
_http_keepalive()

offset = 0
print('Бот «Перепочинок» запущено (токен **/' + TOKEN[-4:] + ')')
while True:
    try:
        ups = tg('getUpdates', offset=offset, timeout=50, allowed_updates=['message','callback_query'])
        for u in ups:
            offset = u['update_id'] + 1
            m = u.get('message')
            if m and m.get('chat') and m.get('text'):
                on_message(m['chat']['id'], m['text'])
            elif u.get('callback_query'):
                on_callback(u['callback_query'])
    except Exception as e:
        print('Помилка:', e)
        time.sleep(5)
