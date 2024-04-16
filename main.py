import pdfplumber
import os
from pathlib import Path


def list_pdf_files(directory):
    """
    Lists all PDF files in a specified directory.
    """
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.pdf')]


def search_in_cv(pdf_path, search_terms):
    """
    Searches for specified terms in a CV and returns the terms matched in each category.
    """
    matches = {category: [] for category in search_terms}
    with pdfplumber.open(pdf_path) as pdf:
        text = ' '.join(page.extract_text() or '' for page in pdf.pages).lower()
        for category, terms in search_terms.items():
            matches[category] = [term for term in terms if term.lower() in text]
    return matches


def search_keywords_in_cvs(directory, search_terms):
    """
    Searches for specific terms related to Skills, Languages, and City in all CVs within a directory.
    Returns CVs with the terms that were matched.
    """
    pdf_paths = list_pdf_files(directory)
    results = {}
    for pdf_path in pdf_paths:
        matches = search_in_cv(pdf_path, search_terms)
        # Check if there are any matches in any category
        if any(matches.values()):
            results[os.path.basename(pdf_path)] = matches
    return results


if __name__ == '__main__':
    # Define your search terms for each category
    search_for_skills = ['Python', 'Git', 'Selenium']
    search_for_languages = ['English', 'German']
    search_for_location = ['Cluj']

    # Combine into a dictionary
    search_terms = {
        'Skills': search_for_skills,
        'Languages': search_for_languages,
        'City': search_for_location
    }

    # Example directory to scan
    directory_path = Path('cvs')

    # Execute the search
    results = search_keywords_in_cvs(directory_path, search_terms)

    # Print results with detailed matches
    for filename, details in results.items():
        print(f"{filename}:")
        for category, matches in details.items():
            if matches:
                print(f"  {category}: {', '.join(matches)}")
            else:
                print(f"  {category}: No matches found")
        print()  # Extra newline for better separation
