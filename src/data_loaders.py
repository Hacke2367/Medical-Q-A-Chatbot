import os
import json
import re
import pandas as pd
import xml.etree.ElementTree as ET


def clean_text(text):

    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def load_medquad_data(data_dir="../data/MedQuAD/"):

    qa_pairs = []
    print(f"DEBUG: Starting load from data_dir: {data_dir}")

    for root, dirs, files in os.walk(data_dir):
        base_name = os.path.basename(root)

        if base_name.startswith(
                ('1_', '2_', '3_', '4_', '5_', '6_', '7_', '8_', '9_', '10_', '11_', '12_')) and base_name.endswith(
                '_QA'):
            print(f"DEBUG:    Matching QA directory found: {base_name}")
            for file_name in files:
                file_path = os.path.join(root, file_name)

                try:
                    if file_name.endswith('.json'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                            for topic in data.get('data', []):
                                for paragraph in topic.get('paragraphs', []):
                                    for qa in paragraph.get('qas', []):
                                        question = qa.get('question')
                                        answers = qa.get('answers', [])
                                        answer_text = " ".join([ans['text'] for ans in answers if 'text' in ans])

                                        if question and answer_text:
                                            qa_pairs.append({
                                                'question': clean_text(question),
                                                'answer': clean_text(answer_text)
                                            })

                    elif file_name.endswith('.xml'):
                        tree = ET.parse(file_path)
                        root_xml = tree.getroot()

                        if root_xml.tag == 'Document':
                            print(f"DEBUG:        Processing 'Document' type XML: {file_name}")
                            qa_pairs_element = root_xml.find('QAPairs')
                            if qa_pairs_element is not None:
                                for qapair_element in qa_pairs_element.findall('QAPair'):
                                    question_element = qapair_element.find('Question')
                                    question = question_element.text if question_element is not None else ""

                                    answer_element = qapair_element.find('Answer')
                                    answer_text = answer_element.text if answer_element is not None else ""

                                    if question and answer_text:
                                        qa_pairs.append({
                                            'question': clean_text(question),
                                            'answer': clean_text(answer_text)
                                        })
                        elif root_xml.tag == 'MedQuAD':
                            print(f"DEBUG:        Processing 'MedQuAD' type XML: {file_name}")
                            for data_element in root_xml.findall('data'):
                                for paragraph_element in data_element.findall('paragraphs'):
                                    for qa_element in paragraph_element.findall('qas'):
                                        question_element = qa_element.find('question')
                                        question = question_element.text if question_element is not None else ""

                                        answers_list = []
                                        answers_element = qa_element.find('answers')
                                        if answers_element is not None:
                                            for answer_elem in answers_element.findall('answer'):
                                                text_elem = answer_elem.find('text')
                                                if text_elem is not None:
                                                    answers_list.append(text_elem.text)

                                        answer_text = " ".join(answers_list)

                                        if question and answer_text:
                                            qa_pairs.append({
                                                'question': clean_text(question),
                                                'answer': clean_text(answer_text)
                                            })
                        else:
                            print(
                                f"DEBUG: Unknown XML root tag '{root_xml.tag}' in file: {file_name}. Skipping.")

                    else:
                        print(f"DEBUG: Skipping unsupported file type: {file_name}")
                        pass

                except ET.ParseError as e:
                    print(f"ERROR: XML parsing failed for {file_name}: {e}")
                except json.JSONDecodeError as e:
                    print(f"ERROR: JSON parsing failed for {file_name}: {e}")
                except Exception as e:
                    print(f"ERROR: General error loading {file_name}: {e}")
                    continue

    print(f"Total {len(qa_pairs)} question-answer pairs loaded.")
    return pd.DataFrame(qa_pairs)


if __name__ == "__main__":
    print("Starting data loading process...")
    df = load_medquad_data(data_dir="../data/MedQuAD/")
    output_file_path_csv = "../data/processed_medquad_qa.csv"

    if not df.empty:
        print("\n--- Sample Loaded Data ---")
        print(df.head())
        print(f"\nShape of DataFrame: {df.shape}")
        df.to_csv(output_file_path_csv, index=False, encoding='utf-8')
    else:
        print("No data loaded. Please check your `data_dir` path and MedQuAD files/structure.")