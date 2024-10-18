from flask import Blueprint, render_template

app = Blueprint("general" , __name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404page.html"), 404

@app.route("/about")
def about():
    return "about us"

# @app.route('/sitemap.xml')
# def sitemap():
#     # لیست URLهای صفحات وب‌سایت شما
#     pages = [
#         {'loc': 'http://example.com/', 'lastmod': '2024-10-18'},
#         {'loc': 'http://example.com/about', 'lastmod': '2024-10-18'},
#         {'loc': 'http://example.com/contact', 'lastmod': '2024-10-18'},
#         # می‌توانید صفحات بیشتری اضافه کنید
#     ]
    
#     # تولید محتوای XML
#     xml = '''<?xml version="1.0" encoding="UTF-8"?>
#     <urlset xmlns="http://www.sitemaps.org/schemas/sitemap-image/1.1">'''
    
#     for page in pages:
#         xml += f'''
#         <url>
#             <loc>{page['loc']}</loc>
#             <lastmod>{page['lastmod']}</lastmod>
#         </url>'''
    
#     xml += '</urlset>'
    
#     return Response(xml, mimetype='application/xml')

