## Extract ALD Structured Information and Upload to the Open Research Knowledge Graph (ORKG) as an AI-ready Database

### Overview

This repository develops AI-ready databases by extracting and integrating knowledge from ALD (Atomic Layer Deposition) process details. We build on existing crowdsourced databases, such as the one launched by [TU/e](https://www.tue.nl/en/) in 2019 ([TU/e Atomic Limits ALD Database](https://www.atomiclimits.com/alddatabase/), DOI: [10.6100/alddatabase](https://doi.org/10.6100/alddatabase)). Our goal is to make these databases ready for AI applications, fostering innovations in materials design, autonomous experimentation, and AI-driven process development.

### Workflow

The workflow consists of two primary steps, each designed to handle specific aspects of data integration and knowledge extraction:

* **[Step 1: Bulk Import and Metadata Resolution](https://github.com/jd-coderepos/awases-ald/tree/main/step%201)**  
  > Import the collection of papers from the ALD database with available full text. Metadata from these papers is automatically fetched and added via Crossref mechanisms within the ORKG.

* **[Step 2: Knowledge Extraction and Integration](https://github.com/jd-coderepos/awases-ald/tree/main/step%202)**  
  > Use OpenAI's GPT models (adaptable to other LLMs) to extract detailed properties related to ALD processes from the full texts. The extracted data is then structured and added to the ALD papers already present in the ORKG ([ORKG](https://orkg.org/)).

### Objectives

This approach not only standardizes data but also enhances the accessibility of AI technologies for analyzing and developing new sustainable materials and fabrication processes.

### Acknowledgements

We acknowledge the collaboration and support of:

* [TU/e](https://www.tue.nl/en/)
* [L3S Research Center](https://www.l3s.de/)
* [University of Warwick](https://warwick.ac.uk/)
* Funding from [MercK](https://www.merckgroup.com/en) and [Intel](https://www.intel.de/content/www/de/de/homepage.html) through the "AI-Aware Pathways to Sustainable Semiconductor Process and Manufacturing Technologies (AWASES)" project.

### References and Further Reading

1. Mackus, A., Macco, B., Karasulu, B., D’Souza, J., Auer, S. & Kessels, E. Turning Online ALD and ALE Databases Into AI-Ready Tools for Development of New Sustainable Materials and Fabrication Processes. Poster presented at AVS 24th Int. Conf. on Atomic Layer Deposition (ALD 2024). [View Poster](https://ald2024.avs.org/wp-content/uploads/2024/04/Abstract-Book.pdf) 
2. [News Article: German MercK and Intel AI Research Project](https://www.chemanager-online.com/en/news/german-merck-and-intel-ai-research-project)
