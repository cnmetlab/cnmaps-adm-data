import os
import pandas as pd

__version__ = "1.0.0"

INDEX_FILE = os.path.join(os.path.dirname(__file__), "index.csv")
DATA_DIR = os.path.dirname(__file__)


def search(
    province: str = None,
    city: str = None,
    district: str = None,
    level: str = None,
    country: str = "中华人民共和国",
    source: str = "高德",
):
    df = pd.read_csv(INDEX_FILE)
    df = df[(df["来源"] == source) & (df["国家"] == country)]
    if level == "国":
        df = df[df["级别"] == "国"]
    elif level == "省":
        df = df[df["级别"] == "省"]
        if province:
            df = df[df["省/直辖市"] == province]
    elif level == "市":
        df = df[df["级别"] == "市"]
        if province:
            df = df[df["省/直辖市"] == province]
        if city:
            df = df[df["市"] == city]
    elif level in ["区", "县", "区县", "区/县"]:
        df = df[df["级别"] == "区县"]
        if province:
            df = df[df["省/直辖市"] == province]
        if city:
            df = df[df["市"] == city]
        if district:
            df = df[df["区/县"] == district]
    elif level is None:
        if district:
            df = df[(df["区/县"] == district) & (df["级别"] == "区县")]
        elif city:
            df = df[(df["市"] == city) & (df["级别"] == "市")]
        elif province:
            df = df[(df["省/直辖市"] == province) & (df["级别"] == "省")]
    else:
        raise ValueError(f'无法识别level等级: {level}, level参数请从"国", "省", "市", "区县"中选择')

    return df


if __name__ == "__main__":
    print(search())
    print(search(district="兴隆县"))
    print(search(province="山西省", level="市"))
    print(search(province="山西省", level="区县"))
