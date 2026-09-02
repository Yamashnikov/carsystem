from django.db import models
from core.models_base import TimeStampedModel, SoftDeleteModel
from core import choices as c


# =========================================================
# 顧客まわり
# =========================================================

class Customer(TimeStampedModel, SoftDeleteModel):
    """顧客（会員）"""
    member_id = models.CharField("会員ID", max_length=8, unique=True, db_index=True)

    last_name = models.CharField("姓", max_length=50)
    first_name = models.CharField("名", max_length=50)
    last_name_kana = models.CharField("セイ", max_length=50)
    first_name_kana = models.CharField("メイ", max_length=50)
    gender = models.CharField("性別", max_length=10, choices=c.GENDER_CHOICES)
    birth_date = models.DateField("生年月日")

    landline_phone = models.CharField("固定電話", max_length=20, blank=True)
    landline_phone_holder = models.CharField("固定電話の名義人", max_length=50, blank=True)
    mobile_phone = models.CharField("携帯（SMS通知先）", max_length=20)
    email = models.EmailField("メアド", blank=True)

    postal_code = models.CharField("郵便番号", max_length=8, blank=True)
    prefecture = models.CharField("都道府県", max_length=10, blank=True)
    address_line = models.CharField("市区町村・番地", max_length=255, blank=True)
    building_room = models.CharField("建物名・居室番号", max_length=100, blank=True)
    address_kana = models.CharField("住所フリガナ", max_length=255, blank=True)

    has_car = models.CharField("車の所有状況", max_length=10, choices=c.YES_NO_CHOICES, blank=True)

    # 会員ページで「未入力の場合のみ入力可・入力後は編集不可」とする対象フィールド名
    CUSTOMER_EDITABLE_ONCE_FIELDS = [
        "email", "postal_code", "prefecture", "address_line", "building_room",
        "address_kana", "landline_phone", "landline_phone_holder", "has_car",
    ]

    class Meta:
        verbose_name = "顧客"
        verbose_name_plural = "顧客"

    def __str__(self):
        return f"{self.member_id} {self.last_name}{self.first_name}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"


