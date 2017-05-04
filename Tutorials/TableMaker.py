
import  types
from    numpy import shape, ndarray

class Latex_pyTable():
    
    def __init__(self, IsolationCheck = True):
        
#         self.Name           = None
#         self.Folder         = None
#         self.Size           = '\scriptize'
#         self.TableWidth     = 'Opt'
#         self.Headers        = None

        self.Tex_File       = None
        self.Isolated_Table = IsolationCheck
            
    def Generate_Table(self):
        
        
        
        return
    
    def Start_TexFile(self, FileFolder, FileName, Document_Configuration = 'Default'):    
        
        L_Document_Declaration          = None
        L_Document_Begin                = None
        L_Package1                      = None
        L_Package2                      = None
        
        if self.Isolated_Table == True:
            if Document_Configuration == 'Default':
                self.Tex_File                 =  open(FileFolder + FileName, "w")
                Document_Type                 = "aastex"
                L_Document_Declaration        = "\\documentclass{"+ Document_Type +"}"
                L_Document_Begin              = "\\begin{document}"
                L_Package1                    = '\\usepackage{underscore}'
                L_Package2                    = '\\usepackage[margin=0.5in]{geometry}'

        self.Add_Line(L_Document_Declaration)
        self.Add_Line(L_Package1)
        self.Add_Line(L_Package2)        
        self.Add_Line(L_Document_Begin)

        return
        
    def Start_Table(self, Colum_just, Table_Configuration = 'Abundances_WHT', Rotated = False, Size = '\\scriptsize', Title = 'Title', Width = '0pt'):
                
        L_TableDeluxeBegin  = "\\begin{deluxetable}{" + Colum_just + "}"
        L_TableSize         = None
        L_Rotation          = None
        L_Caption           = None
        L_TableWidth        = None
        
        if Table_Configuration == 'Abundances_WHT':
            L_TableSize = "\\tabletypesize{" + Size + "}"
        
        if Rotated == True:
            L_Rotation  = '\\rotate'
            
        L_Caption       = "\\tablecaption{" + Title + "}"
        L_TableWidth    = "\\tablewidth{" + Width + "}"
        
        self.Add_Line(L_TableDeluxeBegin)
        self.Add_Line(L_TableSize)
        self.Add_Line(L_Rotation)
        self.Add_Line(L_Caption)
        self.Add_Line(L_TableWidth)

        return

    def Table_Header(self, Columns_Title_List = [None]):
        
        L_Header    = "\\tablehead{\\colhead{" + Columns_Title_List[0] + "}"
        L_StartData = "\\startdata"
         
        for i in range(1, len(Columns_Title_List)):
            L_Header = L_Header + ' & ' + "\\colhead{" + Columns_Title_List[i] + "}"
            
            if i == (len(Columns_Title_List) - 1):
                L_Header = L_Header +'}'
                
        self.Add_Line(L_Header)
        self.Add_Line(L_StartData)
        
        return 
    
    def InsertTable_Row(self, Row_List_Values):
                
        L_Data_Row = None

        for i in range(len(Row_List_Values)):
            
            #Here we put our format convertor
            Datum = self.DataValue_2_Latex(Row_List_Values[i])
            
            #For the first value in the line      
            if i == 0:
                L_Data_Row = Datum
                
            #Anything above the first value
            else:
                L_Data_Row = L_Data_Row + ' & ' + Datum
                
#       Closing the row
        L_Data_Row = L_Data_Row + '\\\\' 
        
        L_Data_Row = self.Check_Recording(L_Data_Row)  

        self.Add_Line(L_Data_Row)
           
        return
        
    def Finish_Table(self):
        
        L_FinishData    = "\\enddata"
        L_FinishTable   = "\\end{deluxetable}"
   
        self.Add_Line(L_FinishData)
        self.Add_Line(L_FinishTable)
        
        return
    
    def Finish_TexFile(self, Document_Configuration = 'Default'):     
        
        L_EndDocument = None
        
        if self.Isolated_Table == True:
            if Document_Configuration == 'Default':
                L_EndDocument = '\end{document}'
                        
        self.Add_Line(L_EndDocument)
        self.Tex_File.close()

        return  
    
    def Add_Line(self, String):
        
        if String != None:
            self.Tex_File.write(String + "\n")
            
        return 
            
    def DataValue_2_Latex(self, Parameter, Null_Output = '---'):
        
        Datum = Null_Output
        
#       Check table parameter has no meaning
        if (Parameter != 'nan') and (Parameter != 'None') and (Parameter != None) and (Parameter != '-'):
            
#           Single value case
            if type(Parameter) not in [types.ListType, ndarray]:
                Datum = str(Parameter)
                
#           Case with a value and error
            else:
                if len(shape(Parameter)) in [1,2]:
                    Datum = '$' + str(Parameter[0]) + '\\pm' + str(Parameter[1]) + '$'
                                        
                else:
                    raise ValueError, "data items must be 1D or 2D"
        
        if 'nan' in Datum:
            Datum = Datum.replace('nan','\\,nan\\,')
        
        return Datum
    
    def ColumnJustifications(self, NumColumns, Format = 'Default'):
        
        Just = 'l'
        
        if Format == 'Default':
            for i in range(1, len(NumColumns)):
                Just = Just + 'c'
                
        return Just
        
    def Check_Recording(self, Data_Row):
        
#       In case the first item of the row is a square braket: 
        if Data_Row[0] == '[':
            Data_Row = Data_Row[0].replace('[','\\null[') + Data_Row[1:]
     

     
        return Data_Row