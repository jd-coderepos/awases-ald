## Add contributions to the paper

In step 1, given the collection of papers as [raw data](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%201/data/1-raw-data.csv) from the [atomic limits ALD database](https://www.atomiclimits.com/alddatabase/), we addressed importing it to the ORKG with the metadata. In this step, we address bulk uploading structured contributions data to each paper.

This repository is structured in the same way as step 1.

### Step 2: Adding Contributions to ORKG Papers

### Processing Steps
1. [`scripts/1-create-paper-info-file-from-orkg.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/scripts/1-create-paper-info-file-from-orkg.py): This script downloads the ORKG paper resource IDs and the paper title metadata. The paper resource IDs are recorded for convenience for any future scripts trying to programmatically add contributions to the papers. The connecting key between the original raw data and the added ORKG papers is the paper doi. The output of this script is the file [4-orkg-papers-info.csv](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/data/4-orkg-papers-info.csv).
2. [`scripts/2-add-reactants-to-orkg.py`](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/scripts/2-add-reactants-to-orkg.py): This script reads the original raw data and creates unique resources in the ORKG for community-curated materials and reactants reported in [atomiclimits ALD database](https://www.atomiclimits.com/alddatabase/). The output of this script is the file [5-orkg-added-reactants.csv](https://github.com/jd-coderepos/awases-ald-data/blob/main/step%202/data/5-orkg-added-reactants.csv).
3. [`scripts/3-get-reactant-specific-structured`]