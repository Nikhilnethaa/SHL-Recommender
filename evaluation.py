import numpy as np
from vector_db import vector_db

# Sample test cases from the problem statement
test_cases = [
    
    {
        "query": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "relevant": [
            "Automata - Fix (New) | SHL",
            "Core Java (Entry Level) (New) | SHL",
            "Java 8 (New) | SHL",
            "Core Java (Advanced Level) (New) | SHL",
            "Agile Software Development | SHL"
        ]
    },
    {
        "query": "I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options",
        "relevant": [
            "Entry level Sales 7.1 (International) | SHL",
            "Entry Level Sales Sift Out 7.1 | SHL",
            "Entry Level Sales Solution | SHL",
            "Sales Representative Solution | SHL"

        ]

    },
     
    {
  "query": "I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour.",
  "relevant": [
    "Motivation Questionnaire MQM5 | SHL",
    "Global Skills Assessment | SHL",
    "Graduate 8.0 Job Focused Assessment | SHL"
  ]
},
{
  "query": "Content Writer required, expert in English and SEO.",
  "relevant": [
    "Drupal (New) | SHL",
    "Search Engine Optimization (New) | SHL",
    "Administrative Professional - Short Form | SHL",
    "Entry Level Sales Sift Out 7.1 | SHL",
    "General Entry Level – Data Entry 7.0 Solution | SHL"
  ]
},
{
  "query": "Join a community that is shaping the future of work! SHL, People Science. People Answers. Are you a seasoned QA Engineer with a flair for innovation? Are you ready to shape the future of talent assessment and empower organizations to unlock their full potential? If so, we want you to be a part of the SHL Team! As a QA Engineer, you will be involved in creating and implementing software solutions that contribute to the development of our groundbreaking products.",
  "relevant": [
    "Automata Selenium | SHL",
    "Automata - Fix (New) | SHL",
    "Automata Front End | SHL",
    "JavaScript (New) | SHL",
    "HTML/CSS (New) | SHL",
    "HTML5 (New) | SHL",
    "CSS3 (New) | SHL",
    "Selenium (New) | SHL",
    "SQL Server (New) | SHL",
    "Automata - SQL (New) | SHL"
  ]
},
{
  "query": "What SHL Can Offer You: Diversity, equity, inclusion and accessibility are key threads in the fabric of SHL’s business and culture. Employee benefits package that takes care of you and your family. Support, coaching, and on-the-job development to achieve career success. A fun and flexible workplace where you’ll be inspired to do your best work. The ability to transform workplaces around the world for others. SHL is an equal opportunity employer. We support and encourage applications from a diverse range of candidates. Development experience – Java or JavaScript, CSS, HTML (Automation), Selenium WebDriver and page object design pattern (Automation), SQL server knowledge, Test case management experience, Manual Testing. Knowledge of the basic concepts of testing, strong solution-finding experience, and strong verbal and written communication skills.",
  "relevant": [
    "Manual Testing (New) | SHL",
    "Automata Selenium | SHL",
    "Automata - Fix (New) | SHL",
    "Automata Front End | SHL",
    "JavaScript (New) | SHL",
    "HTML/CSS (New) | SHL",
    "HTML5 (New) | SHL",
    "CSS3 (New) | SHL",
    "Selenium (New) | SHL",
    "SQL Server (New) | SHL",
    "Automata - SQL (New) | SHL"
  ]
},
{
  "query": "ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 minutes long. Manage the sound-scape of the organization and perform various administrative duties. Looking for candidates with basic administrative skills, numerical and verbal ability, and computer literacy.",
  "relevant": [
    "Administrative Professional - Short Form | SHL",
    "Verify - Numerical Ability | SHL",
    "Financial Professional - Short Form | SHL",
    "Bank Administrative Assistant - Short Form | SHL",
    "General Entry Level – Data Entry 7.0 Solution | SHL",
    "Basic Computer Literacy (Windows 10) (New) | SHL",
    "Verify - Verbal Ability - Next Generation | SHL"
  ]
},
{
  "query": "Radio Station Creative & Programming Head, Experience required 8-12 years. Should manage soundscape, support sales with creative ideas, build brand presence, develop local talent, and oversee programming. Looking for candidates with digital content conceptualization, branding focus, people management, communication, and creative thinking skills. Test duration should be at most 90 minutes.",
  "relevant": [
    "SHL Verify Interactive - Inductive Reasoning | SHL",
    "Occupational Personality Questionnaire OPQ32r | SHL",
    "SHL Verify Interactive - Numerical Reasoning | SHL",
    "Verify - Verbal Ability - Next Generation | SHL",
    "Creative Thinking Test (New) | SHL"
  ]
}


    
]


def recall_at_k(recommended, relevant, k):
    recommended_at_k = set([r['name'] for r in recommended[:k]])
    relevant_set = set(relevant)
    intersection = recommended_at_k.intersection(relevant_set)
    return len(intersection) / len(relevant_set) if relevant_set else 0

def average_precision_at_k(recommended, relevant, k):
    precisions = []
    relevant_set = set(relevant)
    num_relevant = 0
    
    for i in range(min(k, len(recommended))):
        if recommended[i]['name'] in relevant_set:
            num_relevant += 1
            precisions.append(num_relevant / (i + 1))
    
    return sum(precisions) / len(relevant) if relevant else 0

def evaluate():
    mean_recall = 0
    mean_ap = 0
    
    for case in test_cases:
        recommendations = vector_db.search(case['query'])
        recall = recall_at_k(recommendations, case['relevant'], 3)
        ap = average_precision_at_k(recommendations, case['relevant'], 3)
        
        mean_recall += recall
        mean_ap += ap
        
        print(f"Query: {case['query']}")
        print(f"Recall@3: {recall:.2f}")
        print(f"AP@3: {ap:.2f}")
        print("---")
    
    mean_recall /= len(test_cases)
    mean_ap /= len(test_cases)
    
    print(f"Mean Recall@3: {mean_recall:.2f}")
    print(f"Mean AP@3 (MAP@3): {mean_ap:.2f}")

if __name__ == "__main__":
    evaluate()