import json

inperson = [
    "brain of a tourist, hands of a cone",
    "512 Pounds",
    "how to get more points???",
    "Maomao Fanclub",
    "OF!Z",
    "MaLin",
    "ice evaders",
    "BISV",
    "Sigma Coders",
    "Fire Nation",
    "DVCC 2028",
    "The Infinite Loops",
    "future mcdonalds workers",
    "USACO Silver Demons",
    "3 idiots",
    "temporary team name",
    "chicken jockey",
    "Flint and Steel",
    "Class E",
    "Hacking the Beanstalk",
    "nullptr"
]

file = open("submissions.json", "r").read()
subs = json.loads(file)

file2 = open("judgements.json", "r").read()
judg = json.loads(file2)

file3 = open("teams.json", "r").read()
team = json.loads(file3)

teams = {}

for t in team:
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
    tid = int(s['team_id'])
    pid = int(s['problem_id'])
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

for s in subs:
    tid = int(s['team_id'])
    pid = int(s['problem_id']) - mp
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
