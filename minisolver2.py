import json

inperson = [
    "CCA Conspiracy",
    "mathforcesbox",
    " JOT"
]

problems = ["oreo_final_main", "caliconstruction_final_main", "scv_final_main", "fortnite_final_main", "bridge_final_main", "bridge_final_bonus", "literally1984_final_main", "literally1984_final_bonus_1", "literally1984_final_bonus_2", "reservoir_final_main", "reservoir_final_bonus", "celeste_final_main", "celeste_final_bonus", "explorer_final_main", "explorer_final_bonus", "vector_final_main", "torreznos_final_main"]

file = open("submissions.json", "r").read()
subs = json.loads(file)

file2 = open("judgements.json", "r").read()
judg = json.loads(file2)

file3 = open("teams.json", "r").read()
team = json.loads(file3)

teams = {}

for t in team:
    id = 0
    if "-" in list(t["id"]):
        id = int(t["id"].split("-")[1])
    else:
        id = int(t["id"])
    name = t["name"]

    if name not in inperson:
        continue

    teams[id] = name

sub_good = {}
throwout = {}

for j in judg:
    id = int(j['submission_id'])
    verdict = j['judgement_type_id']
    if verdict == 'AC':
        sub_good[id] = True
        throwout[id] = False
    elif verdict == 'CE':
        throwout[id] = True
        sub_good[id] = False
    else:
        sub_good[id] = False
        throwout[id] = False

mp = 1000000000
xp = 0

for s in subs:
    tid = 0
    if "-" in list(s['team_id']):
        tid = int(s['team_id'].split("-")[1])
    else:
        tid = int(s['team_id'])
    pid = problems.index(s['problem_id'])
    mp = min(pid, mp)
    xp = max(pid, xp)

teamsubs = []

probs = xp - mp + 1

team_status = {}
team_pens = {}
solved = {}

for team in teams:
    team_status[team] = [0] * probs
    team_pens[team] = [0] * probs
    solved[team] = [False] * probs

freeze = 120

print(teams)

for s in subs:
    tid = 0
    if "-" in list(s['team_id']):
        tid = int(s['team_id'].split("-")[1])
    else:
        tid = int(s['team_id'])
    name = t["name"]
    pid = problems.index(s['problem_id'])
    sid = int(s['id'])
    time = s['contest_time'].split(":")
    hour = int(time[0])
    min = int(time[1])
    sec = float(time[2])
    if hour < 0:
        continue
    time = hour * 60 + min

    if sid not in sub_good or (sid in throwout and throwout[sid]):
        pass
    else:
        status = sub_good[sid]

        if tid in teams:
            #if "".join(list(teams[tid])[:5]) == "\"prin":
            #    print(time, status)
            teamsubs.append([time, tid, pid, status])

teamsubs = sorted(teamsubs)
for sub in teamsubs:
    time = sub[0]
    name = sub[1]
    pid = sub[2]
    status = sub[3]

    if solved[name][pid]:
        continue

    code = team_status[name][pid]
    if status:
        if time < freeze:
            code = 1
        else:
            code = 3
        if not solved[name][pid]:
            team_pens[name][pid] += time
        else:
            team_pens[name][pid] += 10
        solved[name][pid] = True
    else:
        if not solved[name][pid]:
            if time < freeze:
                code = 2
            else:
                code = 4
        team_pens[name][pid] += 10

    team_status[name][pid] = code

fout = open("resolver_output.txt", "w")

team_list = []
for team in sorted(team_status.keys()):
    team_list.append(['0', '0'] + [str(i) for i in team_status[team]] + [str(i) for i in team_pens[team]] + [teams[team]])

team_list.sort(key=lambda x: x[-1])

for team in team_list:
    fout.write(",".join(team))
    fout.write('\n')
