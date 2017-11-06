import os
import sys
from DZ_observation_reduction import spectra_reduction

sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'

'''
Run externally
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/C0_Response_MasterFlat.py
'''

# Load iraf pypeline object
dz = spectra_reduction()

# Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

ordenes = ['High', 'Low']
orden_mag = {'High': 150, 'Low': 6}
colors = ['Blue', 'Red']

# Loop through the arms
for orden_type in ordenes:
    for arm_color in colors:
        # Get orden magnitude
        orden = orden_mag[orden_type]

        # Get the file we are going to treat
        index_ObjFlat = (dz.reducDf.reduc_tag == 'flatcombine') & (
        dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color)) & (dz.reducDf.valid_file)

        # Task attributes
        dz.task_attributes['color'] = arm_color
        dz.task_attributes['run folder'] = '{folder_run}'.format(folder_run=dz.reducFolders['flat lamp'])
        dz.task_attributes['input'] = dz.reducDf.loc[index_ObjFlat, 'file_location'].values[0] + \
                                      dz.reducDf.loc[index_ObjFlat, 'file_name'].values[0]
        dz.task_attributes['normalizing_flat'] = dz.reducDf.loc[index_ObjFlat, 'file_location'].values[0] + \
                                                 dz.reducDf.loc[index_ObjFlat, 'file_name'].values[0]
        dz.task_attributes['output'] = '{folder_output}nMasterFlat{color}_{orden_type}order.fits'.format(
            folder_output=dz.task_attributes['run folder'], color=dz.task_attributes['color'], orden_type=orden_type)
        dz.task_attributes['threshold'] = '1'
        dz.task_attributes['order'] = orden

        # Run the task
        dz.run_iraf_task('response', run_externally=False)

        dz.save_task_parameter(task='response', parameter='threshold',
                               entry='flat_{order}Order_{color}_fitting_regions'.format(order=orden_type,
                                                                                        color=arm_color))

        # Add objects to data frame with the new reduc_tag
        data_dict = {'reduc_tag': 'nflatcombine_{orden_type}order'.format(orden_type=orden_type)}
        dz.object_to_dataframe(dz.task_attributes['output'], data_dict)

# Generate pdf file
indeces_print = (dz.reducDf.reduc_tag == 'nflatcombine_Highorder') | (dz.reducDf.reduc_tag == 'nflatcombine_Loworder')
dz.generate_step_pdf(indeces_print, file_address=dz.reducFolders['reduc_data'] + 'nMaster_flat', plots_type='flats',
                     ext=0, include_graph=True)
variable = 3.0 * (2.0 + 3.0 * (2.0+3))


dz.beep_alarmn()
