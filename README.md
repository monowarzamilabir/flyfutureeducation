# Fly Future Education — Website

A production-quality Django website for Fly Future Education, a Dhaka-based study-abroad
consultancy (visa processing, university admissions, scholarships, and test prep).

## Tech Stack

- **Backend:** Django 5.1, Python 3.12+
- **Database:** PostgreSQL (via `psycopg2-binary`), configured through `.env`
- **Frontend:** Django templates + Tailwind CSS (compiled with the standalone Tailwind CLI —
  no Node.js required) + a small amount of vanilla JS for interactivity
- **Rich text:** django-ckeditor
- **Images:** Pillow
- **Email:** Django's email backend (console in dev, SMTP in prod)
- **Static files:** WhiteNoise (with `django-storages`/S3 ready to enable for production)

## 1. Prerequisites

- Python 3.12+
- PostgreSQL 14+ running locally or accessible remotely

## 2. Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# then edit .env with your real SECRET_KEY, database credentials, email settings, etc.
```

### PostgreSQL setup

Create a database and user matching your `.env` (defaults shown below):

```sql
CREATE DATABASE flyfuture;
CREATE USER flyfuture WITH PASSWORD 'flyfuture';
ALTER ROLE flyfuture SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE flyfuture TO flyfuture;
```

> **Note:** `settings.py` defaults `DB_ENGINE` to `django.db.backends.postgresql`. For quick
> local experimentation without installing Postgres, you *can* set
> `DB_ENGINE=django.db.backends.sqlite3` in your `.env` — but PostgreSQL is the supported,
> production configuration and is what `.env.example` documents.

### Migrate & create an admin user

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Load sample data (optional but recommended)

Populates services, destinations, universities, scholarships, test-prep courses, team
members, blog posts, testimonials, FAQs, a sample photo/video gallery, and Privacy/Terms
pages — **all clearly sample content**, meant to be replaced via the admin.

```bash
python manage.py seed_sample_data
```

### Run the dev server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` for the admin
(log in with the superuser you created above).

## 3. Frontend / Tailwind CSS

