"""選択肢（choices）を一箇所にまとめておく。
    運用しながら選択肢を増やす時は、ここだけ触ればよい。
"""

GENDER_CHOICES = [("male", "男性"), ("female", "女性")]

YES_NO_CHOICES = [("yes", "有"), ("no", "無")]

RELATIONSHIP_CHOICES = [
    ("self", "本人"), ("spouse", "配偶者"), ("child", "子"),
    ("parent", "親"), ("other", "その他"),
]

LIVING_STATUS_CHOICES = [("together", "同居"), ("separate", "別居")]

HOUSING_STATUS_CHOICES = [
    ("own", "自己所有"), ("family_own", "家族所有"), ("company_house", "社宅"),
    ("rented_house", "借家"), ("rented_apartment", "賃貸マンション"),
    ("public_housing", "公団住宅"), ("apartment", "アパート"), ("dormitory", "寮"),
]

EMPLOYMENT_TYPE_CHOICES = [
    ("full_time", "正社員"), ("contract", "契約社員"), ("dispatch", "派遣社員"),
    ("part_time", "パートアルバイト"), ("self_employed", "自営"), ("other", "その他"),
]

CAR_MAKER_CHOICES = [
    ("toyota", "TOYOTA"), ("nissan", "日産"), ("suzuki", "SUZUKI"),
    ("daihatsu", "ダイハツ"), ("honda", "ホンダ"), ("mazda", "マツダ"),
    ("subaru", "スバル"), ("other", "その他"),
]

USAGE_FREQUENCY_CHOICES = [
    ("daily", "ほぼ毎日"), ("weekend", "月8回程度（週末）"),
]

LICENSE_COLOR_CHOICES = [("green", "緑"), ("blue", "青"), ("gold", "ゴールド")]

INSPECTION_STATUS_CHOICES = [
    ("valid", "車検あり"), ("none", "車検なし"), ("in_progress", "整備中"),
]

LOCATION_STATUS_CHOICES = [
    ("auction_venue", "オークション会場"), ("garage", "整備工場"),
    ("yard", "ヤード（駐車場）"), ("delivered", "納車済"),
]

VEHICLE_STATUS_CHOICES = [
    ("in_stock", "在庫"), ("negotiating", "商談中"), ("sold", "売約済"),
]

PAYMENT_TYPE_CHOICES = [
    ("partner_loan", "提携ローン会社"), ("inhouse_loan", "自社ローン"),
    ("direct_installment", "直接分割"), ("lump_sum", "一括振込"),
]

SALE_PROGRESS_CHOICES = [
    ("inquiry", "問い合わせ"), ("hearing", "ヒアリング中"), ("pre_screening", "仮審査中"),
    ("screening", "本審査中"), ("vehicle_selection", "車両選定中"),
    ("preliminary_contract", "事前契約"), ("awaiting_payment", "入金待ち"),
    ("sourcing", "仕入れ手配中"), ("maintenance", "整備・点検中"),
    ("registration", "登録手続き中"), ("preparing_delivery", "納車準備"),
    ("delivered", "納車済"), ("paid_off", "完済"), ("cancelled", "キャンセル"),
]

LOAN_CONTRACT_TYPE_CHOICES = [
    ("inhouse_loan", "審査あり自社ローン"), ("direct_installment", "直接分割"),
]

BILLING_STATUS_CHOICES = [
    ("unpaid", "未収"), ("paid", "入金済"), ("partial", "一部入金"), ("overdue", "延滞"),
]

APPLICATION_RESULT_CHOICES = [
    ("pending", "審査中"), ("approved", "承認"), ("rejected", "否決"),
]

CONTACT_METHOD_CHOICES = [
    ("phone", "電話"), ("email", "メール"), ("sms", "SMS"), ("visit", "来店"), ("other", "その他"),
]
