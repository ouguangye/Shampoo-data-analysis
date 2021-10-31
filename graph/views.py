from jinja2 import Environment, FileSystemLoader
from numpy import product
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse
from pyecharts import options as opts
from pyecharts.charts import Bar
import pandas as pd

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./graph/templates"))

def graph(request):
    # 读取数据
    df = pd.read_excel('./graph/static/jd_product_info.xlsx').drop_duplicates()
    #数据处理
    df["product_name"] = df["product_name"].str.replace(r'\s','',regex=True)
    df["commentSum"] = df["commentSum"].str.replace('+','',regex=True).str.replace('万','0000',regex=True)
    
    #df["product_price_range"] = df["product_price"].apply(lambda x: range_price(x))
    #df["product_price_range"].value_counts()
    
    product_price_range = [0,0,0,0,0]

    #page=Page()
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return HttpResponse(c.render_embed())