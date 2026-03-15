import argparse
import csv
import gzip
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

def calculate_metrics(input_fastq, output_csv):
    """
    Calculate GC content, read length, and mean quality score for each read in a FASTQ file.
    """
    # Open gzipped or plain text FASTQ
    open_func = gzip.open if input_fastq.endswith(".gz") else open
    
    with open_func(input_fastq, "rt") as handle:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Read_ID', 'Length', 'GC_Content', 'Mean_Quality']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for record in SeqIO.parse(handle, "fastq"):
                read_id = record.id
                length = len(record.seq)
                
                # GC content in percentage
                gc = gc_fraction(record.seq) * 100
                
                # Quality scores calculation
                quals = record.letter_annotations["phred_quality"]
                mean_quality = sum(quals) / length if length > 0 else 0

                writer.writerow({
                    'Read_ID': read_id,
                    'Length': length,
                    'GC_Content': f"{gc:.2f}",
                    'Mean_Quality': f"{mean_quality:.2f}"
                })

def main():
    parser = argparse.ArgumentParser(description="Calculate key metrics from a FASTQ file for individual reads.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTQ file (can be gzipped)")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file")
    args = parser.parse_args()

    calculate_metrics(args.input, args.output)

if __name__ == "__main__":
    main()
