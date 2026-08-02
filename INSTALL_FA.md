# نصب مرحلهٔ Live EPİAŞ

این بسته سه کار انجام می‌دهد:

1. داشبورد Streamlit را دوحالته می‌کند: Demo و Live EPİAŞ.
2. وابستگی‌های لازم برای اتصال HTTPS را به `requirements.txt` اضافه می‌کند.
3. نمونهٔ امن Secrets و راهنمای اتصال را اضافه می‌کند.

## کپی فایل‌ها

محتویات بسته را روی ریشهٔ مخزن محلی زیر کپی کنید:

```text
turkiye-energy-intelligence-platform/
```

هنگام پرسش ویندوز، برای `app/streamlit_app.py` و `requirements.txt` گزینهٔ Replace را بزنید.

## Commit

در GitHub Desktop:

```text
Summary: feat: add secure live EPIAS mode
Commit to main
Push origin
```

منتظر سبزشدن CI بمانید. Streamlit نیز پس از Push برنامه را بازسازی می‌کند.

## بعد از سبزشدن

در EPİAŞ حساب رایگان بسازید و ایمیل فعال‌سازی را تأیید کنید. سپس در Streamlit:

```text
Manage app → Settings → Secrets
```

محتوای `.streamlit/secrets.toml.example` را وارد کنید و فقط username/password را جایگزین کنید. فایل واقعی Secrets را هرگز داخل GitHub نگذارید.
