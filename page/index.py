from datetime import datetime

from flask import request, render_template, redirect, url_for

import dao.vultest

def get():
    return render_template('index.html', vt_list=None)

#def get_data():
#    category = request.atgs.get('category')
#    data = dao.vultest.get_list_by_category(category)
#    return util.josn_dump(data)

def post_xssrf():
    text = request.form.get('value')
    entry = [0, 0, '送信文字列', 0, text, datetime.now(), datetime.now()]
    vt_list = []
    vt_list.append(dao.vultest.Vultest(entry))
    return render_template('index.html', vt_list=vt_list)

def post_xssst():
    text = request.form.get('value')
    if text != '':
        vt = dao.vultest.Vultest([0, dao.vultest.CT_XSSST, '送信文字列', 0, text, None, None])
        dao.vultest.push_one(vt)
    vt_list = dao.vultest.get_list_by_category(dao.vultest.CT_XSSST)
    return render_template('index.html', vt_list=vt_list)

def post_sqli():
    text = request.form.get('value')
    vt_list = dao.vultest.get_list_by_text(text)
    return render_template('index.html', vt_list=vt_list)

def post_oprd():
    if request.method == 'POST':
        text = request.form.get('value')
        host = request.form.get('host')
    else:
        text = request.args.get('value')
        host = request.args.get('host')
    url = 'http://{host}/vultest/#{text}'.format(host=host, text=text)
    return redirect(url)

