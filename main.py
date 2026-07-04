from collections import OrderedDict, defaultdict
from datetime import date,datetime,timezone,timedelta
import math , os
from flask import Flask, render_template, request,jsonify
from dingtalk import UserAPI,RecordAPI,init_token_manager
from datehelper import FormatAPI
from dotenv import load_dotenv

app= Flask(__name__)

load_dotenv()

"""
initial app_key and app_secret to get access token
"""


app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")

if not app_key or not app_secret:
    raise RuntimeError("APP_KEY or APP_SECRET is missing.")


init_token = init_token_manager(app_key,app_secret)




urls = []



def format_datetime(value, fmt="%Y-%m-%d %H:%M:%S"):
    dt = datetime.fromisoformat(value)
    return dt.strftime(fmt)

app.jinja_env.filters['format_datetime'] = format_datetime

def get_paginated_items(items,page_num,per_page):
    start_index = (page_num - 1) * per_page
    end_index = start_index + per_page
    return items[start_index:end_index]


@app.route('/', methods=['GET', 'POST'])
def records():

    today_str = date.today().strftime('%Y-%m-%d')

    start_date = request.args.get('startDate') or request.form.get('startDate') or today_str
    end_date = request.args.get('endDate') or request.form.get('endDate') or today_str
    selected_users = request.args.getlist('userids') or request.form.getlist('userids')

    user_list_resp = UserAPI().get_user()
    users = user_list_resp['result']['list']

    if not selected_users and users:
        selected_users = [users[13]['userid'],users[11]['userid']]
    all_records = []

    for user_id in selected_users:
        user_detail = UserAPI().get_user_detail(user_id)
        user_name = user_detail['result']['name']

        api_resp = RecordAPI(
            user_id,
            start_date=start_date,
            end_date=end_date
        ).get_thumb_record()

        records_list = api_resp.get('recordresult', [])

        if not records_list:
            all_records.append({
                'name': user_name,
                'clock_in': '-',
                'clock_out': '-',
                'rest': '-',
                'workDate_formatted': start_date,
                'empty': True
            })
        else:
            temp = defaultdict(list)

            for record in records_list:
                work_date = FormatAPI(record.get('workDate')).date_day_format()
                base_time = FormatAPI(record.get('baseCheckTime')).time_only_format()
                record['baseCheckTime_formatted'] = base_time
                temp[work_date].append(record)

            for work_date, recs in temp.items():

                recs.sort(key=lambda r: r.get('baseCheckTime') or '9999-12-31 23:59:59')

                clock_in = '-'
                clock_out = '-'
                rest = '-'

                # First OnDuty
                for r in recs:
                    if r.get('checkType') == 'OnDuty':
                        clock_in = r['baseCheckTime_formatted']
                        break

                # Last OffDuty
                for r in reversed(recs):
                    if r.get('checkType') == 'OffDuty':
                        clock_out = r['baseCheckTime_formatted']
                        break

                # Rest periods
                rest_periods = []
                i = 0
                while i < len(recs) - 1:
                    if recs[i].get('checkType') == 'OffDuty' and recs[i+1].get('checkType') == 'OnDuty':
                        rest_periods.append(
                            f"{recs[i]['baseCheckTime_formatted']} - {recs[i+1]['baseCheckTime_formatted']}"
                        )
                        i += 2
                    else:
                        i += 1

                if rest_periods:
                    rest = '; '.join(rest_periods)

                all_records.append({
                    'name': user_name,
                    'clock_in': clock_in,
                    'clock_out': clock_out,
                    'rest': rest,
                    'workDate_formatted': work_date,
                    'empty': False
                })

    all_records.sort(
        key=lambda x: (x['name'], x['workDate_formatted']),
        reverse=True
    )

    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_items = len(all_records)
    total_pages = math.ceil(total_items / per_page)

    paginated_items = get_paginated_items(all_records, page, per_page)

    grouped_records = defaultdict(list)
    for record in paginated_items:
        grouped_records[record['name']].append(record)

    display_fields = [
        ('clock_in', 'Clock In'),
        ('clock_out', 'Clock Out'),
        ('rest', 'Rest'),
        ('workDate_formatted', 'Work Date')
    ]

    return render_template(
        "records.html",
        grouped_records=grouped_records,
        display_fields=display_fields,
        start_date=start_date,
        end_date=end_date,
        users=users,
        selected_users=selected_users,
        items=paginated_items,
        total_pages=total_pages,
        current_page=page,
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=8000)
