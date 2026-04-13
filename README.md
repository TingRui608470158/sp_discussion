# Cross-Domain Collaboration（跨領域媒合平台）

第一階段實作 **痛點公佈欄**：產業領域（Category）、專家／工程師身分（UserProfile）、痛點貼文（PainPoint），並提供首頁、依領域篩選的痛點列表、Markdown 渲染的詳情頁，以及僅 **Expert** 可使用的發布表單。

## 環境需求

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)（建議）

## 安裝與資料庫

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py seed_categories
```

`seed_categories` 會建立五個預設領域：醫療生技、法律服務、傳統製造、零售電商、創意內容。

## 建立帳號與身分

本階段未內建註冊頁，請以管理後台或指令建立使用者：

```bash
uv run python manage.py createsuperuser
```

登入 [管理後台](http://127.0.0.1:8000/admin/)，在 **使用者** 中編輯帳號時可一併設定 **使用者檔案** 的 `role`：

- **Expert**：可發布痛點（`/pain-points/create/`）。
- **Engineer**：可瀏覽列表與詳情；若開啟發布頁會收到 403。

每位使用者在建立時會自動建立一筆 `UserProfile`（預設為 Engineer）。

## 本機執行

```bash
uv run python manage.py runserver
```

## 主要網址

| 路徑 | 說明 |
|------|------|
| `/` | 首頁：產業領域卡片與 CTA |
| `/pain-points/` | 痛點列表（`?category=<slug>` 篩選領域） |
| `/pain-points/<id>/` | 痛點詳情（Markdown 渲染） |
| `/pain-points/create/` | 發布痛點（需登入且為 Expert） |
| `/accounts/login/` | 登入 |
| `/admin/` | Django 管理後台 |

## 技術摘要

- **框架**：Django 6
- **Markdown**：`markdown` + `bleach` 消毒後輸出 HTML
- **樣式**：Tailwind CSS（CDN）
