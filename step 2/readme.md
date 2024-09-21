## Add Contributions to Papers

In Step 1, we imported a collection of papers from the [Atomic Limits ALD Database](https://www.atomiclimits.com/alddatabase/) to the ORKG with their metadata. Step 2 involves bulk uploading structured contributions to each paper. This process leverages an LLM to automatically extract knowledge and employs various modules of the [ORKG Python Package](https://orkg.readthedocs.io/en/latest/index.html) to programmatically upload the structured data, aligning it with the [Comprehensive ALD Profile](https://orkg.org/template/R733029) ORKG semantic template.

This repository is structured similarly to Step 1.

### Overview

The main purpose of this repository is to streamline the process on extracting detailed ALD process knowledge from the full texts of the imported papers and integrating this information into the ORKG. This creates a rich, structured database that enhances the utility of the ORKG for academic and industrial research.

### Workflow

**Step 2: Adding Contributions to ORKG Papers**

Using a GPT LLM, the process extracts ALD-process-relevant structured knowledge from papers. The extraction targets are specified in a [preidentified schema](https://github.com/jd-coderepos/awases-ald/blob/main/step%202/data/ald-schema_ver4.json). Finally, using the ORKG python package all the structured knowledge are added as contributions to the respective ORKG papers. 

### Main Processing Steps

1. **Extract ALD Structured Knowledge with a GPT LLM**   
   [`scripts/3-gpt-assistant-annotate.py`](https://github.com/jd-coderepos/awases-ald/blob/main/step%202/scripts/3-gpt-assistant-annotate.py) - This script processes an input file of papers, extracting ALD process information. The knowledge extraction schema defines the detailed properties of interest, and the output is formatted in JSON.

   **Usage Example:**
   ```bash
   python scripts/3-gpt-assistant-annotate.py
   # User is prompted for several inputs and the final output file to store the extracted knowledge. Examples are provided in the data repository for reproducibility.
   # Input1: Enter your OpenAI API key
   # Input2: Enter the file path for materials CSV (e.g., data/5-orkg-added-materials.csv)
   # Input3: Enter the file path for reactants CSV (e.g., data/5-orkg-added-reactants.csv)
   # Input4: Enter the file path for papers CSV (e.g., data/4-orkg-papers-info.csv)
   # Input5: Enter the file path for raw data CSV (e.g., step 1/data/2-filtered-data.csv)
   # Ouput1: The user is also prompted for a log txt file that registers each paper entry after a successful query to GPT. This file is used in case the script halts for some reason in the middle. On a new run, this file is then read and the already processed data rows for which structured data was already produced are skipped. This tries to balance the cost of the experiment by ensuring that the GPT model is not queried multiple times for the same data point. record_file_path = input("Enter the record file path (e.g., data/6-gpt-annotated-records.txt): ")
   # Output2: Enter the output file path (e.g., data/6-gpt-annotations.csv) # where the extracted knowledge should be stored.
	```

2. **Upload Extracted Structured Knowledge as ALD Paper Contributions to ORKG**   
   [`scripts/4-create-and-upload-orkg-contributions.py`](https://github.com/jd-coderepos/awases-ald/blob/main/step%202/scripts/4-create-and-upload-orkg-contributions.py) - This script takes the extracted data from the previous step and defines an import workflow using the [ORKG Templates component](https://orkg.readthedocs.io/en/latest/client/templates.html). It primarily involves instantiating the ALD process profile ORKG template ([https://orkg.org/template/R733029](https://orkg.org/template/R733029)) with the extracted structured information according to a schema matching the template. Each structured information unit is then added as contributions to the relevant paper on the ORKG. Notably, a paper describing ALD processes for different combinations of materials and reactants can have multiple contributions, with structured descriptions for each unique material and reactant combination.

   **Usage Example:**
   ```bash
   python scripts/4-create-and-upload-orkg-contributions.py
   # User is prompted for several inputs and the final output file to store the extracted knowledge. Examples are provided in the data repository for reproducibility.
   # Input1: Enter ORKG host URL (e.g., https://incubating.orkg.org/)
   # Input2: Enter your ORKG email
   # Input3: getpass.getpass("Enter your ORKG password: ")  # Secure password input
   # Input4: Enter the resource ID of the template to materialize (e.g., R733029 for Comprehensive ALD Profile)
   # Input5: Enter the path to your CSV file (e.g., data/6-gpt-annotations.csv)   # this is file output in the previous step with the extracted knowlege
   # Output1: Enter the path for the output CSV file (e.g., data/7-recorded-orkg-contributions.csv)  # this file keeps a log of all added contributions to the ORKG
   # Input6: Enter the path to the reactant mapping CSV file (e.g., data/5-orkg-added-reactants.csv)
   # Input7: Enter the path to the material mapping CSV file (e.g., data/5-orkg-added-materials.csv)
	``` 

### Supplementary Processing Steps

1. **Create Paper Info File from ORKG**    
   [`scripts/1-create-paper-info-file-from-orkg.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/scripts/1-create-paper-info-file-from-orkg.py) - Downloads ORKG paper resource IDs and paper title metadata, linking them to the original raw data.

2. **Add Material and Reactants as ORKG Resources**     
   [`scripts/2-add-material-and-reactants-to-orkg.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/scripts/2-add-material-and-reactants-to-orkg.py) - This script reads the expert-curated material and reactants annotations in the [atomiclimits ALD database](https://www.atomiclimits.com/alddatabase/) (e.g., step 1/data/2-filtered-data.csv) and creates unique resources in the ORKG for them. The output of this script are the files [5-orkg-added-reactants.csv](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/data/5-orkg-added-reactants.csv) and [5-orkg-added-materials.csv](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/data/5-orkg-added-materials.csv).


## Outcomes and Impact

This section showcases the tangible results and the accessible format of the contributions that have been uploaded to the ORKG, highlighting the real-world applications and benefits of this workflow.

### Featured ORKG Papers and Comparisons

1. **Sample ORKG Paper**    
   View an example of an imported ORKG paper, titled "Atomic Layer Deposition of CsI and CsPbI3", which includes structured ALD process descriptions. This paper features contributions addressing the materials CsI and CsPbI3, enriching the repository with detailed, actionable data:
   - CsI Contribution: [https://orkg.org/paper/R732976/R739356](https://orkg.org/paper/R732976/R739356)
   - CsPbI3 Contribution: [https://orkg.org/paper/R732976/R739360](https://orkg.org/paper/R732976/R739360)

2. **ORKG Comparison Overview**     
   Explore a comparative overview of 167 contributions on ALD processes. This comparison provides a structured summary, facilitating a quick review of research findings and methodologies. The contributions in the comparison are a subsample of the data imported in step 2 elicited in the main processing steps.
   - View Comparison: [https://orkg.org/comparison/R739481](https://orkg.org/comparison/R739481)

### Utilizing Structured Contributions

After the structured data are imported, users can navigate through the ORKG platform to access papers or comparisons, providing a structured overview of research on ALD processes. Specifically the relevant papers can be found in our AWASES project observatory linked [here](https://orkg.org/observatory/AIAware_Pathways_to_Sustainable_Semiconductor_Process_and_Manufacturing_Technologies). This integration supports enhanced discovery and research analytics capabilities, promoting a deeper understanding and further research in ALD technology.


**Note:** For those new to importing data into the ORKG, we recommend starting with our test environments at https://incubating.orkg.org/ or https://sandbox.orkg.org/. Conduct extensive tests in these environments before using the live system at https://orkg.org/ for finalized workflows. For experimentation and troubleshooting, please use our test systems.
