# Welcome to the KLMS Tool version of TableSage

TableSage is a profiling tool for tabular data leveraging the powerful capabilities of LLMs, appropriate for data scientists. 

# Instructions

## Input
TableSage can be executed from the KLMS with the following input json:

```json
{
	"input": {
		"data": [
		    "XXXXXXXX-bucket/temp.csv"
		]
	},
	"output": {
		"profile": "/path/to/write/the/file"
    },
	"parameters": {
        "model": "llama3-8b-8192"
    },
    "secrets": {
        "endpoint": "Endpoint/of/LLM"
		"token": "Token/for/Endpoint"
	}
}
```

### Input

- **`data`** *(str, required)*  
  Path to the csv file.  

### Parameters  

- **`model`** *(str, required)*  
  Specifies the language model to use for processing. At least one model must be provided.  

- **`table_prompt_ids`** *(list, optional, default=None)*  
  List of prompt identifiers associated with table-level descriptions. If not provided, random table-specific prompts are used.  

- **`column_prompt_ids`** *(list, optional, default=None)*  
  List of prompt identifiers associated with column-level descriptions. If not provided, random column-specific prompts are used.  

- **`official_table_description`** *(str, optional, default=None)*  
  A predefined official description of the table. If provided, it is included in the prompt for additional context.  

- **`official_column_descriptions`** *(dict, optional, default=None)*  
  A mapping of column names to their official descriptions. If provided, these descriptions are incorporated into the prompt.  

- **`no_prompts`** *(int, optional, default=3)*  
  Controls the number of prompt variations to use in inference if table_prompt_ids=None or column_prompt_ids=None. If not specified, the default is 3.  
 
## Output

The output of TableSage has the following format:

```json
{
    "message": "Profiler executed successfully!",
	"output": {
		"profile": "path_of_profile_file",
    }
	"metrics": {	
        "time": 1.698,
    },
	"status": "success"
}
```
