# library.py

MASTER_LIBRARY = {
    # --- 核心合成單體 (Aroma Chemicals) ---
    "iso_e_super": {
        "name_cn": "龍涎酮 (Iso E Super)", "note": "Base", "family": "Woody", "cas": "54464-57-2",
        "sg": 0.963, "mol_w": 234.38, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 3.5, "supplier": "單體庫", "type": "Aroma Chemical",
        "ifra_cat4_max": 21.4, "allergens": {},
        "poetic": "乾淨透明的雪松木質與天鵝絨般的偽體香，極佳的結構擴散劑。"
    },
    "hedione": {
        "name_cn": "二氫茉莉酮酸甲酯 (Hedione)", "note": "Mid", "family": "Floral", "cas": "24851-98-7",
        "sg": 1.000, "mol_w": 226.31, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 4.2, "supplier": "單體庫", "type": "Aroma Chemical",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "輕盈透明的水感茉莉微風，無形中提亮所有花香與柑橘輪廓。"
    },
    "galaxolide_50": {
        "name_cn": "佳樂麝香 (Galaxolide)", "note": "Base", "family": "Sweet", "cas": "1222-05-5",
        "sg": 1.005, "mol_w": 258.40, "default_dilution": 50.0, "default_solvent": "IPM (肉豆蔻酸異丙酯)",
        "cost_per_g": 3.0, "supplier": "單體庫", "type": "Aroma Chemical",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "潔淨蓬鬆的現代白麝香，賦予配方持久貼膚的皂感與圓潤度。"
    },
    "ambroxan": {
        "name_cn": "降龍涎香醚 (Ambroxan)", "note": "Base", "family": "Woody", "cas": "6790-58-5",
        "sg": 0.980, "mol_w": 236.39, "default_dilution": 10.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 18.0, "supplier": "單體庫", "type": "Aroma Chemical",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "乾燥礦物感與溫暖龍涎香交織，提供強大尾韻支撐力。"
    },
    "pea": {
        "name_cn": "苯乙醇 (PEA)", "note": "Mid", "family": "Floral", "cas": "60-12-8",
        "sg": 1.020, "mol_w": 122.16, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 2.5, "supplier": "單體庫", "type": "Aroma Chemical",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "新鮮露水玫瑰花瓣的核心骨架，溫潤柔和。"
    },
    "citral_syn": {
        "name_cn": "檸檬醛 (Citral)", "note": "Top", "family": "Citrus", "cas": "5392-40-5",
        "sg": 0.888, "mol_w": 152.24, "default_dilution": 10.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 1.5, "supplier": "單體庫", "type": "Aroma Chemical",
        "ifra_cat4_max": 0.6, "allergens": {"Citral": 1.0},
        "poetic": "銳利清脆的檸檬皮汁液爆發感（注意 IFRA 嚴格限量 0.6%）。"
    },

    # --- 中興化工採購庫存 ---
    "peppermint_eo": {
        "name_cn": "歐薄荷 (Peppermint)", "note": "Top", "family": "Spicy", "cas": "8006-90-4",
        "sg": 0.898, "mol_w": 156.27, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 22.3, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.03, "Linalool": 0.01},
        "poetic": "法國水蒸氣蒸餾，強烈清涼薄荷腦穿透力，瞬間醒腦提神。"
    },
    "ho_wood_eo": {
        "name_cn": "芳樟 (Ho Wood)", "note": "Mid", "family": "Woody", "cas": "8022-91-1",
        "sg": 0.865, "mol_w": 154.25, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 23.1, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Linalool": 0.92},
        "poetic": "富含天然右旋沉香醇，比花梨木更細膩的溫暖花香木質。"
    },
    "copaiba_eo": {
        "name_cn": "古巴香脂 (Copaiba)", "note": "Base", "family": "Woody", "cas": "8001-61-4",
        "sg": 0.900, "mol_w": 204.35, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 27.8, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "深沉溫和的木質樹脂底蘊，極佳的天然定香劑，能圓潤尖銳單體。"
    },
    "ylang_complete_eo": {
        "name_cn": "完全伊蘭 (Ylang Complete)", "note": "Mid", "family": "Floral", "cas": "8006-81-3",
        "sg": 0.930, "mol_w": 180.24, "default_dilution": 10.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 40.9, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 0.8, "allergens": {"Benzyl Benzoate": 0.08, "Linalool": 0.12, "Geraniol": 0.02},
        "poetic": "馬達加斯加完整蒸餾，濃郁異國感與奶油般醉人的熱帶白花香。"
    },
    "sweet_orange_eo": {
        "name_cn": "義大利甜橙 (Sweet Orange)", "note": "Top", "family": "Citrus", "cas": "8028-48-6",
        "sg": 0.844, "mol_w": 136.24, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 12.0, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.94, "Linalool": 0.01},
        "poetic": "義大利果皮冷壓，陽光多汁、純真溫暖的鮮榨果實甜香。"
    },
    "lavender_pop_eo": {
        "name_cn": "高山薰衣草 (Lavender Pop.)", "note": "Mid", "family": "Floral", "cas": "8000-28-0",
        "sg": 0.880, "mol_w": 196.29, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 39.8, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Linalool": 0.38, "Limonene": 0.01, "Coumarin": 0.005},
        "poetic": "法國高地花莖蒸餾，酯類豐富，乾淨細緻且具安撫力的草本花香。"
    },
    "ravintsara_eo": {
        "name_cn": "羅溫莎葉 (Ravintsara)", "note": "Top", "family": "Spicy", "cas": "92201-50-8",
        "sg": 0.900, "mol_w": 154.25, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 38.9, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.03, "Linalool": 0.01},
        "poetic": "馬達加斯加枝葉蒸餾，高含量 1,8-桉油醇，帶來通透潔淨的森林空氣感。"
    },
    "olibanum_eo": {
        "name_cn": "索馬利亞乳香 (Olibanum)", "note": "Base", "family": "Woody", "cas": "8016-36-2",
        "sg": 0.875, "mol_w": 136.24, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 80.0, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.14},
        "poetic": "神聖靜謐的古老樹脂煙燻感，前調帶有清亮微酸的檸檬松針氣息。"
    },
    "tangerine_eo": {
        "name_cn": "義大利紅橘 (Tangerine)", "note": "Top", "family": "Citrus", "cas": "8008-31-9",
        "sg": 0.845, "mol_w": 136.24, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 23.7, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.90, "Linalool": 0.01},
        "poetic": "果皮冷壓，比甜橙更柔和微甜、帶有童趣與撫慰感的柑橘香氣。"
    },
    "petitgrain_eo": {
        "name_cn": "苦橙葉 (Petitgrain)", "note": "Top-Mid", "family": "Spicy", "cas": "8014-17-3",
        "sg": 0.885, "mol_w": 196.29, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 28.3, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Linalool": 0.25, "Limonene": 0.08, "Geraniol": 0.03},
        "poetic": "南美枝葉蒸餾，微苦青澀枝葉中透出細緻橙花氣息，高酯類強力放鬆。"
    },
    "clary_sage_eo": {
        "name_cn": "快樂鼠尾草 (Clary Sage)", "note": "Mid", "family": "Spicy", "cas": "8016-63-5",
        "sg": 0.890, "mol_w": 196.29, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 33.7, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Linalool": 0.22, "Geraniol": 0.02},
        "poetic": "法國蒸餾，堅果草本、微醺茶香與琥珀龍涎氣息交織，深層鎮靜。"
    },
    "cedar_taiwan_eo": {
        "name_cn": "台灣肖楠 (Taiwan Incense Cedar)", "note": "Base", "family": "Woody", "cas": "91770-58-0",
        "sg": 0.940, "mol_w": 220.35, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 74.5, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "台灣特有種蒸餾，沉穩內斂的百年古剎冷冽木質與溫潤奶香。"
    },
    "benzoin_resin": {
        "name_cn": "蘇門答臘安息香原精 (Benzoin)", "note": "Base", "family": "Sweet", "cas": "9000-05-9",
        "sg": 1.150, "mol_w": 212.24, "default_dilution": 50.0, "default_solvent": "TEC (檸檬酸三乙酯)",
        "cost_per_g": 17.4, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 2.0, "allergens": {"Benzyl Benzoate": 0.15, "Cinnamal": 0.01},
        "poetic": "濃稠溫潤的香草焦糖樹脂香（高蠟質，強烈建議以 TEC 預溶防冷濾白濁）。"
    },
    "juniper_berry_eo": {
        "name_cn": "杜松子 (Juniper Berry)", "note": "Top-Mid", "family": "Woody", "cas": "8002-68-4",
        "sg": 0.865, "mol_w": 136.24, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 28.9, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.05},
        "poetic": "琴酒般清脆冷冽的松柏果實木質，帶來通透的空氣感。"
    },
    "black_pepper_eo": {
        "name_cn": "黑胡椒 (Black Pepper)", "note": "Top", "family": "Spicy", "cas": "8006-82-4",
        "sg": 0.875, "mol_w": 204.35, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 34.3, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.18, "Linalool": 0.01},
        "poetic": "乾燥微辛的木質胡椒粒氣息，給予前調躍動的立體能量。"
    },
    "hinoki_taiwan_eo": {
        "name_cn": "台灣紅檜樹心 (Taiwan Red Hinoki)", "note": "Mid-Base", "family": "Woody", "cas": "91745-96-9",
        "sg": 0.940, "mol_w": 222.37, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 37.2, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "台灣高山霧林紅檜樹心蒸餾，檸檬清香與深邃檜木醇完美平衡。"
    },
    "fir_siberian_eo": {
        "name_cn": "西伯利亞冷杉 (Siberian Fir)", "note": "Top", "family": "Woody", "cas": "8021-29-2",
        "sg": 0.900, "mol_w": 196.29, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 22.2, "supplier": "中興化工", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.15},
        "poetic": "高比例乙酸龍腦酯，清冷雪松針葉與微甜樹脂香。"
    },

    # --- 精油好事多 & 沐禾芳療採購庫存 ---
    "palmarosa_eo": {
        "name_cn": "印度玫瑰草 (Palmarosa)", "note": "Mid", "family": "Floral", "cas": "8014-19-5",
        "sg": 0.885, "mol_w": 154.25, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 24.2, "supplier": "精油好事多", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Geraniol": 0.82, "Linalool": 0.03},
        "poetic": "富含天然牻牛兒醇，帶有清新青草露水感的玫瑰替代花香。"
    },
    "rosemary_cineole_eo": {
        "name_cn": "桉油醇迷迭香 (Rosemary Cineole)", "note": "Top", "family": "Spicy", "cas": "8000-25-7",
        "sg": 0.905, "mol_w": 154.25, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 26.0, "supplier": "精油好事多", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.04, "Linalool": 0.02},
        "poetic": "強烈草本清涼穿透力，提升專注力與血氧感，馥奇調核心。"
    },
    "bergamot_eo": {
        "name_cn": "義大利佛手柑 (Bergamot)", "note": "Top", "family": "Citrus", "cas": "8007-75-8",
        "sg": 0.875, "mol_w": 196.29, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 68.6, "supplier": "沐禾芳療", "type": "Natural Essential Oil",
        "ifra_cat4_max": 0.4, "allergens": {"Limonene": 0.42, "Linalool": 0.12, "Citral": 0.01},
        "poetic": "精緻伯爵茶清香，兼顧檸檬活力與薰衣草花香（未去光敏版本 IFRA 限值 0.4%）。"
    },
    "niaouli_eo": {
        "name_cn": "綠花白千層 (Niaouli)", "note": "Top", "family": "Spicy", "cas": "8014-68-4",
        "sg": 0.910, "mol_w": 154.25, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 24.7, "supplier": "沐禾芳療", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.08, "Linalool": 0.01},
        "poetic": "馬達加斯加葉片蒸餾，比茶樹溫和且帶有微甜花果尾韻的氧化物清新。"
    },
    "eucalyptus_radiata_eo": {
        "name_cn": "澳洲尤加利 (Eucalyptus Radiata)", "note": "Top", "family": "Spicy", "cas": "8000-48-4",
        "sg": 0.910, "mol_w": 154.25, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 26.4, "supplier": "沐禾芳療", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.06, "Citral": 0.01},
        "poetic": "清澈微甜的澳洲森林氣息，呼吸感極佳且不嗆鼻。"
    },
    "cypress_eo": {
        "name_cn": "法國絲柏 (Cypress)", "note": "Mid", "family": "Woody", "cas": "8013-86-3",
        "sg": 0.870, "mol_w": 136.24, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 33.9, "supplier": "沐禾芳療", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.04},
        "poetic": "冷冽乾燥的針葉柏木氣息，為木質調帶來垂直向上的森林骨架。"
    },
    "patchouli_eo": {
        "name_cn": "印尼廣藿香 (Patchouli)", "note": "Base", "family": "Woody", "cas": "8014-09-3",
        "sg": 0.965, "mol_w": 222.37, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 38.9, "supplier": "沐禾芳療", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "深邃陳香、微帶黑巧克力與雨後泥土的古老根系，西普調靈魂。"
    },
    "cedar_virginia_eo": {
        "name_cn": "維吉尼亞雪松 (Cedarwood Virginia)", "note": "Base", "family": "Woody", "cas": "8000-27-9",
        "sg": 0.920, "mol_w": 222.37, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 28.3, "supplier": "沐禾芳療", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {},
        "poetic": "乾燥削鉛筆木屑的經典冷冽木質，定香力極強。"
    },
    "elemi_eo": {
        "name_cn": "欖香脂 (Elemi)", "note": "Top-Mid", "family": "Citrus", "cas": "8023-89-0",
        "sg": 0.880, "mol_w": 136.24, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 31.3, "supplier": "沐禾芳療", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.52},
        "poetic": "帶有明亮檸檬與黑胡椒辛香的輕盈樹脂，銜接前調柑橘與後調乳香的橋樑。"
    },
    "tea_tree_eo": {
        "name_cn": "澳洲茶樹 (Tea Tree)", "note": "Top", "family": "Spicy", "cas": "68647-73-4",
        "sg": 0.900, "mol_w": 154.25, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 28.3, "supplier": "沐禾芳療", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Limonene": 0.03, "Linalool": 0.01},
        "poetic": "純淨潔癖般的草本藥草氣息，賦予現代潔淨調真實感。"
    },
    "mallotus_blend_eo": {
        "name_cn": "清輕白楸花複方 (樸草園)", "note": "Mid", "family": "Floral", "cas": "-",
        "sg": 0.910, "mol_w": 180.0, "default_dilution": 50.0, "default_solvent": "DPG (二丙二醇)",
        "cost_per_g": 54.9, "supplier": "樸草園", "type": "Natural Essential Oil",
        "ifra_cat4_max": 100.0, "allergens": {"Linalool": 0.10, "Limonene": 0.05},
        "poetic": "台灣野地白楸花原精結合尤加利與芳樟葉，清甜帶粉感的山野白花香。"
    }
}

CAS_INDEX = {v["cas"]: k for k, v in MASTER_LIBRARY.items() if v.get("cas") and v["cas"] != "-"}
