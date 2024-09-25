from flask import Flask, request, jsonify
import requests as req
import secrets

app = Flask(__name__)

def get_af_ac_enc_dat():
    # Generate 8 random bytes
    random_bytes = secrets.token_bytes(8)

    # Convert each byte to a hex string and concatenate them
    hex_string = ''.join(f'{byte:02x}' for byte in random_bytes)

    # Return the dictionary with the specified key
    return hex_string

@app.route('/get_ratings', methods=['GET'])
def get_ratings():
    itemid = request.args.get('itemid')
    shopid = request.args.get('shopid')
    limit = request.args.get('limit', default=6)
    offset = request.args.get('offset', default=0)
    
    if not itemid or not shopid:
        return jsonify({"error": "กรุณาระบุ itemid และ shopid"}), 400

    url = f"https://shopee.co.th/api/v2/item/get_ratings?exclude_filter=1&filter=3&filter_size=0&flag=1&fold_filter=0&itemid={itemid}&limit={limit}&offset={offset}&relevant_reviews=false&request_source=2&shopid={shopid}&tag_filter=&type=0&variation_filters="
    
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'af-ac-enc-dat': get_af_ac_enc_dat(),
        'content-type': 'application/json',
        'cookie': '_gcl_au=1.1.421080655.1720803920; _fbp=fb.2.1720803920037.86465139452052910; _QPWSDCXHZQA=90572dd8-2a04-4d65-bbc1-7583faeb6f9f; REC7iLP4Q=10aec76d-9546-4d22-9cd3-082d19aedaf9; SPC_F=UQHPLv9dJiQq2t0uvoDrHaRNn5AB4TH4; REC_T_ID=ecc1f717-4070-11ef-82ce-06db26184ed3; language=th; SPC_CLIENTID=VVFIUEx2OWRKaVFxbtdtopjlizncrmqv; _ga_DSXZBPJ4D3=GS1.1.1723469335.1.0.1723469335.60.0.0; _gid=GA1.3.1968924320.1727149737; SPC_SI=cn7yZgAAAAB4TlZVYnh2Rg4nBwAAAAAAY3llcVBjdlk=; SPC_SEC_SI=v1-QUdIMkVJZzNuSGY3S25FWN9WCOzCa0gt/64C3vITMzjjbsPer4eKzYye0HfobbdC1E3/QbJa0DWPBL26Be+YxgVAuWjkf/JusMH4O/qH7L4=; SPC_EC=.amo0dFBneFlUTmtDbmlPZYSL2g/oH5PUFhfgdMCWihakwDyaavz8M57OHteJccsUpgg9rdXlkbLTe70CI1N9zq1bZzbxsBDxy5IRnOzR4q/tHOPpPbPWUW9/j0VLM1JDfprMWfxuDld0rcYq72mxr8JTjw/c5hpJIgx72slcJP5Cz+djztkAE0xWwuIPAsd8NJu3+kirREUEz83EPlfpu4oGqQAT8Eb8u76kly8XNsziNRTrC4OGQKv1CKtLjO9T; SPC_ST=.amo0dFBneFlUTmtDbmlPZYSL2g/oH5PUFhfgdMCWihakwDyaavz8M57OHteJccsUpgg9rdXlkbLTe70CI1N9zq1bZzbxsBDxy5IRnOzR4q/tHOPpPbPWUW9/j0VLM1JDfprMWfxuDld0rcYq72mxr8JTjw/c5hpJIgx72slcJP5Cz+djztkAE0xWwuIPAsd8NJu3+kirREUEz83EPlfpu4oGqQAT8Eb8u76kly8XNsziNRTrC4OGQKv1CKtLjO9T; __LOCALE__null=TH; csrftoken=lTJjYQidgkwGJ8RqCYCJKjicI51EWaBv; SPC_U=1165499981; _sapid=a2ae9cf1f2cc0d975611f59eb1233333eb44dde12da4b1a4c25507d4; SPC_R_T_ID=4+rSQMJgVrh57gMluq0ySDNMVRrMTb/bU70UJJz86q4tA/5SGlDRjDsuOfJz2lfOA4w990lmTAcCBzSibu1/6FVBaD1RWUPUxGvr0TUP/xtI22vutfE3CTD6BwYigEouhQbu5pcfkSmcHRgUSDpOzjICiihnwbfaYRTGyHnktE8=; SPC_R_T_IV=OGY4bVlKMWFjZTFvY3hkNA==; SPC_T_ID=4+rSQMJgVrh57gMluq0ySDNMVRrMTb/bU70UJJz86q4tA/5SGlDRjDsuOfJz2lfOA4w990lmTAcCBzSibu1/6FVBaD1RWUPUxGvr0TUP/xtI22vutfE3CTD6BwYigEouhQbu5pcfkSmcHRgUSDpOzjICiihnwbfaYRTGyHnktE8=; SPC_T_IV=OGY4bVlKMWFjZTFvY3hkNA==; SPC_CDS_CHAT=7d0f64fe-d6da-43b2-af08-f5c0f9caa34d; AC_CERT_D=U2FsdGVkX18K46ma7xmkSRkCsN5MlUl/AcbIrOuaIkFJuKdqO24N5K8gkumkxBsJy/JpgA6/ZkkMhxLfiKyL8QpeCDqhhscIIsW4nez0R2bdOakJG5Oei7TZ9t72swujPtSfef/1Gv/t2AP6/syhcVwWU3DD4xOvewIK9pBmcTJcwVtTJPASIUX9laUWmTCzu7o20KdVqafxhBjWgZl72Usv/wWbjn1xYgSplE4Rv/n38xfjEweoC1+1jpXBOlxuo+KGBOqbLnvm0scmBwttiAUiGEH/tc6pHMStDBFNdqqzCDjc72KXPpY59CbUN6iJsGI/WpetDD0VfFzhVidx89ZA/4z3peH9cz+6sVDMIS+bUvhuUvakW8P/XCBO4QiD4157U9mfog/fcELxE5DwtHjWy0Pca7s8cyeIWXKWO53Terh6Tg6dG1hPyyCjA6/6wSE8aUnIFjq117ubMU0H9TNycmgrpp3L1n0KhaIdvWwxXs76t+DQgOhZoxEkXGaP4e3pIJracIFj9NY1WgMC+LKRsjXlyiQFE/nEi8lY3AzfRQWp7uib8TMs/8HsIqdj64UKxjMgEjzwsxqJKt1xDDK5VvFShHzsYM7UYCRMXuNexctr+85NVbFOOTLHxI36emSKsBesuvI+7JUyH3ZRzyAgIOPkA06wUjx97WQvJqiPiuXHzCmHM2roiYQeGrzQ+Ku3dSXCkmMsDpAHv0kMGJAJf/YfrRt61g3H+X5ByxLL4UhWUkvDDInJysWXF4ylhN5s8H7iP9Sk0bpQlvUUM9r9V9i19yxSP4+bpe1f4Xaidm6HQ0Nnf4fC19FvANhSnVsI1cazzWTNZyKekvF7jZhItqFDnkhHCTZhO761aIl6Oe8WqY9BMI1WnERpCJBGFy7SmvMKDF7M149nPnQ694filY4LrwJBKxTB5wiBUi4VFMpX/GbT2eoJ8oFDYBfFDXYvQnYkxV6NDj+W7HZyZovjd6UCA4qngwJIlkz6PDtuTI11a7mJmnmGOggwtEHeN4LSqEija+PkOlVNZhsAFbqxosNL0aN6mB9iJMOpmCWD9F/90vfsxxsxQlgI5O76WRYN+WafQgfWEvxu7L5c5w==; SPC_IA=1; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.3.1859686166.1720803922; _dc_gtm_UA-61914165-6=1; shopee_webUnique_ccd=D0IsMKknD1QC7quL1nosSg%3D%3D%7CG0drxXjzumcbtWkigGvExlqV3oL%2BSb0%2BoA56tlY01fcskEx8jpnFowbOhv%2FF82xxHx5pnQCMOok%3D%7Cue9tk3hEibq6QVxK%7C08%7C3; ds=dc281c29fb73fd5457f4ff7622f28b0b; _ga_LB1RXY1EGG=GS1.1.1727246335.167.1.1727246349.46.0.0',
        'priority': 'u=1, i',
        'referer': 'https://shopee.co.th/%E0%B8%81%E0%B8%A3%E0%B8%AD%E0%B8%9A%E0%B8%9B%E0%B9%89%E0%B8%B2%E0%B8%A2%E0%B8%95%E0%B8%B4%E0%B8%94%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B5-%E0%B8%81%E0%B8%A3%E0%B8%AD%E0%B8%9A%E0%B8%9B%E0%B9%89%E0%B8%B2%E0%B8%A2%E0%B8%9E%E0%B8%A3%E0%B8%9A-%E0%B9%81%E0%B8%9A%E0%B8%9A%E0%B9%81%E0%B8%82%E0%B9%87%E0%B8%87-%E0%B8%A3%E0%B8%96%E0%B8%A2%E0%B8%99%E0%B8%95%E0%B9%8C-%E0%B8%AD%E0%B8%B0%E0%B8%84%E0%B8%A5%E0%B8%B4%E0%B8%A5%E0%B8%B4%E0%B8%84-%E0%B8%AA%E0%B8%B2%E0%B8%A1%E0%B8%B2%E0%B8%A3%E0%B8%96%E2%80%8B%E0%B8%96%E0%B8%AD%E0%B8%94%E0%B8%AD%E0%B8%AD%E0%B8%81%E0%B9%84%E0%B8%94%E0%B9%89%E0%B8%87%E0%B9%88%E0%B8%B2%E0%B8%A2%E0%B9%80%E0%B8%A1%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B9%84%E0%B8%A1%E0%B9%88%E0%B9%83%E0%B8%8A%E0%B9%89%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B9%81%E0%B8%A5%E0%B9%89%E0%B8%A7-G14-i.244198924.20192357523?sp_atk=1b904acc-82f9-44a5-9ee6-d49a7056698a&xptdk=1b904acc-82f9-44a5-9ee6-d49a7056698a',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        'x-api-source': 'pc',
        'x-requested-with': 'XMLHttpRequest',
        'x-shopee-language': 'th',
        'x-sz-sdk-version': '1.10.15'
    }
    
    response = req.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": f"เกิดข้อผิดพลาด: {response.status_code}"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
