## Bulk Import Papers and their Metadata

This repository contains [scripts](https://github.com/jd-coderepos/awases-ald-data/tree/main/step%201/scripts) and [data](https://github.com/jd-coderepos/awases-ald-data/tree/main/step%201/data) used to bulk add papers to the Open Research Knowledge Graph (ORKG) using the [CSV import feature](https://orkg.org/csv-import).

### Overview

The primary function of this repository is to facilitate the addition of academic papers to the ORKG by DOI, leveraging the ORKG's CSV import functionality. This allows for the bulk addition of papers along with the automatic fetching of their metadata.

### Workflow

**Step 1: Adding Papers to the ORKG**

Papers are added to the ORKG database by DOI, making use of the ORKG CSV import capability to manage bulk additions and metadata acquisition. This process is supported by scripts that filter and prepare data for import.

### Processing Steps

1. **Filter Papers**  
   [`scripts/1-filter-papers.py`](https://github.com/jd-coderepos/awases-ald/blob/main/step%201/scripts/1-filter-papers.py) - This script processes a raw data file containing a list of ALD papers to produce an output file containing only the ALD paper rows that have a full-text column value.

   **Usage Example:**
   ```bash
   python scripts/1-filter-papers.py
   # User is prompted to enter the input and output files. Examples are provided in the [data repo](https://github.com/jd-coderepos/awases-ald/blob/main/step%201/data/) for reproducibility.
   # Input: [data/1-raw-data.csv](https://github.com/jd-coderepos/awases-ald/blob/main/step%201/data/1-raw-data.csv)
   # Output: [data/2-filtered-data.csv](https://github.com/jd-coderepos/awases-ald/blob/main/step%201/data/2-filtered-data.csv)
	```

2. [`scripts/2-create-orkg-csv-import-file.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%201/scripts/2-create-orkg-csv-import-file.py): This script takes the output file from the previous step and converts it into a format suitable for import into the ORKG. It also removes any duplicate papers if found.

``
Usage example

python scripts/2-create-orkg-csv-import-file.py

The user is prompted to enter the input and output files.

Input: [data/2-filtered-data.csv](https://github.com/jd-coderepos/awases-ald/blob/main/step%201/data/2-filtered-data.csv)
Output: [data/3-orkg-csv-papers-import.csv](https://github.com/jd-coderepos/awases-ald/blob/main/step%201/data/3-orkg-csv-papers-import.csv)
``