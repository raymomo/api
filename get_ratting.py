from flask import Flask, request, jsonify
import requests as req
import secrets
import logging

app = Flask(__name__)

# กำหนดการบันทึกข้อผิดพลาด
logging.basicConfig(level=logging.ERROR)

def get_af_ac_enc_dat():
    # Generate 8 random bytes
    random_bytes = secrets.token_bytes(8)
    # Convert each byte to a hex string and concatenate them
    hex_string = ''.join(f'{byte:02x}' for byte in random_bytes)
    # Return the hex string
    return hex_string

@app.route('/get_ratings', methods=['POST'])
def get_ratings():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data or missing Content-Type header"}), 400

        itemid = data.get('itemid')
        shopid = data.get('shopid')
        limit = data.get('limit', 6)
        offset = data.get('offset', 0)
        cookie = data.get('cookie')

        if not itemid or not shopid:
            return jsonify({"error": "กรุณาระบุ itemid และ shopid"}), 400
        if not cookie:
            return jsonify({"error": "กรุณาระบุ cookie"}), 400

        url = f"https://shopee.co.th/api/v2/item/get_ratings?exclude_filter=1&filter=3&filter_size=0&flag=1&fold_filter=0&itemid={itemid}&limit={limit}&offset={offset}&relevant_reviews=false&request_source=2&shopid={shopid}&tag_filter=&type=0&variation_filters="
        
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'af-ac-enc-dat': get_af_ac_enc_dat(),
            'content-type': 'application/json',
            'cookie': cookie,
            'priority': 'u=1, i',
            'referer': f'https://shopee.co.th/product/{shopid}/{itemid}',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
            'x-api-source': 'android',
            'x-requested-with': 'XMLHttpRequest',
            'x-shopee-language': 'th',
            'x-sz-sdk-version': '1.10.15'
        }
        
        response = req.get(url, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                return jsonify(data)
            except ValueError:
                app.logger.error(f"Invalid JSON response from Shopee API: {response.text}")
                return jsonify({"error": "Invalid JSON response from Shopee API"}), 500
        else:
            app.logger.error(f"Shopee API returned status code {response.status_code}: {response.text}")
            return jsonify({"error": f"เกิดข้อผิดพลาด: {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        app.logger.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
