import re


def format_response(raw_response: str) -> str:
    """
    Format the raw AI response for better presentation.
    Converts markdown-style formatting to cleaner, more readable text.
    
    Args:
        raw_response (str): Raw response from the AI model
        
    Returns:
        str: Formatted response with proper structure
    """
    if not raw_response:
        return raw_response
    
    # Clean up excessive markdown bold
    formatted = raw_response.replace('**', '')
    
    # Add proper spacing around sections
    formatted = re.sub(r'(Education:|Skills:|Experience:|Projects:|Summary:)', r'\n\n\1', formatted)
    
    # Clean up bullet points - ensure consistent formatting
    formatted = re.sub(r'\*\s+', '• ', formatted)
    
    # Add spacing after colons for better readability
    formatted = re.sub(r':(\w)', r': \1', formatted)
    
    # Remove excessive newlines (more than 2)
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)
    
    # Clean up any leading/trailing whitespace
    formatted = formatted.strip()
    
    return formatted


def format_as_html(raw_response: str) -> str:
    """
    Format the response as HTML for web display with proper styling.
    
    Args:
        raw_response (str): Raw response from AI
        
    Returns:
        str: HTML formatted response
    """
    if not raw_response:
        return raw_response
    
    html = raw_response
    
    # Convert markdown bold to HTML
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # Convert section headers
    html = re.sub(r'^(Education:|Skills:|Experience:|Projects:|Summary:)', 
                  r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Convert bullet points to HTML list items
    lines = html.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('*') or stripped.startswith('•'):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            item_text = re.sub(r'^[\*•]\s*', '', stripped)
            formatted_lines.append(f'  <li>{item_text}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            if stripped:
                formatted_lines.append(f'<p>{stripped}</p>')
    
    if in_list:
        formatted_lines.append('</ul>')
    
    return '\n'.join(formatted_lines)


def format_as_structured_text(raw_response: str) -> str:
    """
    Format response as clean structured text with clear sections.
    Best for terminal/console display.
    
    Args:
        raw_response (str): Raw AI response
        
    Returns:
        str: Clean structured text
    """
    if not raw_response:
        return raw_response
    
    # Remove all markdown formatting
    text = raw_response.replace('**', '')
    
    # Split into lines for processing
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            continue
        
        # Section headers
        if stripped.endswith(':') and len(stripped.split()) <= 3:
            formatted_lines.append('')
            formatted_lines.append('━' * 60)
            formatted_lines.append(stripped.upper())
            formatted_lines.append('━' * 60)
        
        # Bullet points
        elif stripped.startswith('*') or stripped.startswith('•'):
            item = re.sub(r'^[\*•]\s*', '', stripped)
            formatted_lines.append(f'  • {item}')
        
        # Regular text
        else:
            formatted_lines.append(stripped)
    
    return '\n'.join(formatted_lines)


def format_for_frontend(raw_response: str, format_type: str = 'clean') -> dict:
    """
    Format response for frontend display with multiple format options.
    
    Args:
        raw_response (str): Raw AI response
        format_type (str): 'clean', 'html', or 'structured'
        
    Returns:
        dict: Formatted response with metadata
    """
    if format_type == 'html':
        formatted = format_as_html(raw_response)
    elif format_type == 'structured':
        formatted = format_as_structured_text(raw_response)
    else:  # 'clean'
        formatted = format_response(raw_response)
    
    # Extract sections for structured access
    sections = {}
    current_section = None
    
    for line in raw_response.split('\n'):
        stripped = line.strip()
        if stripped.endswith(':') and len(stripped.split()) <= 3:
            current_section = stripped[:-1].lower().replace(' ', '_')
            sections[current_section] = []
        elif current_section and stripped:
            sections[current_section].append(stripped)
    
    return {
        'formatted_text': formatted,
        'raw_text': raw_response,
        'sections': sections,
        'format_type': format_type
    }


def create_professional_summary(raw_response: str) -> str:
    """
    Create a professional, well-formatted summary from the raw response.
    This is the recommended format for portfolio assistant responses.
    
    Args:
        raw_response (str): Raw AI response
        
    Returns:
        str: Professionally formatted response
    """
    # Remove markdown bold
    text = raw_response.replace('**', '')
    
    # Split into paragraphs and sections
    paragraphs = []
    current_para = []
    
    for line in text.split('\n'):
        stripped = line.strip()
        
        if not stripped:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
            continue
        
        # Check if it's a section header
        if stripped.endswith(':') and len(stripped.split()) <= 3:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
            paragraphs.append(f'\n{stripped}')
        
        # Check if it's a bullet point
        elif stripped.startswith('*') or stripped.startswith('•'):
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
            item = re.sub(r'^[\*•]\s*', '', stripped)
            paragraphs.append(f'  • {item}')
        
        # Regular text
        else:
            current_para.append(stripped)
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    result = '\n'.join(paragraphs)
    
    # Clean up extra newlines
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result.strip()