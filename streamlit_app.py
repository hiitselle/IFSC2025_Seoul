def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder or reference entry"""
    import re  # Import at the top of the function
    
    name_str = str(name).strip().lower()
    
    # Check for "Athlete X" pattern
    if name_str.startswith('athlete '):
        remaining = name_str[8:].strip()
        if remaining.isdigit():
            return True
    
    placeholder_patterns = [
        r'^n/a$|^na$',                # Not available
        r'^athlete\s+\d+',            # "Athlete 1", "Athlete 23"
        r'^climber\s+\d+',            # "Climber 1", "Climber 23"  
        r'^competitor\s+\d+',         # "Competitor 1"
        r'^\d+',                      # Just numbers
        r'^\d+\.\d+',                 # Decimal numbers
        r'^\d+\+',                    # "25+"
        r'^tbd$|^tba$',               # To be determined/announced
        r'^n\/a$|^na$',               # Not available
        r'^hold\s+\d+',               # "Hold 25"
        r'^zone\s+\d+',               # "Zone 40"
        r'^top\s+\d+',                # "Top 50"
        r'qualification|threshold',    # Reference text
        r'worst|best|average',        # Statistical text
        r'points|score|rank',         # Score-related text
    ]
    
    # Check against patterns
    for pattern in placeholder_patterns:
        if re.match(pattern, name_str):
            return True
    
    # Check for very short names (likely not real names)
    if len(name_str) < 3:
        return True
    
    # Check if name contains no letters (likely not a real name)
    if not any(c.isalpha() for c in name_str):
        return True
    
    return False
