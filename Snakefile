configfile: "config.yaml"

rule all:
    input:
        "results/nanoplot_out/NanoPlot-report.html",
        "results/metrics_summary.csv",
        "results/visuals_plots.png",
        "results/visuals_summary_statistics.txt"

rule run_nanoplot:
    input:
        config["fastq_file"]
    output:
        "results/nanoplot_out/NanoPlot-report.html"
    log:
        "logs/nanoplot.log"
    shell:
        """
        NanoPlot --fastq {input} -o results/nanoplot_out/ 2> {log}
        """

rule calculate_metrics:
    input:
        fastq=config["fastq_file"]
    output:
        csv="results/metrics_summary.csv"
    log:
        "logs/calculate_metrics.log"
    shell:
        """
        python scripts/calculate_metrics.py -i {input.fastq} -o {output.csv} 2> {log}
        """

rule visualize_metrics:
    input:
        csv="results/metrics_summary.csv"
    output:
        plots="results/visuals_plots.png",
        stats="results/visuals_summary_statistics.txt"
    log:
        "logs/visualize_metrics.log"
    shell:
        """
        python scripts/visualize_metrics.py -i {input.csv} -o results/visuals 2> {log}
        """
