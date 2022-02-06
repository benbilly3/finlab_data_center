# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BrokerInfo(models.Model):
    stock_id = models.CharField(max_length=8)
    broker_name = models.CharField(max_length=16)
    date_of_establishment = models.CharField(max_length=16)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=16)
    department = models.CharField(max_length=16)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=8, blank=True, null=True)
    district = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'broker_info'


class BrokerTrade(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    buy_num = models.FloatField(blank=True, null=True)
    sell_num = models.FloatField(blank=True, null=True)
    net_bs = models.FloatField(blank=True, null=True)
    net_bs_cost = models.FloatField(blank=True, null=True)
    transactions_pt = models.FloatField(blank=True, null=True)
    broker_name = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'broker_trade'
        unique_together = (('stock_id', 'date', 'broker_name'),)


class CompanyInfo(models.Model):
    stock_id = models.CharField(max_length=12)
    update_time = models.DateTimeField()
    name = models.CharField(max_length=32, blank=True, null=True)
    short_name = models.CharField(max_length=16, blank=True, null=True)
    category = models.CharField(max_length=8, blank=True, null=True)
    registered_country = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    chairman = models.CharField(max_length=32, blank=True, null=True)
    ceo = models.CharField(max_length=32, blank=True, null=True)
    spokesman = models.CharField(max_length=32, blank=True, null=True)
    spokesman_title = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    establishment_date = models.CharField(max_length=32, blank=True, null=True)
    sii_date = models.CharField(max_length=32, blank=True, null=True)
    otc_date = models.CharField(max_length=32, blank=True, null=True)
    rotc_date = models.CharField(max_length=32, blank=True, null=True)
    capital = models.BigIntegerField(blank=True, null=True)
    shares_issued = models.BigIntegerField(blank=True, null=True)
    private_shares = models.BigIntegerField(blank=True, null=True)
    special_shares = models.BigIntegerField(blank=True, null=True)
    dividend_frequency = models.CharField(max_length=100, blank=True, null=True)
    stock_transfer_institution = models.CharField(max_length=100, blank=True, null=True)
    visa_accounting_firm = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    investor_relations_contact = models.CharField(max_length=100, blank=True, null=True)
    investor_relations_email = models.CharField(max_length=100, blank=True, null=True)
    english_abbreviation = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=8, blank=True, null=True)
    district = models.CharField(max_length=8, blank=True, null=True)
    market = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'company_info'


