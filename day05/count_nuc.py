import sys

def merge_counts(main_dict, add_fh):
    """Merge two nucleotide count dictionaries."""
    for key in add_fh:
        main_dict[key] = main_dict.get(key, 0) + add_fh.get(key, 0)
    return main_dict

def open_fh(file_path):
    """Open a file, read its contents, and return the sequence as a string."""
    try:
        with open(file_path, "r") as fh:
            seq = fh.read().strip()
        return seq
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""

def statistic(seq):
    """Count nucleotide occurrences in a sequence and return a dictionary of counts."""
    count_dict = {"A": 0, "T": 0, "G": 0, "C": 0, "Unknown": 0}
    for nuc in seq.upper():
        if nuc in count_dict:
            count_dict[nuc] += 1
        else:
            count_dict["Unknown"] += 1

    # Total nucleotides
    total_nucs = sum(count_dict.values())

    # Display the results for the sequence
    for nuc, count in count_dict.items():
        percentage = (count / total_nucs) * 100 if total_nucs > 0 else 0
        print(f"{nuc}: {count} ({percentage:.2f}%)")
    print(f"Total nucleotides: {total_nucs}\n")

    return count_dict

def main():
    """Main function to process files provided as command-line arguments."""
    # Check if at least one file is provided
    if len(sys.argv) < 2:
        print("Error: At least one file path must be provided as an argument.")
        return

    combined_count = {"A": 0, "T": 0, "G": 0, "C": 0, "Unknown": 0}

    # Process each file provided as an argument
    for file_path in sys.argv[1:]:
        seq = open_fh(file_path)
        if seq:
            file_count = statistic(seq)
            combined_count = merge_counts(combined_count, file_count)

    # Display the combined results if more than one file is processed
    if len(sys.argv[1:]) > 1:
        total_combined = sum(combined_count.values())
        print(f"Combined Results from {len(sys.argv[1:])} files:")
        for nuc, count in combined_count.items():
            percentage = (count / total_combined) * 100 if total_combined > 0 else 0
            print(f"{nuc}: {count} ({percentage:.2f}%)")
        print(f"Total nucleotides: {total_combined}\n")

# Run the program if it is the main execution
if __name__ == "__main__":
    main()



