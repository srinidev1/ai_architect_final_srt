def general_agent(state):
    return {
        "messages": [
            {
                "role": "assistant",
                "content": """
                    I can currently help with:
                    1. Annual report filings and tax calculations for Delaware companies
                    2. Disaster event information
                    3. Weather information
                    Please ask a question related to one of these topics!"""
            }
        ]
    }