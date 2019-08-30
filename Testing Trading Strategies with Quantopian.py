from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume


def initialize(context):
    '''
    Call once at the start of the algorithm.
    :param context:
    :return:
    '''
    schedule_function(my_rebalance, date_rules.every_day(), time_rules.market_open(hours=1))
    schedule_function(my_record_vars, date_rules.every_day(), time_rules.market_close())
    attach_pipeline(make_pipeline(), 'my_pipeline')
    context.aapl = sid(24)
    schedule_function(ma_crossover_handling, date_rules.every_day(), time_rules.market_open(hours=1))


def my_rebalance(context, data):
    pass

def my_record_vars(context, data):
    pass

def my_assign_weights(context, data):
    pass

def ma_crossover_handling(context, data):
    hist = data.history(context.aapl, 'price', 50, '1d')
    sma_50 = hist.mean()
    sma_20 = hist[-20:].mean()

    open_orders = get_open_orders()
    if sma_20 > sma_50:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, 1.0)
    elif sma_20 < sma_50:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, -1.0)


def make_pipeline():
    dollar_volume = AverageDollarVolume(window_length=1)
    high_dollar_volume = dollar_volume.percentile_between(99, 100)

    pipe = Pipeline(
        screen = high_dollar_volume,
        columns = {'dollar_volume': dollar_volume}
    )

    return pipe


def before_trading_start(context, data):
    context.output = pipeline_output('my_pipeline')
    context.security_list = context.output.index


def handle_data(context, data):
    hist = data.history(context.aapl, 'price', 50, '1d')
    sma_50 = hist.mean()
    sma_20 = hist[-20:].mean()

    if sma_20 > sma_50:
        order_target_percent(context.aapl, 1.0)
    elif sma_20 < sma_50:
        order_target_percent(conte.aapl, -1.0)

    record(leverage=context.aacount.leverage)

    open_orders = get_open_orders()
    if sma_20 > sma_50:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, 1.0)
    elif sma_20 < sma_50:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, -1.0)






