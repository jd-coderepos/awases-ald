## Add Contributions to Papers

In Step 1, we imported a collection of papers from the [Atomic Limits ALD Database](https://www.atomiclimits.com/alddatabase/) to the ORKG with their metadata. Step 2 involves bulk uploading structured contributions to each paper. This process leverages an LLM to automatically extract knowledge and employs various modules of the [ORKG Python Package](https://orkg.readthedocs.io/en/latest/index.html) to programmatically upload the structured data, aligning it with the [Comprehensive ALD Profile](https://orkg.org/template/R733029) ORKG semantic template.

This repository is structured similarly to Step 1.

### Overview

This step focuses on extracting detailed ALD process knowledge from the full texts of the imported papers and integrating this information into the ORKG. This creates a rich, structured database that enhances the utility of the ORKG for academic and industrial research.

### Workflow

**Step 2: Adding Contributions to ORKG Papers**

### Main Processing Steps

1. **Extract ALD Structured Knowledge with a GPT LLM**
   [`scripts/3-gpt-assistant-annotate.py`](https://github.com/jd-coderepos/awases-ald/blob/main/step%202/scripts/3-gpt-assistant-annotate.py) - This script processes an input file of papers, extracting ALD process information. The knowledge extraction schema defines the detailed properties of interest, and the output is formatted in JSON.

   **Usage Example:**
   ```bash
   python scripts/3-gpt-assistant-annotate.py
   # Prompts for multiple inputs and the final output file to store extracted knowledge. Examples are provided in the data repository.
   # API key, paths for materials, reactants, papers, raw data, and a record file path for logging processed papers are required to avoid redundancy in querying.
   # Output: Path to the output file where extracted knowledge is stored (e.g., 'data/6-gpt-annotations.csv').
	```



### Main Processing Steps

1. **Extract ALD Structured Knowledge w/ a GPT LLM**
   [`scripts/3-gpt-assistant-annotate.py`](https://github.com/jd-coderepos/awases-ald/blob/main/step%202/scripts/3-gpt-assistant-annotate.py) - This script reads an input file of relevant papers from which ALD process information should be extracted. For each set of the expert-annotated material and reactants in the ALD database, the script prompts a GPT assistant which task instructions and the knowledge extraction schema defining the detailed extraction properties of interestabout ALD processes specifying JSON as the response format which it then stores in an output file.

   **Usage Example:**
   ```bash
   python scripts/3-gpt-assistant-annotate.py
   # User is prompted for several inputs and the final output file to store the extracted knowledge. Examples are provided in the data repository for reproducibility.
   # The user is first prompted for their OpenAI API key. api_key = getpass.getpass('Enter your OpenAI API key: ')
   # materials_path = input("Enter the file path for materials CSV (e.g., data/5-orkg-added-materials.csv): ")
   # reactants_path = input("Enter the file path for reactants CSV (e.g., data/5-orkg-added-reactants.csv): ")
   # papers_path = input("Enter the file path for papers CSV (e.g., data/4-orkg-papers-info.csv): ")
   # raw_data_path = input("Enter the file path for raw data CSV (e.g., step 1/data/2-filtered-data.csv): ")
   # The user is also prompted for a log txt file that registers each paper entry after a successful query to GPT. This file is used in case the script halts for some reason in the middle. On a new run, this file is then read and the already processed data rows for which structured data was already produced are skipped. This tries to balance the cost of the experiment by ensuring that the GPT model is not queried multiple times for the same data point. record_file_path = input("Enter the record file path (e.g., data/6-gpt-annotated-records.txt): ")
   # output_file_path = input("Enter the output file path (e.g., data/6-gpt-annotations.csv): ") where the extracted knowledge should be stored.
	```

2. **Upload Extracted Structured Knowledge as ALD Paper Contributions to ORKG**
   [`scripts/4-create-and-upload-orkg-contributions.py`](https://github.com/jd-coderepos/awases-ald/blob/main/step%202/scripts/4-create-and-upload-orkg-contributions.py) - This script reads the extracted data from the file produced in the previous step, then defines an import workflow using the functions defined in the [ORKG Templates component](https://orkg.readthedocs.io/en/latest/client/templates.html) which mainly involves instantiating the ALD process profile ORKG template (https://orkg.org/template/R733029) with the extracted structured information according to a schema matching the template, and finally adding each structured information unit as contributions to the pertinent paper on the ORKG. Note, a paper describing ALD processes for different combinations of materials and reactants can have multiple contributions with the structured descriptions for each unique material and reactants combination. 

   ```bash
   python scripts/3-gpt-assistant-annotate.py
   # User is prompted for several inputs and the final output file to store the extracted knowledge. Examples are provided in the data repository for reproducibility.
   # orkg_host = input("Enter ORKG host URL (e.g., https://incubating.orkg.org/): ")
   # orkg_email = input("Enter your ORKG email: ")
   # orkg_password = getpass.getpass("Enter your ORKG password: ")  # Secure password input
   # template_resource_id = input("Enter the resource ID of the template to materialize (e.g., R733029 for Comprehensive ALD Profile): ")
   # csv_file_path = input("Enter the path to your CSV file (e.g., data/6-gpt-annotations.csv): ")  # this is file output in the previous step with the extracted knowlege
   # output_file_path = input("Enter the path for the output CSV file (e.g., data/7-recorded-orkg-contributions.csv): ")  # this file keeps a log of all added contributions to the ORKG
   # reactant_mapping_path = input("Enter the path to the reactant mapping CSV file (e.g., data/5-orkg-added-reactants.csv): ")
   # material_mapping_path = input("Enter the path to the material mapping CSV file (e.g., data/5-orkg-added-materials.csv): ")
	```   

### Supplementary Processing Steps

1. [`scripts/1-create-paper-info-file-from-orkg.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/scripts/1-create-paper-info-file-from-orkg.py): This script downloads the ORKG paper resource IDs and the paper title metadata. The paper resource IDs are recorded for convenience for any future scripts trying to programmatically add contributions to the papers. The connecting key between the original raw data (e.g., step 1/data/2-filtered-data.csv) and the added ORKG papers is the paper doi. The output of this script is the file [4-orkg-papers-info.csv](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/data/4-orkg-papers-info.csv).

2. [`scripts/2-add-material-and-reactants-to-orkg.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/scripts/2-add-material-and-reactants-to-orkg.py): This script reads the expert-curated material and reactants annotations in the [atomiclimits ALD database](https://www.atomiclimits.com/alddatabase/) (e.g., step 1/data/2-filtered-data.csv) and creates unique resources in the ORKG for them. The output of this script are the files [5-orkg-added-reactants.csv](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/data/5-orkg-added-reactants.csv) and [5-orkg-added-materials.csv](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/data/5-orkg-added-materials.csv).



**Note:** For those new to importing data into the ORKG, we recommend starting with our test environments at https://incubating.orkg.org/ or https://sandbox.orkg.org/. Feel free to conduct extensive tests here. Use the live system at https://orkg.org/ only for finalized workflows. For experimentation and troubleshooting, please stick to our test systems.