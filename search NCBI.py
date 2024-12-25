import argparse
import csv
import os
from Bio import Entrez
from datetime import datetime

def fetch_data(term, db="nucleotide", number=10):
    """Fetch data from the NCBI database."""
    Entrez.email = "your.email@example.com"  # Replace with your email

    # Search the database
    print(f"Searching for '{term}' in the '{db}' database...")
    handle = Entrez.esearch(db=db, term=term, retmax=number)
    search_results = Entrez.read(handle)
    handle.close()

    ids = search_results["IdList"]
    total_found = search_results["Count"]
    print(f"Found {total_found} items. Downloading up to {number}...")

    filenames = []
    for i, uid in enumerate(ids):
        # Fetch each record
        fetch_handle = Entrez.efetch(db=db, id=uid, rettype="gb", retmode="text")
        data = fetch_handle.read()
        fetch_handle.close()

        # Save to a file
        filename = f"{term}_{i+1}.gb"
        with open(filename, "w") as file:
            file.write(data)
        filenames.append(filename)
        print(f"Saved: {filename}")

    return filenames, total_found

def save_metadata(term, db, number, total_found, filenames, metadata_file="metadata.csv"):
    """Save metadata about the query to a CSV file."""
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the file exists to write the header only once
    write_header = not os.path.exists(metadata_file)

    with open(metadata_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["Date", "Database", "Search Term", "Number Requested", "Total Found", "Files"])
        writer.writerow([date, db, term, number, total_found, ";".join(filenames)])

    print(f"Metadata saved to {metadata_file}")

def main():
    parser = argparse.ArgumentParser(description="Download data from NCBI and save metadata.")
    parser.add_argument("term", help="Search term for the NCBI database.")
    parser.add_argument("db", default="nucleotide", help="NCBI database to search (default: nucleotide).")
    parser.add_argument("number", type=int, default=10, help="Number of items to download (default: 10).")
    parser.add_argument("-o", default="metadata.csv", help="Output CSV file for metadata (default: metadata.csv).")

    args = parser.parse_args()

    filenames, total_found = fetch_data(args.term, db=args.db, number=args.number)
    save_metadata(args.term, args.db, args.number, total_found, filenames, metadata_file=args.o)

if __name__ == "__main__":
    main()