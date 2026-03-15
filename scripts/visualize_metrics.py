import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(input_csv, output_prefix):
    # Read the data
    df = pd.read_csv(input_csv)

    # Calculate summary statistics
    stats = df[['Length', 'GC_Content', 'Mean_Quality']].describe().loc[['mean', '50%', 'min', 'max']]
    stats.rename(index={'50%': 'median'}, inplace=True)
    
    with open(f"{output_prefix}_summary_statistics.txt", "w") as f:
        f.write("Summary Statistics for Quality Metrics:\n\n")
        f.write(stats.to_string())
        f.write("\n")
        
    print("Summary Statistics:\n", stats)

    # Set up the matplotlib figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Long-read Sequencing Quality Distributions', fontsize=16)

    # 1. GC Content Distribution
    sns.histplot(df['GC_Content'], bins=50, kde=True, ax=axes[0], color='skyblue')
    axes[0].set_title('GC Content Distribution')
    axes[0].set_xlabel('GC Content (%)')
    axes[0].set_ylabel('Frequency')

    # 2. Read Length Distribution
    sns.histplot(df['Length'], bins=50, kde=True, ax=axes[1], color='salmon')
    axes[1].set_title('Read Length Distribution')
    axes[1].set_xlabel('Read Length (bp)')
    axes[1].set_ylabel('Frequency')

    # 3. Mean Read Quality Scores
    sns.histplot(df['Mean_Quality'], bins=50, kde=True, ax=axes[2], color='lightgreen')
    axes[2].set_title('Mean Quality Score Distribution')
    axes[2].set_xlabel('Mean Quality Score (PHRED)')
    axes[2].set_ylabel('Frequency')

    # Adjust layout and save
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f"{output_prefix}_plots.png", dpi=300)
    print(f"Plots saved to {output_prefix}_plots.png")

def main():
    parser = argparse.ArgumentParser(description="Visualize distributions of FASTQ QC metrics.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file from calculate_metrics.py")
    parser.add_argument("-o", "--output_prefix", required=True, help="Prefix for output files (e.g. output directory/prefix)")
    args = parser.parse_args()

    # Apply seaborn style
    sns.set_theme(style="whitegrid")
    
    create_visualizations(args.input, args.output_prefix)

if __name__ == "__main__":
    main()
