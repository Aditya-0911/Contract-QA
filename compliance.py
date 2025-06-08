import google.generativeai as genai

def check_compliance(text: str) -> str:
    """Check compliance of the contract."""
    prompt = f"""
    You are a specialized legal compliance analyst. Review the following contract and provide a structured analysis using this format:

    CLASSIFICATION

    Contract Type:
    Jurisdiction:
    Key Parties:

    COMPLIANCE STATUS [GREEN/YELLOW/RED]

    Overall Rating:
    Rationale:

    CRITICAL ISSUES
    List top 3 compliance risks, ordered by severity:

    Risk 1:
    Risk 2:
    Risk 3:

    REQUIRED ACTIONS
    List immediate steps needed:
    [Action]
    [Action]
    [Action]
    
    SUMMARY
    2-3 sentences highlighting key compliance concerns and recommendations.

    Rules:
    - Focus only on material compliance issues
    - Prioritize regulatory and legal risks
    - Be direct and specific
    - Flag any time-sensitive requirements
    - Highlight missing critical clauses
    - Do not use any special characters like curly quotes, bullet points, or other non-ASCII characters.
    - Stick to plain text and ASCII characters only.

    Contract text:
    {text}
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()


def check_compliance_HTML(text: str) -> str:
    """Check compliance of the contract and generate only the HTML code with proper table borders and left-aligned text."""
    prompt = f"""
    
    You are a professional HTML and CSS developer. Please convert the given contract text into a fully structured and well-organized HTML file, following these requirements:
    
    ### Requirements:
    
        - Include proper HTML5 structure (doctype, head, body, etc.)
        - Use clear and appropriate section headers (e.g., <h1>, <h2>, <h3>)
        - Format text into paragraphs (<p>) and lists (<ul>/<ol>) where applicable
        - Use tables (<table>) to organize any data, deadlines, or key points
        - Ensure **all tables have borders** and are properly styled with borders around each cell using `border-collapse: collapse;` and `border: 1px solid black;`
        - All text must be **left-aligned** and **properly indented**
        - Use inline CSS to ensure text alignment is left and maintain table styling with borders and padding
        - Add a section to track compliance with contractual deadlines in a timeline format
        - Ensure the HTML is properly indented, well-formed, and includes basic inline CSS for styling such as padding, margins, borders, and text alignment
        - The page size is A4

    ### Instructions:
    
        - Generate **only** the HTML output, do not include any extra explanations or comments
        - Ensure complete and correct HTML structure, starting from '<!DOCTYPE html>' and ending with '</html>'
        - Apply CSS styles directly in the HTML
        - Use Times New Roman as Font

    Contract text:
    {text}
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()