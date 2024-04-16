from cv_search_utils import *
from pathlib import Path


# Define the directory where the CV PDF files are stored
directory_path = Path('cvs')


# Define the criteria for the search. These lists can be customized to search for specific skills,
# languages, and locations mentioned within the CVs. An empty list in languages or location would
# normally mean "match all", but this behavior should be implemented in the `cv_search_utils` module.

search_for_skills = ['python']
search_for_languages = ['English']
search_for_location = ['Cluj-Nonpoca']

if __name__ == '__main__':

    sorted_results = search_keywords_in_cvs(directory_path, search_for_skills, search_for_languages, search_for_location)

    for filename, (details, score) in sorted_results:
        print(f"\n{filename} - Total Score: {score}")
        for category, matches in details.items():
            print(f"  {category}: {', '.join(matches) if matches else 'No value'}")
