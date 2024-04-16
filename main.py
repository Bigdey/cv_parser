import pdfplumber
import os
import re
from pathlib import Path


def load_pdf_files(directory):
    """
    Load all PDF files in a specified directory.
    """
    if not os.path.exists(directory):
        raise ValueError(f"The specified path {directory} does not exist.")
    if not os.path.isdir(directory):
        raise ValueError(f"The specified path {directory} is not a directory.")

    pdf_files = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path) and full_path.endswith('.pdf'):
            pdf_files.append(full_path)
    return pdf_files


def find_terms_in_text(text, terms):
    """
    Finds terms in the provided text and returns a list of matched terms.
    """
    matched_terms = []
    text = text.lower()
    for term in terms:
        if term.lower() in text:
            matched_terms.append(term)
    return matched_terms


def search_in_cv(pdf_path, skills, languages, location):
    """
    Searches skills, languages, and locations within a CV.
    Only includes results if skills are found.
    """
    results = {'Skills': [], 'Languages': [], 'City': []}
    with pdfplumber.open(pdf_path) as pdf:
        text = ' '.join(page.extract_text() or '' for page in pdf.pages)

        results['Skills'] = find_terms_in_text(text, skills)
        results['Languages'] = find_terms_in_text(text, languages)
        results['City'] = find_terms_in_text(text, location)

    # Only return results if skills were found
    if not results['Skills'] or not results['Languages'] or not results['City']:
        return None, 0  # No skills found, so return None and score of 0

    # Calculate score based on the number of matches in each category
    score = len(results['Skills']) + len(results['Languages']) + len(results['City'])
    return results, score


def search_keywords_in_cvs(directory, skills, languages, location):
    """
    Searches for specific terms related to Skills, Languages, and City in all CVs within a directory.
    Sort results based on scores, excluding candidates without any skills found.
    """
    pdf_paths = load_pdf_files(directory)
    results = {}
    for pdf_path in pdf_paths:
        cv_matches, cv_score = search_in_cv(pdf_path, skills, languages, location)
        if cv_matches:  # Check if there are any skills found
            results[os.path.basename(pdf_path)] = (cv_matches, cv_score)

    # Sort results by score in descending order
    sorted_results = sorted(results.items(), key=lambda item: item[1][1], reverse=True)
    return sorted_results


if __name__ == '__main__':
    search_for_skills = ['python']
    search_for_languages = ['English']
    search_for_location = ['Cluj-Nonpoca']

    directory_path = Path('cvs')
    sorted_results = search_keywords_in_cvs(directory_path, search_for_skills, search_for_languages, search_for_location)

    for filename, (details, score) in sorted_results:
        print(f"\n{filename} - Total Score: {score}")
        for category, matches in details.items():
            print(f"  {category}: {', '.join(matches) if matches else 'No value'}")