class LoanScreeningInfo(TimeStampedModel):
    """ローン審査情報（顧客と1:1）"""
    customer = models.OneToOneField(Customer, verbose_name="顧客", on_delete=models.PROTECT,
                                     related_name="loan_screening_info")

    has_spouse = models.CharField("配偶者の有無", max_length=10, choices=c.YES_NO_CHOICES, blank=True)
    spouse_has_job = models.CharField("配偶者の職の有無", max_length=10, choices=c.YES_NO_CHOICES, blank=True)
    children_count = models.PositiveIntegerField("同居の子供人数", null=True, blank=True)
    household_members_count = models.PositiveIntegerField("同一生計人数（本人含む）", null=True, blank=True)

    primary_breadwinner = models.CharField("主たる生計者", max_length=10, choices=c.RELATIONSHIP_CHOICES, blank=True)
    primary_breadwinner_other = models.CharField("主たる生計者（その他詳細）", max_length=50, blank=True)
    breadwinner_living_status = models.CharField("主たる生計者との居住実態", max_length=10,
                                                   choices=c.LIVING_STATUS_CHOICES, blank=True)

    housing_status = models.CharField("住居状況", max_length=20, choices=c.HOUSING_STATUS_CHOICES, blank=True)
    residence_years = models.PositiveIntegerField("居住年数", null=True, blank=True)
    residence_months = models.PositiveIntegerField("居住月数", null=True, blank=True)
    has_housing_loan_or_rent = models.CharField("住宅ローン又は家賃負担の有無", max_length=10,
                                                  choices=c.YES_NO_CHOICES, blank=True)
    monthly_rent = models.PositiveIntegerField("月々の家賃（円）", null=True, blank=True)
    annual_income = models.PositiveIntegerField("年収（万円）", null=True, blank=True)

    guarantor1_name = models.CharField("連帯保証人①氏名", max_length=50, blank=True)
    guarantor1_relationship = models.CharField("連帯保証人①続柄", max_length=10, choices=c.RELATIONSHIP_CHOICES, blank=True)
    guarantor1_phone = models.CharField("連帯保証人①電話番号", max_length=20, blank=True)
    guarantor2_name = models.CharField("連帯保証人②氏名", max_length=50, blank=True)
    guarantor2_relationship = models.CharField("連帯保証人②続柄", max_length=10, choices=c.RELATIONSHIP_CHOICES, blank=True)
    guarantor2_phone = models.CharField("連帯保証人②電話番号", max_length=20, blank=True)

    employer_name = models.CharField("勤務先会社名", max_length=100, blank=True)
    employer_name_kana = models.CharField("勤務先会社名フリガナ", max_length=100, blank=True)
    job_type = models.CharField("職種", max_length=50, blank=True)
    employer_phone = models.CharField("勤務先電話番号", max_length=20, blank=True)
    employer_postal_code = models.CharField("勤務先郵便番号", max_length=8, blank=True)
    employer_prefecture = models.CharField("勤務先都道府県", max_length=10, blank=True)
    employer_address_line = models.CharField("勤務先市区町村・番地", max_length=255, blank=True)
    employer_building_room = models.CharField("勤務先建物名・居室番号", max_length=100, blank=True)
    employer_address_kana = models.CharField("勤務先住所フリガナ", max_length=255, blank=True)
    employment_years = models.PositiveIntegerField("勤務年数", null=True, blank=True)
    employment_months = models.PositiveIntegerField("勤務月数", null=True, blank=True)
    employment_type = models.CharField("勤務形態", max_length=20, choices=c.EMPLOYMENT_TYPE_CHOICES, blank=True)
    employment_type_other = models.CharField("勤務形態（その他詳細）", max_length=50, blank=True)
    dispatch_company_name = models.CharField("派遣先会社名", max_length=100, blank=True)
    dispatch_company_phone = models.CharField("派遣先電話番号", max_length=20, blank=True)

    spouse_last_name = models.CharField("配偶者の姓", max_length=50, blank=True)
    spouse_first_name = models.CharField("配偶者の名", max_length=50, blank=True)
    spouse_last_name_kana = models.CharField("配偶者の姓フリガナ", max_length=50, blank=True)
    spouse_first_name_kana = models.CharField("配偶者の名フリガナ", max_length=50, blank=True)
    spouse_annual_income = models.PositiveIntegerField("配偶者の年収（万円）", null=True, blank=True)
    spouse_monthly_credit_payment = models.PositiveIntegerField("配偶者の分割払クレジット月支払額（円）",
                                                                  null=True, blank=True)

    # 会員ページで「未入力の場合のみ入力可・入力後は編集不可」とする対象フィールド名
    CUSTOMER_EDITABLE_ONCE_FIELDS = [
        "has_spouse", "spouse_has_job", "children_count", "household_members_count",
        "primary_breadwinner", "primary_breadwinner_other", "breadwinner_living_status",
        "housing_status", "residence_years", "residence_months",
        "has_housing_loan_or_rent", "monthly_rent", "annual_income",
        "guarantor1_name", "guarantor1_relationship", "guarantor1_phone",
        "guarantor2_name", "guarantor2_relationship", "guarantor2_phone",
        "employer_name", "employer_name_kana", "job_type", "employer_phone",
        "employer_postal_code", "employer_prefecture", "employer_address_line",
        "employer_building_room", "employer_address_kana",
        "employment_years", "employment_months", "employment_type", "employment_type_other",
        "dispatch_company_name", "dispatch_company_phone",
        "spouse_last_name", "spouse_first_name", "spouse_last_name_kana", "spouse_first_name_kana",
        "spouse_annual_income", "spouse_monthly_credit_payment",
    ]

    class Meta:
        verbose_name = "ローン審査情報"
        verbose_name_plural = "ローン審査情報"

    def __str__(self):
        return f"ローン審査情報（{self.customer}）"


