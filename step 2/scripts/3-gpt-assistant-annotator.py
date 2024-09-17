import pandas as pd
from openai import OpenAI

#client = OpenAI(api_key="")

system_message = '''
                <role>
                You are assigned as a specialist in Atomic Layer Deposition (ALD). Your primary task is to process scientific articles related to ALD, extracting specific scientific information as detailed below.
                </role>

                <task>
                Upon receiving an article, identify and extract data according to a predefined schema. Record values for each property specified in the schema. If a property is not mentioned in the article, denote this with a "-". Additionally, if the article discusses relevant properties that are not included in the schema, extract these as well and list them under an "extra_properties" section as key-value pairs.
                </task>

                <extraction-schema>
                [
                {
                    "process_parameters": {
                    "reactants": [
                        "List of reactants used"
                    ],
                    "temperature_range": "Range of temperatures used for the deposition process",
                    "pressure_range": "Range of pressures used for the deposition process"
                    },
                    "film_properties": {
                    "material": "Chemical composition of the deposited film",
                    "thickness_control": "Methods and results of thickness control",
                    "uniformity": "Uniformity of the film across the substrate",
                    "conformality": "Conformality of the film on 3D structures",
                    "film_thickness": "Thickness of the deposited film",
                    "film_density": "Density of the deposited film",
                    "surface_roughness": "Surface roughness of the deposited film",
                    "refractive_index": "Refractive index of the deposited film"
                    },
                    "process_characteristics": {
                    "self_limiting_behavior": "Evidence of self-limiting behavior in the ALD process",
                    "nucleation_behavior": "Description of nucleation behavior observed",
                    "growth_per_cycle": "Growth per cycle observed in the process"
                    },
                    "safety": "Safety considerations for the process and materials",
                    "stability": "Stability of the deposited films over time",
                    "reproducibility": "Reproducibility of the film thickness and properties",
                    "precursor_consumption": "Efficiency and consumption rate of precursors",
                    "device_performance": "Performance of the ALD films in practical devices",
                    "extra_properties": {
                    "Additional property 1": "Value of additional property 1",
                    "Additional property 2": "Value of additional property 2",
                    "...": "..."
                    },
                    "presence_checks": {
                    "property 1": "Yes if property 1 is investigated, otherwise no",
                    "property 2": "Yes if property 2 is investigated, otherwise no",
                    "...": "..."
                    }
                }
                ]
                </extraction-schema>
                    
                <output-response-format>
                Your responses should be formatted in JSON, strictly adhering to the provided schema. Ensure the formatting and data integrity are maintained as per the guidelines. Use the "-" symbol for any property not mentioned in the article.
                </output-response-format>
        '''

file_path = 'ALD_Data_Ask_Completed.xlsx'
df = pd.read_excel(file_path)
df['gpt_annotation'] = ""
doi_annotation_dict = {}

for index, row in df.iterrows():

    reference_doi = row['reference_doi']
    title = row['title']
    abstract = row['abstract']
    full_text = row['full_text']
    if abstract != "-" and reference_doi not in doi_annotation_dict:

        article_text = f"{full_text}" if full_text != "-" else f"{title}\n{abstract}"
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Extract the information as instructed from this article:\n{article_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            seed=54,
        )

        if completion.choices[0].finish_reason == "stop":
            df.at[index, 'gpt_annotation'] = completion.choices[0].message.content
            doi_annotation_dict[reference_doi] = completion.choices[0].message.content

        else:
            df.at[index, 'gpt_annotation'] = "-"

    elif abstract != "-" and reference_doi in doi_annotation_dict:
        gpt_annotation = doi_annotation_dict[reference_doi]
        df.at[index, 'gpt_annotation'] = gpt_annotation

    else:
        df.at[index, 'gpt_annotation'] = "-"

output_file_path = 'ALD_Data_Ask_GPT_Completed.xlsx'
df.to_excel(output_file_path, index=False)
