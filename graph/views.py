from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie,Page, WordCloud

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./graph/templates"))

def graph(request):
    # 读取数据
    df = pd.read_excel('./graph/static/jd_product_info.xlsx').drop_duplicates()
    #数据处理
    df["product_name"] = df["product_name"].str.replace(r'\s','',regex=True)
    df["commentSum"] = df["commentSum"].str.replace('+','',regex=True).str.replace('万','0000',regex=True)
    product_price_range = [0,0,0,0,0,0]
    product_price_range_title = ['0到100之间','100到200之间','200到300之间','300到600之间','600到1000之间','1000以上']
    for i in df["product_price"]:
        if 0<=i<100:
            product_price_range[0] += 1
        elif 100<=i<200:
            product_price_range[1] += 1
        elif 200<=i<300:
            product_price_range[2] += 1
        elif 300<=i<600:
            product_price_range[3] += 1
        elif 600<= i < 1000:
            product_price_range[4] += 1
        else:
            product_price_range[5] += 1

    product_price_range = [round(i/len(df["product_price"])*100,2) for i in product_price_range]

    shop_counts = df["product_shop_name"].value_counts().head(6)# 售卖数量
    df_shop_counts = pd.DataFrame(shop_counts).index.values.tolist()# 商店名称
    shop_counts_sum = 0
    shop_counts = shop_counts.tolist()
    for i in shop_counts:
        shop_counts_sum += i
    shop_counts = [round(i/shop_counts_sum*100,2) for i in shop_counts]

    word_list = []
    word_dir = {}
    for i in df["product_function"]:
        if i=='None':
            continue
        word_list.extend(i.strip("功效：").split("，"))
    for i in word_list:
        if i in word_dir:
            word_dir[i] += 1
        else:
            word_dir[i] = 1
    print(word_dir)

    # 作图
    page = Page(layout=Page.SimplePageLayout)
    a=(
        Pie()
        .add("",[list(z) for z in zip(product_price_range_title,product_price_range) ])
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="洗发水价格分布情况",
            pos_right="40",
            pos_top="40",
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    )

    b = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(df_shop_counts,shop_counts)],
            radius=["50%", "70%"],
            
            )
        .set_global_opts(title_opts=opts.TitleOpts(
            title="前20各个旗舰店销售的产品数量",
            pos_right="40",
            pos_top="40",
            ))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    )

    c = (
            WordCloud()
            .add("", word_dir.items(), word_size_range=[20, 100])
            .set_global_opts(title_opts=opts.TitleOpts(title="洗发水功能词云图"))
        )

    page.add(a,b,c)
        
    
    return HttpResponse(page.render_embed())