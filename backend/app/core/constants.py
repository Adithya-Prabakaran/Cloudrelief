"""Shared constants used across the severity pipeline and classifier stub."""

# Labels the mock/real classifier can return.
CLASSIFIER_LABELS = ["flood", "fire", "structural_damage", "normal"]

# Labels that count toward the classifier component of the severity score.
SEVERITY_RELEVANT_LABELS = ["flood", "fire", "structural_damage"]

# Keywords that bump the keyword component of the severity score when present
# (case-insensitive) in a citizen's incident description.
URGENT_KEYWORDS = [
    "trapped",
    "fire",
    "flooding",
    "collapsed",
    "urgent",
    "help",
    "injured",
    "drowning",
]

# Mock rescue teams offered in the admin assignment dropdown.
MOCK_TEAMS = [
    "Alpha Rescue Squad",
    "Bravo Fire & Flood Unit",
    "Charlie Medical Response",
    "Delta Structural Team",
    "Echo Water Rescue",
]
