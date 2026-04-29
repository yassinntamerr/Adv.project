import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

class RecognitionAnalyzer:
    """Analyze face recognition logs"""
    
    def __init__(self, log_file="recognition_log.json"):
        self.log_file = Path(log_file)
        self.data = []
        self.load_logs()
    
    def load_logs(self):
        """Load recognition logs from JSON file"""
        if not self.log_file.exists():
            print(f"❌ Log file not found: {self.log_file}")
            return
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    self.data.append(entry)
                except json.JSONDecodeError:
                    continue
        
        print(f"✅ Loaded {len(self.data)} recognition events")
    
    def get_statistics(self):
        """Get overall statistics"""
        if not self.data:
            print("No data to analyze")
            return {}
        
        df = pd.DataFrame(self.data)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        stats = {
            'total_recognitions': len(df),
            'unique_students': df['student_id'].nunique(),
            'date_range': {
                'start': df['timestamp'].min().isoformat(),
                'end': df['timestamp'].max().isoformat()
            },
            'average_confidence': df['confidence'].mean(),
            'min_confidence': df['confidence'].min(),
            'max_confidence': df['confidence'].max()
        }
        
        return stats
    
    def get_student_stats(self):
        """Get per-student statistics"""
        if not self.data:
            return {}
        
        df = pd.DataFrame(self.data)
        
        student_stats = defaultdict(lambda: {
            'name': '',
            'count': 0,
            'avg_confidence': 0,
            'min_confidence': 1.0,
            'max_confidence': 0,
            'first_seen': None,
            'last_seen': None
        })
        
        for _, row in df.iterrows():
            sid = row['student_id']
            student_stats[sid]['name'] = row['student_name']
            student_stats[sid]['count'] += 1
            student_stats[sid]['avg_confidence'] += row['confidence']
            student_stats[sid]['min_confidence'] = min(student_stats[sid]['min_confidence'], row['confidence'])
            student_stats[sid]['max_confidence'] = max(student_stats[sid]['max_confidence'], row['confidence'])
            
            ts = pd.to_datetime(row['timestamp'])
            if student_stats[sid]['first_seen'] is None:
                student_stats[sid]['first_seen'] = ts
            student_stats[sid]['last_seen'] = ts
        
        # Calculate averages
        for sid in student_stats:
            if student_stats[sid]['count'] > 0:
                student_stats[sid]['avg_confidence'] /= student_stats[sid]['count']
        
        return dict(student_stats)
    
    def print_summary(self):
        """Print summary statistics"""
        stats = self.get_statistics()
        
        if not stats:
            return
        
        print("\n" + "=" * 70)
        print("📊 RECOGNITION SESSION SUMMARY")
        print("=" * 70)
        
        print(f"\n📈 Overall Statistics:")
        print(f"   Total Recognitions: {stats['total_recognitions']}")
        print(f"   Unique Students: {stats['unique_students']}")
        print(f"   Date Range: {stats['date_range']['start']} to {stats['date_range']['end']}")
        print(f"\n🎯 Confidence Scores:")
        print(f"   Average: {stats['average_confidence']:.2%}")
        print(f"   Minimum: {stats['min_confidence']:.2%}")
        print(f"   Maximum: {stats['max_confidence']:.2%}")
        
        # Student statistics
        student_stats = self.get_student_stats()
        
        print(f"\n👥 Top 10 Recognized Students:")
        print(f"{'Name':<30} {'Count':<10} {'Avg Confidence':<15}")
        print("-" * 70)
        
        sorted_students = sorted(
            student_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        for sid, info in sorted_students[:10]:
            print(f"{info['name'][:28]:<30} {info['count']:<10} {info['avg_confidence']:.2%:<15}")
        
        print("\n" + "=" * 70)
    
    def export_to_csv(self, output_file="recognition_report.csv"):
        """Export statistics to CSV"""
        student_stats = self.get_student_stats()
        
        rows = []
        for sid, info in student_stats.items():
            rows.append({
                'Student ID': sid,
                'Student Name': info['name'],
                'Recognition Count': info['count'],
                'Average Confidence': f"{info['avg_confidence']:.2%}",
                'Min Confidence': f"{info['min_confidence']:.2%}",
                'Max Confidence': f"{info['max_confidence']:.2%}",
                'First Seen': info['first_seen'].isoformat() if info['first_seen'] else 'N/A',
                'Last Seen': info['last_seen'].isoformat() if info['last_seen'] else 'N/A'
            })
        
        df = pd.DataFrame(rows)
        df = df.sort_values('Recognition Count', ascending=False)
        df.to_csv(output_file, index=False)
        print(f"✅ Report exported to {output_file}")
        return df
    
    def plot_statistics(self):
        """Create visualization of statistics"""
        student_stats = self.get_student_stats()
        
        if not student_stats:
            print("No data to plot")
            return
        
        # Top 15 students by recognition count
        sorted_students = sorted(
            student_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:15]
        
        names = [info['name'][:20] for _, info in sorted_students]
        counts = [info['count'] for _, info in sorted_students]
        confidences = [info['avg_confidence'] for _, info in sorted_students]
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart of recognition counts
        axes[0].barh(names, counts, color='steelblue')
        axes[0].set_xlabel('Recognition Count')
        axes[0].set_title('Top 15 Students by Recognition Count')
        axes[0].grid(axis='x', alpha=0.3)
        
        # Scatter plot of counts vs confidence
        axes[1].scatter(counts, confidences, s=100, alpha=0.6, color='darkgreen')
        for i, name in enumerate(names):
            axes[1].annotate(name, (counts[i], confidences[i]), fontsize=8, alpha=0.7)
        axes[1].set_xlabel('Recognition Count')
        axes[1].set_ylabel('Average Confidence')
        axes[1].set_title('Recognition Count vs Average Confidence')
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('recognition_analysis.png', dpi=150, bbox_inches='tight')
        print("✅ Visualization saved to recognition_analysis.png")
        plt.show()
    
    def get_hourly_statistics(self):
        """Get recognition statistics by hour"""
        if not self.data:
            return {}
        
        df = pd.DataFrame(self.data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.floor('H')
        
        hourly_stats = df.groupby('hour').size()
        
        return hourly_stats.to_dict()


def main():
    """Main analysis function"""
    import sys
    
    # Check if log file exists
    log_file = "recognition_log.json"
    if not Path(log_file).exists():
        print(f"❌ No recognition log found: {log_file}")
        print("   Run main.py first to create the log.")
        sys.exit(1)
    
    # Analyze
    analyzer = RecognitionAnalyzer(log_file)
    
    # Print summary
    analyzer.print_summary()
    
    # Export to CSV
    analyzer.export_to_csv()
    
    # Show visualization
    try:
        analyzer.plot_statistics()
    except Exception as e:
        print(f"⚠️ Could not create visualization: {e}")


if __name__ == "__main__":
    main()
