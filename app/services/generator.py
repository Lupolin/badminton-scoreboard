from collections import defaultdict
import os, time, random

def chooseM(n):  # 保留你的規則
    return {4:12,5:20,6:18,7:21,8:20}.get(n, 0)

def _pid(pair): 
    return tuple(sorted(pair))

def generate_schedule(names, seed=None):
    """
    產生賽程（隨機化版）
    - 每次呼叫都不同；若想重現結果，可傳 seed。
    - 仍優先讓「較少上場」且「休息較久」的人先上。
    """
    n = len(names)
    M = chooseM(n)
    if M == 0 or n < 4:
        return []

    # 建立本次專用 RNG（不干擾全域 random）
    if seed is None:
        seed = (time.time_ns() ^ os.getpid() ^ int.from_bytes(os.urandom(8), "big"))
    rng = random.Random(seed)

    # 先把名單打亂，避免固定起手
    pool = names[:]
    rng.shuffle(pool)

    plays = {x: 0 for x in pool}         # 每人已上場
    rest  = {x: 0 for x in pool}         # 連續休息場數
    partner_count = defaultdict(int)     # 搭檔次數
    matches = []
    prev_key = None

    def matchup_key(p):  # 不考慮左右，只看兩隊的搭檔
        return tuple(sorted((_pid(p[0]), _pid(p[1]))))

    for _ in range(M):
        # 對平手情況加一點隨機抖動（只當作排序最後一鍵）
        jitter = {x: rng.random() for x in pool}
        order = sorted(pool, key=lambda x: (plays[x], -rest[x], jitter[x]))

        # 取前四位上場（已包含隨機 tie-break）
        a, b, c, d = order[:4]

        # 三種配對的評分，越小越好（先看最壞搭檔次數，再看總搭檔次數）
        options = [([a,b],[c,d]), ([a,c],[b,d]), ([a,d],[b,c])]
        def score(p):
            p1, p2 = p
            s1 = partner_count[_pid(p1)]
            s2 = partner_count[_pid(p2)]
            return (max(s1, s2), s1 + s2)

        # 找到最小分的選項，若有多個，隨機挑一個
        min_score = min(score(p) for p in options)
        tied = [p for p in options if score(p) == min_score]
        pr = rng.choice(tied)

        # 避免與上一場完整對戰重複；若撞到就從其它選項隨機挑
        cur_key = matchup_key(pr)
        if prev_key is not None and cur_key == prev_key:
            alts = [p for p in options if matchup_key(p) != prev_key]
            if alts:
                pr = rng.choice(alts)
                cur_key = matchup_key(pr)

        # 呈現上 50% 機率左右交換（純外觀）
        if rng.random() < 0.5:
            pr = (pr[1], pr[0])

        matches.append({"left": pr[0], "right": pr[1]})
        prev_key = cur_key

        # 更新統計
        playing = set(pr[0] + pr[1])
        for p in pool:
            if p in playing:
                plays[p] += 1
                rest[p] = 0
            else:
                rest[p] += 1
        partner_count[_pid(pr[0])] += 1
        partner_count[_pid(pr[1])] += 1

    return matches
