import csv
import os

scientists = {}   
papers = {}      
name_to_ids = {}  

def load_data(directory):
    """Loads data from CSV files into dictionaries."""
    
    
    with open(os.path.join(directory, "scientists.csv"), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            scientist_id = row["scientist_id"].strip()
            name = row["name"].strip()

            scientists[scientist_id] = {"name": name, "papers": set()}


            if name not in name_to_ids:
                name_to_ids[name] = set()
            name_to_ids[name].add(scientist_id)


    with open(os.path.join(directory, "papers.csv"), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            paper_id = row["paper_id"].strip()
            title = row["title"].strip()
            year = row["year"].strip()

            papers[paper_id] = {"title": title, "year": year, "authors": set()}


    with open(os.path.join(directory, "authors.csv"), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            paper_id = row["paper_id"].strip()
            scientist_id = row["scientist_id"].strip()

            if paper_id in papers:
                papers[paper_id]["authors"].add(scientist_id)

            if scientist_id in scientists:
                scientists[scientist_id]["papers"].add(paper_id)

    print("Data loaded successfully!")
    print(f"Total scientists loaded: {len(scientists)}")
    print(f"Total papers loaded: {len(papers)}")
