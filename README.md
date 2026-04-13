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

## 註冊與登入

本站使用 [django-allauth](https://docs.allauth.org/)，提供：

- **帳號密碼註冊／登入**：`/accounts/signup/`、`/accounts/login/`。
- **Google OAuth**（可選）：設定憑證後，登入與註冊頁會顯示「使用 Google」按鈕。

### Google OAuth 設定

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)，建立 OAuth 2.0「網頁應用程式」憑證。
2. 在「已授權的重新導向 URI」加入與實際存取網址一致的 callback，例如本機：  
   `http://127.0.0.1:8000/accounts/google/login/callback/`  
   若使用其他主機或埠（例如 `http://10.8.60.54:8000/...`），請另列一筆。
3. 啟動前設定環境變數（勿將 Secret 寫入版本庫）：

   ```bash
   export GOOGLE_CLIENT_ID="你的 Client ID"
   export GOOGLE_CLIENT_SECRET="你的 Client Secret"
   ```

   專案會在兩者皆存在時，將憑證注入 `SOCIALACCOUNT_PROVIDERS['google']['APP']`，登入／註冊頁即可顯示 Google 按鈕。

**替代方式**：未設定環境變數時，可在 Django Admin 的 **Social applications** 新增 Google，填入 Client ID／Secret，並勾選對應的 **Site**（`django.contrib.sites`）。

### `sites` 框架（django.contrib.sites）

Allauth 依賴 **Site**（預設 `SITE_ID = 1`）。若寄信或產生連結時網域不正確，請至 Admin → **網站** 將網域與顯示名稱改成實際對外網址。

## 建立帳號與身分（Expert）

可自行註冊，或以管理後台／指令建立使用者：

```bash
uv run python manage.py createsuperuser
```

登入 [管理後台](http://127.0.0.1:8000/admin/)，在 **使用者** 中編輯帳號時可一併設定 **使用者檔案** 的 `role`：

- **Expert**：可發布痛點（`/pain-points/create/`）。
- **Engineer**：可瀏覽列表與詳情；若開啟發布頁會收到 403。

每位使用者在建立時會自動建立一筆 `UserProfile`（預設為 Engineer）。**自行註冊或 Google 登入者同樣為 Engineer**，若需 Expert，仍由管理員於後台調整。

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
| `/accounts/signup/` | 註冊 |
| `/accounts/google/login/` | Google OAuth 登入流程（由 allauth 提供） |
| `/admin/` | Django 管理後台 |

## 技術摘要

- **框架**：Django 6
- **帳號**：django-allauth（Google OAuth、帳密註冊）
- **Markdown**：`markdown` + `bleach` 消毒後輸出 HTML
- **樣式**：Tailwind CSS（CDN）
