#!/usr/bin/env python3
"""
Insight Generator for Claude Code Insights

Analyzes conversation patterns and generates insight reports with
visualizations, metrics, and actionable recommendations.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import click

try:
    from jinja2 import Template, Environment, FileSystemLoader
except ImportError:
    print("Error: jinja2 not installed. Run: pip install jinja2")
    exit(1)


class PatternDetector:
    """Detects patterns in conversation data"""

    def __init__(self, db_path: Path, verbose: bool = False):
        self.db_path = db_path
        self.verbose = verbose
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row

    def _log(self, message: str):
        """Log if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def get_date_range_filter(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> Tuple[str, List]:
        """Build date range SQL filter"""
        conditions = []
        params = []

        if date_from:
            conditions.append("timestamp >= ?")
            params.append(date_from)
        if date_to:
            conditions.append("timestamp <= ?")
            params.append(date_to)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        return where_clause, params

    def get_overview_metrics(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> Dict[str, Any]:
        """Get high-level overview metrics"""
        where_clause, params = self.get_date_range_filter(date_from, date_to)

        cursor = self.conn.execute(f"""
            SELECT
                COUNT(*) as total_conversations,
                SUM(message_count) as total_messages,
                SUM(user_messages) as total_user_messages,
                SUM(assistant_messages) as total_assistant_messages,
                AVG(message_count) as avg_messages_per_conversation,
                MIN(timestamp) as earliest_conversation,
                MAX(timestamp) as latest_conversation,
                COUNT(DISTINCT DATE(timestamp)) as active_days
            FROM conversations
            WHERE {where_clause}
        """, params)

        row = cursor.fetchone()

        return {
            'total_conversations': row['total_conversations'] or 0,
            'total_messages': row['total_messages'] or 0,
            'total_user_messages': row['total_user_messages'] or 0,
            'total_assistant_messages': row['total_assistant_messages'] or 0,
            'avg_messages_per_conversation': round(row['avg_messages_per_conversation'] or 0, 1),
            'earliest_conversation': row['earliest_conversation'],
            'latest_conversation': row['latest_conversation'],
            'active_days': row['active_days'] or 0
        }

    def get_file_hotspots(self, date_from: Optional[str] = None, date_to: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get most frequently modified files"""
        where_clause, params = self.get_date_range_filter(date_from, date_to)

        cursor = self.conn.execute(f"""
            SELECT
                fi.file_path,
                COUNT(DISTINCT fi.conversation_id) as conversation_count,
                SUM(CASE WHEN fi.interaction_type = 'read' THEN 1 ELSE 0 END) as read_count,
                SUM(CASE WHEN fi.interaction_type = 'write' THEN 1 ELSE 0 END) as write_count,
                SUM(CASE WHEN fi.interaction_type = 'edit' THEN 1 ELSE 0 END) as edit_count
            FROM file_interactions fi
            JOIN conversations c ON fi.conversation_id = c.id
            WHERE {where_clause}
            GROUP BY fi.file_path
            ORDER BY conversation_count DESC
            LIMIT ?
        """, params + [limit])

        return [
            {
                'file_path': row['file_path'],
                'conversation_count': row['conversation_count'],
                'read_count': row['read_count'],
                'write_count': row['write_count'],
                'edit_count': row['edit_count'],
                'total_interactions': row['read_count'] + row['write_count'] + row['edit_count']
            }
            for row in cursor.fetchall()
        ]

    def get_tool_usage(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tool usage statistics"""
        where_clause, params = self.get_date_range_filter(date_from, date_to)

        cursor = self.conn.execute(f"""
            SELECT
                tu.tool_name,
                COUNT(DISTINCT tu.conversation_id) as conversation_count,
                SUM(tu.usage_count) as total_uses
            FROM tool_usage tu
            JOIN conversations c ON tu.conversation_id = c.id
            WHERE {where_clause}
            GROUP BY tu.tool_name
            ORDER BY total_uses DESC
        """, params)

        return [
            {
                'tool_name': row['tool_name'],
                'conversation_count': row['conversation_count'],
                'total_uses': row['total_uses']
            }
            for row in cursor.fetchall()
        ]

    def get_topic_clusters(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get most common topics"""
        where_clause, params = self.get_date_range_filter(date_from, date_to)

        cursor = self.conn.execute(f"""
            SELECT topics FROM conversations
            WHERE {where_clause} AND topics IS NOT NULL
        """, params)

        topic_counter = Counter()
        for row in cursor.fetchall():
            topics = json.loads(row['topics'])
            topic_counter.update(topics)

        return [
            {'topic': topic, 'count': count}
            for topic, count in topic_counter.most_common(20)
        ]

    def get_activity_timeline(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> Dict[str, int]:
        """Get conversation count by date"""
        where_clause, params = self.get_date_range_filter(date_from, date_to)

        cursor = self.conn.execute(f"""
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM conversations
            WHERE {where_clause}
            GROUP BY DATE(timestamp)
            ORDER BY date
        """, params)

        return {row['date']: row['count'] for row in cursor.fetchall()}

    def get_hourly_distribution(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> Dict[int, int]:
        """Get conversation distribution by hour of day"""
        where_clause, params = self.get_date_range_filter(date_from, date_to)

        cursor = self.conn.execute(f"""
            SELECT
                CAST(strftime('%H', timestamp) AS INTEGER) as hour,
                COUNT(*) as count
            FROM conversations
            WHERE {where_clause}
            GROUP BY hour
            ORDER BY hour
        """, params)

        return {row['hour']: row['count'] for row in cursor.fetchall()}

    def get_weekday_distribution(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> Dict[str, int]:
        """Get conversation distribution by day of week"""
        where_clause, params = self.get_date_range_filter(date_from, date_to)

        cursor = self.conn.execute(f"""
            SELECT
                CASE CAST(strftime('%w', timestamp) AS INTEGER)
                    WHEN 0 THEN 'Sunday'
                    WHEN 1 THEN 'Monday'
                    WHEN 2 THEN 'Tuesday'
                    WHEN 3 THEN 'Wednesday'
                    WHEN 4 THEN 'Thursday'
                    WHEN 5 THEN 'Friday'
                    WHEN 6 THEN 'Saturday'
                END as weekday,
                COUNT(*) as count
            FROM conversations
            WHERE {where_clause}
            GROUP BY weekday
        """, params)

        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        result = {day: 0 for day in weekday_order}
        for row in cursor.fetchall():
            result[row['weekday']] = row['count']

        return result

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class InsightGenerator:
    """Generates insight reports from pattern data"""

    def __init__(self, db_path: Path, templates_dir: Path, verbose: bool = False):
        self.db_path = db_path
        self.templates_dir = templates_dir
        self.verbose = verbose
        self.detector = PatternDetector(db_path, verbose=verbose)

        # Setup Jinja2 environment
        if templates_dir.exists():
            self.jinja_env = Environment(loader=FileSystemLoader(str(templates_dir)))
        else:
            self.jinja_env = None

    def _log(self, message: str):
        """Log if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def _create_ascii_bar_chart(self, data: Dict[str, int], max_width: int = 50) -> str:
        """Create ASCII bar chart"""
        if not data:
            return "No data"

        max_value = max(data.values())
        lines = []

        for label, value in data.items():
            bar_length = int((value / max_value) * max_width) if max_value > 0 else 0
            bar = "█" * bar_length
            lines.append(f"{label:15} {bar} {value}")

        return "\n".join(lines)

    def _create_sparkline(self, values: List[int]) -> str:
        """Create sparkline chart"""
        if not values:
            return ""

        chars = "▁▂▃▄▅▆▇█"
        min_val = min(values)
        max_val = max(values)

        if max_val == min_val:
            return chars[0] * len(values)

        normalized = [(v - min_val) / (max_val - min_val) for v in values]
        return "".join(chars[int(n * (len(chars) - 1))] for n in normalized)

    def generate_weekly_report(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> str:
        """Generate weekly activity report"""
        self._log("Generating weekly report...")

        # Auto-calculate date range if not provided
        if not date_from:
            date_from = (datetime.now() - timedelta(days=7)).date().isoformat()
        if not date_to:
            date_to = datetime.now().date().isoformat()

        # Gather data
        overview = self.detector.get_overview_metrics(date_from, date_to)
        file_hotspots = self.detector.get_file_hotspots(date_from, date_to, limit=10)
        tool_usage = self.detector.get_tool_usage(date_from, date_to)
        topics = self.detector.get_topic_clusters(date_from, date_to)
        timeline = self.detector.get_activity_timeline(date_from, date_to)
        weekday_dist = self.detector.get_weekday_distribution(date_from, date_to)

        # Build report
        report_lines = [
            f"# Weekly Insights Report",
            f"**Period:** {date_from} to {date_to}",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Overview",
            f"- **Total Conversations:** {overview['total_conversations']}",
            f"- **Active Days:** {overview['active_days']}",
            f"- **Total Messages:** {overview['total_messages']}",
            f"- **Avg Messages/Conversation:** {overview['avg_messages_per_conversation']}",
            "",
            "## Activity Timeline",
            "```",
            self._create_ascii_bar_chart(timeline, max_width=40),
            "```",
            "",
            "## Weekday Distribution",
            "```",
            self._create_ascii_bar_chart(weekday_dist, max_width=40),
            "```",
            ""
        ]

        if file_hotspots:
            report_lines.extend([
                "## File Hotspots (Top 10)",
                ""
            ])
            for i, file in enumerate(file_hotspots, 1):
                heat = "🔥" * min(3, (file['conversation_count'] + 2) // 3)
                report_lines.append(
                    f"{i}. {heat} **{file['file_path']}** "
                    f"({file['conversation_count']} conversations, "
                    f"R:{file['read_count']} W:{file['write_count']} E:{file['edit_count']})"
                )
            report_lines.append("")

        if tool_usage:
            report_lines.extend([
                "## Tool Usage",
                ""
            ])
            tool_dict = {t['tool_name']: t['total_uses'] for t in tool_usage[:10]}
            report_lines.append("```")
            report_lines.append(self._create_ascii_bar_chart(tool_dict, max_width=40))
            report_lines.append("```")
            report_lines.append("")

        if topics:
            report_lines.extend([
                "## Top Topics",
                ""
            ])
            topic_dict = {t['topic']: t['count'] for t in topics[:15]}
            report_lines.append("```")
            report_lines.append(self._create_ascii_bar_chart(topic_dict, max_width=40))
            report_lines.append("```")
            report_lines.append("")

        # Insights and recommendations
        report_lines.extend([
            "## Insights & Recommendations",
            ""
        ])

        # File hotspot insights
        if file_hotspots and file_hotspots[0]['conversation_count'] >= 5:
            top_file = file_hotspots[0]
            report_lines.append(
                f"- 🔥 **High Activity File:** `{top_file['file_path']}` was modified in "
                f"{top_file['conversation_count']} conversations. Consider reviewing for refactoring opportunities."
            )

        # Topic insights
        if topics and topics[0]['count'] >= 3:
            top_topic = topics[0]
            report_lines.append(
                f"- 📌 **Trending Topic:** '{top_topic['topic']}' appeared in {top_topic['count']} conversations. "
                f"This might warrant documentation or team knowledge sharing."
            )

        # Activity pattern insights
        if overview['active_days'] < 3:
            report_lines.append(
                f"- 📅 **Low Activity:** Only {overview['active_days']} active days this week. "
                f"Consider scheduling regular development sessions."
            )

        if not report_lines[-1]:  # If no insights were added
            report_lines.append("- No significant patterns detected this period.")

        return "\n".join(report_lines)

    def generate_file_heatmap_report(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> str:
        """Generate detailed file interaction heatmap"""
        self._log("Generating file heatmap report...")

        file_hotspots = self.detector.get_file_hotspots(date_from, date_to, limit=50)

        report_lines = [
            "# File Interaction Heatmap",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## File Hotspots",
            ""
        ]

        if not file_hotspots:
            report_lines.append("No file interactions found in the specified period.")
            return "\n".join(report_lines)

        for i, file in enumerate(file_hotspots, 1):
            heat_level = min(5, (file['conversation_count'] + 1) // 2)
            heat_emoji = "🔥" * heat_level

            report_lines.extend([
                f"### {i}. {heat_emoji} {file['file_path']}",
                f"- **Conversations:** {file['conversation_count']}",
                f"- **Reads:** {file['read_count']}",
                f"- **Writes:** {file['write_count']}",
                f"- **Edits:** {file['edit_count']}",
                f"- **Total Interactions:** {file['total_interactions']}",
                ""
            ])

        return "\n".join(report_lines)

    def generate_tool_usage_report(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> str:
        """Generate tool usage analytics report"""
        self._log("Generating tool usage report...")

        tool_usage = self.detector.get_tool_usage(date_from, date_to)

        report_lines = [
            "# Tool Usage Analytics",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Tool Statistics",
            ""
        ]

        if not tool_usage:
            report_lines.append("No tool usage data found.")
            return "\n".join(report_lines)

        total_uses = sum(t['total_uses'] for t in tool_usage)

        for i, tool in enumerate(tool_usage, 1):
            percentage = (tool['total_uses'] / total_uses * 100) if total_uses > 0 else 0
            report_lines.extend([
                f"### {i}. {tool['tool_name']}",
                f"- **Total Uses:** {tool['total_uses']}",
                f"- **Used in Conversations:** {tool['conversation_count']}",
                f"- **Percentage of Total:** {percentage:.1f}%",
                ""
            ])

        return "\n".join(report_lines)

    def close(self):
        """Close connections"""
        self.detector.close()


@click.command()
@click.argument('report_type', type=click.Choice(['weekly', 'file-heatmap', 'tool-usage', 'custom']))
@click.option('--db-path', type=click.Path(), default='.claude/skills/cc-insights/.processed/conversations.db',
              help='SQLite database path')
@click.option('--templates-dir', type=click.Path(), default='.claude/skills/cc-insights/templates',
              help='Templates directory')
@click.option('--date-from', type=str, help='Start date (ISO format)')
@click.option('--date-to', type=str, help='End date (ISO format)')
@click.option('--output', type=click.Path(), help='Save to file (default: stdout)')
@click.option('--verbose', is_flag=True, help='Show detailed logs')
def main(report_type: str, db_path: str, templates_dir: str, date_from: Optional[str],
         date_to: Optional[str], output: Optional[str], verbose: bool):
    """Generate insight reports from conversation data

    Report types:
      weekly        - Weekly activity summary with metrics
      file-heatmap  - File modification heatmap
      tool-usage    - Tool usage analytics
      custom        - Custom report from template
    """
    db_path = Path(db_path)
    templates_dir = Path(templates_dir)

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        exit(1)

    generator = InsightGenerator(db_path, templates_dir, verbose=verbose)

    try:
        # Generate report based on type
        if report_type == 'weekly':
            report = generator.generate_weekly_report(date_from, date_to)
        elif report_type == 'file-heatmap':
            report = generator.generate_file_heatmap_report(date_from, date_to)
        elif report_type == 'tool-usage':
            report = generator.generate_tool_usage_report(date_from, date_to)
        else:
            print("Custom templates not yet implemented")
            exit(1)

        # Output report
        if output:
            Path(output).write_text(report)
            print(f"✓ Report saved to {output}")
        else:
            print(report)

    finally:
        generator.close()


if __name__ == '__main__':
    main()
