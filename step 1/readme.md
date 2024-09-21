## Bulk Import Papers and their Metadata

This repository contains [scripts](https://github.com/jd-coderepos/awases-ald-data/tree/main/step%201/scripts) and [data](https://github.com/jd-coderepos/awases-ald-data/tree/main/step%201/data) for bulk adding papers to the Open Research Knowledge Graph (ORKG) using the [ORKG's CSV import feature](https://orkg.org/csv-import).

### Overview

The main purpose of this repository is to streamline the addition of academic papers to the ORKG by DOI, utilizing the ORKG's CSV import functionality. This process enables the bulk addition of papers and the automatic retrieval of their associated metadata.

### Workflow

**Step 1: Adding Papers to the ORKG**

Using the ORKG CSV import feature, this process manages the bulk addition of papers and facilitates the acquisition of metadata. It is supported by scripts designed to filter and prepare the data necessary for import.

### Processing Steps

1. **Filter Papers**  
   [`scripts/1-filter-papers.py`](https://github.com/jd-coderepos/awases-ald/blob/main/step%201/scripts/1-filter-papers.py) - This script filters a raw data file to retain only those ALD papers that include a full-text column. The output is a streamlined list ready for further processing.

   **Usage Example:**
   ```bash
   python scripts/1-filter-papers.py
   # User is prompted to enter the input and output files. Examples are provided in the data repository for reproducibility.
   # Input: Path to your raw data file listing ALD papers with DOIs, e.g., 'data/1-raw-data.csv'
   # Output: Path to your output file for storing filtered ALD papers that have full text, e.g., 'data/2-filtered-data.csv'
	```

2. **Create ORKG CSV Import File**  
   [`scripts/2-create-orkg-csv-import-file.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%201/scripts/2-create-orkg-csv-import-file.py) - This script converts the filtered paper's data from the previous step into a format suitable for the ORKG import. It also checks and removes any duplicate papers.

   **Usage Example:**
   ```bash
   python scripts/2-create-orkg-csv-import-file.py
   # User is prompted to enter the input and output files. Examples are provided in the data repository for reproducibility.
   # Input: Path to the output file from the previous step, e.g., 'data/2-filtered-data.csv'
   # Output: Path to your output file for storing the formatted and deduplicated fiel for ORKG csv import, e.g., 'data/3-orkg-csv-papers-import.csv'
	```