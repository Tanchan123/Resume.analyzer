from typing import Dict, List, Union

class ResumeAnalyzer:
    def generate_suggestions(self, parsed_info: Dict[str, Union[List, str, int]]) -> Dict[str, Union[Dict, int]]:
        """
        Generate improvement suggestions based on parsed resume information
        and provide a resume score out of 100.
        """
        suggestions = {
            'General': [],
            'Skills': [],
            'Education': [],
            'Experience': [],
            'Formatting': []
        }

        score = 100  # Start with full score

        # General suggestions & scoring
        if not parsed_info.get('contact', {}).get('email'):
            suggestions['General'].append("📧 Add your email address for contact information.")
            score -= 10
        if not parsed_info.get('contact', {}).get('phone'):
            suggestions['General'].append("📞 Include your phone number for better reachability.")
            score -= 10
        if len(parsed_info.get('experience', [])) < 2:
            suggestions['General'].append("💼 Consider adding internships, projects, or freelance work to strengthen your resume.")
            score -= 8

        # Skills analysis & scoring
        num_skills = len(parsed_info.get('skills', []))
        if num_skills == 0:
            suggestions['Skills'].append("🛠 Add a list of technical and soft skills relevant to your industry.")
            score -= 15
        elif num_skills < 5:
            suggestions['Skills'].append("📚 Expand your skill set with in-demand technologies or industry-specific tools.")
            score -= 7
        elif num_skills > 15:
            suggestions['Skills'].append("🎯 Refine your skills section to highlight the most relevant and impactful ones.")
            score -= 5

        # Education analysis & scoring (FIXED BUG)
        education_levels = {
            "High School": "Consider pursuing a diploma, bachelor's degree, or vocational training in your field.",
            "Diploma": "Enhance your qualifications with a bachelor's degree or industry-recognized certifications.",
            "Bachelor": "Strengthen your resume with a master's degree, certifications, or specialized courses.",
            "Master": "You may consider a Ph.D. or professional certifications to advance your expertise.",
            "Ph.D.": "Explore post-doctoral research, executive education, or industry leadership programs."
        }

        education_info = parsed_info.get('education', [])

        # ✅ FIX: Ensure `education_info` is a list of strings
        if isinstance(education_info, int):  
            education_info = [str(education_info)]  # Convert int (like `2024`) into a string list
        elif isinstance(education_info, str):
            education_info = [education_info]  # Convert single string into a list
        elif not isinstance(education_info, list):
            education_info = []  # If it's anything else, make it an empty list

        # Check if education is missing
        if not education_info:
            suggestions['Education'].append("🎓 Add your educational background, including degrees, certifications, or relevant training.")
            score -= 15
        else:
            highest_edu = str(education_info[-1])  # Convert last education entry to string
            missing_year = not any(char.isdigit() for char in highest_edu)

            # Recommend next step in education
            for level, advice in education_levels.items():
                if level.lower() in highest_edu.lower():
                    suggestions['Education'].append(f"📖 {advice}")
                    break

            # Check if graduation/completion year is missing
            if missing_year:
                suggestions['Education'].append("📅 Consider including graduation/completion years for clarity.")
                score -= 5

        # Experience analysis & scoring
        experience_list = parsed_info.get('experience', [])
        if not isinstance(experience_list, list):
            experience_list = [str(experience_list)]  # Convert to list if not already

        if not experience_list:
            suggestions['Experience'].append("💼 Add work experience, internships, or significant projects with details about your contributions.")
            score -= 20
        elif len(experience_list) < 3:
            suggestions['Experience'].append("📄 Include more details about your past projects, responsibilities, and key achievements.")
            score -= 10

        # Formatting & Readability suggestions
        suggestions['Formatting'].extend([
            "📝 Use consistent font, bullet points, and spacing for a clean resume.",
            "📏 Ensure your resume is well-structured and easy to read.",
            "🔹 Keep your resume concise (ideally one page for less than 5 years of experience)."
        ])
        score -= 5  # General formatting penalty

        # Additional resume improvement suggestions
        suggestions['General'].extend([
            "🔹 Use action verbs to describe your experiences (e.g., 'Developed', 'Managed', 'Led')."
        ])

        suggestions['Experience'].extend([
            "📊 Quantify your achievements with numbers or percentages (e.g., 'Increased efficiency by 20%').",
            "📝 Focus on outcomes and impact rather than just listing job responsibilities."
        ])

        # Ensure score doesn't go below 0
        score = max(score, 0)

        return {
            'suggestions': {k: v for k, v in suggestions.items() if v},  # Remove empty categories
            'resume_score': score
        }
