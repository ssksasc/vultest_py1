import sys
import json
from datetime import date, datetime
import bcrypt

### debug ----------------------------------------
def debug(text, obj):
    print('Debug : {}({}, {})'.format(text, str(obj), type(obj)), file=sys.stderr)
def error(text, obj):
    print('Error : {}({}, {})'.format(text, str(obj), type(obj)), file=sys.stderr)

### datetime ----------------------------------------
def now():
    return datetime.now()
def strftime(time):
    return time.strftime('%Y-%m-%d %H:%M:%S')
def strptiem(strtime):
    return datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')
def strfdate(time):
    return time.strftime('%Y-%m-%d')

### json ----------------------------------------
def _json_default(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    elif isinstance(item, (datetime, date)):
        return strftime(item)
    else:
        error('Json encode Error', item)
        raise TypeError
def json_dump(data):
    return json.dumps(data, default=_json_default, indent=2)

### password ----------------------------------------
def passHash(password):
    salt = bcrypt.gensalt(rounds=10, prefix=b'2a')
    passhash = bcrypt.hashpw(password.encode(), salt).decode()
    return passhash
def passCheck(password, passhash):
    return bcrypt.checkpw(password.encode(), passhash.encode())

### validation ----------------------------------------
def getApprovals(approval_type):
    approvals = ''
    if 'a' in approval_type:
        approvals += 'abcdefghijklmnopqrstuvwxyz'
    if 'A' in approval_type:
        approvals += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if '0' in approval_type:
        approvals += '0123456789'
    if '!' in approval_type:
        approvals += '!#$%&=~|+-*?_.,'
    if '@' in approval_type:
        approvals += '@'
    return approvals
def inputCheck(string, minlength, maxlength, approval_type):
    strlen = len(string)
    if minlength > 0 and strlen < minlength:
        return False
    if maxlength > 0 and strlen > maxlength:
        return False
    if approval_type != '':
        approvals = getApprovals(approval_type)
        for c in string:
            if not c in approvals:
                return False
    return True





