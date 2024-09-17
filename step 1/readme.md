## Bulk Import Papers and their Metadata

This repository contains [scripts](https://github.com/jd-coderepos/awases-ald-data/tree/main/step%201/scripts) and [data](https://github.com/jd-coderepos/awases-ald-data/tree/main/step%201/data) used to bulk add papers to the ORKG using the [CSV import feature](https://orkg.org/csv-import).

### Step 1: Adding Papers to the ORKG
We add papers to the ORKG by DOI, leveraging the ORKG CSV import functionality to bulk add papers and automatically [fetch their metadata](https://gitlab.com/TIBHannover/orkg/orkg-frontend/-/blob/fd41ed6c867f0b521f6204ddaabf391cf687e649/src/components/ConfirmBulkImport/useImportBulkData.js).

### Processing Steps
1. [`scripts/1-filter-papers.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%201/scripts/1-filter-papers.py): This script takes our raw data file as input and processes it to produce an output file where each row includes the full-text column value.
2. [`scripts/2-create-orkg-csv-import-file.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%201/scripts/2-create-orkg-csv-import-file.py): This script takes the output file from the previous step and converts it into a format suitable for import into the ORKG. It also removes any duplicate papers if found.