class FuturePrice(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    contract_date = models.CharField(max_length=16, blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    quote_change = models.FloatField(blank=True, null=True)
    turnover_vol = models.FloatField(blank=True, null=True)
    settlement_price = models.FloatField(blank=True, null=True)
    open_interest = models.FloatField(blank=True, null=True)
    best_bid = models.FloatField(blank=True, null=True)
    best_ask = models.FloatField(blank=True, null=True)
    trading_halt = models.CharField(max_length=16, blank=True, null=True)
    trading_session = models.CharField(max_length=16, blank=True, null=True)
    cross_contract_vol = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_price'
        unique_together = (('stock_id', 'date'),)


class InsiderShareholdingDeclarationTransfer(models.Model):
    date = models.DateTimeField()
    stock_id = models.CharField(max_length=16, blank=True, null=True)
    stock_name = models.CharField(max_length=16, blank=True, null=True)
    declarant_identity = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    shares_transfer_method = models.CharField(max_length=32, blank=True, null=True)
    transferred_shares_num = models.FloatField(blank=True, null=True)
    maximum_transferable_shares_in_one_day = models.FloatField(blank=True, null=True)
    assignee = models.CharField(max_length=128, blank=True, null=True)
    current_shares = models.FloatField(blank=True, null=True)
    current_shares_trust = models.FloatField(blank=True, null=True)
    transferred_own_shares_total_num = models.FloatField(blank=True, null=True)
    transferred_trust_shares_total_num = models.FloatField(blank=True, null=True)
    after_transfer_own_shareholding = models.FloatField(blank=True, null=True)
    after_transfer_trust_shareholding = models.FloatField(blank=True, null=True)
    declare_uncompleted_transfer = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    market = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insider_shareholding_declaration_transfer'
        unique_together = (('stock_id', 'date', 'name', 'assignee'),)


class MonthlyRevenue(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    stock_name = models.CharField(max_length=16, blank=True, null=True)
    this_month_rev = models.FloatField(blank=True, null=True)
    last_month_rev = models.FloatField(blank=True, null=True)
    last_year_rev = models.FloatField(blank=True, null=True)
    cp_last_month_rev = models.FloatField(blank=True, null=True)
    cp_last_year_rev = models.FloatField(blank=True, null=True)
    cm_this_month_rev = models.FloatField(blank=True, null=True)
    cm_last_year_rev = models.FloatField(blank=True, null=True)
    cp_cm_rev = models.FloatField(blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monthly_revenue'
        unique_together = (('stock_id', 'date'),)


class RotcStockPrice(models.Model):
    stock_id = models.CharField(max_length=8)
    date = models.DateTimeField()
    stock_name = models.CharField(max_length=16)
    vol = models.FloatField(blank=True, null=True)
    turnover_price = models.FloatField(blank=True, null=True)
    mean_price = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    transactions_number = models.FloatField(blank=True, null=True)
    finally_reveal_buy_price = models.FloatField(blank=True, null=True)
    finally_reveal_sell_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rotc_stock_price'
        unique_together = (('stock_id', 'date'),)


class Stock3PRatio(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    stock_name = models.CharField(max_length=16, blank=True, null=True)
    dividend_yield = models.FloatField(blank=True, null=True)
    pe = models.FloatField(blank=True, null=True)
    pb = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_3P_ratio'
        unique_together = (('stock_id', 'date'),)


class StockDivideRatio(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    stock_name = models.CharField(max_length=16, blank=True, null=True)
    divide_before = models.FloatField(blank=True, null=True)
    divide_after = models.FloatField(blank=True, null=True)
    divide_open = models.FloatField(blank=True, null=True)
    divide_value = models.FloatField(blank=True, null=True)
    divide_category = models.CharField(max_length=16, blank=True, null=True)
    divide_ratio = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_divide_ratio'
        unique_together = (('stock_id', 'date', 'divide_category'),)


class StockIndexPrice(models.Model):
    stock_id = models.CharField(max_length=24)
    date = models.DateTimeField()
    index_price = models.FloatField(blank=True, null=True)
    quote_change = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_index_price'
        unique_together = (('stock_id', 'date'),)


class StockIndexVol(models.Model):
    stock_id = models.CharField(max_length=24)
    date = models.DateTimeField()
    turnover_vol = models.FloatField(blank=True, null=True)
    turnover_price = models.FloatField(blank=True, null=True)
    turnover_num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_index_vol'
        unique_together = (('stock_id', 'date'),)


class StockInsiderHold(models.Model):
    stock_id = models.CharField(max_length=8)
    date = models.DateTimeField()
    stock_name = models.CharField(max_length=16, blank=True, null=True)
    issued_num = models.FloatField(blank=True, null=True)
    director_add = models.FloatField(blank=True, null=True)
    director_lower = models.FloatField(blank=True, null=True)
    director_hold = models.FloatField(blank=True, null=True)
    director_hold_ratio = models.FloatField(blank=True, null=True)
    manager_hold = models.FloatField(blank=True, null=True)
    big10_hold = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_insider_hold'
        unique_together = (('stock_id', 'date'),)


class StockInsiderHoldDetail(models.Model):
    stock_id = models.CharField(max_length=8)
    date = models.DateTimeField()
    title = models.CharField(max_length=16, blank=True, null=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    act_hold = models.FloatField(blank=True, null=True)
    hold = models.FloatField(blank=True, null=True)
    pledge = models.FloatField(blank=True, null=True)
    pledge_ratio = models.FloatField(blank=True, null=True)
    family_hold = models.FloatField(blank=True, null=True)
    family_pledge = models.FloatField(blank=True, null=True)
    family_pledge_ratio = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_insider_hold_detail'
        unique_together = (('stock_id', 'date'),)


class StockListTaifex(models.Model):
    stock_id = models.CharField(max_length=16)
    spot_id = models.CharField(max_length=16, blank=True, null=True)
    stock_name = models.CharField(max_length=24)
    check_fc = models.IntegerField()
    check_opt = models.IntegerField()
    check_sii = models.IntegerField()
    check_otc = models.IntegerField()
    check_etf = models.IntegerField()
    spot_unit = models.FloatField(blank=True, null=True)
    company_info = models.ForeignKey(CompanyInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_list_taifex'


class StockMarginTransactions(models.Model):
    stock_id = models.CharField(max_length=8)
    date = models.DateTimeField()
    stock_name = models.CharField(max_length=16)
    mt_buy = models.FloatField(blank=True, null=True)
    mt_sell = models.FloatField(blank=True, null=True)
    cash_redemption = models.FloatField(blank=True, null=True)
    mt_balance_pd = models.FloatField(blank=True, null=True)
    mt_balance_now = models.FloatField(blank=True, null=True)
    mt_quota = models.FloatField(blank=True, null=True)
    short_covering = models.FloatField(blank=True, null=True)
    short_sale = models.FloatField(blank=True, null=True)
    stock_redemption = models.FloatField(blank=True, null=True)
    ss_balance_pd = models.FloatField(blank=True, null=True)
    ss_balance_now = models.FloatField(blank=True, null=True)
    ss_quota = models.FloatField(blank=True, null=True)
    offset = models.FloatField(blank=True, null=True)
    note = models.CharField(max_length=64, blank=True, null=True)
    mt_use_rate = models.FloatField(blank=True, null=True)
    ss_use_rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_margin_transactions'
        unique_together = (('stock_id', 'date'),)


class StockPrice(models.Model):
    stock_id = models.CharField(max_length=8)
    date = models.DateTimeField()
    stock_name = models.CharField(max_length=16)
    vol = models.FloatField(blank=True, null=True)
    turnover_price = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    transactions_number = models.FloatField(blank=True, null=True)
    finally_reveal_buy_price = models.FloatField(blank=True, null=True)
    finally_reveal_sell_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_price'
        unique_together = (('stock_id', 'date'),)


class StockTdcc(models.Model):
    stock_id = models.CharField(max_length=8)
    date = models.DateTimeField()
    hold_class = models.IntegerField(blank=True, null=True)
    people = models.IntegerField(blank=True, null=True)
    hold_num = models.FloatField(blank=True, null=True)
    hold_pt = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_tdcc'
        unique_together = (('stock_id', 'date', 'hold_class'),)


class StockTii(models.Model):
    stock_id = models.CharField(max_length=8)
    date = models.DateTimeField()
    stock_name = models.CharField(max_length=16, blank=True, null=True)
    fm_buy = models.FloatField(blank=True, null=True)
    fm_sell = models.FloatField(blank=True, null=True)
    fm_net = models.FloatField(blank=True, null=True)
    fd_buy = models.FloatField(blank=True, null=True)
    fd_sell = models.FloatField(blank=True, null=True)
    fd_net = models.FloatField(blank=True, null=True)
    ft_net = models.FloatField(blank=True, null=True)
    itc_buy = models.FloatField(blank=True, null=True)
    itc_sell = models.FloatField(blank=True, null=True)
    itc_net = models.FloatField(blank=True, null=True)
    dealer_ppt_buy = models.FloatField(blank=True, null=True)
    dealer_ppt_sell = models.FloatField(blank=True, null=True)
    dealer_ppt_net = models.FloatField(blank=True, null=True)
    dealer_hedge_buy = models.FloatField(blank=True, null=True)
    dealer_hedge_sell = models.FloatField(blank=True, null=True)
    dealer_hedge_net = models.FloatField(blank=True, null=True)
    dealer_net = models.FloatField(blank=True, null=True)
    tii_net = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_tii'
        unique_together = (('stock_id', 'date'),)


class StockTiiMarket(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    buy_price = models.FloatField(blank=True, null=True)
    sell_price = models.FloatField(blank=True, null=True)
    net = models.FloatField(blank=True, null=True)
    market = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'stock_tii_market'
        unique_together = (('stock_id', 'date', 'market'),)


class TejFundamental(models.Model):
    stock_id = models.CharField(max_length=16, blank=True, null=True)
    date = models.DateTimeField()
    上市別 = models.CharField(max_length=16, blank=True, null=True)
    季別 = models.CharField(max_length=16, blank=True, null=True)
    合併_y_n = models.CharField(max_length=16, blank=True, null=True)
    單季_q_單半年_h = models.CharField(max_length=16, blank=True, null=True)
    月份 = models.CharField(max_length=16, blank=True, null=True)
    幣別 = models.CharField(max_length=16, blank=True, null=True)
    現金及約當現金 = models.FloatField(blank=True, null=True)
    透過損益按公允價值衡量之金融資產_流動 = models.FloatField(blank=True, null=True)
    合約資產_流動 = models.FloatField(blank=True, null=True)
    應收帳款及票據 = models.FloatField(blank=True, null=True)
    其他應收款 = models.FloatField(blank=True, null=True)
    資金貸予他人_流動 = models.FloatField(blank=True, null=True)
    存貨 = models.FloatField(blank=True, null=True)
    待出售非流動資產 = models.FloatField(blank=True, null=True)
    當期所得稅資產_流動 = models.FloatField(blank=True, null=True)
    流動資產 = models.FloatField(blank=True, null=True)
    按攤銷後成本衡量之金融資產_非流動 = models.FloatField(blank=True, null=True)
    採權益法之長期股權投資 = models.FloatField(blank=True, null=True)
    預付投資款 = models.FloatField(blank=True, null=True)
    不動產廠房及設備 = models.FloatField(blank=True, null=True)
    商譽及無形資產合計 = models.FloatField(blank=True, null=True)
    遞延所得稅資產 = models.FloatField(blank=True, null=True)
    投資性不動產淨額 = models.FloatField(blank=True, null=True)
    其他非流動資產 = models.FloatField(blank=True, null=True)
    非流動資產 = models.FloatField(blank=True, null=True)
    資產總額 = models.FloatField(blank=True, null=True)
    短期借款 = models.FloatField(blank=True, null=True)
    透過損益按公允價值衡量之金融負債_流動 = models.FloatField(blank=True, null=True)
    合約負債_流動 = models.FloatField(blank=True, null=True)
    應付帳款及票據 = models.FloatField(blank=True, null=True)
    其他應付款 = models.FloatField(blank=True, null=True)
    當期所得稅負債 = models.FloatField(blank=True, null=True)
    與待出售非流動資產直接相關之負債 = models.FloatField(blank=True, null=True)
    一年內到期長期負債 = models.FloatField(blank=True, null=True)
    流動負債 = models.FloatField(blank=True, null=True)
    透過損益按公允價值衡量之金融負債_非流動 = models.FloatField(blank=True, null=True)
    應付公司債_非流動 = models.FloatField(blank=True, null=True)
    銀行借款_非流動 = models.FloatField(blank=True, null=True)
    負債準備_非流動 = models.FloatField(blank=True, null=True)
    應計退休金負債 = models.FloatField(blank=True, null=True)
    遞延所得稅 = models.FloatField(blank=True, null=True)
    非流動負債 = models.FloatField(blank=True, null=True)
    負債總額 = models.FloatField(blank=True, null=True)
    股本 = models.FloatField(blank=True, null=True)
    資本公積合計 = models.FloatField(blank=True, null=True)
    法定盈餘公積 = models.FloatField(blank=True, null=True)
    特別盈餘公積 = models.FloatField(blank=True, null=True)
    未分配盈餘 = models.FloatField(blank=True, null=True)
    保留盈餘 = models.FloatField(blank=True, null=True)
    其他權益 = models.FloatField(blank=True, null=True)
    庫藏股票帳面值 = models.FloatField(blank=True, null=True)
    母公司股東權益合計 = models.FloatField(blank=True, null=True)
    共同控制下前手權益 = models.FloatField(blank=True, null=True)
    合併前非屬共同控制股權 = models.FloatField(blank=True, null=True)
    非控制權益 = models.FloatField(blank=True, null=True)
    股東權益總額 = models.FloatField(blank=True, null=True)
    負債及股東權益總額 = models.FloatField(blank=True, null=True)
    營業收入淨額 = models.FloatField(blank=True, null=True)
    營業成本 = models.FloatField(blank=True, null=True)
    營業毛利 = models.FloatField(blank=True, null=True)
    營業費用 = models.FloatField(blank=True, null=True)
    研究發展費 = models.FloatField(blank=True, null=True)
    預期信用減損_損失_利益_營業費用 = models.FloatField(blank=True, null=True)
    營業利益 = models.FloatField(blank=True, null=True)
    其他收入 = models.FloatField(blank=True, null=True)
    其他利益及損失 = models.FloatField(blank=True, null=True)
    財務成本 = models.FloatField(blank=True, null=True)
    採權益法之關聯企業及合資損益之份額 = models.FloatField(blank=True, null=True)
    預期信用減損_損失_利益 = models.FloatField(blank=True, null=True)
    除列按攤銷後成本衡量金融資產淨損益 = models.FloatField(blank=True, null=True)
    金融資產重分類淨損益 = models.FloatField(blank=True, null=True)
    營業外收入及支出_其他 = models.FloatField(blank=True, null=True)
    營業外收入及支出 = models.FloatField(blank=True, null=True)
    稅前淨利 = models.FloatField(blank=True, null=True)
    所得稅費用 = models.FloatField(blank=True, null=True)
    繼續營業單位損益 = models.FloatField(blank=True, null=True)
    停業單位損益 = models.FloatField(blank=True, null=True)
    合併前非屬共同控制股權損益 = models.FloatField(blank=True, null=True)
    其他損益調整項_非常項目及累計影響數 = models.FloatField(blank=True, null=True)
    合併總損益 = models.FloatField(blank=True, null=True)
    其他綜合損益_oci = models.FloatField(blank=True, null=True)
    本期綜合損益總額 = models.FloatField(blank=True, null=True)
    歸屬母公司淨利_損 = models.FloatField(blank=True, null=True)
    歸屬非控制權益淨利_損 = models.FloatField(blank=True, null=True)
    歸屬共同控制下前手權益淨利_損 = models.FloatField(blank=True, null=True)
    綜合損益歸屬母公司 = models.FloatField(blank=True, null=True)
    綜合損益歸屬非控制權益 = models.FloatField(blank=True, null=True)
    綜合損益歸屬共同控制下前手權益 = models.FloatField(blank=True, null=True)
    每股盈餘 = models.FloatField(blank=True, null=True)
    加權平均股數 = models.FloatField(blank=True, null=True)
    發放特別股股息 = models.FloatField(blank=True, null=True)
    稀釋稅後淨利 = models.FloatField(blank=True, null=True)
    每股盈餘_完全稀釋 = models.FloatField(blank=True, null=True)
    加權平均股數_稀釋 = models.FloatField(blank=True, null=True)
    稅前息前淨利 = models.FloatField(blank=True, null=True)
    稅前息前折舊前淨利 = models.FloatField(blank=True, null=True)
    常續性稅後淨利 = models.FloatField(blank=True, null=True)
    期末普通股_現金股利 = models.FloatField(blank=True, null=True)
    期末普通股_股票股利 = models.FloatField(blank=True, null=True)
    普通股每股現金股利_盈餘及公積 = models.FloatField(blank=True, null=True)
    普通股每股現金股利_盈餘 = models.FloatField(blank=True, null=True)
    普通股每股現金股利_公積 = models.FloatField(blank=True, null=True)
    普通股每股股票股利_盈餘 = models.FloatField(blank=True, null=True)
    普通股每股股票股利_公積 = models.FloatField(blank=True, null=True)
    資本公積_現金股利 = models.FloatField(blank=True, null=True)
    資本公積轉增資_股票股利 = models.FloatField(blank=True, null=True)
    稅前淨利_cfo = models.FloatField(blank=True, null=True)
    折舊_cfo = models.FloatField(blank=True, null=True)
    攤提_cfo = models.FloatField(blank=True, null=True)
    來自營運之現金流量 = models.FloatField(blank=True, null=True)
    新增投資_cfi = models.FloatField(blank=True, null=True)
    出售投資_cfi = models.FloatField(blank=True, null=True)
    購置不動產廠房設備_含預付_cfi = models.FloatField(blank=True, null=True)
    處分不動產廠房設備_含預付_cfi = models.FloatField(blank=True, null=True)
    投資活動之現金流量 = models.FloatField(blank=True, null=True)
    現金增_減_資_cff = models.FloatField(blank=True, null=True)
    支付現金股利_cff = models.FloatField(blank=True, null=True)
    籌資活動之現金流量 = models.FloatField(blank=True, null=True)
    匯率影響數 = models.FloatField(blank=True, null=True)
    本期產生現金流量 = models.FloatField(blank=True, null=True)
    期初現金及約當現金 = models.FloatField(blank=True, null=True)
    期末現金及約當現金 = models.FloatField(blank=True, null=True)
    預計稅額扣抵比率 = models.FloatField(blank=True, null=True)
    稅額扣抵比率 = models.FloatField(blank=True, null=True)
    bs透過損益按公允價值衡量之金融資產_流動_ifrs = models.FloatField(blank=True, null=True)
    bs持有至到期日金融資產_非流動 = models.FloatField(blank=True, null=True)
    bs透過損益按公允價值衡量之金融負債_流動_ifrs = models.FloatField(blank=True, null=True)
    bs應付建造合約款 = models.FloatField(blank=True, null=True)
    bs以成本衡量之金融負債_非流動 = models.FloatField(blank=True, null=True)
    roa_c_稅前息前折舊前 = models.FloatField(blank=True, null=True)
    roa_a_稅後息前 = models.FloatField(blank=True, null=True)
    roa_b_稅後息前折舊前 = models.FloatField(blank=True, null=True)
    roa_綜合損益 = models.FloatField(blank=True, null=True)
    roe_a_稅後 = models.FloatField(blank=True, null=True)
    稅前息前折舊前淨利率 = models.FloatField(blank=True, null=True)
    roe_b_常續利益 = models.FloatField(blank=True, null=True)
    roe_綜合損益 = models.FloatField(blank=True, null=True)
    營業毛利率 = models.FloatField(blank=True, null=True)
    已實現銷貨毛利率 = models.FloatField(blank=True, null=True)
    營業利益率 = models.FloatField(blank=True, null=True)
    稅前淨利率 = models.FloatField(blank=True, null=True)
    稅後淨利率 = models.FloatField(blank=True, null=True)
    業外收支_營收 = models.FloatField(blank=True, null=True)
    常續利益率_稅後 = models.FloatField(blank=True, null=True)
    貝里比率 = models.FloatField(blank=True, null=True)
    營業資產報酬率 = models.FloatField(blank=True, null=True)
    員工人數 = models.FloatField(blank=True, null=True)
    營業費用率 = models.FloatField(blank=True, null=True)
    用人費用率 = models.FloatField(blank=True, null=True)
    研究發展費用率 = models.FloatField(blank=True, null=True)
    呆帳費用率 = models.FloatField(blank=True, null=True)
    現金流量比率 = models.FloatField(blank=True, null=True)
    有息負債利率 = models.FloatField(blank=True, null=True)
    稅率_a = models.FloatField(blank=True, null=True)
    稅率_b = models.FloatField(blank=True, null=True)
    每股淨值_b = models.FloatField(blank=True, null=True)
    每股淨值_a = models.FloatField(blank=True, null=True)
    每股淨值_c = models.FloatField(blank=True, null=True)
    每股淨值_f_tse公告數 = models.FloatField(blank=True, null=True)
    常續性eps = models.FloatField(blank=True, null=True)
    每股現金流量 = models.FloatField(blank=True, null=True)
    每股營業額 = models.FloatField(blank=True, null=True)
    每股營業利益 = models.FloatField(blank=True, null=True)
    每股稅前淨利 = models.FloatField(blank=True, null=True)
    每股綜合損益 = models.FloatField(blank=True, null=True)
    季底每股稅前淨利 = models.FloatField(blank=True, null=True)
    季底每股稅後淨利 = models.FloatField(blank=True, null=True)
    營收成長率 = models.FloatField(blank=True, null=True)
    營業毛利成長率 = models.FloatField(blank=True, null=True)
    已實現銷貨毛利成長率 = models.FloatField(blank=True, null=True)
    營業利益成長率 = models.FloatField(blank=True, null=True)
    稅前淨利成長率 = models.FloatField(blank=True, null=True)
    稅後淨利成長率 = models.FloatField(blank=True, null=True)
    經常淨利成長率 = models.FloatField(blank=True, null=True)
    常續淨利成長率 = models.FloatField(blank=True, null=True)
    總資產成長率 = models.FloatField(blank=True, null=True)
    淨值成長率 = models.FloatField(blank=True, null=True)
    折舊性fa成長率 = models.FloatField(blank=True, null=True)
    總資產報酬成長率 = models.FloatField(blank=True, null=True)
    營收變動率 = models.FloatField(blank=True, null=True)
    營業利益變動率 = models.FloatField(blank=True, null=True)
    淨利變動率_單季 = models.FloatField(blank=True, null=True)
    稅前盈餘變動率 = models.FloatField(blank=True, null=True)
    現金流量允當比 = models.FloatField(blank=True, null=True)
    現金再投資比 = models.FloatField(blank=True, null=True)
    流動比率 = models.FloatField(blank=True, null=True)
    速動比率 = models.FloatField(blank=True, null=True)
    利息支出率 = models.FloatField(blank=True, null=True)
    利息支出率_b = models.FloatField(blank=True, null=True)
    總負債_總淨值 = models.FloatField(blank=True, null=True)
    負債比率 = models.FloatField(blank=True, null=True)
    淨值_資產 = models.FloatField(blank=True, null=True)
    長期資金適合率_a = models.FloatField(blank=True, null=True)
    長短期借款 = models.FloatField(blank=True, null=True)
    借款依存度 = models.FloatField(blank=True, null=True)
    或有負債_淨值 = models.FloatField(blank=True, null=True)
    利息保障倍數 = models.FloatField(blank=True, null=True)
    內部保留比率 = models.FloatField(blank=True, null=True)
    營運資金 = models.FloatField(blank=True, null=True)
    股利支付率 = models.FloatField(blank=True, null=True)
    存貨及應收帳款_淨值 = models.FloatField(blank=True, null=True)
    應收帳款週轉次數 = models.FloatField(blank=True, null=True)
    總資產週轉次數 = models.FloatField(blank=True, null=True)
    平均收帳天數 = models.FloatField(blank=True, null=True)
    存貨週轉率_次 = models.FloatField(blank=True, null=True)
    平均售貨天數 = models.FloatField(blank=True, null=True)
    固定資產週轉次數 = models.FloatField(blank=True, null=True)
    淨值週轉率_次 = models.FloatField(blank=True, null=True)
    應付帳款付現天數 = models.FloatField(blank=True, null=True)
    淨營業週期_日 = models.FloatField(blank=True, null=True)
    季底收款天數 = models.FloatField(blank=True, null=True)
    季底售貨天數 = models.FloatField(blank=True, null=True)
    自由現金流量_d = models.FloatField(blank=True, null=True)
    營運槓桿度 = models.FloatField(blank=True, null=True)
    財務槓桿度 = models.FloatField(blank=True, null=True)
    每人營收 = models.FloatField(blank=True, null=True)
    每人營業利益 = models.FloatField(blank=True, null=True)
    每人配備率 = models.FloatField(blank=True, null=True)
    季底普通股市值 = models.FloatField(blank=True, null=True)
    當季季底p_e = models.FloatField(blank=True, null=True)
    當季季底p_b = models.FloatField(blank=True, null=True)
    當季季底psr = models.FloatField(blank=True, null=True)
    股利殖利率 = models.FloatField(blank=True, null=True)
    現金股利率 = models.FloatField(blank=True, null=True)
    tobinsq = models.CharField(max_length=16, blank=True, null=True)
    tobinsq_a = models.CharField(max_length=16, blank=True, null=True)
    財報發布日 = models.CharField(max_length=16, blank=True, null=True)
    財報類別_1個別2個體3合併 = models.CharField(max_length=16, blank=True, null=True)
    財報年月起日 = models.CharField(max_length=16, blank=True, null=True)
    財報年月迄日 = models.CharField(max_length=16, blank=True, null=True)
    市場別 = models.CharField(max_length=16, blank=True, null=True)
    交易所主產業代碼 = models.CharField(max_length=16, blank=True, null=True)
    交易所子產業代碼 = models.CharField(max_length=16, blank=True, null=True)
    tej主產業代碼 = models.CharField(max_length=16, blank=True, null=True)
    tej子產業代碼 = models.CharField(max_length=16, blank=True, null=True)
    財報附註tej是否完成y_n = models.CharField(max_length=16, blank=True, null=True)
    透過其他綜合損益按公允價值衡量之金融資產_流動 = models.FloatField(blank=True, null=True)
    按攤銷後成本衡量之金融資產_流動 = models.FloatField(blank=True, null=True)
    避險之金融資產_流動 = models.FloatField(blank=True, null=True)
    透過損益按公允價值衡量之金融資產_非流動 = models.FloatField(blank=True, null=True)
    透過其他綜合損益按公允價值衡量之金融資產_非流動 = models.FloatField(blank=True, null=True)
    避險之金融資產_非流動 = models.FloatField(blank=True, null=True)
    合約資產_非流動 = models.FloatField(blank=True, null=True)
    遞延資產合計 = models.FloatField(blank=True, null=True)
    使用權資產 = models.FloatField(blank=True, null=True)
    應付商業本票_承兌匯票 = models.FloatField(blank=True, null=True)
    避險之金融負債_流動 = models.FloatField(blank=True, null=True)
    按攤銷後成本衡量之金融負債_流動 = models.FloatField(blank=True, null=True)
    負債準備_流動 = models.FloatField(blank=True, null=True)
    租賃負債_流動 = models.FloatField(blank=True, null=True)
    特別股負債_流動 = models.FloatField(blank=True, null=True)
    避險之金融負債_非流動 = models.FloatField(blank=True, null=True)
    按攤銷後成本衡量之金融負債_非流動 = models.FloatField(blank=True, null=True)
    合約負債_非流動 = models.FloatField(blank=True, null=True)
    特別股負債_非流動 = models.FloatField(blank=True, null=True)
    其他長期借款_非流動 = models.FloatField(blank=True, null=True)
    租賃負債_非流動 = models.FloatField(blank=True, null=True)
    遞延貸項 = models.FloatField(blank=True, null=True)
    普通股股本 = models.FloatField(blank=True, null=True)
    特別股股本 = models.FloatField(blank=True, null=True)
    預收股款 = models.FloatField(blank=True, null=True)
    待分配股票股利 = models.FloatField(blank=True, null=True)
    換股權利證書 = models.FloatField(blank=True, null=True)
    聯屬公司已_未_實現銷貨利益 = models.FloatField(blank=True, null=True)
    已實現銷貨毛利 = models.FloatField(blank=True, null=True)
    其他收益及費損淨額 = models.FloatField(blank=True, null=True)
    利息收入 = models.FloatField(blank=True, null=True)
    不重分類至損益之項目_oci = models.FloatField(blank=True, null=True)
    後續可能重分類至損益之項目_oci = models.FloatField(blank=True, null=True)
    合併前非屬共同控制股權綜合損益淨額_oci = models.FloatField(blank=True, null=True)
    期中普通股_現金股利 = models.FloatField(blank=True, null=True)
    期中普通股_股票股利 = models.FloatField(blank=True, null=True)
    期中特別股_現金股利 = models.FloatField(blank=True, null=True)
    期中特別股_股票股利 = models.FloatField(blank=True, null=True)
    期末特別股_現金股利 = models.FloatField(blank=True, null=True)
    期末特別股_股票股利 = models.FloatField(blank=True, null=True)
    淨負債 = models.FloatField(blank=True, null=True)
    營業利益_實收資本比 = models.FloatField(blank=True, null=True)
    稅前純益_實收資本 = models.FloatField(blank=True, null=True)
    季底應收帳款_營收tse = models.FloatField(blank=True, null=True)
    季底存貨_營收tse = models.FloatField(blank=True, null=True)
    stock_name = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tej_fundamental'
        unique_together = (('stock_id', 'date'),)
