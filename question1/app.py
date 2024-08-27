from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


AUTH_URL = "http://20.244.56.144/test/auth"
PRODUCTS_URL_TEMPLATE = "http://20.244.56.144/test/companies/{company}/categories/{category}/products"
AUTH_PAYLOAD = {
    "companyName": "Gitam University Visakhapatnam",
    "clientID": "6b5c6ad2-5ddb-435f-bbd6-9d273b41b776",
    "clientSecret": "GwhcoMynoPjVOGYZ",
    "ownerName": "Balanagu Jishnu Vardhan",
    "ownerEmail": "jbalanag@gitam.in",
    "rollNo": "VU21CSEN0101025"
}


token_info = {
    "access_token": None,
    "expires_in": None
}

def get_token():
    response = requests.post(AUTH_URL, json=AUTH_PAYLOAD)
    if response.status_code == 200:
        data = response.json()
        token_info["access_token"] = data["access_token"]
        token_info["expires_in"] = data["expires_in"]
    else:
        raise Exception("Failed to fetch token")

    @app.route('/products', methods=['GET'])
    def get_products():
        company = request.args.get('company')
        category = request.args.get('category')
        top = request.args.get('top')
        min_price = request.args.get('minPrice')
        max_price = request.args.get('maxPrice')

        if not all([company, category, top, min_price, max_price]):
            return jsonify({"error": "Missing required query parameters"}), 400

        if not token_info["access_token"]:
            get_token()

        headers = {
            "Authorization": f"Bearer {token_info["access_token"]}"
        }
        products_url = PRODUCTS_URL_TEMPLATE.format(company=company, category=category)
        params = {
            "top": top,
            "minPrice": min_price,
            "maxPrice": max_price
        }

        response = requests.get(products_url, headers=headers, params=params)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch products"}), response.status_code


    if not token_info["access_token"]:

        pass

    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzI0NzM1MjkyLCJpYXQiOjE3MjQ3MzQ5OTIsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjZiNWM2YWQyLTVkZGItNDM1Zi1iYmQ2LTlkMjczYjQxYjc3NiIsInN1YiI6ImpiYWxhbmFnQGdpdGFtLmluIn0sImNvbXBhbnlOYW1lIjoiR2l0YW0gVW5pdmVyc2l0eSBWaXNha2hwYXRuYW0iLCJjbGllbnRJRCI6IjZiNWM2YWQyLTVkZGItNDM1Zi1iYmQ2LTlkMjczYjQxYjc3NiIsImNsaWVudFNlY3JldCI6Ikd3aGNvTXlub1BqVlFHWVoiLCJvd25lck5hbWUiOiJCYWxhbmFndSBKaXNobnUgVmFyZGhhbiIsIm93bmVyRW1haWwiOiJqYmFsYW5hZ0BnaXRhbS5pbiIsInJvbGxObyI6IlZVMjFDU0VOMDEwMTAyNSJ9.eWa-DnAWa2uo4LggxGFV8ijafayFyNRZ970cfrV0iLA"
    }

    products_url = PRODUCTS_URL_TEMPLATE.format(company=company, category=category)
    params = {
        "top": top,
        "minPrice": min_price,
        "maxPrice": max_price
    }

    response = requests.get(products_url, headers=headers, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch products"}), response.status_code

@app.route('/categories/<categoryname>/products', methods=['GET'])
def get_products_by_category(categoryname):
    company = request.args.get('company')
    top = request.args.get('top')
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')

    if not all([company, top, min_price, max_price]):
        return jsonify({"error": "Missing required query parameters"}), 400


    if not token_info["access_token"]:
        get_token()

    headers = {
        "Authorization": f"Bearer {token_info['access_token']}"
    }

    products_url = PRODUCTS_URL_TEMPLATE.format(company=company, category=categoryname)
    params = {
        "top": top,
        "minPrice": min_price,
        "maxPrice": max_price
    }

    response = requests.get(products_url, headers=headers, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch products"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
