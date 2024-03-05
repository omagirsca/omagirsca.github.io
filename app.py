from flask import Flask, render_template, request, send_file
import PyPDF2
import os

app = Flask(__name__)


def cortar_pdf(pdf_path, inicio, fim, output_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(inicio - 1, fim):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf = request.files['pdf']
        inicio = int(request.form['inicio'])
        fim = int(request.form['fim'])
        nome_saida = request.form['nome_saida']

        # Salvar o PDF enviado pelo usuário
        pdf_path = os.path.join('uploads', pdf.filename)
        pdf.save(pdf_path)

        # Criar o nome do PDF de saída
        output_path = os.path.join('downloads', f'{nome_saida}.pdf')

        # Cortar o PDF
        cortar_pdf(pdf_path, inicio, fim, output_path)

        # Remover o PDF de entrada
        os.remove(pdf_path)

        return send_file(output_path, as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
