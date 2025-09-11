from flask import Blueprint, render_template, request, session, current_app, make_response, url_for
from ..services.roster import roster_with_flags
from ..services.generator import generate_schedule

web_bp = Blueprint("web", __name__)

def _ctx():
    return dict(
        matches=session.get("matches", []),
        idx=session.get("idx", 0),
        scores=session.get("scores", {}),
    )

# 進站：預設名單頁
@web_bp.get("/")
def index():
    roster, checked = roster_with_flags(
        current_app.config["DEFAULT_PLAYERS"],
        current_app.config.get("MYSQL_URL"),
        current_app.config.get("APP_TIMEZONE"),
    )
    return render_template("index.html", mode="setup", roster=roster, checked=checked, **_ctx())

# 清單頁
@web_bp.get("/list")
def list_page():
    roster, checked = roster_with_flags(
        current_app.config["DEFAULT_PLAYERS"],
        current_app.config.get("MYSQL_URL"),
        current_app.config.get("APP_TIMEZONE"),
    )
    return render_template("index.html", mode="list", roster=roster, checked=checked, **_ctx())

# 計分頁
@web_bp.get("/score")
def score_page():
    roster, checked = roster_with_flags(
        current_app.config["DEFAULT_PLAYERS"],
        current_app.config.get("MYSQL_URL"),
        current_app.config.get("APP_TIMEZONE"),
    )
    return render_template("index.html", mode="score", roster=roster, checked=checked, **_ctx())

# 產生賽程：存到 session，並請 HTMX 直接導向 /list（清單）
@web_bp.post("/generate")
def generate():
    from flask import make_response, url_for
    selected = request.form.getlist("names")
    if not selected:
        _, checked = roster_with_flags(
            current_app.config["DEFAULT_PLAYERS"],
            current_app.config.get("MYSQL_URL"),
            current_app.config.get("APP_TIMEZONE"),
        )
        selected = list(checked)

    # 這行就是「分隊/產生賽程」的地方（見下方第 2 點）
    sched = generate_schedule(selected)

    session["matches"] = sched
    session["idx"] = 0
    session["scores"] = {}

    # ✅ 讓 HTMX 直接跳到 /list（清單）
    resp = make_response("", 204)
    resp.headers["HX-Redirect"] = url_for("web.list_page")
    return resp


# 切換場次（只更新舞台）
@web_bp.post("/nav")
def nav():
    action = request.form.get("action")
    matches = session.get("matches", [])
    idx = session.get("idx", 0)
    if matches:
        if action == "next": idx = (idx + 1) % len(matches)
        elif action == "prev": idx = (idx - 1 + len(matches)) % len(matches)
    session["idx"] = idx
    return render_template("_stage.html", matches=matches, idx=idx, scores=session.get("scores", {}))

# 記分（只更新舞台）
@web_bp.post("/score")
def score():
    which = request.form.get("which")
    idx = session.get("idx", 0)
    scores = session.get("scores", {})
    cur = scores.get(str(idx), {"l":0, "r":0})
    if   which == "left_plus":  cur["l"] = min(30, cur["l"] + 1)
    elif which == "left_minus": cur["l"] = max(0, cur["l"] - 1)
    elif which == "right_plus": cur["r"] = min(30, cur["r"] + 1)
    elif which == "right_minus":cur["r"] = max(0, cur["r"] - 1)
    elif which == "reset":      cur = {"l":0, "r":0}
    scores[str(idx)] = cur
    session["scores"] = scores
    return render_template("_stage.html",
                           matches=session.get("matches", []),
                           idx=session.get("idx", 0),
                           scores=scores)
@web_bp.post("/swap")
def swap():
    # 取得目前場次
    idx = session.get("idx", 0)
    matches = session.get("matches", [])
    scores  = session.get("scores", {})

    if matches and 0 <= idx < len(matches):
        # 1) 交換左右球員
        m = matches[idx]
        m["left"], m["right"] = m["right"], m["left"]
        matches[idx] = m
        session["matches"] = matches

        # 2) 交換左右分數
        sc = scores.get(str(idx), {"l": 0, "r": 0})
        scores[str(idx)] = {"l": sc.get("r", 0), "r": sc.get("l", 0)}
        session["scores"] = scores

    # 回傳最新舞台
    return render_template(
        "_stage.html",
        matches=matches,
        idx=idx,
        scores=scores
    )