class CustomerCurrentVehicle(TimeStampedModel):
    """現在使用中の車両情報（顧客と0または1件）"""
    customer = models.OneToOneField(Customer, verbose_name="顧客", on_delete=models.PROTECT,
                                     related_name="current_vehicle")
    car_maker = models.CharField("車両メーカー名", max_length=20, choices=c.CAR_MAKER_CHOICES, blank=True)
    car_maker_other = models.CharField("メーカー（その他詳細）", max_length=50, blank=True)
    car_model = models.CharField("車種名", max_length=50, blank=True)
    car_model_year = models.PositiveIntegerField("製造年式", null=True, blank=True)
    car_mileage = models.PositiveIntegerField("走行距離", null=True, blank=True)
    has_optional_insurance = models.CharField("任意保険の加入状況", max_length=10, choices=c.YES_NO_CHOICES, blank=True)
    insurance_grade = models.PositiveIntegerField("任意保険の等級", null=True, blank=True)
    usage_frequency = models.CharField("車の使用頻度", max_length=10, choices=c.USAGE_FREQUENCY_CHOICES, blank=True)

    CUSTOMER_EDITABLE_ONCE_FIELDS = [
        "car_maker", "car_maker_other", "car_model", "car_model_year", "car_mileage",
        "has_optional_insurance", "insurance_grade", "usage_frequency",
    ]

    class Meta:
        verbose_name = "現在使用中の車両情報"
        verbose_name_plural = "現在使用中の車両情報"

    def __str__(self):
        return f"現在使用中の車両情報（{self.customer}）"


class CustomerIdVerification(TimeStampedModel):
    """本人確認書類（顧客と1:1）"""
    customer = models.OneToOneField(Customer, verbose_name="顧客", on_delete=models.PROTECT,
                                     related_name="id_verification")
    license_number = models.CharField("運転免許証番号", max_length=20, blank=True)
    license_color = models.CharField("運転免許証の色", max_length=10, choices=c.LICENSE_COLOR_CHOICES, blank=True)
    license_image_url = models.CharField("運転免許画像", max_length=500, blank=True)
    insurance_card_image_url = models.CharField("保険証画像", max_length=500, blank=True)

    CUSTOMER_EDITABLE_ONCE_FIELDS = ["license_number", "license_color", "license_image_url",
                                      "insurance_card_image_url"]

    class Meta:
        verbose_name = "本人確認書類"
        verbose_name_plural = "本人確認書類"

    def __str__(self):
        return f"本人確認書類（{self.customer}）"


class ContactLog(TimeStampedModel):
    """対応履歴（顧客とのやり取り）"""
    customer = models.ForeignKey(Customer, verbose_name="顧客", on_delete=models.PROTECT,
                                  related_name="contact_logs")
    contact_method = models.CharField("対応手段", max_length=10, choices=c.CONTACT_METHOD_CHOICES, blank=True)
    content = models.TextField("対応内容")
    logged_at = models.DateTimeField("対応日時")
    created_by = models.CharField("対応した担当者名", max_length=50, blank=True)

    class Meta:
        verbose_name = "対応履歴"
        verbose_name_plural = "対応履歴"
        ordering = ["-logged_at"]

    def __str__(self):
        return f"{self.customer} - {self.logged_at:%Y-%m-%d}"


# =========================================================
# マスタ系
# =========================================================

class Seller(TimeStampedModel, SoftDeleteModel):
    """買取客（下取りではなく単純売却のみの相手）"""
    name = models.CharField("氏名", max_length=100)
    phone_number = models.CharField("連絡先", max_length=20, blank=True)
    memo = models.TextField("メモ", blank=True)

    class Meta:
        verbose_name = "買取客"
        verbose_name_plural = "買取客"

    def __str__(self):
        return self.name


