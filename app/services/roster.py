from sqlalchemy import create_engine, text
import time

# 30 秒快取，避免每次切換面板都打遠端 RDS
_cache = {"ts": 0.0, "names": set()}

def get_prechecked_yes(mysql_url: str):
    """
    回傳 badminton_reply 中 reply_text='要' 的 user_name（不限日期，去重）。
    具 30 秒快取。
    """
    if not mysql_url:
        return set()

    now = time.time()
    if now - _cache["ts"] < 30:
        return _cache["names"]

    engine = create_engine(mysql_url, pool_pre_ping=True)
    sql = text("""
        SELECT DISTINCT br.user_name
        FROM badminton_reply br
        WHERE br.reply_text = :yes
    """)
    with engine.begin() as conn:
        rows = conn.execute(sql, {"yes": "要"}).all()

    names = {row[0] for row in rows}
    _cache["ts"] = now
    _cache["names"] = names
    return names

def _canon(s: str) -> str:
    """大小寫不敏感 + 去除所有空白字元"""
    if s is None:
        return ""
    return "".join(str(s).split()).casefold()

def roster_with_flags(default_players, mysql_url, tz_name=None):
    """
    回傳 (roster_list, checked_set)
    - roster_list：固定名單（來自 DEFAULT_PLAYERS）
    - checked_set：DB 有回『要』者（不限日期），與名單比對（大小寫/空白容錯）
    """
    roster = list(default_players)
    yes_set = get_prechecked_yes(mysql_url)
    yes_canon = {_canon(n) for n in yes_set}
    checked = {n for n in roster if _canon(n) in yes_canon}
    return roster, checked

# 相容舊程式：不再僅限今天；直接回「不限日期」的人名（已排序）
def get_today_attendees(mysql_url: str, tz_name: str = None):
    return sorted(get_prechecked_yes(mysql_url))
