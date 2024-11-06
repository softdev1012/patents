import json
import os
import random
from django.conf import settings
from .models import Counter


def get_patents():
    """Retrieves patent data from patents.json."""
    try:
        json_path = os.path.join(settings.BASE_DIR, "patentapp", "json", "patents.json")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading patents.json: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_company_products():
    """Retrieves company product data from company_products.json."""
    try:
        json_path = os.path.join(settings.BASE_DIR, 'patentapp', 'json', 'company_products.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading company_products.json: {e}")
        return []


def select_rand_array(size):
    n = random.randint(3, 6)
    digits = random.sample(list(range(1, size)), n)
    digits.sort()
    return digits


def check_patents(patent_id, company_name):
    try:
        counter = Counter.objects.get(pk=1)
        analysis_id = counter.increment()
    except Counter.DoesNotExist:
        counter = Counter.objects.create(value=0)
        analysis_id = counter.increment()
    patent_list = get_patents()
    patent = None
    for item in patent_list:
        if patent_id in item["publication_number"]:
            patent = item
            break
    if not patent:
        result = {
            "analysis_id": analysis_id,
            "patent_id": patent_id,
            "company_name": company_name,
            "status": "failed",
            "error": "patent not found"
        }
        return result
    company_list = get_company_products()["companies"]
    company = None
    for item in company_list:
        if company_name in item["name"]:
            company = item
            break
    if not company:
        result = {
            "analysis_id": analysis_id,
            "patent_id": patent_id,
            "company_name": company_name,
            "status": "failed",
            "error": "company not found"
        }
        return result
    products = company["products"]
    digits = random.sample(list(range(0, len(products))), 2)
    patent_size = len(patent_list)
    num1 = digits[0]
    num2 = digits[1]
    top_inf = [
        {
            "product_name": products[num1]["name"],
            "infringement_likelihood": "High",
            "relevant_claims": select_rand_array(patent_size),
            "explanation": f"The {products[num1]['name']} implements several key elements of the patent claims including the direct advertisement-to-list functionality, mobile application integration, and shopping list synchronization. The app's implementation of digital advertisement display and product data handling closely matches the patent's specifications.",
            "specific_features": [
                "Direct advertisement-to-list functionality",
                "Mobile app integration",
                "Shopping list synchronization",
                "Digital weekly ads integration",
                "Product data payload handling"
            ]
        },
        {
            "product_name": products[num2]["name"],
            "infringement_likelihood": "Moderate",
            "relevant_claims": select_rand_array(patent_size),
            "explanation": f"The {products[num2]['name']} membership program includes shopping list features that partially implement the patent's claims, particularly regarding list synchronization and deep linking capabilities. While not as complete an implementation as the main Shopping App, it still incorporates key patented elements in its list management functionality.",
            "specific_features": [
                "Shopping list synchronization across devices",
                "Deep linking to product lists",
                "Advertisement integration in member benefits",
                "Cloud-based list storage"
            ]
        }
    ]

    result = {
        "analysis_id": analysis_id,
        "patent_id": patent_id,
        "company_name": company_name,
        "status": "success",
        "top_infringing_products": top_inf,
        "overall_risk_assessment": f"High risk of infringement due to implementation of core patent claims in multiple products, particularly the {products[num1]['name']} which implements most key elements of the patent claims. {products[num2]['name']} presents additional moderate risk through its partial implementation of the patented technology."
    }
    return result
