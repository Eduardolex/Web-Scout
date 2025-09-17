import csv, json, os, re, time
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from readability import Document
import tldextract

OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (compatible; SiteScout/1.0)"}

def domain_key(url:str)->str:
    netloc = urlparse(url).netloc
    return netloc.replace(":", "_")

def get(url, timeout=15):
    try:
        t0 = time.time()
        r = requests.get(url, headers=UA, timeout=timeout)
        dt = (time.time() - t0) * 1000
        return r, int(dt)
    except Exception:
        return None, None

def extract_basic(url:str):
    r, rt_ms = get(url)
    if not r or not r.text:
        return {"ok": False, "status": getattr(r, "status_code", None), "rt_ms": rt_ms}

    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    # Readability content
    try:
        doc = Document(html)
        main_html = doc.summary()
        main_soup = BeautifulSoup(main_html, "html.parser")
        main_text = re.sub(r"\s+", " ", main_soup.get_text(" ", strip=True)).strip()
    except Exception:
        main_text = ""

    title = (soup.title.get_text(strip=True) if soup.title else "")
    meta_desc = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md and md.get("content"):
        meta_desc = md["content"].strip()

    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""

    # Heuristics
    has_viewport = bool(soup.find("meta", attrs={"name": "viewport"}))
    uses_https = urlparse(url).scheme == "https"
    phone = bool(re.search(r"\+?\d[\d\-\s\(\)]{7,}\d", html))
    email = bool(re.search(r"mailto:|[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}", html))
    has_booking = any(k in html.lower() for k in ["book now","appointment","schedule","reserve","book an appointment"])
    has_ga = "gtag(" in html or "googletagmanager.com" in html or "analytics.js" in html
    img_count = len(soup.find_all("img"))

    # CMS/framework hints
    generator = ""
    gen = soup.find("meta", attrs={"name": "generator"})
    if gen and gen.get("content"): generator = gen["content"].strip()
    is_wordpress = "wp-content" in html.lower() or "WordPress" in generator
    is_wix = "wix.com" in html.lower()
    is_squarespace = "squarespace" in html.lower()
    is_shopify = "cdn.shopify.com" in html.lower()

    # robots & sitemap
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    robots_ok, sitemap = None, None
    rob = requests.get(urljoin(base, "/robots.txt"), headers=UA, timeout=8)
    if rob.status_code == 200:
        robots_ok = True
        m = re.search(r"(?im)^sitemap:\s*(\S+)", rob.text)
        if m: sitemap = m.group(1)
    else:
        robots_ok = False

    return {
        "ok": True,
        "status": r.status_code,
        "rt_ms": rt_ms,
        "title": title[:200],
        "meta_desc": meta_desc[:300],
        "h1": h1_text[:200],
        "word_count": len(main_text.split()),
        "has_viewport": has_viewport,
        "uses_https": uses_https,
        "has_phone": phone,
        "has_email": email,
        "has_booking": has_booking,
        "has_ga": has_ga,
        "img_count": img_count,
        "cms_hint": {
            "generator": generator,
            "wordpress": is_wordpress,
            "wix": is_wix,
            "squarespace": is_squarespace,
            "shopify": is_shopify
        },
        "robots_txt": robots_ok,
        "sitemap": sitemap
    }

def score_site(d:dict):
    # Simple 0–100 scout score with big weight on basics a small business cares about
    score = 0
    if not d.get("ok"): return 0
    # responsiveness & basics
    score += 10 if d.get("has_viewport") else 0
    score += 10 if d.get("uses_https") else 0
    # contactability
    score += 10 if d.get("has_phone") else 0
    score += 10 if d.get("has_email") else 0
    # booking CTA
    score += 15 if d.get("has_booking") else 0
    # content presence
    wc = d.get("word_count", 0)
    score += 10 if wc >= 200 else (5 if wc >= 80 else 0)
    # meta basics
    score += 10 if d.get("meta_desc") else 0
    # perf proxy (very rough)
    rt = d.get("rt_ms") or 9999
    score += 15 if rt < 800 else (8 if rt < 1400 else 0)
    # analytics
    score += 5 if d.get("has_ga") else 0
    return min(score, 100)

def facts_block(url:str, d:dict, score:int)->str:
    ext = tldextract.extract(url)
    domain = ".".join([x for x in [ext.domain, ext.suffix] if x])
    lines = [
        f"Domain: {domain}",
        f"URL: {url}",
        f"ScoutScore: {score}/100",
        f"Title: {d.get('title','')}",
        f"H1: {d.get('h1','')}",
        f"Meta description present: {bool(d.get('meta_desc'))}",
        f"Word count (main content): {d.get('word_count')}",
        f"Uses HTTPS: {d.get('uses_https')}",
        f"Mobile viewport tag: {d.get('has_viewport')}",
        f"First-byte response time (ms): {d.get('rt_ms')}",
        f"Has phone on page: {d.get('has_phone')}",
        f"Has email on page: {d.get('has_email')}",
        f"Has booking CTA: {d.get('has_booking')}",
        f"Images found: {d.get('img_count')}",
        f"CMS hint: {d.get('cms_hint')}",
        f"robots.txt present: {d.get('robots_txt')}, sitemap: {d.get('sitemap')}"
    ]
    return "\n".join(lines)

def md_block(url:str, d:dict, score:int)->str:
    def yn(x): return "Yes" if x else "No"
    return f"""# Scout Report — {url}

**Score:** {score}/100
**Title:** {d.get('title','')}
**H1:** {d.get('h1','')}

## Basics
- HTTPS: {yn(d.get('uses_https'))}
- Mobile viewport: {yn(d.get('has_viewport'))}
- Meta description present: {yn(bool(d.get('meta_desc')))}
- First-byte response time: {d.get('rt_ms')} ms
- Main content word count: {d.get('word_count')}
- Images: {d.get('img_count')}

## Contactability & Conversion
- Phone on page: {yn(d.get('has_phone'))}
- Email on page: {yn(d.get('has_email'))}
- Booking call-to-action: {yn(d.get('has_booking'))}

## CMS / Platform (heuristics)
{json.dumps(d.get('cms_hint'), indent=2)}

## Robots / Sitemap
- robots.txt present: {yn(d.get('robots_txt'))}
- sitemap: {d.get('sitemap')}
"""

def save_outputs(url:str, data:dict):
    key = domain_key(url)
    score = score_site(data)
    # JSON
    with open(os.path.join(OUT_DIR, f"{key}.json"), "w", encoding="utf-8") as f:
        json.dump({"url": url, "score": score, "data": data}, f, indent=2, ensure_ascii=False)
    # Markdown
    with open(os.path.join(OUT_DIR, f"{key}.md"), "w", encoding="utf-8") as f:
        f.write(md_block(url, data, score))
    # Facts bundle for pitching
    with open(os.path.join(OUT_DIR, f"{key}.facts.txt"), "w", encoding="utf-8") as f:
        f.write(facts_block(url, data, score))

def main():
    # Install deps tip
    #   python -m venv .venv && source .venv/bin/activate
    #   pip install -r requirements.txt
    with open("targets.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        url = row["url"].strip()
        if not url: continue
        if not url.startswith("http"):
            url = "https://" + url
        print("→ Scouting", url)
        try:
            data = extract_basic(url)
            save_outputs(url, data)
        except Exception as e:
            print("  ! Error:", e)

if __name__ == "__main__":
    main()