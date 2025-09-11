from app import create_app
app = create_app()

if __name__ == "__main__":
    # ⭐ 從.env讀取port（沒有就預設5000）
    port = 5000
    app.run(host="0.0.0.0", port=port)