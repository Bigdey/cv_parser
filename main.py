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
    Searches for specified terms in a CV and returns counts of matches in each category.
    """
    match_counts = {category: 0 for category in search_terms}
    with pdfplumber.open(pdf_path) as pdf:
        text = ' '.join(page.extract_text() or '' for page in pdf.pages).lower()
        for category, terms in search_terms.items():
            match_counts[category] = sum(term.lower() in text for term in terms)
    return match_counts


def search_keywords_in_cvs(directory, search_terms):
    """
    Searches for specific terms related to Skills, Languages, and City in all CVs within a directory.
    Calculate scores based on the number of matches and ranks CVs.
    """
    pdf_paths = list_pdf_files(directory)
    results = {}
    for pdf_path in pdf_paths:
        matches = search_in_cv(pdf_path, search_terms)
        # Calculate total score as the sum of all match counts
        total_score = sum(matches.values())
        results[os.path.basename(pdf_path)] = (matches, total_score)

    # Sort results by score in descending order
    sorted_results = sorted(results.items(), key=lambda item: item[1][1], reverse=True)
    return sorted_results


if __name__ == '__main__':
    # Define your search terms for each category
    search_for_skills = ['Python', 'Git', 'Selenium']
    search_for_languages = ['English', 'Romanian']
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

    # Print sorted results with scores
    for filename, (details, score) in results:
        print(f"\n{filename} - Score: {score}")
        for category, count in details.items():
            print(f"  {category}: {count}")
