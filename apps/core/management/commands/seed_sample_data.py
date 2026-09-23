"""Seeds the database with realistic sample content so the site looks populated
out of the box. Safe to re-run: uses get_or_create throughout.

NOTE: Everything created here — consultants, testimonials, blog posts, gallery
photos, etc. — is SAMPLE DATA for demonstration purposes, not real content.
Replace it via the Django admin before going live.
"""

from datetime import timedelta
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from apps.blog.models import Category, Post
from apps.core.models import (
    FAQ,
    Benefit,
    FAQCategory,
    ProcessStep,
    SiteSettings,
    SiteStat,
    StaticPage,
    Testimonial,
)
from apps.destinations.models import Country, University
from apps.gallery.models import PhotoAlbum, Photo, VideoItem
from apps.scholarships.models import Scholarship
from apps.services.models import Service
from apps.team.models import Consultant
from apps.trainings.models import TestPrepCourse


def _poster_file(filename):
    """Loads one of the real Fly Future Education Facebook campaign posters
    (extracted from the client-provided posts.pdf) as a Django file object."""
    import os

    path = os.path.join(os.path.dirname(__file__), "seed_assets", "posters", filename)
    with open(path, "rb") as f:
        return ContentFile(f.read(), name=filename)


def _placeholder_image(text, size=(800, 500), bg=(15, 95, 166), fg=(255, 255, 255)):
    """Generates a simple branded placeholder graphic (no external/stock imagery)."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", 42)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, font=font, fill=fg)
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return ContentFile(buffer.getvalue(), name=f"{slugify(text)}.jpg")


class Command(BaseCommand):
    help = "Seed the database with sample content (services, destinations, team, blog, etc.)"

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample data...")
        self._site_settings()
        self._services()
        countries = self._destinations()
        self._universities(countries)
        self._scholarships(countries)
        self._trainings()
        consultants = self._team()
        self._process_steps()
        self._benefits()
        self._stats()
        self._testimonials()
        self._faqs()
        self._blog(consultants)
        self._gallery()
        self._static_pages()
        self.stdout.write(self.style.SUCCESS("Sample data seeded successfully."))

    # ------------------------------------------------------------------
    def _site_settings(self):
        settings_obj = SiteSettings.load()
        if not settings_obj.about_short:
            settings_obj.about_short = (
                "Fly Future Education is a Dhaka-based study-abroad consultancy helping "
                "students with admissions, visas, scholarships, and test preparation."
            )
        if not settings_obj.logo:
            settings_obj.logo.save("logo.png", _brand_logo_file(), save=False)
        if not settings_obj.favicon:
            settings_obj.favicon.save("favicon.png", _brand_logo_file(), save=False)
        settings_obj.save()

    # ------------------------------------------------------------------
    def _services(self):
        services = [
            ("Student Visa Support", "document", "End-to-end student visa filing, documentation, and interview preparation."),
            ("Visit Visa Support", "plane", "Guidance for short-term visit visas for family or exploratory trips abroad."),
            ("Spouse Visa Support", "shield", "Dependent and spouse visa applications for students already studying abroad."),
            ("Bank Statement & Financial Support", "bank", "Proof-of-funds guidance and financial documentation for embassy requirements."),
            ("Application & Admission Support", "graduation", "University shortlisting and complete application filing on your behalf."),
            ("Visa Processing Support", "document", "Full visa processing management from submission to decision."),
            ("Accommodation Support", "home", "Help finding safe, affordable student housing at your destination."),
            ("Air-Ticket & Immigration Support", "plane", "Flight booking guidance and pre-departure immigration briefing."),
        ]
        for i, (title, icon, desc) in enumerate(services, start=1):
            Service.objects.get_or_create(
                title=title,
                defaults=dict(
                    short_description=desc,
                    body=f"<p>{desc}</p><p>Our counsellors handle this process end-to-end so you can focus on preparing for your new chapter abroad.</p>",
                    icon=icon,
                    is_featured=i <= 4,
                    order=i,
                ),
            )

    # ------------------------------------------------------------------
    def _destinations(self):
        data = [
            dict(
                name="Denmark",
                poster="denmark.jpg",
                intake_seasons="February, September",
                tuition_range="DKK 45,000 - 120,000 / year",
                cost_of_living="DKK 6,000 - 9,000 / month",
                why_study_here="<ul><li>No admission interview required</li><li>Study gap accepted</li><li>Apply with your spouse and children</li><li>Part-time work opportunities</li></ul>",
                visa_requirements="<p>Applicants generally need an unconditional offer letter, proof of funds, and a valid passport. No mandatory bank statement or in-person interview for most cases.</p>",
                work_rights="<p>Students can work part-time during their studies and explore job opportunities after graduation under Denmark's post-study work provisions.</p>",
            ),
            dict(
                name="Sweden",
                poster="sweden.jpg",
                intake_seasons="September (Spring intake applications close 17 August)",
                tuition_range="SEK 80,000 - 190,000 / year",
                cost_of_living="SEK 8,000 - 11,000 / month",
                why_study_here="<ul><li>World-renowned universities and research culture</li><li>Work while you study</li><li>Apply with spouse and children</li><li>Free education for your children</li></ul>",
                visa_requirements="<p>A residence permit for studies requires an admission letter, proof of funds, and comprehensive insurance where applicable.</p>",
                work_rights="<p>Sweden offers strong pathways to long-term residency and permits part-time work throughout your studies.</p>",
            ),
            dict(
                name="Malaysia",
                poster="malaysia.jpg",
                intake_seasons="February, September",
                tuition_range="MYR 20,000 - 45,000 / year",
                cost_of_living="MYR 1,500 - 2,500 / month",
                why_study_here="<ul><li>No IELTS required for many programs</li><li>Student visa within about 1 month</li><li>Complete a bachelor's degree in 3 years</li><li>Transfer pathways to 300+ universities in the UK, Australia, and Canada</li></ul>",
                visa_requirements="<p>Malaysia offers a fast, straightforward student visa process with study-gap and low-CGPA applicants generally accepted.</p>",
                work_rights="<p>Limited part-time work is available for eligible students during semester breaks.</p>",
            ),
            dict(
                name="Australia",
                poster="australia.jpg",
                intake_seasons="February, July, October",
                tuition_range="AUD 22,000 - 45,000 / year",
                cost_of_living="AUD 1,800 - 2,500 / month",
                why_study_here="<ul><li>World-class, globally ranked universities</li><li>Apply with your spouse</li><li>Excellent post-study career opportunities</li><li>Minimum CGPA of 70% generally accepted</li></ul>",
                visa_requirements="<p>A Genuine Student requirement, proof of funds, and English proficiency (IELTS 6.5 or PTE equivalent) are typically required.</p>",
                work_rights="<p>Students can work part-time during term and full-time during scheduled breaks, with strong post-study work visa options.</p>",
            ),
            dict(
                name="Hungary",
                poster="hungary.jpg",
                intake_seasons="September",
                tuition_range="EUR 2,500 - 6,000 / year",
                cost_of_living="EUR 400 - 600 / month",
                why_study_here="<ul><li>Apply without IELTS for many programs</li><li>Internationally recognised degrees</li><li>Affordable tuition fees</li><li>Authentic European lifestyle experience</li></ul>",
                visa_requirements="<p>We assist with subject selection, admission applications, financial guidance, and embassy documentation for a smooth visa process.</p>",
                work_rights="<p>Part-time work opportunities are available to eligible international students.</p>",
            ),
            dict(
                name="Cyprus",
                poster="cyprus.jpg",
                intake_seasons="September, January",
                tuition_range="EUR 5,500 - 7,000 / year",
                cost_of_living="EUR 450 - 650 / month",
                why_study_here="<ul><li>Offer letters in as little as 72 hours</li><li>Study gap accepted, no interview required</li><li>Previous visa refusals can still apply</li><li>High visa success rate</li></ul>",
                visa_requirements="<p>IELTS requirements are flexible (4.5-5.5 depending on program), making Cyprus accessible for a wide range of applicants.</p>",
                work_rights="<p>Limited part-time work is permitted for international students under relevant visa conditions.</p>",
            ),
            dict(
                name="Malta",
                poster="malta.jpg",
                intake_seasons="October, February",
                tuition_range="EUR 6,000 - 12,000 / year",
                cost_of_living="EUR 500 - 700 / month",
                why_study_here="<ul><li>One of the best visa approval ratios currently available</li><li>Pay tuition after visa approval</li><li>IELTS optional for many programs</li><li>No hidden charges</li></ul>",
                visa_requirements="<p>Full document and bank support is provided to simplify Malta's student visa process.</p>",
                work_rights="<p>Eligible students may take on limited part-time work during their studies.</p>",
            ),
            dict(
                name="Italy",
                poster="italy.jpg",
                intake_seasons="2026/2027 intake ongoing",
                tuition_range="EUR 1,000 - 4,000 / year (public universities)",
                cost_of_living="EUR 700 - 1,000 / month",
                why_study_here="<ul><li>Bachelor's, Master's, and PhD programs available</li><li>Globally respected, historic universities</li><li>Rich cultural and academic environment</li></ul>",
                visa_requirements="<p>Applicants apply directly to top Italian universities; we manage the process end-to-end from admission to visa.</p>",
                work_rights="<p>International students may work part-time (up to 20 hours/week) during their studies.</p>",
            ),
            dict(
                name="USA",
                poster="usa-canada.jpg",
                intake_seasons="Fall (August/September), Spring (January)",
                tuition_range="USD 15,000 - 45,000 / year",
                cost_of_living="USD 1,000 - 1,800 / month",
                why_study_here="<ul><li>Top-ranked universities worldwide</li><li>Strong scholarship opportunities</li><li>High-paying career opportunities after graduation</li></ul>",
                visa_requirements="<p>The F-1 student visa requires an I-20 from your university, proof of funds, and a successful visa interview at the U.S. embassy.</p>",
                work_rights="<p>On-campus work is available during studies, with Optional Practical Training (OPT) available after graduation.</p>",
            ),
            dict(
                name="Canada",
                poster="usa-canada.jpg",
                intake_seasons="Fall (September), Winter (January), Summer (May)",
                tuition_range="CAD 15,000 - 35,000 / year",
                cost_of_living="CAD 1,200 - 2,000 / month",
                why_study_here="<ul><li>Good visa approval rate</li><li>Work permit after graduation</li><li>Clear pathway to permanent residency</li></ul>",
                visa_requirements="<p>A Canadian study permit requires a Letter of Acceptance, proof of funds, and (for many applicants) a clean immigration history.</p>",
                work_rights="<p>Students can work part-time during studies and apply for a Post-Graduation Work Permit (PGWP) after completing their program.</p>",
            ),
        ]
        countries = {}
        for i, item in enumerate(data, start=1):
            country, _ = Country.objects.get_or_create(
                name=item["name"],
                defaults=dict(
                    overview=f"<p>{item['name']} is a popular study destination for Bangladeshi students, offering quality education and a welcoming environment for international students.</p>",
                    why_study_here=item["why_study_here"],
                    visa_requirements=item["visa_requirements"],
                    work_rights=item["work_rights"],
                    tuition_range=item["tuition_range"],
                    cost_of_living=item["cost_of_living"],
                    intake_seasons=item["intake_seasons"],
                    is_featured=True,
                    order=i,
                ),
            )
            # Attach the real Fly Future Education campaign poster as the hero
            # image (idempotent: fills it in even on a re-run of an older seed).
            if item.get("poster") and not country.hero_image:
                country.hero_image.save(item["poster"], _poster_file(item["poster"]), save=True)
            countries[item["name"]] = country
        return countries

    # ------------------------------------------------------------------
    def _universities(self, countries):
        italy_universities = [
            "University of Bologna",
            "Politecnico di Milano",
            "Sapienza University of Rome",
            "University of Padua",
            "University of Florence",
            "University of Naples Federico II",
        ]
        italy = countries.get("Italy")
        if italy:
            for i, name in enumerate(italy_universities, start=1):
                University.objects.get_or_create(
                    country=italy,
                    name=name,
                    defaults=dict(programs_offered="Bachelor's, Master's, PhD", order=i),
                )

    # ------------------------------------------------------------------
    def _scholarships(self, countries):
        items = [
            ("Nordic Excellence Scholarship", "Denmark", "Up to 50% tuition waiver"),
            ("Malaysia Merit Award", "Malaysia", "Up to 30% tuition reduction"),
            ("Australia Global Talent Scholarship", "Australia", "AUD 5,000 - 10,000 one-time award"),
        ]
        for i, (title, country_name, coverage) in enumerate(items, start=1):
            Scholarship.objects.get_or_create(
                title=title,
                defaults=dict(
                    country=countries.get(country_name),
                    amount_coverage=coverage,
                    description=f"<p>{title} supports high-achieving students pursuing studies in {country_name}.</p>",
                    eligibility="<ul><li>Minimum CGPA as required by the partner university</li><li>Valid English proficiency test score</li><li>Complete application submitted before the deadline</li></ul>",
                    deadline=timezone.now().date() + timedelta(days=60 + i * 15),
                    is_featured=True,
                    order=i,
                ),
            )

    # ------------------------------------------------------------------
    def _trainings(self):
        items = [
            ("IELTS Preparation", "6 weeks, 3 classes/week", "BDT 8,000", "Comprehensive preparation covering all four IELTS modules with mock tests."),
            ("PTE Academic Preparation", "4 weeks, 3 classes/week", "BDT 9,000", "Focused coaching on PTE's computer-based format with practice sessions."),
            ("TOEFL iBT Preparation", "5 weeks, 3 classes/week", "BDT 8,500", "Structured TOEFL coaching for reading, listening, speaking, and writing."),
            ("Duolingo English Test Preparation", "3 weeks, 2 classes/week", "BDT 5,000", "Fast-track preparation for the Duolingo English Test, ideal for quick intakes."),
        ]
        for i, (title, duration, fee, desc) in enumerate(items, start=1):
            TestPrepCourse.objects.get_or_create(
                title=title,
                defaults=dict(
                    short_description=desc,
                    description=f"<p>{desc}</p>",
                    duration=duration,
                    fee=fee,
                    schedule_info="<p>New batches start every month. Contact us for the next available schedule.</p>",
                    is_featured=True,
                    order=i,
                ),
            )

    # ------------------------------------------------------------------
    def _team(self):
        consultants_data = [
            ("Farhana Akter", "Senior Study Abroad Counsellor", "counselling"),
            ("Imran Kabir", "Visa Processing Specialist", "visa"),
            ("Tasnia Rahman", "Admissions Officer", "admissions"),
            ("Shafiul Islam", "IELTS & Test Prep Coordinator", "test_prep"),
        ]
        consultants = []
        for i, (name, designation, dept) in enumerate(consultants_data, start=1):
            consultant, _ = Consultant.objects.get_or_create(
                name=name,
                defaults=dict(
                    designation=designation,
                    department=dept,
                    bio=f"<p>{name} is a member of the Fly Future Education team, specializing in {designation.lower()}. (Sample profile.)</p>",
                    order=i,
                ),
            )
            consultants.append(consultant)
        return consultants

    # ------------------------------------------------------------------
    def _process_steps(self):
        steps = [
            (1, "Free Consultation", "Share your academic goals with our counsellors."),
            (2, "University Selection", "We shortlist the best-fit programs for your profile."),
            (3, "Application & Visa", "We manage documentation, applications, and visa filing."),
            (4, "Fly Abroad", "Pre-departure briefing, then off to your new campus."),
        ]
        for number, title, desc in steps:
            ProcessStep.objects.get_or_create(step_number=number, defaults=dict(title=title, description=desc, order=number))

    # ------------------------------------------------------------------
    def _benefits(self):
        benefits = [
            ("Licensed & Authorized", "A fully authorized consultancy you can trust with your future.", "shield"),
            ("High Visa Success Rate", "Honest advice and careful preparation behind every application.", "check-circle"),
            ("Free Profile Assessment", "A no-cost initial evaluation of your study-abroad options.", "document"),
            ("Scholarship Matching", "We actively match students to relevant scholarships and waivers.", "coin"),
            ("End-to-End Support", "From counselling to arrival — one team, one process.", "globe"),
            ("Experienced Counsellors", "Our team has guided thousands of students through their journeys.", "graduation"),
        ]
        for i, (title, desc, icon) in enumerate(benefits, start=1):
            Benefit.objects.get_or_create(title=title, defaults=dict(description=desc, icon=icon, order=i))

    # ------------------------------------------------------------------
    def _stats(self):
        stats = [
            ("Students Guided", 3000, "+"),
            ("Partner Universities", 150, "+"),
            ("Study Destinations", 10, "+"),
            ("Years of Experience", 8, "+"),
        ]
        for i, (label, value, suffix) in enumerate(stats, start=1):
            SiteStat.objects.get_or_create(label=label, defaults=dict(value=value, suffix=suffix, order=i))

    # ------------------------------------------------------------------
    def _testimonials(self):
        testimonials = [
            ("Rakib Hasan", "Now studying in Denmark", "Fly Future Education made my visa process seamless from start to finish.", 5),
            ("Nusrat Jahan", "Now studying in Malaysia", "Honest advice and constant support — they never oversold anything.", 5),
            ("Tanvir Ahmed", "Now studying in Australia", "The team helped me secure a scholarship I didn't even know I was eligible for.", 5),
            ("Farzana Sultana", "Now studying in Hungary", "Professional, transparent, and always available to answer my questions.", 4),
            ("Mahmudul Hasan", "Now studying in Italy", "From document prep to the airport, they were with me every step.", 5),
        ]
        for i, (name, role, message, rating) in enumerate(testimonials, start=1):
            Testimonial.objects.get_or_create(
                name=name,
                defaults=dict(role=role, message=message, rating=rating, is_featured=True, order=i),
            )

    # ------------------------------------------------------------------
    def _faqs(self):
        categories = {
            "Visa": [
                ("Do I need an IELTS score to apply?", "It depends on the destination and program. Several of our partner countries and universities accept applications without IELTS — ask your counsellor which options fit your profile."),
                ("What if I've had a visa refused before?", "A previous refusal doesn't automatically disqualify you. Some destinations, like Cyprus, still accept applicants with prior refusals — we'll review your case individually."),
            ],
            "Application": [
                ("How long does the application process take?", "Timelines vary by country and university, but most applications take 4-12 weeks from document submission to offer letter."),
                ("Can I apply with a study gap?", "Yes, many of our partner universities accept applicants with study gaps. We'll help you present your gap clearly in your application."),
            ],
            "Scholarship": [
                ("Am I eligible for a scholarship?", "Eligibility depends on your academic record, destination, and program. Book a free consultation and we'll assess your eligibility."),
                ("Is the consultation free?", "Yes — your first profile assessment and consultation with Fly Future Education is completely free."),
            ],
        }
        for cat_order, (cat_name, faqs) in enumerate(categories.items(), start=1):
            category, _ = FAQCategory.objects.get_or_create(name=cat_name, defaults=dict(order=cat_order))
            for i, (question, answer) in enumerate(faqs, start=1):
                FAQ.objects.get_or_create(
                    category=category,
                    question=question,
                    defaults=dict(answer=f"<p>{answer}</p>", order=i),
                )

    # ------------------------------------------------------------------
    def _blog(self, consultants):
        User = get_user_model()
        author = User.objects.filter(is_superuser=True).first()
        category, _ = Category.objects.get_or_create(name="Destination Updates")
        news_category, _ = Category.objects.get_or_create(name="News")

        posts = [
            (
                "Study in Denmark: February 2027 Intake Now Open",
                category,
                "denmark.jpg",
                "Denmark offers modern education and strong international career opportunities. Here's what Bangladeshi students need to know about the February 2027 intake.",
                "<p>Denmark continues to be a top choice for students seeking a high-quality, English-medium education in Europe. The February 2027 intake is now open for applications.</p>"
                "<h3>Highlights</h3><ul><li>No admission interview required</li><li>Study gap accepted</li><li>Apply with your spouse and children</li><li>Part-time work opportunities available</li></ul>"
                "<p>Our counsellors provide full support — from admissions and documentation to visa guidance — so you can focus on preparing for the move.</p>",
            ),
            (
                "Why Malaysia Is a Smart Choice Right After SSC",
                category,
                "malaysia.jpg",
                "No IELTS required, visas within a month, and transfer pathways to 300+ universities — here's why Malaysia is booming among Bangladeshi students.",
                "<p>Malaysia has become one of the most accessible study destinations for students starting their higher education journey straight after SSC.</p>"
                "<h3>Why students are choosing Malaysia</h3><ul><li>No IELTS required for many programs</li><li>Student visa within about a month</li><li>Complete a bachelor's degree in just 3 years</li>"
                "<li>Transfer pathways to 300+ universities in the UK, Australia, and Canada</li><li>Affordable tuition with English-medium programs</li></ul>",
            ),
            (
                "Sweden Spring 2027 Intake: Key Dates and Requirements",
                category,
                "sweden.jpg",
                "Sweden's spring 2027 intake application window is open. Here's what you need to prepare before the deadline.",
                "<p>Sweden combines world-class universities with strong research culture and family-friendly study options.</p>"
                "<h3>Why Sweden?</h3><ul><li>Globally respected universities</li><li>Work opportunities alongside your studies</li><li>Apply together with your spouse and children</li>"
                "<li>Free education for your children while you study</li></ul><p>Applications for the spring 2027 intake close in mid-August — start your application early to secure your spot.</p>",
            ),
            (
                "Protecting Students: Why Working With an Authorized Consultancy Matters",
                news_category,
                None,
                "Following a recent industry press conference on student protection, here's why choosing an authorized consultancy matters more than ever.",
                "<p>Studying abroad is a major decision, and unfortunately, misinformation and unauthorized consultancies continue to put students and families at risk.</p>"
                "<p>Fly Future Education fully supports recent industry initiatives focused on protecting students' interests and improving transparency in the higher-education consultancy sector. "
                "If you're planning to study in the UK, Canada, Australia, or elsewhere, always verify that you're working with a trusted, authorized consultancy.</p>",
            ),
        ]
        for i, (title, cat, poster, excerpt, body) in enumerate(posts):
            published_at = timezone.now() - timedelta(days=i * 4)
            post, _ = Post.objects.get_or_create(
                title=title,
                defaults=dict(
                    category=cat,
                    excerpt=excerpt,
                    body=body,
                    author=author,
                    published_at=published_at,
                    is_published=True,
                ),
            )
            if poster and not post.cover_image:
                post.cover_image.save(poster, _poster_file(poster), save=True)

    # ------------------------------------------------------------------
    def _gallery(self):
        album, created = PhotoAlbum.objects.get_or_create(
            title="Student Send-Off Event 2026",
            defaults=dict(description="Sample gallery — replace with real event photos.", order=1),
        )
        if created:
            for i, label in enumerate(["Send-Off 1", "Send-Off 2", "Send-Off 3"], start=1):
                photo = Photo(album=album, caption=f"{label} (sample image)", order=i)
                photo.image.save(f"sample-{i}.jpg", _placeholder_image(label, bg=(20, 166, 182)), save=False)
                photo.save()

        poster_album, poster_created = PhotoAlbum.objects.get_or_create(
            title="Facebook Campaign Posters",
            defaults=dict(description="Our recent study-abroad campaign posters from Facebook.", order=0),
        )
        if poster_created:
            posters = [
                ("denmark.jpg", "Study in Denmark — February 2027 Intake"),
                ("sweden.jpg", "Study in Sweden — Your Future Starts Here"),
                ("malaysia.jpg", "Study in Malaysia After SSC"),
                ("malaysia-2.jpg", "Why Malaysia Is the Right Choice for Bangladeshi Students"),
                ("australia.jpg", "Master's in Australia — Fly With Your Spouse"),
                ("hungary.jpg", "Study in Hungary — No IELTS Required"),
                ("cyprus.jpg", "Study in Cyprus"),
                ("malta.jpg", "Study in Malta"),
                ("italy.jpg", "Your Journey to Italy Starts Here"),
                ("usa-canada.jpg", "Study in USA & Canada"),
            ]
            if not poster_album.cover_image:
                poster_album.cover_image.save("denmark.jpg", _poster_file("denmark.jpg"), save=True)
            for i, (filename, caption) in enumerate(posters, start=1):
                photo = Photo(album=poster_album, caption=caption, order=i)
                photo.image.save(filename, _poster_file(filename), save=False)
                photo.save()

        VideoItem.objects.get_or_create(
            title="Fly Future Education — Sample Video",
            defaults=dict(
                video_id="aqz-KE-bpKQ",
                description="Sample placeholder video — replace with real content in the admin.",
                order=1,
            ),
        )

    # ------------------------------------------------------------------
    def _static_pages(self):
        StaticPage.objects.get_or_create(
            slug="privacy-policy",
            defaults=dict(
                title="Privacy Policy",
                body=(
                    "<p>Fly Future Education (\"we\", \"us\") respects your privacy. This policy explains how we "
                    "collect, use, and protect the personal information you share with us through this website, "
                    "including via our Apply Now and Contact forms.</p>"
                    "<h3>Information We Collect</h3><p>Name, email, phone number, and study-related details you "
                    "voluntarily submit through our forms, along with any documents you upload.</p>"
                    "<h3>How We Use Your Information</h3><p>To respond to your enquiries, process your application, "
                    "and provide study-abroad counselling services. We do not sell your personal information.</p>"
                    "<h3>Data Security</h3><p>We take reasonable technical and organizational measures to protect "
                    "your information from unauthorized access.</p>"
                    "<h3>Contact Us</h3><p>For privacy-related questions, contact us at flufutureeducation@gmail.com.</p>"
                ),
            ),
        )
        StaticPage.objects.get_or_create(
            slug="terms-conditions",
            defaults=dict(
                title="Terms & Conditions",
                body=(
                    "<p>By using this website, you agree to the following terms.</p>"
                    "<h3>Use of Our Services</h3><p>Fly Future Education provides study-abroad consultancy services "
                    "including admissions guidance, visa support, and scholarship advice. Submitting a form does not "
                    "guarantee admission, scholarship, or visa approval, which remain at the discretion of the "
                    "relevant institution or government authority.</p>"
                    "<h3>Accuracy of Information</h3><p>You agree to provide accurate and truthful information in "
                    "any form submitted on this site.</p>"
                    "<h3>Intellectual Property</h3><p>All content on this website is the property of Fly Future "
                    "Education unless otherwise noted, and may not be reproduced without permission.</p>"
                    "<h3>Changes to These Terms</h3><p>We may update these terms from time to time. Continued use "
                    "of the site constitutes acceptance of the updated terms.</p>"
                ),
            ),
        )


def _brand_logo_file():
    import os

    from django.conf import settings as dj_settings

    path = os.path.join(dj_settings.BASE_DIR, "static", "img", "brand", "logo-square.png")
    with open(path, "rb") as f:
        return ContentFile(f.read(), name="logo.png")
