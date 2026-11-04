# -*- coding: utf-8 -*-
"""Arabic number-to-text utility for Saudi Riyal currency.

Grammar rules handled:
- For 3-9 in the ones place: gender is OPPOSITE the counted noun (ريال m / هللة f)
- For 1 and 2: gender MATCHES the counted noun
- For 11-19: same gender rules as above (11 = أحد عشر m / إحدى عشرة f; 12 = اثنا عشر m / اثنتا عشرة f)
- Scale words (ألف/مليون/مليار) take tanween (ألفاً/مليوناً/ملياراً) when the chunk is 11-99
"""

# Masculine ones (for masculine nouns like ريال)
_ONES_M = {
    0: '', 1: 'واحد', 2: 'اثنان', 3: 'ثلاثة', 4: 'أربعة', 5: 'خمسة',
    6: 'ستة', 7: 'سبعة', 8: 'ثمانية', 9: 'تسعة',
    10: 'عشرة', 11: 'أحد عشر', 12: 'اثنا عشر', 13: 'ثلاثة عشر',
    14: 'أربعة عشر', 15: 'خمسة عشر', 16: 'ستة عشر', 17: 'سبعة عشر',
    18: 'ثمانية عشر', 19: 'تسعة عشر',
}

# Feminine ones (for feminine nouns like هللة)
_ONES_F = {
    0: '', 1: 'واحدة', 2: 'اثنتان', 3: 'ثلاث', 4: 'أربع', 5: 'خمس',
    6: 'ست', 7: 'سبع', 8: 'ثمان', 9: 'تسع',
    10: 'عشرة', 11: 'إحدى عشرة', 12: 'اثنتا عشرة', 13: 'ثلاث عشرة',
    14: 'أربع عشرة', 15: 'خمس عشرة', 16: 'ست عشرة', 17: 'سبع عشرة',
    18: 'ثماني عشرة', 19: 'تسع عشرة',
}

_TENS = {
    2: 'عشرون', 3: 'ثلاثون', 4: 'أربعون', 5: 'خمسون',
    6: 'ستون', 7: 'سبعون', 8: 'ثمانون', 9: 'تسعون',
}

_HUNDREDS = {
    1: 'مائة', 2: 'مائتان', 3: 'ثلاثمائة', 4: 'أربعمائة', 5: 'خمسمائة',
    6: 'ستمائة', 7: 'سبعمائة', 8: 'ثمانمائة', 9: 'تسعمائة',
}

# Scale names — base form, dual form, plural form (3-10), tanween form (11+)
_SCALES = {
    1: ('ألف', 'ألفان', 'آلاف', 'ألفاً'),
    2: ('مليون', 'مليونان', 'ملايين', 'مليوناً'),
    3: ('مليار', 'ملياران', 'مليارات', 'ملياراً'),
    4: ('تريليون', 'تريليونان', 'تريليونات', 'تريليوناً'),
}


def _two_digit_to_arabic(n, feminine=False):
    """Convert 0-99 to Arabic words."""
    if n == 0:
        return ''
    table = _ONES_F if feminine else _ONES_M
    if n < 20:
        return table[n]
    tens, ones = divmod(n, 10)
    if ones == 0:
        return _TENS[tens]
    return f'{table[ones]} و{_TENS[tens]}'


def _three_digit_to_arabic(n, feminine=False):
    """Convert 0-999 to Arabic words."""
    if n == 0:
        return ''
    hundreds, rest = divmod(n, 100)
    parts = []
    if hundreds:
        parts.append(_HUNDREDS[hundreds])
    if rest:
        parts.append(_two_digit_to_arabic(rest, feminine=feminine))
    return ' و'.join(parts)


def _scale_chunk(n, scale_idx, feminine=False):
    """Convert a 3-digit chunk with a scale word (0=ones, 1=thousands...)."""
    if n == 0:
        return ''
    if scale_idx == 0:
        return _three_digit_to_arabic(n, feminine=feminine)

    base, dual, plural, tanween = _SCALES[scale_idx]
    # Choose the right scale word:
    # 1 → just base (no number prefix), 2 → just dual, 3-10 → number + plural,
    # 11+ → number + tanween form
    if n == 1:
        return base
    if n == 2:
        return dual
    chunk_text = _three_digit_to_arabic(n, feminine=False)
    if 3 <= n <= 10:
        scale_word = plural
    else:
        scale_word = tanween
    return f'{chunk_text} {scale_word}'


def int_to_arabic_words(n, feminine=False):
    """Convert a non-negative integer to Arabic words.

    :param feminine: if True, use feminine forms (for هللة etc.)
    """
    if n == 0:
        return 'صفر'
    if n < 0:
        return 'سالب ' + int_to_arabic_words(-n, feminine=feminine)

    chunks = []
    while n > 0:
        n, r = divmod(n, 1000)
        chunks.append(r)

    parts = []
    for i, chunk in enumerate(chunks):
        if chunk == 0:
            continue
        # Only the lowest chunk (ones) takes the gender from the noun;
        # higher chunks (thousands, millions...) always use masculine grammatically
        # because the scale word (ألف/مليون) is masculine.
        parts.append(_scale_chunk(chunk, i, feminine=(feminine if i == 0 else False)))

    parts.reverse()
    return ' و'.join(parts)


def amount_to_arabic_text(amount, currency_name='ريال', halala_name='هللة',
                          currency_plural='ريالاً سعودياً'):
    """Convert a monetary amount to Arabic text in the Saudi style.

    Examples:
        6035.00 -> "فقط ستة آلاف وخمسة وثلاثون ريالاً سعودياً لا غير"
        120969.62 -> "فقط مائة وعشرون ألفاً وتسعمائة وتسعة وستون ريالاً سعودياً واثنتان وستون هللة لا غير"
    """
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        amount = 0.0

    negative = amount < 0
    amount = abs(amount)
    integer_part = int(amount)
    fractional = round((amount - integer_part) * 100)
    if fractional >= 100:
        integer_part += 1
        fractional -= 100

    parts = []
    if integer_part > 0:
        # ريال is masculine
        int_words = int_to_arabic_words(integer_part, feminine=False)
        parts.append(f'{int_words} {currency_plural}')
    if fractional > 0:
        # هللة is feminine
        halala_words = int_to_arabic_words(fractional, feminine=True)
        parts.append(f'{halala_words} {halala_name}')

    if not parts:
        parts.append(f'صفر {currency_plural}')

    text = ' و'.join(parts)
    if negative:
        text = 'سالب ' + text
    return f'فقط {text} لا غير'
