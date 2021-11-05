from django.shortcuts import render, redirect
from datetime import datetime
from .utils import run_sql
from json import dumps

# Create your views here.


# 1
# polling units
def pu(request):
    ids = {}
    sql = 'SELECT * FROM announced_pu_results'
    all_d = run_sql(sql)
    for v in all_d:
        if v[2] in ids.keys():
            ids[v[1]] += v[3]
        else:
            ids[v[1]] = v[3]
    js_ids = dumps(ids)
    return render(request, "pu.html", {'ids': ids, 'js_ids': js_ids})


# 2
def lg(request):
    # local governments
    lg = {}
    sql = 'SELECT * FROM lga'
    lga = run_sql(sql)
    for v in lga:
        query = f'SELECT * FROM polling_unit WHERE lga_id={v[1] }'
        result = run_sql(query)
        # sum of results of all pu in lga
        score = 0
        # polling unit unique ids
        puui = [u[0] for u in result]
        sql = 'SELECT * FROM announced_pu_results'
        pu_results = run_sql(sql)
        for k in pu_results:
            if k[1] in puui:
                print(True)
                score += k[3]
        lg[v[2]] = score
    js_lga = dumps(lg)
    return render(request, 'lg.html', {'lga': lg, 'js_lga': js_lga})


# 3
def party(request):
    sql = 'SELECT * FROM party'
    res = run_sql(sql)
    parties = [r[1] for r in res]
    if request.method == 'POST':
        pu_id = request.POST['pu_id']
        score = request.POST['score']
        for p in parties:
            partyy = request.POST[p]
            datee = datetime.utcnow()

            # im supposed to create  new polling unit first
            # but the data to be added to the table (ward_id and lga_id) isn't available

            sql = "INSERT INTO announced_pu_results (polling_unit_uniqueid, party_abbreviation, party_score, entered_by_user, date_entered, user_ip_address) VALUES ({}, {}, {}, 'bose', {}, '127.0.0.1')".format(pu_id, partyy, score, datee)
            result = run_sql(sql)
    return render(request, "party.html", {'parties': parties})