class Supplier(TimeStampedModel, SoftDeleteModel):
    """仕入先（業者）"""
    name = models.CharField("業者名", max_length=100)
    contact_person = models.CharField("担当者名", max_length=50, blank=True)
    phone_number = models.CharField("連絡先", max_length=20, blank=True)
    transport_company_name = models.CharField("陸送業者名", max_length=100, blank=True)
    standard_transport_cost = models.PositiveIntegerField("標準陸送費", null=True, blank=True)

    class Meta:
        verbose_name = "仕入先"
        verbose_name_plural = "仕入先"

    def __str__(self):
        return self.name


class LoanCompanyMaster(TimeStampedModel, SoftDeleteModel):
    """ローン会社マスタ"""
    name = models.CharField("会社名", max_length=100)
    phone_number = models.CharField("連絡先", max_length=20, blank=True)

    class Meta:
        verbose_name = "ローン会社マスタ"
        verbose_name_plural = "ローン会社マスタ"

    def __str__(self):
        return self.name


# =========================================================
# 車両・販売・買取（中心テーブル）
# =========================================================

class Purchase(TimeStampedModel):
    """買取（下取り・単純買取）"""
    customer = models.ForeignKey(Customer, verbose_name="顧客（下取り時）", on_delete=models.PROTECT,
                                  null=True, blank=True, related_name="purchases_as_customer")
    seller = models.ForeignKey(Seller, verbose_name="買取客（単純買取時）", on_delete=models.PROTECT,
                                null=True, blank=True, related_name="purchases")
    vehicle_info = models.CharField("車両情報", max_length=255, blank=True)
    purchase_price = models.PositiveIntegerField("買取額")
    purchase_date = models.DateField("買取日")
    listed_to = models.CharField("出品先", max_length=100, blank=True)
    sold_price = models.PositiveIntegerField("成立額", null=True, blank=True)

    class Meta:
        verbose_name = "買取"
        verbose_name_plural = "買取"

    def __str__(self):
        who = self.customer or self.seller
        return f"買取#{self.pk} {who}"


class Vehicle(TimeStampedModel, SoftDeleteModel):
    """車両（在庫）"""
    supplier = models.ForeignKey(Supplier, verbose_name="仕入先", on_delete=models.PROTECT,
                                  null=True, blank=True, related_name="vehicles")
    origin_purchase = models.ForeignKey(Purchase, verbose_name="買取からの在庫転用（例外）",
                                         on_delete=models.PROTECT, null=True, blank=True,
                                         related_name="converted_vehicles")

    maker = models.CharField("メーカー", max_length=50)
    model_name = models.CharField("車種", max_length=50)
    type_code = models.CharField("型式", max_length=30, blank=True)
    model_year = models.PositiveIntegerField("年式", null=True, blank=True)
    grade = models.CharField("グレード", max_length=50, blank=True)
    color = models.CharField("カラー", max_length=30, blank=True)
    mileage = models.PositiveIntegerField("走行距離", null=True, blank=True)
    chassis_number = models.CharField("車体番号", max_length=50, blank=True)
    license_plate = models.CharField("ナンバープレート", max_length=20, blank=True)
    registration_date = models.DateField("登録日", null=True, blank=True)

    purchase_price = models.PositiveIntegerField("仕入れ価格")
    auction_fee = models.PositiveIntegerField("オークション料", null=True, blank=True)
    inspection_cost = models.PositiveIntegerField("車検代", null=True, blank=True)
    maintenance_cost = models.PositiveIntegerField("整備費", null=True, blank=True)
    name_change_fee = models.PositiveIntegerField("名義変更費", null=True, blank=True)
    compulsory_insurance_cost = models.PositiveIntegerField("自賠責", null=True, blank=True)
    misc_cost = models.PositiveIntegerField("その他費用", null=True, blank=True)
    misc_cost_note = models.CharField("その他費用の内訳", max_length=100, blank=True)

    purchase_date = models.DateField("仕入日")
    inspection_status = models.CharField("車検状況", max_length=15, choices=c.INSPECTION_STATUS_CHOICES)
    inspection_expiry = models.DateField("車検有効期限", null=True, blank=True)
    location_status = models.CharField("所在", max_length=20, choices=c.LOCATION_STATUS_CHOICES,
                                        default="auction_venue")
    status = models.CharField("販売進捗", max_length=15, choices=c.VEHICLE_STATUS_CHOICES, default="in_stock")
    ownership_released_at = models.DateField("所有権解除日", null=True, blank=True)

    class Meta:
        verbose_name = "車両"
        verbose_name_plural = "車両"

    def __str__(self):
        return f"{self.maker} {self.model_name}（{self.chassis_number or '車台番号未登録'}）"

    @property
    def total_cost(self):
        """原価合計（画面表示用に都度計算する）"""
        parts = [self.purchase_price, self.auction_fee, self.inspection_cost,
                 self.maintenance_cost, self.name_change_fee,
                 self.compulsory_insurance_cost, self.misc_cost]
        return sum(p for p in parts if p)


