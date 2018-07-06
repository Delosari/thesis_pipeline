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
norm_factor = 1000

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
Headers = [r'$\lambda(\AA)$'] + [r'$EW(\AA)$', r'$F(\lambda)$', r'$I(\lambda)$'] * obj_per_page
column_code = ['line_Eqw', 'line_Flux', 'line_Int']
linformat_df = read_csv(lines_log_format_address, names=['line_label', 'ion', 'lambda_theo', 'latex_format'],
                        delim_whitespace=True)
linformat_df.lambda_theo = round(linformat_df.lambda_theo.values, 2)

columns_output = ['ion', 'Eqw (angstroms)', 'Err Eqw (angstroms)', 'Flux (normalized Hbeta = 1000)',
                  'Err Flux (normalized Hbeta = 1000)', 'Intensity (normalized Hbeta = 1000)',
                  'Err Intensity (normalized Hbeta = 1000)']

for objName in catalogue_df.loc[dz.idx_include].index:

    local_reference = objName.replace('_', '-')

    quick_reference = catalogue_df.loc[objName].quick_index

    pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/object_lines/{}_lineFluxes'.format(quick_reference)
    table_address = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/supplementary material online/{}_lineFluxes.txt'.format(quick_reference)

    #dz.create_pdfDoc(pdf_address, pdf_type='table')

    dz.pdf_insert_table(table_format='l' + 'c' * (3 * obj_per_page))

    group_dict = OrderedDict()

    # Make dict with all the objects lines dataframes
    ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
    linelog_reducAddress = '{objfolder}{codeName}_WHT_linesLog_reduc.txt'.format(objfolder=ouput_folder,
                                                                                 codeName=objName)
    linelog_emisAddress = '{objfolder}{codeName}_WHT_linesLog_emission_2nd.txt'.format(objfolder=ouput_folder,
                                                                                       codeName=objName)
    reduc_linedf = dz.load_lineslog_frame(linelog_reducAddress)
    emission_linedf = dz.load_lineslog_frame(linelog_emisAddress)

    cHbeta = catalogue_df.loc[objName, cHbeta_type]
    dz.deredden_lines(reduc_linedf, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
    dz.deredden_lines(emission_linedf, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)

    group_dict[str(objName) + '_df'] = reduc_linedf
    group_dict[str(objName) + '_dfemis'] = emission_linedf

    group_dict[str(objName) + '_Hbeta_F'] = emission_linedf.loc['H1_4861A'].line_Flux
    group_dict[str(objName) + '_Hbeta_I'] = emission_linedf.loc['H1_4861A'].line_Int

    lambdas_array = emission_linedf['lambda_theo'].values

    # Short array and remove repeated entries
    lambdas_array = unique(lambdas_array)

    # Insert the row with the names
    row_objs = ['', '', quick_reference, '']
    dz.addTableRow(row_objs, last_row=False)

    # Add the parameters row
    dz.addTableRow(Headers, last_row=True)

    output_df = DataFrame(columns=columns_output)
    output_df.index.name = 'lambda'

    # Loop through the observed lines an ad them to the table
    for wave in lambdas_array:

        if wave in linformat_df['lambda_theo'].values:
            idx_label = (linformat_df['lambda_theo'] == wave)
            ion = linformat_df.loc[idx_label, 'latex_format'].values[0]
            label = linformat_df.loc[idx_label, 'line_label'].values[0]
            wave = 4861.0 if label == 'H1_4861A' else wave
            wave_lam_ref = int(round(wave, 0))
            line_label = r'{} ${}$'.format(wave_lam_ref, ion)
            row = [line_label]
            table_row = [None] * 7

            if linformat_df.loc[idx_label, 'line_label'].values[0] not in ['O2_10012A', 'S8_9913A']:

                row_i = ['-'] * 3  # By default empty cells
                if label in group_dict[str(objName) + '_dfemis'].index:
                    row_i = list(group_dict[str(objName) + '_dfemis'].loc[label, column_code].values)

                    # Special treatment for the equivalent length: Using flux
                    continua_reduc = group_dict[str(objName) + '_df'].loc[label, 'con_dered']
                    Eqw_special = row_i[2] / continua_reduc

                    if Eqw_special >= 5.0:
                        rounddig = 3
                        rounddig_er = 3
                    else:
                        rounddig = 1
                        rounddig_er = 1

                    row_i[0] = dz.format_for_table(Eqw_special, rounddig=rounddig, rounddig_er=rounddig_er)
                    row_i[1] = row_i[1] / group_dict[str(objName) + '_Hbeta_F'] * norm_factor
                    row_i[2] = row_i[2] / group_dict[str(objName) + '_Hbeta_I'] * norm_factor

                row = row + row_i

                dz.addTableRow(row, last_row=False)

                # Ascii row
                table_row[0] = ion
                table_row[1] = row_i[0].split('$\pm$')[0]
                table_row[2] = row_i[0].split('$\pm$')[1]
                flux_entry = dz.format_for_table(row_i[1])
                table_row[3] = flux_entry.split('$\pm$')[0]
                table_row[4] = flux_entry.split('$\pm$')[1]
                int_entry = dz.format_for_table(row_i[2])
                table_row[5] = int_entry.split('$\pm$')[0]
                table_row[6] = int_entry.split('$\pm$')[1]
                output_df.loc[str(wave_lam_ref)] = table_row



            else:
                print 'ESTA FALLA', wave

    dz.table.add_hline()

    # Add bottom rows with the Hbeta flux and reddening
    row_F, row_cHbeta = [r'$I(H\beta)$ $(erg\,cm^{-2} s^{-1} \AA^{-1})$'], [r'$c(H\beta)$']

    F_hbeta = dz.format_for_table(group_dict[str(objName) + '_Hbeta_F'], rounddig=2, scientific_notation=True)
    I_hbeta = dz.format_for_table(group_dict[str(objName) + '_Hbeta_I'], rounddig=2, scientific_notation=True)
    row_F += ['', dz.format_for_table(group_dict[str(objName) + '_Hbeta_F'], rounddig=2, scientific_notation=True),
              dz.format_for_table(group_dict[str(objName) + '_Hbeta_I'], rounddig=2, scientific_notation=True)]
    cHbeta_reduc, cHbeta_emis = catalogue_df.loc[objName, 'cHbeta_reduc'], catalogue_df.loc[objName, 'cHbeta_emis']

    cHbeta_reduc_entry = '{}$\pm${}'.format(round_sig(cHbeta_reduc.nominal_value, 2, scien_notation=False),
                                            round_sig(cHbeta_reduc.std_dev, 1, scien_notation=False))
    cHbeta_emis_entry = '{}$\pm${}'.format(round_sig(cHbeta_emis.nominal_value, 2, scien_notation=False),
                                           round_sig(cHbeta_emis.std_dev, 1, scien_notation=False))
    row_cHbeta += ['', cHbeta_emis_entry, '']

    dz.addTableRow(row_F, last_row=False)
    dz.addTableRow(row_cHbeta, last_row=True)
    dz.table.add_hline()

    #dz.generate_pdf()
    dz.generate_pdf(output_address=pdf_address)

    # table_row = [''] * 7
    # # table_row[0] = '$(erg\,cm^{-2} s^{-1} \AA^{-1})$'
    # table_row[3] = F_hbeta.split('$\pm$')[0]
    # table_row[4] = F_hbeta.split('$\pm$')[1]
    # table_row[5] = I_hbeta.split('$\pm$')[0]
    # table_row[6] = I_hbeta.split('$\pm$')[1]
    # output_df.loc[row_F[0] + '$(erg\,cm^{-2} s^{-1} \AA^{-1})$'] = table_row
    #
    # table_row = [''] * 7
    # table_row[3] = cHbeta_emis_entry.split('$\pm$')[0]
    # table_row[4] = cHbeta_emis_entry.split('$\pm$')[1]
    # output_df.loc[row_cHbeta[0]] = table_row
    #
    # with open(table_address, 'w') as f:
    #     f.write(output_df.to_string(index=True, index_names=False))  # float_format=lambda x: "{:15.8f}".format(x)


