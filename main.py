import json as js
import sys
import traceback
from tablesage import TableSage
from utils.mclient import MinioClient
from time import time

def run(json):

    try:
        ################################## MINIO INIT #################################
        minio_id = json['minio']['id']
        minio_key = json['minio']['key']
        minio_skey = json['minio'].get('skey', None)
        minio_endpoint = json['minio']['endpoint_url']
        #Init MinIO Client with acquired credentials from tool execution metadata
        mc = MinioClient(minio_endpoint, minio_id, minio_key, secure=True, session_token=minio_skey)
        ###############################################################################

        ##### Tool Logic #####
        # First script parameters
        
        log = mc.get_object(s3_path=json["input"]['data'][0], local_path='file.csv')
        if 'error' in log:
            raise ValueError(log['error'])
        
        separator = json["parameters"].get('separator', ',')
        encoding = json["parameters"].get('encoding', 'utf-8')
        engine = json["parameters"].get('engine', 'python')
        
        p = TableSage()
        p.load_dataset('file.csv', separator=separator,
                       encoding=encoding, engine=engine)
        
        if 'model' not in json['parameters']:
            raise ValueError('At least 1 model must be provided.')
        model = json["parameters"]['model'] 
        
        table_prompt_ids = json["parameters"].get('table_prompt_ids', None)
        column_prompt_ids = json["parameters"].get('column_prompt_ids', None)
        official_table_description = json["parameters"].get('official_table_description', None)
        official_column_descriptions = json["parameters"].get('official_column_descriptions', None)
        no_prompts = json["parameters"].get('engine', 3)
        
        
        endpoint = json["secrets"].get('endpoint', None)
        token = json["secrets"].get('token', None)
        
        t = time()
        profile = p.profile_dataset(model=model,
                                    table_prompt_ids=table_prompt_ids, 
                                    column_prompt_ids=column_prompt_ids,
                                    endpoint=endpoint,
                                    token=token,
                                    official_table_description=official_table_description, 
                                    official_column_descriptions=official_column_descriptions,
                                    no_prompts=no_prompts,
                                    verbose=True)
        t = time() - t
        
        with open('profile.json', 'w') as f:
            f.write(js.dumps(profile, indent=4)+"\n")
        
        if 'profile' in json['output']:
            mc.put_object(s3_path=json['output']['profile'], file_path='profile.json')

        #Evaluate Responses
        metrics = {'time': t }

        json= {
                'message': 'Profiler Executed Succesfully',
                'output': json['output'], 
                'metrics': metrics,
                'status': 200,
              }
        print(json)
        return json

    except Exception as e:
        print(traceback.format_exc())
        return {
            'message': 'An error occurred during data processing.',
            'error': traceback.format_exc(),
            'status': 500
        }
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Please provide 2 files.")
    with open(sys.argv[1]) as o:
        j = js.load(o)
    response = run(j)
    with open(sys.argv[2], 'w') as o:
        o.write(js.dumps(response, indent=4))