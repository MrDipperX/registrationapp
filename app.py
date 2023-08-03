from flask import Flask, render_template, request, redirect, abort
import requests
import time
import uvicorn
from db.db import PgConn
from config.config import REG_PAGE_TIME, BOT_TOKEN, BOT_USERNAME, APP_HOST, APP_PORT

from utils.constants import FINISH_MESSAGE_INVESTOR, FINISH_MESSAGE_STARTUPPER, INVESTOR

# from utils.loggging import logging

app = Flask(__name__)


# Home page with registration form
@app.route('/chainapp/register/', methods=['GET', 'POST'])
def home():
    # try:
    db_conn = PgConn()

    if request.method == 'GET':
        data = request.args.to_dict()
        code = data['c']
        # user_info = db_conn.get_sec_code_time(code)
        # if user_info is None:

        code_time, user_id = db_conn.get_sec_code_time(code)
        now = time.time()

        if code_time >= now:
            now = time.time()
            code_time = now + REG_PAGE_TIME * 60
            db_conn.update_user_sec_info(user_id, code_time)

            fields = db_conn.get_fields()

            user = db_conn.get_user_full_info(user_id)

            # return render_template('index.html', user_id=user_id)

            return render_template('regFlask/index2.html', user_id=user_id, fields=fields, user=user)

        return render_template('regFlask/return.html', bot=BOT_USERNAME)

    elif request.method == 'POST':
        print(request.form)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        midname = request.form['midname']
        role = request.form['role']
        email = request.form['email']
        phone = request.form['phone']
        soc_link = request.form['socLink']
        user_id = request.form['userId']

        field = request.form.getlist('field')
        field = [int(f) for f in field]

        code, code_time = db_conn.get_user_sec_info(user_id)
        now = time.time()
        if code_time >= now:

            db_conn.update_user(user_id, firstname, lastname, midname, role, email, phone, soc_link)

            if role == "Startupper":
                startupp_name = request.form['startupName']
                startupp_desc = request.form['startupDescription']

                db_conn.add_startup(user_id, startupp_name, startupp_desc)

            db_conn.set_field(user_id, field)

            return render_template('regFlask/success.html', code=code)

        return render_template('regFlask/return.html', bot=BOT_USERNAME)
    # except TypeError:
    #     abort(400)
    # except Exception as e:
    #     logging.error(e)


@app.route('/chainapp/send_message')
def send_message():
    try:
        db_conn = PgConn()
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        code = request.args.get('c')

        role, user_id = db_conn.get_role_and_idtg(code)

        if role == INVESTOR:
            message = FINISH_MESSAGE_INVESTOR
        else:
            message = FINISH_MESSAGE_STARTUPPER

        requests.post(api_url, json={
            'chat_id': user_id,
            'text': message
        })

        return redirect(f"https://t.me/{BOT_USERNAME}")
    except Exception as e:
        # logging.error(e)

        print(e)
#
# @app.errorhandler(500)
# def internal_error(error):
#
#     return "500 error"
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return "404 error"
#
#
# @app.errorhandler(400)
# def bad_request(error):
#     return "400 error"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2610)
