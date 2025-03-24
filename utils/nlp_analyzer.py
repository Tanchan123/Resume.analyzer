import spacy
import re
from typing import Dict, List

class NLPAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common skills keywords
        self.skill_patterns = [
            "python", "java", "javascript", "html", "css", "sql", "react",
            "angular", "vue", "node", "django", "flask", "spring", "docker",
            "kubernetes", "aws", "azure", "gcp", "machine learning", "ai",
            "data analysis", "project management", "agile", "scrum"
        ]

    def parse_resume(self, text: str) -> Dict:
        """
        Parse resume text and extract structured information.
        """
        doc = self.nlp(text)
        
        return {
            'contact': self._extract_contact_info(text),
            'skills': self._extract_skills(text),
            'education': self._extract_education(text),
            'experience': self._extract_experience(text)
        }

    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information using regex patterns."""
        contact_info = {}

        # Email pattern (more robust)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]  # Store the first match

        # Phone pattern (supports international formats)
        phone_pattern = r'\b(?:\+?\d{1,3})?[-.\s]?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0]  # Store the first match

        return contact_info

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills using regex for better accuracy."""
        skill_regex = r'\b(' + '|'.join(self.skill_patterns) + r')\b'
        skills_found = re.findall(skill_regex, text, re.IGNORECASE)
        return list(set([skill.title() for skill in skills_found]))  # Remove duplicates & title-case them

    def _extract_education(self, text: str) -> List[str]:
        """Extract education information."""
        education_keywords = r"(Bachelor|Master|PhD|BSc|MSc|MBA|Associate|Degree|University|College)"
        education_sections = re.finditer(education_keywords, text, re.IGNORECASE)

        education = []
        for match in education_sections:
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 100)
            education_line = text[start:end].split('\n')[0].strip()
            if education_line and len(education_line) > 10:  # Avoid short results
                education.append(education_line)

        return list(set(education))  # Remove duplicates

    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience details."""
        experience = []

        # Split text into lines and analyze for job roles
        lines = text.split('\n')
        job_keywords = r"\b(Engineer|Developer|Manager|Director|Analyst|Consultant|Lead|Senior|Junior|Intern|Specialist)\b"

        for i, line in enumerate(lines):
            if re.search(job_keywords, line, re.IGNORECASE):
                job_info = line.strip()

                # Look for company name in the next few lines (if available)
                if i + 1 < len(lines) and len(lines[i + 1]) < 50:  # Assume company names are short
                    job_info += f" at {lines[i + 1].strip()}"

                # Look for a date range nearby (e.g., "Jan 2020 - Dec 2022")
                date_pattern = r"(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\w\s,-]*\d{4}\b)"
                date_match = re.search(date_pattern, job_info)
                if date_match:
                    job_info += f" ({date_match.group()})"

                experience.append(job_info)

        return list(set(experience))  # Remove duplicates
