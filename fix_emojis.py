import re

# Read the test runner file
with open('tests/test_runner.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace emojis with plain text
replacements = {
    '🎯': 'TARGET',
    '🧪': 'TESTS',
    '❌': 'FAILED',
    '⏭️': 'SKIPPED',
    '🔧': 'TOOLS',
    '🎨': 'FEATURES',
    '📋': 'SUITE',
    '✅': 'PASS',
    '🚨': 'ISSUES',
    '💡': 'RECOMMENDATIONS',
    '🏆': 'EXCELLENT',
    '👍': 'GOOD',
    '⚠️': 'ACCEPTABLE',
    '🚫': 'POOR',
    '🎯': 'NEXT',
    '⏱️': 'TIME',
    '📄': 'REPORT'
}

for emoji, text in replacements.items():
    content = content.replace(emoji, text)

# Write back the file
with open('tests/test_runner.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Emojis replaced successfully!")