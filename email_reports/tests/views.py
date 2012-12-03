from django.http import HttpReponse


def report(request):
    "Minimal HTML report response."
    html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"  
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">  
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">  
        <head>  
            <meta http-equiv="content-type" content="text/html; charset=utf-8"/>  
            <title>title</title>
        </head>  
        <body>
            <div id='report-title'>Foo</div>
            <div id='report-content'>Bar</div>  
        </body>  
    </html>
    """
    return HttpReponse(content=html)
