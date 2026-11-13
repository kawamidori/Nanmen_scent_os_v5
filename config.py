# config.py

PERFUME_CONCENTRATION_PRESETS = {
    "Eau de Cologne (EdC) - 5%": 0.05,
    "Eau de Toilette (EdT) - 10%": 0.10,
    "Eau de Parfum (EdP) - 15% (商業主力推薦)": 0.15,
    "Eau de Parfum Intense - 18%": 0.18,
    "Extrait de Parfum - 25% (頂級沙龍高濃度)": 0.25
}

REGULATORY_REGIONS = {
    "EU (歐盟 EC 1223/2009 & IFRA 51st)": {
        "code": "EU",
        "allergen_ppm_threshold": 10.0,
        "desc": "全球最嚴苛標準，駐留型產品致敏原超過 10 ppm (0.001%) 強制外盒標示，嚴格遵守 IFRA 51st 限量。"
    },
    "TW (台灣衛福部 TFDA 化粧品法規)": {
        "code": "TW",
        "allergen_ppm_threshold": 10.0,
        "desc": "依台灣衛福部化粧品成分標示規定，駐留型香精致敏原超過 10 ppm 須展開標示。"
    },
    "US (美國 FDA MoCRA)": {
        "code": "US",
        "allergen_ppm_threshold": 10.0,
        "desc": "美國現代化粧品法案 (MoCRA)，要求致敏原全面揭露與產品安全佐證。"
    }
}

DILUTION_TIERS = [100.0, 50.0, 20.0, 10.0, 1.0]

SOLVENT_DATABASE = {
    "None (100%純原液)": {"cas": "-", "sg": 1.000, "inci": ""},
    "DPG (二丙二醇)": {"cas": "25265-71-8", "sg": 1.023, "inci": "DIPROPYLENE GLYCOL"},
    "TEC (檸檬酸三乙酯)": {"cas": "77-93-0", "sg": 1.137, "inci": "TRIETHYL CITRATE"},
    "IPM (肉豆蔻酸異丙酯)": {"cas": "110-27-0", "sg": 0.853, "inci": "ISOPROPYL MYRISTATE"},
    "Ethanol (95%變性酒精)": {"cas": "64-17-5", "sg": 0.812, "inci": "ALCOHOL DENAT."},
    "Jojoba Oil (荷荷巴油)": {"cas": "61789-91-1", "sg": 0.865, "inci": "SIMMONDSIA CHINENSIS SEED OIL"},
    "Grapeseed Oil (葡萄籽油)": {"cas": "8024-22-4", "sg": 0.920, "inci": "VITIS VINIFERA SEED OIL"},
    "Sweet Almond Oil (甜杏仁油)": {"cas": "8007-69-0", "sg": 0.915, "inci": "PRUNUS AMYGDALUS DULCIS OIL"}
}
SOLVENT_CHOICES = list(SOLVENT_DATABASE.keys())

DROP_VOLUME_ML = 0.025
