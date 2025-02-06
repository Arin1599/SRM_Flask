
global TSJ_AREA_IM_DICT
TSJ_AREA_IM_DICT= {
    'C': 'C-Blast Furnace',
    'E': 'E-Blast Furnace',
    'F': 'F-Blast Furnace',
    'H': 'H-Blast Furnace',
    'G': 'G-Blast Furnace',
    'I': 'I-Blast Furnace',
    '5,6&7': 'Coke Plant 5,6&7',
    'batt 8-9': 'Coke Plant 8,9',
    'batt 10-11': 'Coke Plant 10,11',
    'Pellet': 'Pellet Plant',
    'Sp-1': 'Sinter Plant-1',
    'Sp-2': 'Sinter Plant-2',
    'Sp-3': 'Sinter Plant-3',
    'RMBB-1': 'RMBB-1',
    'RMBB-2': 'RMBB-2',
    'HMC': 'Haldia Met Coke',
    'Limefines Crushing(O)': 'Lime Fines Crushing',
    'Ferroshots': 'Ferroshots',
    'ASRF': 'ASRF'
}

global TSJ_AREA_SM_DICT
TSJ_AREA_SM_DICT=[
    'LD1',
 'LD2',
 'LD3 & TSCR',
 'HSM',
 'CRM',
 'TSCR',
 'WRM E',
 'MM',
 'NBM',
 'Lime Plant'
]

global TSJ_AREA_SS_DICT
TSJ_AREA_SS_DICT=['IMMM',
 'SMMM',
 'MMM',
 'Central services',
 'IMEM',
 'SMEM',
 'Steel CG1',
 'MEM',
 'Mills CG2',
 'Utilities',
 'PH3',
 'PH4',
 'DG',
 'PH5 & CDQ',
 'BPH',
 'FMD',
 'WMD',
 'SMG',
 'Engg Services',
 'EQMS Own',
 'EQMS customer',
 'Others']

global TSG_AREA_IM_DICT
TSG_AREA_IM_DICT=['RMHS', 'Pellet', 'DRI', 'Coke', 'Sinter', 'Blast Furnace']

global TSG_AREA_SM_DICT
TSG_AREA_SM_DICT=['SMS', 'WRM', 'Bloom', 'Bar', 'Wire']

global TSK_AREA_IM_DICT
SK_AREA_IM_DICT= {
    'RMHS (In) - PH1': 'Raw Material Handling Section (in phase 1)',
 'RMHS (In) - Pellet' : 'Raw Material Handling Section (in Pellet)',
 'RMHS (In) - PH 2' : 'Raw Material Handling Section (in phase 2)',
 'RMHS (Out) - PH1' : 'Raw Material Handling Section (out phase 1)',
 'RMHS (Out) - PLTCM': 'Raw Material Handling Section (out PLTCM)',
 'RMHS (Out) - PH 2': 'Raw Material Handling Section (out phase 2)',
 'Coke Plant': 'Coke Plant 1',
 'Coke Plant 2': 'Coke Plant 2',
 'Sinter Plant': 'Sinter Plant ',
 'Sinter Plant (Kiln 3&4)':'Sinter Plant (Kiln 3&4)',
 'BF':'Blast Furnace 1',
 'BF 2':'Blast Furnace 2',
 'Pellet': 'Pellet Plant'}

global TSK_AREA_SM_DICT
TSK_AREA_SM_DICT=['LCP',
 'SMS (Without Caster 2)',
 'SMS (Caster 2)',
 'HSM',
 'HSM (ph2)',
 'Pellet',
 'CRM - PLTCM',
 'CRM - CAL',
 'GM Sir Fund']

global TSK_AREA_SS_DICT
TSK_AREA_SS_DICT=['Water System ph2',
 'Power System (CDQ & DG)',
 'Power System (CDQ & DG) ph2',
 'Fuel Management (BPG & IG)',
 'Fuel Management (BPG & IG) ph 2']


global TSM_AREA_IM_DICT
TSM_AREA_IM_DICT= {
    
    'RMHS & RMPP': 'Raw Material Handling Section', 
    'CO-1' : 'Coke Plant 1',
    'CO-2' : 'Coke Plant 2',
    'SP-1': 'Sinter Plant 1', 
    'SP-2&3': 'Sinter Plant 2&3',
    'BF-1': 'Blast Furnace 1',
    'BF-2': 'Blast Furnace 2',
    'DRI' : 'DRI Plant'
}

global TSM_AREA_SM_DICT
TSM_AREA_SM_DICT=['Lime Plant',
 'SMS',
 'HSM ',
 '110 MW',
 'BFPP-1',
 'BFPP-2',
 'AEL (Before Merger)',
 'Oxygen Plant',
 'Common Services (incl. Utility)',
 'CRM-Angul',
 'CRM-Khopoli',
 'CRM-Sahibabad']

global TSM_AREA_SS_DICT
TSM_AREA_SS_DICT=['RMHS & RMPP',
 'CO-1',
 'CO-2',
 'SP-1',
 'SP-2&3',
 'BF-1',
 'BF-2',
 'DRI',
 'Lime Plant',
 'SMS',
 'HSM ',
 '110 MW',
 'BFPP-1',
 'BFPP-2',
 'AEL (Before Merger)',
 'Oxygen Plant',
 'Common Services (incl. Utility)',
 'CRM-Angul',
 'CRM-Khopoli',
 'CRM-Sahibabad']

def get_location_context(locations):
    context = []
    for loc in locations:
        im_var = globals().get(f"{loc}_AREA_IM_DICT", "Not Available")
        sm_var = globals().get(f"{loc}_AREA_SM_DICT", "Not Available")
        ss_var = globals().get(f"{loc}_AREA_SS_DICT", "Not Available")
        
        loc_context = f"""
        For {loc}:
        - Iron Making Plants: {im_var}
        - Steel Making Plants: {sm_var}
        - Shared Services Plants: {ss_var}
        """
        context.append(loc_context)
    
    return "\n".join(context)