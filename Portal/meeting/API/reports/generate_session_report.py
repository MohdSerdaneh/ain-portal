import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import os

class SessionReport:
    """
    Generates a full session report from interaction logs:
    - Loads and cleans log data
    - Charts emotion over time
    - Computes engagement metrics
    - Exports a visual PDF report with timeline + sentence summary
    """

    def __init__(self, log_file="interaction_log.csv", output_dir="reports/result"):
        self.log_file = log_file
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
        self.df = self._load_data()
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def _load_data(self):
        """
        Loads interaction CSV into a DataFrame and parses timestamps.
        """
        cols = ["Timestamp", "Gesture", "Emotion", "Sentence", "Confidence", "Feedback"]
        df = pd.read_csv(self.log_file, names=cols)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
        return df

    def generate_timeline_chart(self, output_path):
        """
        Generates a time-series chart of emotion vs. timestamp.
        Annotates sentences on the chart.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.df["Timestamp"], self.df["Emotion"], marker="o", linestyle="-", label="Emotion")
        for i, row in self.df.iterrows():
            if pd.notnull(row["Sentence"]) and str(row["Sentence"]).strip().endswith("."):
                plt.text(row["Timestamp"], row["Emotion"], row["Sentence"], fontsize=8, rotation=45)
        plt.title("Emotion Timeline")
        plt.xlabel("Time")
        plt.ylabel("Detected Emotion")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def calculate_engagement(self):
        """
        Calculates user engagement as a % of 'active' frames (hands/emotion detected).
        """
        total_rows = len(self.df)
        active_rows = self.df[(self.df["Gesture"] != "None") | (self.df["Emotion"] != "No face")]
        percent = (len(active_rows) / total_rows) * 100 if total_rows else 0
        return round(percent, 2)

    def summarize(self):
        """
        Extracts key session stats into a dictionary.
        """
        summary = {
            "Total Sentences": self.df["Sentence"].str.endswith(".").sum(),
            "Average Confidence": round(self.df["Confidence"].mean(), 2),
            "Engagement %": self.calculate_engagement(),
            "Mismatches": self.df["Feedback"].astype(str).str.contains("Mismatch").sum()
        }
        return summary

    def export_pdf(self):
        """
        Generates a full PDF report with:
        - Summary metrics
        - Emotion timeline chart
        - Last 5 completed sentences
        """
        chart_path = os.path.join(self.output_dir, f"timeline_{self.timestamp}.png")
        self.generate_timeline_chart(chart_path)
        summary = self.summarize()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "ASL + Emotion Session Report", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Date: {self.timestamp}", ln=True)
        pdf.ln(5)

        # Write summary stats
        for key, value in summary.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)

        # Add timeline chart
        pdf.ln(10)
        pdf.cell(0, 10, "Emotion Timeline:", ln=True)
        pdf.image(chart_path, w=180)
        pdf.ln(10)

        # Add recent sentence logs
        pdf.cell(0, 10, "Recent Sentences:", ln=True)
        recent = self.df[self.df["Sentence"].str.endswith(".")].tail(5)
        for _, row in recent.iterrows():
            pdf.multi_cell(0, 10, f"[{row['Timestamp'].strftime('%H:%M:%S')}] {row['Sentence']} ({row['Emotion']}, {row['Feedback']})")

        output_pdf = os.path.join(self.output_dir, f"SessionReport_{self.timestamp}.pdf")
        pdf.output(output_pdf)
        print(f"[✅] PDF report saved to: {output_pdf}")


# Optional standalone usage
if __name__ == "__main__":
    report = SessionReport()
    report.export_pdf()
