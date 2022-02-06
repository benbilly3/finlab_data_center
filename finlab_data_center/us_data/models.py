# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IndexComponents(models.Model):
    id = models.IntegerField(primary_key=True)
    stock_id = models.CharField(max_length=16)
    name = models.CharField(max_length=64, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    index_name = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'index_components'
        unique_together = (('stock_id', 'index_name'),)


class SharadarActions(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    action = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    contraticker = models.CharField(max_length=32, blank=True, null=True)
    contraname = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharadar_actions'
        unique_together = (('stock_id', 'date'),)


class SharadarDaily(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    ev = models.FloatField(blank=True, null=True)
    evebit = models.FloatField(blank=True, null=True)
    evebitda = models.FloatField(blank=True, null=True)
    marketcap = models.FloatField(blank=True, null=True)
    pb = models.FloatField(blank=True, null=True)
    pe = models.FloatField(blank=True, null=True)
    ps = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharadar_daily'
        unique_together = (('stock_id', 'date'),)


class SharadarSep(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    dividends = models.FloatField(blank=True, null=True)
    closeunadj = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharadar_sep'
        unique_together = (('stock_id', 'date'),)


class SharadarSf1(models.Model):
    stock_id = models.CharField(max_length=16)
    datekey = models.DateTimeField(blank=True, null=True)
    dimension = models.CharField(max_length=8, blank=True, null=True)
    date = models.DateTimeField()
    reportperiod = models.DateTimeField(blank=True, null=True)
    lastupdated = models.DateTimeField(blank=True, null=True)
    accoci = models.FloatField(blank=True, null=True)
    assets = models.FloatField(blank=True, null=True)
    assetsavg = models.FloatField(blank=True, null=True)
    assetsc = models.FloatField(blank=True, null=True)
    assetsnc = models.FloatField(blank=True, null=True)
    assetturnover = models.FloatField(blank=True, null=True)
    bvps = models.FloatField(blank=True, null=True)
    capex = models.FloatField(blank=True, null=True)
    cashneq = models.FloatField(blank=True, null=True)
    cashnequsd = models.FloatField(blank=True, null=True)
    cor = models.FloatField(blank=True, null=True)
    consolinc = models.FloatField(blank=True, null=True)
    currentratio = models.FloatField(blank=True, null=True)
    de = models.FloatField(blank=True, null=True)
    debt = models.FloatField(blank=True, null=True)
    debtc = models.FloatField(blank=True, null=True)
    debtnc = models.FloatField(blank=True, null=True)
    debtusd = models.FloatField(blank=True, null=True)
    deferredrev = models.FloatField(blank=True, null=True)
    depamor = models.FloatField(blank=True, null=True)
    deposits = models.FloatField(blank=True, null=True)
    divyield = models.FloatField(blank=True, null=True)
    dps = models.FloatField(blank=True, null=True)
    ebit = models.FloatField(blank=True, null=True)
    ebitda = models.FloatField(blank=True, null=True)
    ebitdamargin = models.FloatField(blank=True, null=True)
    ebitdausd = models.FloatField(blank=True, null=True)
    ebitusd = models.FloatField(blank=True, null=True)
    ebt = models.FloatField(blank=True, null=True)
    eps = models.FloatField(blank=True, null=True)
    epsdil = models.FloatField(blank=True, null=True)
    epsusd = models.FloatField(blank=True, null=True)
    equity = models.FloatField(blank=True, null=True)
    equityavg = models.FloatField(blank=True, null=True)
    equityusd = models.FloatField(blank=True, null=True)
    ev = models.FloatField(blank=True, null=True)
    evebit = models.FloatField(blank=True, null=True)
    evebitda = models.FloatField(blank=True, null=True)
    fcf = models.FloatField(blank=True, null=True)
    fcfps = models.FloatField(blank=True, null=True)
    fxusd = models.FloatField(blank=True, null=True)
    gp = models.FloatField(blank=True, null=True)
    grossmargin = models.FloatField(blank=True, null=True)
    intangibles = models.FloatField(blank=True, null=True)
    intexp = models.FloatField(blank=True, null=True)
    invcap = models.FloatField(blank=True, null=True)
    invcapavg = models.FloatField(blank=True, null=True)
    inventory = models.FloatField(blank=True, null=True)
    investments = models.FloatField(blank=True, null=True)
    investmentsc = models.FloatField(blank=True, null=True)
    investmentsnc = models.FloatField(blank=True, null=True)
    liabilities = models.FloatField(blank=True, null=True)
    liabilitiesc = models.FloatField(blank=True, null=True)
    liabilitiesnc = models.FloatField(blank=True, null=True)
    marketcap = models.FloatField(blank=True, null=True)
    ncf = models.FloatField(blank=True, null=True)
    ncfbus = models.FloatField(blank=True, null=True)
    ncfcommon = models.FloatField(blank=True, null=True)
    ncfdebt = models.FloatField(blank=True, null=True)
    ncfdiv = models.FloatField(blank=True, null=True)
    ncff = models.FloatField(blank=True, null=True)
    ncfi = models.FloatField(blank=True, null=True)
    ncfinv = models.FloatField(blank=True, null=True)
    ncfo = models.FloatField(blank=True, null=True)
    ncfx = models.FloatField(blank=True, null=True)
    netinc = models.FloatField(blank=True, null=True)
    netinccmn = models.FloatField(blank=True, null=True)
    netinccmnusd = models.FloatField(blank=True, null=True)
    netincdis = models.FloatField(blank=True, null=True)
    netincnci = models.FloatField(blank=True, null=True)
    netmargin = models.FloatField(blank=True, null=True)
    opex = models.FloatField(blank=True, null=True)
    opinc = models.FloatField(blank=True, null=True)
    payables = models.FloatField(blank=True, null=True)
    payoutratio = models.FloatField(blank=True, null=True)
    pb = models.FloatField(blank=True, null=True)
    pe = models.FloatField(blank=True, null=True)
    pe1 = models.FloatField(blank=True, null=True)
    ppnenet = models.FloatField(blank=True, null=True)
    prefdivis = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    ps = models.FloatField(blank=True, null=True)
    ps1 = models.FloatField(blank=True, null=True)
    receivables = models.FloatField(blank=True, null=True)
    retearn = models.FloatField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    revenueusd = models.FloatField(blank=True, null=True)
    rnd = models.FloatField(blank=True, null=True)
    roa = models.FloatField(blank=True, null=True)
    roe = models.FloatField(blank=True, null=True)
    roic = models.FloatField(blank=True, null=True)
    ros = models.FloatField(blank=True, null=True)
    sbcomp = models.FloatField(blank=True, null=True)
    sgna = models.FloatField(blank=True, null=True)
    sharefactor = models.FloatField(blank=True, null=True)
    sharesbas = models.FloatField(blank=True, null=True)
    shareswa = models.FloatField(blank=True, null=True)
    shareswadil = models.FloatField(blank=True, null=True)
    sps = models.FloatField(blank=True, null=True)
    tangibles = models.FloatField(blank=True, null=True)
    taxassets = models.FloatField(blank=True, null=True)
    taxexp = models.FloatField(blank=True, null=True)
    taxliabilities = models.FloatField(blank=True, null=True)
    tbvps = models.FloatField(blank=True, null=True)
    workingcapital = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharadar_sf1'
        unique_together = (('stock_id', 'date', 'dimension'),)


class SharadarSf3A(models.Model):
    stock_id = models.CharField(max_length=16)
    date = models.DateTimeField()
    name = models.CharField(max_length=64)
    shrholders = models.FloatField(blank=True, null=True)
    cllholders = models.FloatField(blank=True, null=True)
    putholders = models.FloatField(blank=True, null=True)
    wntholders = models.FloatField(blank=True, null=True)
    dbtholders = models.FloatField(blank=True, null=True)
    prfholders = models.FloatField(blank=True, null=True)
    fndholders = models.FloatField(blank=True, null=True)
    undholders = models.FloatField(blank=True, null=True)
    shrunits = models.FloatField(blank=True, null=True)
    cllunits = models.FloatField(blank=True, null=True)
    putunits = models.FloatField(blank=True, null=True)
    wntunits = models.FloatField(blank=True, null=True)
    dbtunits = models.FloatField(blank=True, null=True)
    prfunits = models.FloatField(blank=True, null=True)
    fndunits = models.FloatField(blank=True, null=True)
    undunits = models.FloatField(blank=True, null=True)
    shrvalue = models.FloatField(blank=True, null=True)
    cllvalue = models.FloatField(blank=True, null=True)
    putvalue = models.FloatField(blank=True, null=True)
    wntvalue = models.FloatField(blank=True, null=True)
    dbtvalue = models.FloatField(blank=True, null=True)
    prfvalue = models.FloatField(blank=True, null=True)
    fndvalue = models.FloatField(blank=True, null=True)
    undvalue = models.FloatField(blank=True, null=True)
    totalvalue = models.FloatField(blank=True, null=True)
    percentoftotal = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharadar_sf3a'
        unique_together = (('stock_id', 'date'),)


class SharadarSf3B(models.Model):
    investorname = models.CharField(max_length=64)
    date = models.DateTimeField()
    shrholdings = models.FloatField(blank=True, null=True)
    cllholdings = models.FloatField(blank=True, null=True)
    putholdings = models.FloatField(blank=True, null=True)
    wntholdings = models.FloatField(blank=True, null=True)
    dbtholdings = models.FloatField(blank=True, null=True)
    prfholdings = models.FloatField(blank=True, null=True)
    fndholdings = models.FloatField(blank=True, null=True)
    undholdings = models.FloatField(blank=True, null=True)
    shrunits = models.FloatField(blank=True, null=True)
    cllunits = models.FloatField(blank=True, null=True)
    putunits = models.FloatField(blank=True, null=True)
    wntunits = models.FloatField(blank=True, null=True)
    dbtunits = models.FloatField(blank=True, null=True)
    prfunits = models.FloatField(blank=True, null=True)
    fndunits = models.FloatField(blank=True, null=True)
    undunits = models.FloatField(blank=True, null=True)
    shrvalue = models.FloatField(blank=True, null=True)
    cllvalue = models.FloatField(blank=True, null=True)
    putvalue = models.FloatField(blank=True, null=True)
    wntvalue = models.FloatField(blank=True, null=True)
    dbtvalue = models.FloatField(blank=True, null=True)
    prfvalue = models.FloatField(blank=True, null=True)
    fndvalue = models.FloatField(blank=True, null=True)
    undvalue = models.FloatField(blank=True, null=True)
    totalvalue = models.FloatField(blank=True, null=True)
    percentoftotal = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharadar_sf3b'
        unique_together = (('investorname', 'date'),)


class SharadarTickers(models.Model):
    stock_id = models.CharField(max_length=16)
    table = models.CharField(max_length=16)
    permaticker = models.CharField(max_length=16, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    exchange = models.CharField(max_length=16, blank=True, null=True)
    isdelisted = models.CharField(max_length=4, blank=True, null=True)
    category = models.CharField(max_length=16, blank=True, null=True)
    cusips = models.CharField(max_length=16, blank=True, null=True)
    siccode = models.CharField(max_length=16, blank=True, null=True)
    sicsector = models.CharField(max_length=16, blank=True, null=True)
    sicindustry = models.CharField(max_length=16, blank=True, null=True)
    famasector = models.CharField(max_length=16, blank=True, null=True)
    famaindustry = models.CharField(max_length=16, blank=True, null=True)
    sector = models.CharField(max_length=16, blank=True, null=True)
    industry = models.CharField(max_length=16, blank=True, null=True)
    scalemarketcap = models.CharField(max_length=16, blank=True, null=True)
    scalerevenue = models.CharField(max_length=16, blank=True, null=True)
    relatedtickers = models.CharField(max_length=16, blank=True, null=True)
    currency = models.CharField(max_length=8, blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    lastupdated = models.DateTimeField(blank=True, null=True)
    firstadded = models.DateTimeField(blank=True, null=True)
    firstpricedate = models.DateTimeField(blank=True, null=True)
    lastpricedate = models.DateTimeField(blank=True, null=True)
    firstquarter = models.DateTimeField(blank=True, null=True)
    lastquarter = models.DateTimeField(blank=True, null=True)
    secfilings = models.TextField(blank=True, null=True)
    companysite = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharadar_tickers'
        unique_together = (('stock_id', 'table'),)


class SharaderSp500(models.Model):
    id = models.IntegerField(primary_key=True)
    stock_id = models.CharField(unique=True, max_length=16)
    date = models.DateTimeField()
    action = models.CharField(max_length=16, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    contraticker = models.CharField(max_length=64, blank=True, null=True)
    contraname = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharader_sp500'
        unique_together = (('stock_id', 'date'),)
