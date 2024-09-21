## Extract ALD structured information and upload to the Open Research Knowledge Graph (ORKG) as an AI-ready database

### Background

The advancement of AI-based process development and material synthesis requires databases with extensive training data as input. Building on popular crowd-sourced databases containing ALD and ALE process details as launched by [TU/e](https://www.tue.nl/en/) in 2019 (see here [https://www.atomiclimits.com/alddatabase/](https://www.atomiclimits.com/alddatabase/), DOI: [10.6100/alddatabase](https://doi.org/10.6100/alddatabase)), the goal is to start making these databases AI-ready, while exploring new opportunities for AI-inspired process development, materials design and autonomous experimentation.

### How-to

This repository presents a data science-oriented workflow that utilizes expert-curated knowledge on materials and reactants from the ALD database. It includes an easy-to-reuse 2-step knowledge extraction pipeline that showcases the use of Large Language Models (LLMs)--we demonstrate this w.r.t. OpenAI's GPT models, however the approach easily extends to any LLM--to extract knowledge about over 20 properties related to ALD processes from scientific literature. The extracted knowledge is then integrated into the Open Research Knowledge Graph (ORKG, [https://orkg.org/](https://orkg.org/)) to create an AI-ready database.

The 2 steps of the workflow perform the following:

[step 1](https://github.com/jd-coderepos/awases-ald/tree/main/step%201): Given a collection of all papers in the ALD database, filter to those with full text available, and simply bulk import the papers to the ORKG. Given metadata resolution mechanisms in the ORKG, the metadata for the papers which are bulk imported based on their DOIs is automatically fetched and added from Crossref. Furthermore, in this step, we filter for papers with available full-text since in step 2 for effective knowledge extraction it needs to be run on the full-text where just the title and abstract do not suffice for the knowledge extraction targets.

[step 2](https://github.com/jd-coderepos/awases-ald/tree/main/step%202): This step is about using an LLM to automatically extract knowledge from the full-text of ALD papers given a detailed set of properties defining the knowledge extraction scope. Furthermore, adding the extracted information as contributions to the already added ALD papers in the ORKG is also addressed. 

### Acknowledgements

This repo is a demonstration toward the project titled "Turning Online ALD and ALE Databases Into AI-Ready Tools for Development of New Sustainable Materials and Fabrication Processes" [1] with collaborating organizations [TU/e](https://www.tue.nl/en/), [L3S](https://www.l3s.de/), and [Warwick](https://warwick.ac.uk/). We acknowledge project funding by [MercK](https://www.merckgroup.com/en) and [Intel](https://www.intel.de/content/www/de/de/homepage.html) coopertations along the funding line "AI-Aware Pathways to Sustainable Semiconductor Process and Manufacturing Technologies (AWASES)" [2].

### References and News

1. Mackus, A., Macco, B., Karasulu, B., D’Souza, J., Auer, S. & Kessels, E. Turning Online ALD and ALE Databases Into AI-Ready Tools for Development of New Sustainable Materials and Fabrication Processes. Poster at AVS 24th Int. Conf. on Atomic Layer Deposition (ALD 2024) https://ald2024.avs.org/wp-content/uploads/2024/04/Abstract-Book.pdf 
2. https://www.chemanager-online.com/en/news/german-merck-and-intel-ai-research-project
