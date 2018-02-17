notification = {
    'pushover': {
        'user': '',
        'token': '',
    },
}

crawler = {
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

spiders = {
    'imbak': [
        { 'category': '014009' }, # 유제품/치즈
    ],
    'thirtymall': [
        { 'code': '000300040003' }, # 빙과/유제품/디저트
    ],
    'cheesequeen': [
        { 'code': '00520003' }, # 기한임박할인
    ],
    'cheeseparty': [
        { 'cate_no': '283' }, # 세일파티
    ],
    'choosecheese': [
        { 'xcode': '001', 'mcode': '007' }, # 할인코너 / 기한임박, 과재고
    ],
}

keywords = [
    # (name to search, name to display)
    ('마스카포네', '마스카포네 치즈'),
    ('마스카르포네', '마스카포네 치즈'),
]