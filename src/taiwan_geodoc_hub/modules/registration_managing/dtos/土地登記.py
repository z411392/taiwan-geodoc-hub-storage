from typing import TypedDict, Optional, List

# -------------------
# 共用部分
# -------------------


class 比例(TypedDict):
    公同共有: bool
    分母: str
    分子: str


# -------------------
# 謄本資訊
# -------------------


class 謄本資訊(TypedDict):
    行政區: str
    段名: str
    地號: str
    列印時間: str
    謄本種類碼: str
    電謄字號: str
    資料管轄機關: str
    謄本核發機關: str


# -------------------
# 土地標示部
# -------------------


class 公告土地現值(TypedDict):
    年月: str
    現值: str  # 元/平方公尺


class 地上建物建號(TypedDict):
    段名: str
    建號: str


class 土地標示(TypedDict):
    # 登記日期: str
    # 登記原因: str
    面積: str
    # 使用分區: Optional[str]
    # 使用地類別: Optional[str]
    公告土地現值: List[公告土地現值]
    地上建物建號: List[地上建物建號]
    # 其他登記事項: Optional[str]


# -------------------
# 土地標示部
# -------------------


class 當期申報地價(TypedDict):
    年月: str
    地價: str  # 單位：元/平方公尺


class 前次移轉現值或原規定地價(TypedDict):
    年月: str
    現值: str  # 單位：元/平方公尺


class 土地所有權(TypedDict):
    登記次序: str
    登記日期: str
    登記原因: str
    # 原因發生日期: Optional[str]
    所有權人: str
    統一編號: str
    住址: Optional[str]
    權利範圍: 比例
    # 權狀字號: Optional[str]
    # 當期申報地價: 當期申報地價
    # 前次移轉現值或原規定地價: 前次移轉現值或原規定地價
    # 歷次取得權利範圍: 比例
    相關他項權利登記次序: List[str]
    # 其他登記事項: Optional[str]


# -------------------
# 土地他項權利部
# -------------------


class 共同擔保地號(TypedDict):
    段名: str
    地號: str


class 共同擔保建號(TypedDict):
    段名: str
    建號: str


class 存續期間(TypedDict):
    自: str
    至: str


class 土地他項權利(TypedDict):
    登記次序: str
    權利種類: str
    # 收件年期: str
    # 字號: str
    登記日期: str
    登記原因: str
    權利人: str
    # 統一編號: Optional[str]
    # 住址: Optional[str]
    # 債權額比例: Optional[比例]
    擔保債權總金額: Optional[str]
    # 存續期間: Optional[存續期間]
    # 利息率: Optional[str]
    # 遲延利息率: Optional[str]
    # 違約金: Optional[str]
    # 清償日期: Optional[str]
    # 權利標的: str
    # 標的登記次序: List[str]
    # 設定權利範圍: 比例
    # 證明書字號: Optional[str]
    # 共同擔保地號: List[共同擔保地號]
    # 共同擔保建號: List[共同擔保建號]
    # 其他登記事項: Optional[str]


# -------------------
# 土地登記謄本
# -------------------


class 土地登記(TypedDict):
    謄本資訊: 謄本資訊
    土地標示部: Optional[土地標示]
    土地所有權部: List[土地所有權]
    土地他項權利部: List[土地他項權利]
