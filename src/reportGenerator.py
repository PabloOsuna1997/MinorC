
import itertools
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)
    
def export_to_pdf(data, type_):
    path = ''
    if type_ == 1:
        type_ = "ERRORES LEXICOS:"
        path = '../reports/lexicalReport.pdf'
    elif type_ == 2:
        type_ = "ERRORES SINTACTICOS:"
        path = '../reports/sintacticReport.pdf'
    else:
        type_ ="ERRORES SEMANTICOS:"
        path = '../reports/semanticReport.pdf'

    c = canvas.Canvas(f"{path}", pagesize=A4)
    c.drawImage('../resources/logo.jpg', 25, 750, 50, 50)
    c.drawString(90,790,"Universidad de San Carlos de Guatemala")
    c.drawString(90,770,"Juan Pablo Osuna de Leon - 201503911")
    c.drawString(90,750,f"{type_}")

    w, h = A4
    max_rows_per_page = 45
    # Margin.
    x_offset = 75
    y_offset = 115
    # Space between rows.
    padding = 15

    xlist = []
    if type_ == 2:       
        xlist = [x + x_offset for x in [10, 200, 275, 350]]
    elif type_ == 1:
        xlist = [x + x_offset for x in [100, 200, 275, 350]]
    else:
        x_offset = 10
        xlist = [x + x_offset for x in [100, 400, 475, 550]]

    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
                
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    c.save()