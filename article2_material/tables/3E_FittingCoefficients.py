from dazer_methods import Dazer
from collections import OrderedDict
from lib.inferenceModel import SpectraSynthesizer
from pylatex import Package
import uncertainties

# Headers
headers_dic = OrderedDict()
headers_dic['line_label'] = r'$Line$'
headers_dic['a'] = r'a'
headers_dic['b'] = r'b'
headers_dic['c'] = r'c'
headers_dic['d'] = r'd'
headers_dic['e'] = r'd'

# Import functions
dz = Dazer()
specS = SpectraSynthesizer()

# Declare data location
article_folder = 'E:\\Dropbox\\Astrophysics\\Papers\\Yp_BayesianMethodology\\source files\\tables\\'

# # Generate pdf
tableAddress = article_folder + 'emissivityCoefficients'
# dz.create_pdfDoc(tableAddress, pdf_type='table')
# # dz.pdfDoc.packages.append(Package('nicefrac'))
dz.pdf_insert_table(headers_dic.values())

default_lines = ['H1_4341A',
                'O3_4363A',
                'He1_4471A',
                'He2_4686A',
                'Ar4_4740A',
                'O3_4959A',
                'O3_5007A',
                'He1_5876A',
                'S3_6312A',
                'N2_6548A',
                'H1_6563A',
                'N2_6584A',
                'He1_6678A',
                'S2_6716A',
                'S2_6731A',
                'Ar3_7136A',
                'O2_7319A_b',
                'S3_9069A',
                'S3_9531A']

# Loop through the objects
for i in range(len(default_lines)):

    # Object references
    lineLabel = default_lines[i]
    lineCoeffs = specS.config[lineLabel + '_coeffs']

    row = ['-'] * 6
    row[0] = specS.linesDb.loc[lineLabel, 'latex_code']

    for j in range(1, 6):
        if j-1 < len(lineCoeffs):
            row[j] = lineCoeffs[j-1]

    dz.addTableRow(row, last_row=False if default_lines[-1] != lineLabel else True, rounddig=3, rounddig_er=1)

# dz.generate_pdf()
dz.generate_pdf(output_address=tableAddress)