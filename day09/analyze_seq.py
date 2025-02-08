import re
import argparse
from collections import defaultdict

def read_file(file_path):
    """Reads a Fasta or GeneBank file and extracts the sequence."""
    sequence = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if not line.startswith('>') and not line.startswith('//'):
                    sequence.append(line.strip())
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        exit(1)
    return ''.join(sequence)

def find_longest_repeated_subsequence(sequence):
    """Finds the longest subsequence that repeats itself in the given sequence."""
    n = len(sequence)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    result = ""

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if sequence[i - 1] == sequence[j - 1] and i != j:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > len(result):
                    result = sequence[i - dp[i][j]:i]
            else:
                dp[i][j] = 0

    return result

def calculate_gc_content(sequence):
    """Calculates the GC content of the sequence."""
    gc_count = sequence.count('G') + sequence.count('C')
    total_count = len(sequence)
    return (gc_count / total_count) * 100 if total_count > 0 else 0

def main():
    parser = argparse.ArgumentParser(description="Analyze genetic sequences.")
    parser.add_argument("file", help="Path to the Fasta or GeneBank file.")
    parser.add_argument("--duplicate", action="store_true", help="Find the longest repeated subsequence.")
    parser.add_argument("--gc_content", action="store_true", help="Calculate the GC content.")

    args = parser.parse_args()

    sequence = read_file(args.file)

    if args.duplicate:
        longest_repeated = find_longest_repeated_subsequence(sequence)
        if longest_repeated:
            print(f"Longest repeated subsequence: {longest_repeated}")
        else:
            print("No repeated subsequences found.")

    if args.gc_content:
        gc_content = calculate_gc_content(sequence)
        print(f"GC content: {gc_content:.2f}%")

if __name__ == "__main__":
    main()
