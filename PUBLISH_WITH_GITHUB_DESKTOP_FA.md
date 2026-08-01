# انتشار مخزن با GitHub Desktop

پوشه آماده انتشار:

`turkiye-energy-intelligence-platform`

## ۱. افزودن مخزن محلی

در GitHub Desktop:

1. `File` → `Add Local Repository`
2. پوشه پروژه را انتخاب کنید.
3. اگر برنامه گفت این پوشه هنوز Git repository نیست، گزینه ساخت repository را بزنید.

## ۲. انتشار

1. دکمه `Publish repository` را بزنید.
2. نام را دقیقاً بگذارید: `turkiye-energy-intelligence-platform`
3. تیک `Keep this code private` را بردارید.
4. Owner را `FaramarzKowsari` انتخاب کنید.
5. روی `Publish Repository` بزنید.

## ۳. About

در صفحه اصلی مخزن، کنار About روی چرخ‌دنده بزنید و مقادیر `ABOUT.md` را کپی کنید.

## ۴. GitHub Pages

در `Settings` → `Pages`، منبع را `GitHub Actions` انتخاب کنید. workflow آماده داخل مخزن قرار دارد.

## ۵. Zenodo

پس از اتصال Zenodo به GitHub، مخزن را در Zenodo فعال کنید و GitHub Release با تگ `v1.0.0` بسازید. پس از صدور DOI، دستور زیر را اجرا و تغییرات را push کنید:

```bash
python scripts/apply_zenodo_doi.py 10.5281/zenodo.YOUR_ID
```

## ۶. Google Search Console

فایل HTML تأیید گوگل را دانلود کنید و این دستور را اجرا کنید:

```bash
python scripts/install_search_console_verification.py "C:\Path\google123456.html"
```

سپس commit و push کنید و در Search Console، `sitemap.xml` را ثبت کنید.
