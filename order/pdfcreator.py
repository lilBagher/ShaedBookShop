# order/pdfcreator.py
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def renderPdf(template, content={}):
    t = get_template(template)
    send_data = t.render(content)
    result = BytesIO()

    # TF-8 انکود کنیم
    pdf = pisa.pisaDocument(BytesIO(send_data.encode("UTF-8")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return None