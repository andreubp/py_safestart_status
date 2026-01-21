from datetime import datetime
import redcap
import params
import tokens

import pandas as pd

def generate_redcap_labels():
    """
    Function to get actual data, change the label status based on the participant
    profile types.
    """

    for project_name in tokens.REDCAP_QUALI_PROJECT:
        print(project_name)

        to_import_dict = []
        project = redcap.Project(tokens.URL,tokens.REDCAP_QUALI_PROJECT[project_name])
        df = project.export_records(format_type='df',events=['general_informatio_arm_1'])

        df = df.reset_index()

        # 1. Extract Label Components
        def get_parts(row):
            x = params.site_map.get(row['interv_site'], 'NA')
            yyy = params.activity_map.get(row['data_collection_activity'], 'UNK')
            
            # Determine ZZZ based on YYY
            zzz = ''
            if yyy == 'KII': zzz = params.subtype_maps['KII'].get(row['interv_partic_profile'], '')
            elif yyy == 'FGD': zzz = params.subtype_maps['FGD'].get(row['interv_fg_profile'], '')
            elif yyy == 'Obs': zzz = params.subtype_maps['Obs'].get(row['interv_obs_profile'], '')
            
            # Determine VV for DHMT
            vv = params.dhmt_map.get(row['interv_partic_profile_dhmt'], '') if zzz == 'DHMT' else ''
            
            return pd.Series([x, yyy, zzz, vv])

        df[['X', 'YYY', 'ZZZ', 'VV']] = df.apply(get_parts, axis=1)

        # 2. Calculate Sequential Number (N) 
        # This counts occurrences of the same type within the same site
        df['N'] = df.groupby(['X', 'YYY', 'ZZZ', 'VV']).cumcount() + 1

        # 3. Format Final String
        def assemble(row):
            # Filter out empty components (like VV when not applicable)
            components = [row['X'], row['YYY'], row['ZZZ'], row['VV'], str(row['N'])]
            return "_".join([c for c in components if c])

        df['participant_label'] = df.apply(assemble, axis=1)

        # 4. Export to REDCap
        for k,el in df.T.items():
            label = el['participant_label']
            tmp_dict = {'record_id':el['record_id'],'participant_status':label}
            to_import_dict.append(tmp_dict)
        print(to_import_dict)
        response = project.import_records(to_import_dict)
        print(str(datetime.now())+"[SAFESTART QUALI STATUS UPDATES]: {}".format(response.get('count')))