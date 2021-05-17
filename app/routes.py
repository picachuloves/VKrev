from app import server
from flask import render_template, request, redirect, jsonify, url_for, session
from app.vkparser import VkParser
from app.vkauth import VkAuth
from app.classifier import Classifier
from flask_login import current_user, login_required
from app.models import User
from app import db
import os
import shutil


vkauth = VkAuth()
classifier = Classifier()


@server.route('/')
@server.route('/index')
def index():
    global vkparser
    vkparser = VkParser()
    return render_template('index.html')


@server.route('/get_access')
def get_access():
    client_code = request.args.get('code')
    token = vkauth.get_session(client_code)
    vkparser.new_api(token)
    return redirect(url_for('index'))


@server.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        return redirect(vkauth.authorize())
    return redirect(url_for('index'))


@server.route('/logout')
@login_required
def logout():
    vkauth.logout()
    return redirect(url_for('index'))


@server.route('/test')
@login_required
def test():
    # res = vkparser.check_groups()
    a = current_user
    # return jsonify(res)
    return jsonify(current_user.id)


@server.route('/load', methods=['GET', 'POST'])
@login_required
def load():
    # 107376732_33308147 9154https://vk.com/topic-107376732_33308147 ?offset=9120 420
    # 15811056_22459674 8549 https://vk.com/topic-15811056_22459674 duhi
    # 64545476_29268766 3748 https://vk.com/topic-64545476_29268766 odezhda
    groups = {
        'Интернет-магазин женской одежды': ['Отзывы'],
        '4:20 SHOP': ['Напиши пожалуйста отзыв:'],
        'Духи.рф ✦ Магазин парфюмерии': ['Отзывы о нашем магазине']
    }
    names = {'Интернет-магазин женской одежды': '64545476',
             '4:20 SHOP': '107376732',
             'Духи.рф ✦ Магазин парфюмерии': '15811056'}
    ids = {
        '64545476': ['29268766'],
        '107376732': ['33308147'],
        '15811056': ['22459674']
    }
    counts = {'29268766': 3748,
              '33308147': 9154,
              '22459674': 8549}

    if request.method == 'POST':
        name = request.form['name']
        user = User.query.filter_by(id=current_user.id).first()
        user.name = name
        db.session.commit()
        method = request.form['method']
        group = request.form['group']
        board = request.form['board']
        board_index = groups[group].index(board)
        group_id = names[group]
        board_id = ids[group_id][board_index]
        count = counts[board_id]
        path = vkparser.load(group_id, board_id, count, name)
        classifier.classify(path, method)
        print('loaded')
        return jsonify(dict(redirect=url_for(f'/dashboard/')))

    return render_template('load.html', groups=groups)


@server.route('/dashs', methods=['GET', 'POST'])
@login_required
def dashs():
    dirname = f'results/{current_user.id}'
    if request.method == 'POST':
        if 'btn' in  request.form:
            name = request.form['btn']
            print(name)
            user = User.query.filter_by(id=current_user.id).first()
            user.name = name
            db.session.commit()
            return redirect(url_for('/dashboard/'))
        if 'delete' in request.form:
            delete = request.form['delete']
            shutil.rmtree(dirname + '/' + delete)
    files = os.listdir(dirname)
    return render_template('dashs.html', dashs=files)