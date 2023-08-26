import PyPDF2, os

pdfiles = ["1.pdf","2.pdf"]

# for filename in os.listdir('.'):
#     if filename.endswith('.pdf'):
#         if filename != 'merged.pdf':
#             pdfiles.append(filename)
#
# pdfiles.sort(key=str.lower)


pdfMerge = PyPDF2.PdfMerger()

for filename in pdfiles:
        pdfFile = open(filename, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFile)
        pdfMerge.append(pdfReader)

pdfFile.close()
pdfMerge.write('merged.pdf')