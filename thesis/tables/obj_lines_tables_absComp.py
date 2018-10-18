from dazer_methods import Dazer
from collections import OrderedDict
from numpy import concatenate, unique, round, nan
from pandas import read_csv, isnull, notnull, DataFrame
from lib.CodeTools.sigfig import round_sig

lines_log_format_headers = ['Ions', 'lambda_theo', 'notation']
lines_log_format_address = '/home/vital/PycharmProjects/dazer/format/emlines_pyneb_optical_infrared.dz'
lines_df = read_csv(lines_log_format_address, index_col=0, names=lines_log_format_headers, delim_whitespace=True)

# Generate dazer object
dz = Dazer()

# Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
norm_factor = 100

# Treatment add quick index
dz.quick_indexing(catalogue_df)

# Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'

# Reddening properties
R_v = 3.4
red_curve = 'G03_average'
cHbeta_type = 'cHbeta_emis'

# Define table properties
obj_per_page = 1
column_code = ['line_Eqw', 'line_Flux', 'line_Int']
linformat_df = read_csv(lines_log_format_address, names=['ion', 'lambda_theo', 'latex_format'], header=0, delim_whitespace=True)
linformat_df.lambda_theo = round(linformat_df.lambda_theo.values, 2)

for objName in catalogue_df.loc[dz.idx_include].index:

    if objName in ['8', 'SHOC579']:

        local_reference = objName.replace('_', '-')

        quick_reference = catalogue_df.loc[objName].quick_index

        pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/images/{}_absEffect.png'.format(quick_reference)

        dz.create_pdfDoc(pdf_address, pdf_type='table')

        dz.pdf_insert_table(table_format='l' + 'ccc')

        group_dict = OrderedDict()

        # Make dict with all the objects lines dataframes
        ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
        linelog_reducAddress = '{objfolder}{codeName}_WHT_linesLog_reduc.txt'.format(objfolder=ouput_folder,
                                                                                     codeName=objName)
        linelog_emisAddress = '{objfolder}{codeName}_WHT_linesLog_emission_2nd.txt'.format(objfolder=ouput_folder,
                                                                                           codeName=objName)
        reduc_linedf = dz.load_lineslog_frame(linelog_reducAddress)
        emission_linedf = dz.load_lineslog_frame(linelog_emisAddress)

        Hbeta_F = reduc_linedf.loc['H1_4861A'].line_Flux
        Hbeta_emisF = emission_linedf.loc['H1_4861A'].line_Flux

        lambdas_array = emission_linedf['lambda_theo'].values

        # Short array and remove repeated entries
        lambdas_array = unique(lambdas_array)

        # Add the parameters row
        Headers = [r'$\lambda(\AA)$', 'Observed flux', 'Emission flux', '\% Difference']
        dz.addTableRow(Headers, last_row=True)

        # Loop through the observed lines an ad them to the table
        for i in range(len(reduc_linedf.index)):

            lineLabel = reduc_linedf.iloc[i].name
            wave = reduc_linedf.iloc[i].lambda_theo
            recombLine = True if (('H1' in lineLabel) or ('He1' in lineLabel) or ('He2' in lineLabel)) and wave < 6900 else False
            print 'wave', wave, recombLine

            if recombLine:

                if lineLabel != 'H1_6563A_w':
                    #idx_label = (linformat_df['lambda_theo'] == wave)
                    ion = linformat_df.loc[lineLabel, 'latex_format']
                    wave = 4861.0 if lineLabel == 'H1_4861A' else wave
                    wave_lam_ref = int(round(wave, 0))
                    lineFlabel = r'{} ${}$'.format(wave_lam_ref, ion)
                    row = [lineFlabel]
                    row_i = [row] * 3

                    line_F = reduc_linedf.iloc[i].line_Flux
                    line_emisF = emission_linedf.iloc[i].line_Flux

                    row_i[0] = line_F/Hbeta_F * norm_factor
                    row_i[1] = line_emisF/Hbeta_F * norm_factor
                    diff = (1.0 - line_F/line_emisF)*100
                    row_i[2] = round(diff.nominal_value,1)#/Hbeta_emisF * norm_factor

                    row = row + row_i

                    dz.addTableRow(row, last_row=False)

        dz.generate_pdf()



        # for wave in lambdas_array:
        #
        #     if wave in linformat_df['lambda_theo'].values:
        #         idx_label   = (linformat_df['lambda_theo'] == wave)
        #         ion         = linformat_df.loc[idx_label, 'latex_format'].values[0]
        #         label       = linformat_df.loc[idx_label, 'line_label'].values[0]
        #         wave        = 4861.0 if label == 'H1_4861A' else wave
        #         wave_lam_ref = int(round(wave, 0))
        #         line_label  = r'{} ${}$'.format(wave_lam_ref, ion)
        #         row         = [line_label]
        #         table_row   = [None] * 7
        #
        #         if ion in ['H1', 'He1', 'He2']:
        #
        #             row_i = ['-'] * 1  # By default empty cells
        #             if label in group_dict[str(objName) + '_dfemis'].index:
        #                 row_i = list(group_dict[str(objName) + '_dfemis'].loc[label, column_code].values)
        #
        #                 # Special treatment for the equivalent length: Using flux
        #                 continua_reduc = group_dict[str(objName) + '_df'].loc[label, 'con_dered']
        #                 Eqw_special = row_i[2] / continua_reduc
        #
        #                 if Eqw_special >= 5.0:
        #                     rounddig = 3
        #                     rounddig_er = 3
        #                 else:
        #                     rounddig = 1
        #                     rounddig_er = 1
        #
        #                 row_i[1] = row_i[1] / group_dict[str(objName) + '_Hbeta_F'] * norm_factor
        #                 row_i[2] = row_i[2] / group_dict[str(objName) + '_Hbeta_I'] * norm_factor
        #
        #             row = row + row_i
        #
        #             dz.addTableRow(row, last_row=False)
        #
        #         else:
        #             print 'ESTA FALLA', wave


        #dz.generate_pdf(output_address=pdf_address)