class Sale(TimeStampedModel):
    """販売／取引（中心テーブル）"""
    customer = models.ForeignKey(Customer, verbose_name="顧客", on_delete=models.PROTECT, related_name="sales")
    vehicle = models.ForeignKey(Vehicle, verbose_name="車両", on_delete=models.PROTECT,
                                 null=True, blank=True, related_name="sale")
    trade_in_purchase = models.ForeignKey(Purchase, verbose_name="下取りとの紐付け", on_delete=models.PROTECT,
                                           null=True, blank=True, related_name="trade_in_sales")

    desired_spec = models.CharField("希望車種", max_length=255, blank=True)
    budget = models.PositiveIntegerField("予算", null=True, blank=True)

    contract_date = models.DateField("契約日")
    delivery_date = models.DateField("納車日", null=True, blank=True)
    delivery_address = models.CharField("納車先住所", max_length=255, blank=True)

    sale_price = models.PositiveIntegerField("確定額", null=True, blank=True)
    payment_type = models.CharField("支払方法", max_length=20, choices=c.PAYMENT_TYPE_CHOICES)
    loan_company = models.ForeignKey(LoanCompanyMaster, verbose_name="承認された提携ローン会社",
                                      on_delete=models.PROTECT, null=True, blank=True, related_name="sales")
    collection_amount = models.PositiveIntegerField("徴収額", null=True, blank=True)
    collection_date = models.DateField("徴収日", null=True, blank=True)

    progress_status = models.CharField("進捗ステータス", max_length=25, choices=c.SALE_PROGRESS_CHOICES,
                                        default="inquiry")
    documents_collected_at = models.DateTimeField("登録書類回収日時", null=True, blank=True)
    terms_agreed_at = models.DateTimeField("約款同意日時", null=True, blank=True)

    gps_installed = models.BooleanField("GPS搭載の有無", default=False)
    gps_install_cost = models.PositiveIntegerField("GPS設置費用", null=True, blank=True)
    gps_installed_date = models.DateField("GPS設置日", null=True, blank=True)
    gps_device_number = models.CharField("GPS端末番号", max_length=50, blank=True)

    assigned_staff = models.CharField("担当スタッフ", max_length=50, blank=True)
    notes = models.TextField("備考", blank=True)

    class Meta:
        verbose_name = "販売/取引"
        verbose_name_plural = "販売/取引"
        ordering = ["-contract_date"]

    def __str__(self):
        return f"取引#{self.pk} {self.customer}"


# =========================================================
# ローン関連
# =========================================================

