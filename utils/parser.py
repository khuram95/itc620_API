# utils/parser.py
from bs4 import BeautifulSoup
import re

def parse_response(html):

  # Parse the HTML
  soup = BeautifulSoup(html, "html.parser")

  # Extract report summary
  report_summary = {
      "total_interactions": int(soup.find("p", class_="ddc-mgb-0").text.split()[0]),
      # Find the correct <ul> after the <p> tag
      "drugs": [li.get_text(strip=True) for li in soup.find("p", class_="ddc-mgb-0").find_next("ul").find_all("li")]
  }

  # Extract interaction filters
  interaction_filters = []
  for filter_div in soup.find("fieldset", class_="ddc-form-filter").find_all("div", class_="ddc-form-check"):
      filter_type = filter_div.find("b").get_text(strip=True)
      filter_text = filter_div.find("span").get_text(strip=True)
      # Use regex to extract the number inside parentheses
      filter_count = int(re.search(r"\((\d+)\)", filter_text).group(1))
      interaction_filters.append({"type": filter_type, "count": filter_count})

  # Extract interactions between drugs
  interactions_between_drugs = []
  for interaction in soup.find_all("div", class_="interactions-reference"):
      severity = interaction.find("span", class_="ddc-status-label").get_text(strip=True)
      title = interaction.find("h3").get_text(strip=True)
      # description = interaction.find("p").get_text(strip=True)
      description = interaction.find_all("p")[1].get_text(separator="")
      applies_to = interaction.find("p", text=lambda x: x and "Applies to:" in x).get_text(strip=True).replace("Applies to:", "").split(", ")
      interactions_between_drugs.append({
          "severity": severity,
          "title": title,
          "description": description,
          "applies_to": applies_to
      })

  # Extract drug and food interactions
  drug_and_food_interactions = []
  for interaction in soup.find_all("div", class_="interactions-reference"):
      severity = interaction.find("span", class_="ddc-status-label").get_text(strip=True)
      title = interaction.find("h3").get_text(strip=True)
      description = interaction.find_all("p")[1].get_text(separator="")
      applies_to = interaction.find("p", text=lambda x: x and "Applies to:" in x).get_text(strip=True).replace("Applies to:", "").split(", ")
      drug_and_food_interactions.append({
          "severity": severity,
          "title": title,
          "description": description,
          "applies_to": applies_to
      })

  # Extract therapeutic duplication warnings
  therapeutic_duplication_warnings = {
      "message": soup.find("h2", text="Therapeutic duplication warnings").find_next("p").get_text(strip=True),
      "details": soup.find("h2", text="Therapeutic duplication warnings").find_next("p").find_next("p").get_text(strip=True)
  }

  # Combine everything into the final JSON
  result = {
      "report_summary": report_summary,
      "interaction_filters": interaction_filters,
      "interactions_between_drugs": interactions_between_drugs,
      "drug_and_food_interactions": drug_and_food_interactions,
      "therapeutic_duplication_warnings": therapeutic_duplication_warnings
  }

  # Print the result
  print(result)
  return result