from typing import List, Optional, TypedDict

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
    建號: str
    列印時間: str
    謄本種類碼: str
    電謄字號: str
    資料管轄機關: str
    謄本核發機關: str


# -------------------
# 建物標示部
# -------------------


class 建物坐落地號(TypedDict):
    段名: str
    地號: str


class 層次(TypedDict):
    層次: str
    面積: str


class 附屬建物(TypedDict):
    用途: str
    面積: str


class 共有部分(TypedDict):
    段名: str
    建號: str
    面積: str
    權利範圍: 比例
    # 其他登記事項: Optional[str]


class 建物標示(TypedDict):
    # 登記日期: str
    # 登記原因: str
    建物門牌: str
    建物坐落地號: List[建物坐落地號]
    # 主要用途: Optional[str]
    主要建材: Optional[str]
    層數: str
    # 總面積: str
    層次: List[層次]
    附屬建物: List[附屬建物]
    共有部分: Optional[共有部分]
    建築完成日期: Optional[str]
    # 使用執照字號: Optional[str]
    # 其他登記事項: Optional[str]
    廊台面積: Optional[str]


# -------------------
# 建物標示部
# -------------------


class 建物所有權(TypedDict):
    登記次序: str
    登記日期: str
    登記原因: str
    # 原因發生日期: Optional[str]
    所有權人: str
    住址: Optional[str]
    統一編號: Optional[str]
    權利範圍: 比例
    # 權狀字號: Optional[str]
    相關他項權利登記次序: List[str]
    # 其他登記事項: Optional[str]


# -------------------
# 建物他項權利部
# -------------------


class 存續期間(TypedDict):
    自: str
    至: str


class 共同擔保地號(TypedDict):
    段名: str
    地號: str


class 共同擔保建號(TypedDict):
    段名: str
    建號: str


class 建物他項權利(TypedDict):
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
    # 擔保債權確定期日: Optional[str]
    # 清償日期: Optional[str]
    # 利息率: Optional[str]
    # 遲延利息率: Optional[str]
    # 違約金: Optional[str]
    # 擔保債權種類及範圍: Optional[str]
    # 其他擔保範圍約定: Optional[str]
    # 權利標的: str
    # 標的登記次序: List[str]
    # 設定權利範圍: 比例
    # 證明書字號: Optional[str]
    # 共同擔保地號: List[共同擔保地號]
    # 共同擔保建號: List[共同擔保建號]
    # 流抵約定: Optional[str]
    # 其他登記事項: Optional[str]


# -------------------
# 建物登記謄本
# -------------------


class 建物登記(TypedDict):
    謄本資訊: 謄本資訊
    建物標示部: Optional[建物標示]
    建物所有權部: List[建物所有權]
    建物他項權利部: List[建物他項權利]