class LoanApplication(TimeStampedModel):
    """ローン審査申込履歴（内規の優先順位に従い複数社に申込む）"""
    sale = models.ForeignKey(Sale, verbose_name="取引", on_delete=models.PROTECT, related_name="loan_applications")
    loan_company = models.ForeignKey(LoanCompanyMaster, verbose_name="申込先", on_delete=models.PROTECT,
                                      related_name="applications")
    priority_order = models.PositiveIntegerField("申込順位")
    applied_date = models.DateField("申込日")
    result = models.CharField("審査結果", max_length=10, choices=c.APPLICATION_RESULT_CHOICES, default="pending")
    result_date = models.DateField("結果確定日", null=True, blank=True)

    class Meta:
        verbose_name = "ローン審査申込履歴"
        verbose_name_plural = "ローン審査申込履歴"
        ordering = ["sale", "priority_order"]

    def __str__(self):
        return f"{self.sale} → {self.loan_company}（第{self.priority_order}希望）"


class InhouseLoanContract(TimeStampedModel):
    """自社ローン契約（審査あり自社ローン／直接分割の両方をここで管理）"""
    sale = models.OneToOneField(Sale, verbose_name="取引", on_delete=models.PROTECT, related_name="inhouse_loan")
    type = models.CharField("種別", max_length=20, choices=c.LOAN_CONTRACT_TYPE_CHOICES)
    contract_amount = models.PositiveIntegerField("契約額")
    installment_count = models.PositiveIntegerField("分割回数")
    interest_rate = models.DecimalField("金利（審査あり自社ローンのみ）", max_digits=5, decimal_places=2,
                                         null=True, blank=True)
    completed_at = models.DateField("完済日", null=True, blank=True)

    class Meta:
        verbose_name = "自社ローン契約"
        verbose_name_plural = "自社ローン契約"

    def __str__(self):
        return f"自社ローン契約（{self.sale}）"

    @property
    def remaining_balance(self):
        """残債＝入金済み以外の回の (請求額-入金額) 合計"""
        unpaid = self.payments.exclude(status="paid")
        return sum((p.amount_due - (p.paid_amount or 0)) for p in unpaid)

    @property
    def remaining_count(self):
        return self.payments.exclude(status="paid").count()

    def generate_payment_schedule(self):
        """契約確定時に、全回分の返済予定レコードを一括生成する"""
        import datetime
        if self.payments.exists():
            return
        monthly = self.contract_amount // self.installment_count
        base_date = self.sale.delivery_date or datetime.date.today()
        for i in range(1, self.installment_count + 1):
            month = base_date.month - 1 + i
            year = base_date.year + month // 12
            month = month % 12 + 1
            day = min(base_date.day, 28)
            due = datetime.date(year, month, day)
            amount = monthly if i < self.installment_count else \
                self.contract_amount - monthly * (self.installment_count - 1)
            InhouseLoanPayment.objects.create(
                contract=self, installment_no=i,
                original_due_date=due, original_amount_due=amount,
                due_date=due, amount_due=amount,
            )


class InhouseLoanPayment(TimeStampedModel):
    """自社ローン返済（請求予定と入金実績を1レコードで管理）"""
    contract = models.ForeignKey(InhouseLoanContract, verbose_name="自社ローン契約", on_delete=models.PROTECT,
                                  related_name="payments")
    installment_no = models.PositiveIntegerField("第◯回")
    original_due_date = models.DateField("当初の予定支払期日")
    original_amount_due = models.PositiveIntegerField("当初の予定請求額")
    due_date = models.DateField("現在の支払期日")
    amount_due = models.PositiveIntegerField("現在の請求額")
    paid_amount = models.PositiveIntegerField("入金額", null=True, blank=True)
    paid_date = models.DateField("入金日", null=True, blank=True)
    payment_method = models.CharField("入金方法", max_length=30, blank=True)
    status = models.CharField("状況", max_length=10, choices=c.BILLING_STATUS_CHOICES, default="unpaid")
    notes = models.TextField("手動変更の理由メモ", blank=True)

    class Meta:
        verbose_name = "自社ローン返済"
        verbose_name_plural = "自社ローン返済"
        ordering = ["contract", "installment_no"]
        unique_together = [["contract", "installment_no"]]

    def __str__(self):
        return f"{self.contract} 第{self.installment_no}回"
