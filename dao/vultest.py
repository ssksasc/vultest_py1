from dbcon import db
import util

'''
create table vultest (
    `id`       int unsigned not null auto_increment,
    `category` int unsigned not null,
    `name`     varchar(32)  not null,
    `number`   int unsigned not null,
    `text`     varchar(256) not null,
    `idate`    datetime     not null,
    `udate`    datetime     not null,
    primary key (`id`),
    index `idx_vultest_1` (`id`, `category`, `name`)
);

'''

CT_XSSST = 1
CT_SQLI   = 2

class Vultest:
    def __init__(self, entry):
        self.id       = entry[0]
        self.category = entry[1]
        self.name     = entry[2]
        self.number   = entry[3]
        self.text     = entry[4]
        self.idate    = entry[5]
        self.udate    = entry[6]

### ------------------------------------------------------------

def valid_name(name):
    if len(name) <= 32:
        return True
    return False


### ------------------------------------------------------------

def get_one(vtid):
    sql = '''
    select * from vultest
    where `id` = %s
    '''
    params = (vtid,)
    data = db.query(sql, params)
    if data is None or len(data) == 0:
        return None
    vt = Vultest(data[0])
    return vt

def get_list_by_category(category):
    sql = '''
    select * from vultest
    where `category` = %s
    '''
    params = (category,)
    data = db.query(sql, params)
    if data is None:
        return []
    vt_list = []
    for entry in data:
        vt_list.append(Vultest(entry))
    return vt_list

def get_list_by_name(name):
    likename = '%{}%'.format(name)
    sql = '''
    select * from vultest
    where `name` like %s
    '''
    params = (likename,)
    data = db.query(sql, params)
    if data is None:
        return []
    vt_list = []
    for entry in data:
        vt_list.append(Vultest(entry))
    return vt_list

def get_list_by_text(text): ### vulnerable
    sql = '''
    select * from vultest
    where `text` like '%{}%'
    '''.format(text)
    data = db.query(sql)
    if data is None:
        return []
    vt_list = []
    for entry in data:
        vt_list.append(Vultest(entry))
    return vt_list


### ------------------------------------------------------------

def push_one(vt):
    sql = '''
    insert into vultest (`category`, `name`, `number`, `text`, `idate`, `udate`)
    values (%s, %s, %s, %s, now(), now())
    '''
    params = (vt.category, vt.name, vt.number, vt.text)
    return db.execute(sql, params)

def push_list(vt_list):
    sql = '''
    insert into vultest (`category`, `name`, `number`, `text`, `idate`, `udate`)
    values (%s, %s, %s, %s, now(), now())
    '''
    for vt in vt_list:
        params = (vt.category, vt.name, vt.number, vt.text)
        result = db.execute(sql, params)
        if not result:
            return False
    return True

def update_one(vt):
    sql = '''
    update vultest set
        `category` = %s,
        `name`     = %s,
        `number`   = %s,
        `text`     = %s,
        `udate`    = now()
    where `id` = %s
    '''
    params = (vt.category, vt.name, vt.number, vt.text, vt.id)
    return db.execute(sql, params)