Styles are compiled ahead of time with the official **standalone Tailwind CLI** binary
(`tools/tailwindcss.exe` on Windows — see [Tailwind's releases page](https://github.com/tailwindlabs/tailwindcss/releases)
for macOS/Linux binaries) so the project has **no Node.js/npm dependency**. Source styles
live in `static_src/input.css`; the compiled, production-ready file is
`static/css/tailwind.css`, which is committed so the site works out of the box.

If you edit any Tailwind classes in templates or `static_src/input.css`, rebuild with:

```bash
./tools/tailwindcss.exe -i ./static_src/input.css -o ./static/css/tailwind.css --minify
```

(On macOS/Linux, download the matching `tailwindcss-<platform>` binary from the link above,
place it at `tools/tailwindcss`, `chmod +x` it, and run the same command.)

## 4. Project Structure

```
flyfuture/            Project settings, urls.py, sitemaps.py (env-driven via django-environ)
apps/
  core/                SiteSettings (singleton), Testimonial, FAQ, StaticPage, ProcessStep,
                       Benefit, SiteStat, JobPosting/JobApplication (careers)
  services/            Service (list/detail)
  destinations/        Country, University (list/detail, filter/search)
  scholarships/        Scholarship (list/detail)
  trainings/           TestPrepCourse — IELTS/TOEFL/PTE/Duolingo (list/detail)
  team/                Consultant (list/detail)
  applications/        Application — the "Apply Now" form + admin triage workflow
  blog/                Category, Post (tags via django-taggit)
  gallery/             PhotoAlbum, Photo, VideoItem
  contact/             ContactMessage — the Contact form + admin triage workflow
templates/             base.html, partials/ (navbar, footer, WhatsApp/Messenger bubble,
                       reusable cards, form fields, pagination), and one folder per app
static/                Compiled Tailwind CSS, main.js, brand logo & favicons
static_src/            Tailwind input CSS (source of truth for styles)
tools/                 Standalone Tailwind CLI binary
```

Every content model has `created_at`/`updated_at` timestamps and an auto-generated unique
`slug`. Every public-facing model has `meta_title`/`meta_description` fields for SEO.

## 5. Admin

The Django admin (`/admin/`) is heavily customized for non-technical staff:

- Readable `list_display`, `search_fields`, `list_filter`, and `list_editable` on every model
- Inlines (e.g. Universities under Country, FAQs under FAQCategory, Photos under PhotoAlbum)
- `prepopulated_fields` for slugs
- **Applications** and **Contact Messages** are sortable/filterable by status and date for
  daily staff triage
- `SiteSettings` is a singleton — logo, contact info, social links, office hours, and default
  SEO/Open Graph fields are all editable there, with nothing hardcoded in templates

## 6. SEO

- Per-page `<title>` / meta description on every page, with sensible fallbacks
  (page-specific → `SiteSettings` defaults)
- Open Graph + Twitter Card tags on every page (with per-post cover images on blog articles)
- `sitemap.xml` (via `django.contrib.sitemaps`) and `robots.txt`, both environment-aware
- Canonical URLs on every page
- Custom, on-brand 404 and 500 error pages (the 500 page is fully self-contained with no
  database/template dependency, so it still renders even if the database itself is down)

## 7. Forms & Spam Protection

The **Apply Now**, **Contact**, and **Careers application** forms:

- Validate server-side (Django forms) and client-side (HTML5 `required`/`type` attributes)
- Save to the database and email the admin (`ADMIN_NOTIFICATION_EMAIL` in `.env`); Apply Now
  also sends the applicant a confirmation email
- Include an invisible honeypot field for basic spam protection
- Have a **TODO** slot for Google reCAPTCHA: fill in `RECAPTCHA_PUBLIC_KEY` /
  `RECAPTCHA_PRIVATE_KEY` in `.env` and wire up `django-recaptcha` when you're ready
  (`settings.RECAPTCHA_ENABLED` is already computed from those keys)

## 8. Tests

```bash
python manage.py test
```

Covers model behavior (slug generation, singleton settings) and view/response-code checks
across the public site.

## 9. Deploying to Render (recommended)

This repo includes `render.yaml`, a Render "Blueprint" that provisions the web service and a
managed PostgreSQL database together. Render was chosen because it needs no server
maintenance (no Nginx/SSL/OS patching to manage yourself), has git-push deploys, and a free
automatic SSL certificate for your custom domain.

### Step 1 — Get the code onto GitHub

Render deploys from a git repository. If this project isn't in one yet:

```bash
git init
git add .
git commit -m "Initial commit"
```

Then create a new (private is fine) repository on [github.com](https://github.com/new) and
push this project to it.

### Step 2 — Create the Render Blueprint

1. Sign up at [render.com](https://render.com) (a card is required for paid plans, but no
   charge until you confirm).
2. Click **New +** → **Blueprint**, and connect the GitHub repo you just pushed.
3. Render reads `render.yaml` automatically and shows you the `flyfuture-web` service and
   `flyfuture-db` database it's about to create. Click **Apply**.
4. Two environment variables are marked `sync: false` in `render.yaml` and need to be filled
   in manually in the Render dashboard once the service exists:
   - `EMAIL_HOST_USER` — a Gmail address (or your real SMTP account)
   - `EMAIL_HOST_PASSWORD` — for Gmail, this must be a 16-character
     [App Password](https://myaccount.google.com/apppasswords), not your normal Gmail
     password (Gmail blocks regular passwords for SMTP)
5. Wait for the first deploy to finish (Render shows build/deploy logs live).
6. Once it's live, open a Render shell for the service (**Shell** tab) and run:
   ```bash
   python manage.py createsuperuser
   python manage.py seed_sample_data   # optional, only if you want sample content
   ```

### Step 3 — Point flyfutureeducation.com at Render

1. In the Render dashboard, open `flyfuture-web` → **Settings** → **Custom Domains**.
2. Add both `flyfutureeducation.com` and `www.flyfutureeducation.com`. Render shows you the
   exact DNS records to add.
3. Go to wherever you bought the domain (your registrar's DNS settings) and add those
   records — typically:
   - An **A record** for `@` (the bare domain) pointing at the IP Render gives you
   - A **CNAME record** for `www` pointing at the `.onrender.com` address Render gives you
4. DNS changes can take anywhere from a few minutes to a few hours to propagate. Render
   automatically issues a free SSL certificate once it detects the DNS is pointed correctly —
   no action needed from you.
5. Once both are verified in Render, set `www.flyfutureeducation.com` as the **primary**
   domain so `flyfutureeducation.com` redirects to it (avoids duplicate-content SEO issues).

### A note on uploaded images (media files)

`render.yaml` attaches a small persistent Disk mounted at the app's `media/` folder, so
photos/CVs uploaded through the admin or the Apply Now form **survive redeploys**. If your
media storage needs grow later (many photos/videos), it's easy to switch to S3-compatible
object storage instead — set `USE_S3=True` and fill in the `AWS_*` variables in Render's
environment variables (see `.env.example`); `django-storages` is already wired up for this,
you'd just need to `pip install django-storages` (it's commented out in `requirements.txt`
until you need it) and point it at AWS S3 or Cloudflare R2 (which has a free tier).

### General production checklist

- `DEBUG=False`, a real `SECRET_KEY`, and correct `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` are
  already set by `render.yaml` — double check them in the Render dashboard after first deploy
- `collectstatic` and `migrate` run automatically on every deploy (see `buildCommand`/
  `startCommand` in `render.yaml`)
- Replace the sample data (see note below) with real content before sharing the domain publicly
- Consider filling in `RECAPTCHA_PUBLIC_KEY`/`RECAPTCHA_PRIVATE_KEY` (see §7) once the site is
  getting real public traffic, to cut down spam submissions

### Hosting elsewhere instead

If you'd rather use a different platform (Railway, DigitalOcean App Platform, a VPS with
Docker, PythonAnywhere, etc.), the app itself doesn't need to change — it's already fully
`.env`-driven with `gunicorn` as the WSGI server and WhiteNoise serving static files. You'd
just translate the same environment variables and `buildCommand`/`startCommand` from
`render.yaml` into that platform's format. Ask and I can prepare the equivalent config
(Dockerfile, Railway config, Nginx + systemd for a VPS, etc.).

## Note on Sample Data

Everything created by `seed_sample_data` — consultant profiles, testimonials, blog posts,
gallery photos/video — is placeholder content for demonstration purposes. Replace it with
real content via the admin before launch.
