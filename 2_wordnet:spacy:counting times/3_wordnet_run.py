import csv
from nltk.corpus import wordnet as wn

def get_hyponyms(synset):
    hyponyms = set()
    for hyponym in synset.hyponyms():
        hyponyms.add(hyponym)
        hyponyms.update(get_hyponyms(hyponym))
    return hyponyms

def extract_people_related_terms():
    human_synsets = wn.synsets('human', pos=wn.NOUN)
    person_synsets = wn.synsets('person', pos=wn.NOUN)
    people_synsets = wn.synsets('people', pos=wn.NOUN)
    social_group_synsets = wn.synsets('social_group', pos=wn.NOUN)

    all_synsets = human_synsets + person_synsets + people_synsets + social_group_synsets

    all_hyponyms = set()
    for synset in all_synsets:
        all_hyponyms.update(get_hyponyms(synset))

    terms = set()
    for hyponym in all_hyponyms:
        for lemma in hyponym.lemmas():
            terms.add(lemma.name().replace('_', ' '))

    return terms

def write_to_csv(terms, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Term"])  # Write the header
        for term in sorted(terms):
            writer.writerow([term])

if __name__ == "__main__":
    people_related_terms = extract_people_related_terms()
    print(f"Identified {len(people_related_terms)} people-related terms.")
    for term in sorted(people_related_terms):
        print(term)
    
    # Write the terms to a CSV file
    csv_filename = "people_related_terms_aug_5_2024.csv"
    write_to_csv(people_related_terms, csv_filename)
    print(f"Terms have been written to {csv_filename}")