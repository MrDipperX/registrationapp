from flask import Flask, render_template, request, redirect, abort
import requests
import time
from db.db import PgConn
from config.config import REG_PAGE_TIME, BOT_TOKEN, BOT_USERNAME, APP_HOST, APP_PORT

from utils.constants import FINISH_MESSAGE_EN, FINISH_MESSAGE_RU, INVESTOR, STARTUPPER, HR, EMPLOYEE

from utils.logging import logging

app = Flask(__name__)


# Home page with registration form
@app.route('/chainapp/register/', methods=['GET', 'POST'])
def home():
    try:
        db_conn = PgConn()

        if request.method == 'GET':
            data = request.args.to_dict()
            code = data['c']

            code_time, user_id = db_conn.get_sec_code_time(code)
            now = time.time()
            user_lang = db_conn.get_user_lang(user_id)

            if code_time >= now:
                now = time.time()
                code_time = now + REG_PAGE_TIME * 60
                db_conn.update_user_sec_info(user_id, code_time)

                # fields = db_conn.get_fields()

                user = db_conn.get_user_full_info(user_id)

                # return render_template('index.html', user_id=user_id)

                return render_template('regFlask/index2.html', user_id=user_id, user=user, lang=user_lang)

            return render_template('regFlask/return.html', bot=BOT_USERNAME, lang=user_lang)

        elif request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            about = request.form['about']
            # midname = request.form['midname']
            role = request.form['role']
            email = request.form['email']
            # phone = request.form['phone']
            soc_link = request.form['socLink']
            user_id = request.form['userId']

            interested_in = [[field] for field in request.form['interestedIn'].split(",")]
            work_with = [[field] for field in request.form['workWith'].split(",")]

            user_lang = db_conn.get_user_lang(user_id)

            code, code_time = db_conn.get_user_sec_info(user_id)
            now = time.time()
            if code_time >= now:
                db_conn.update_user(user_id, firstname, lastname, role, email, soc_link, about)
                interested_in = db_conn.add_fields(interested_in)
                work_with = db_conn.add_fields(work_with)

                if role == STARTUPPER:
                    startupp_name = request.form['startupName']
                    startupp_desc = request.form['startupDescription']

                    db_conn.add_startup(user_id, startupp_name, startupp_desc)

                db_conn.set_work_with(user_id, work_with)
                db_conn.set_interested_in(user_id, interested_in)

                db_conn.update_state(user_id, "finish")

                return render_template('regFlask/success.html', code=code, lang=user_lang)

            return render_template('regFlask/return.html', bot=BOT_USERNAME, lang=user_lang)
    except TypeError as e:
        logging.error(e)
        abort(400)
    except Exception as e:
        logging.error(e)


@app.route('/chainapp/send_message')
def send_message():
    try:
        db_conn = PgConn()
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        code = request.args.get('c')

        role, user_id = db_conn.get_role_and_idtg(code)
        user_lang = db_conn.get_user_lang(user_id)

        if user_lang == 'ru':
            message = FINISH_MESSAGE_RU
        else:
            message = FINISH_MESSAGE_EN

        requests.post(api_url, json={
            'chat_id': user_id,
            'text': message
        })

        return redirect(f"https://t.me/{BOT_USERNAME}")
    except Exception as e:
        logging.error(e)

        # print(e)


@app.errorhandler(500)
def internal_error(error):

    return "500 error"


@app.errorhandler(404)
def not_found(error):
    return "404 error"


@app.errorhandler(400)
def bad_request(error):
    return "400 error"


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
