# Weekly Activity Summary
**Period:** {{ date_from }} to {{ date_to }}
**Generated:** {{ generation_date }}

## Overview
- **Total Conversations:** {{ total_conversations }}
- **Active Days:** {{ active_days }}
- **Total Messages:** {{ total_messages }}
- **Average Messages per Conversation:** {{ avg_messages }}

## Activity Timeline
{{ activity_timeline }}

## Top Files Modified
{% for file in top_files %}
{{ loop.index }}. {{ file.heat_emoji }} **{{ file.path }}**
   - Conversations: {{ file.count }}
   - Interactions: Read {{ file.read }}, Write {{ file.write }}, Edit {{ file.edit }}
{% endfor %}

## Tool Usage
{% for tool in top_tools %}
{{ loop.index }}. **{{ tool.name }}**: {{ tool.count }} uses ({{ tool.percentage }}%)
{% endfor %}

## Topics
{% for topic in top_topics %}
- {{ topic.name }}: {{ topic.count }} mentions
{% endfor %}

## Insights & Recommendations
{{ insights }}
