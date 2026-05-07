def build_prompt(property_type, location, price, features, target_buyer):
    return f"""
You are a professional real estate marketing copywriter specializing in the Nigerian property market.

A property agent has provided the following details:
- Property Type: {property_type}
- Location: {location}
- Price: {price}
- Key Features: {features}
- Target Buyer: {target_buyer}

Generate the following marketing content:

1. **LISTING DESCRIPTION** (150 words, professional and compelling)
2. **INSTAGRAM CAPTION** (engaging, with emojis and relevant hashtags)
3. **VIDEO SCRIPT** (30-second property tour reel script)

Format your response clearly with each section labeled exactly as shown above.
"""