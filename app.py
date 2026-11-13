# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import copy
import hmac
from datetime import datetime

from config import PERFUME_CONCENTRATION_PRESETS, SOLVENT_CHOICES, REGULATORY_REGIONS, DILUTION_TIERS, SOLVENT_DATABASE
from library import MASTER_LIBRARY
import core

st.set_page_config(page_title="Nanmen Scent Lab OS", layout="wide", page_icon="🧪")

# ------------------------------------------------------------------------------
# 🔒 門禁密碼系統 (Password Protection)
# ------------------------------------------------------------------------------
def check_password():
    if st.session_state.get("authenticated"):
        return True

    st.markdown("""
        <div style='text-align:center; padding-top:40px;'>
            <h1>🧪 Nanmen Scent Lab OS</h1>
            <p style='color:#64748B;'>Enterprise Perfumery Operating System</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        pwd = st.text_input("🔒 實驗室門禁密碼", type="password", placeholder="請輸入存取密碼...")
        correct_pwd = st.secrets.get("APP_PASSWORD", "nanmen2026")
        if st.button("登入系統", use_container_width=True, type="primary"):
            if hmac.compare_digest(pwd, correct_pwd):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ 密碼錯誤，請重新輸入。")
    return False

if not check_password():
    st.stop()

# ------------------------------------------------------------------------------
# UI CSS (Desktop + Mobile Responsive)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    @media (max-width: 768px) {
        .block-container { padding: 4.2rem 0.4rem 1rem 0.4rem !important; }
        .stTabs [data-baseweb="tab-list"] { display: flex; overflow-x: auto; white-space: nowrap; -webkit-overflow-scrolling: touch; }
        .stats-bar { flex-direction: column; gap: 6px; text-align: left; align-items: flex-start !important; }
        input[type="number"] { font-size: 16px !important; }
    }
    .mod-pill { background: #0F172A; color: #38BDF8; padding: 3px 10px; border-radius: 6px; font-weight: bold; border: 1px solid #0284C7; font-size: 13px; }
    .mat-card { background: #F8FAFC; border: 1px solid #CBD5E1; padding: 12px; border-radius: 8px; margin-top: 8px; }
    .scale-chip { background: #064E3B; color: #6EE7B7; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 13px; font-weight: bold; display: inline-block; }
    .cas-badge { background: #F1F5F9; color: #475569; padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 11px; border: 1px solid #CBD5E1; }
    .stats-bar { background: #0F172A; color: white; padding: 12px 18px; border-radius: 8px; margin-top: 14px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .sample-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .doc-sheet { background: white; padding: 20px; border: 1px solid #CBD5E1; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); color: #0F172A; margin-bottom: 14px; }
    .doc-title { border-bottom: 2px solid #0F172A; padding-bottom: 8px; margin-bottom: 14px; }
    .cert-box { background: #FFFFFF; border: 2px solid #0F172A; border-radius: 8px; padding: 18px; margin-bottom: 14px; }
    .nda-box { background: #FFFBEB; border: 2px solid #D97706; border-radius: 8px; padding: 18px; margin-bottom: 14px; color: #78350F; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------------------------------------------------------
if "mods" not in st.session_state:
    st.session_state.mods = {
        "Mod 1": {
            "iso_e_super": {"gross_g": 1.500, "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)"},
            "hedione": {"gross_g": 1.200, "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)"},
            "bergamot_eo": {"gross_g": 0.400, "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)"},
            "cedar_taiwan_eo": {"gross_g": 0.600, "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)"}
        }
    }
if "active_mod" not in st.session_state:
    st.session_state.active_mod = "Mod 1"
if "mod_notes" not in st.session_state:
    st.session_state.mod_notes = {"Mod 1": "初始版：台灣肖楠與佛手柑的清冷木質骨架。"}
if "dosed_checklist" not in st.session_state:
    st.session_state.dosed_checklist = {}
if "selected_region_key" not in st.session_state:
    st.session_state.selected_region_key = list(REGULATORY_REGIONS.keys())[0]
if "selected_tier_key" not in st.session_state:
    st.session_state.selected_tier_key = list(PERFUME_CONCENTRATION_PRESETS.keys())[2]
if "locked_for_pif" not in st.session_state:
    st.session_state.locked_for_pif = False

# ==============================================================================
# TOP GLOBAL PROJECT BRIEF RIBBON (頂部全局專案設計書，不鎖在側邊欄)
# ==============================================================================
st.markdown("### 🧪 Nanmen Scent Lab OS")
with st.container():
    tb1, tb2, tb3, tb4 = st.columns([1.3, 1.5, 1.5, 1.0])
    with tb1:
        mod_list = list(st.session_state.mods.keys())
        st.session_state.active_mod = st.selectbox("📂 當前操作版本 (Mod)", mod_list, index=mod_list.index(st.session_state.active_mod))
    with tb2:
        st.session_state.selected_region_key = st.selectbox("🌐 專案法規基準 (Regulatory)", list(REGULATORY_REGIONS.keys()), index=list(REGULATORY_REGIONS.keys()).index(st.session_state.selected_region_key))
    with tb3:
        st.session_state.selected_tier_key = st.selectbox("🎯 目標成品賦香率 (Dosage)", list(PERFUME_CONCENTRATION_PRESETS.keys()), index=list(PERFUME_CONCENTRATION_PRESETS.keys()).index(st.session_state.selected_tier_key))
    with tb4:
        st.write("")
        c_m1, c_m2 = st.columns(2)
        if c_m1.button("➕ 複製", use_container_width=True, help="複製當前 Mod 為新版本"):
            new_name = f"Mod {len(mod_list) + 1}"
            st.session_state.mods[new_name] = copy.deepcopy(st.session_state.mods[st.session_state.active_mod])
            st.session_state.mod_notes[new_name] = f"複製自 {st.session_state.active_mod}"
            st.session_state.active_mod = new_name
            st.session_state.locked_for_pif = False
            st.rerun()
        if c_m2.button("🗑️ 清空", use_container_width=True, help="清空當前 Mod 配方"):
            st.session_state.mods[st.session_state.active_mod] = {}
            st.session_state.locked_for_pif = False
            st.rerun()

region_info = REGULATORY_REGIONS[st.session_state.selected_region_key]
dosage_ratio = PERFUME_CONCENTRATION_PRESETS[st.session_state.selected_tier_key]
current_formula = st.session_state.mods[st.session_state.active_mod]
total_jus_g = sum([d.get("gross_g", 0.0) for d in current_formula.values()])

rt_calc = core.analyze_formula_realtime(current_formula, dosage_ratio, MASTER_LIBRARY)
mod_calc = core.calculate_mod_profile(current_formula, dosage_ratio, {"bottles": 1, "vol_ml": 10}, MASTER_LIBRARY)
mac_meta = core.predict_maceration_and_filtration(current_formula, dosage_ratio, {"bottles": 1, "vol_ml": 10}, MASTER_LIBRARY)

# ==============================================================================
# LINEAR 4-PHASE TOP NAVIGATION: Phase 1 > Phase 2 > Phase 3 > Phase 4
# ==============================================================================
active_phase = st.radio(
    "研發流程階段：",
    [
        "💻 Phase 1：數位配方創作",
        "⚖️ Phase 2：實驗室放樣與投料單",
        "📑 Phase 3：PIF 產品資訊與合規證書",
        "🏭 Phase 4：商業量產與投遞框架"
    ],
    horizontal=True,
    label_visibility="collapsed"
)
st.divider()

# ==============================================================================
# PHASE 1: 數位配方創作與配方總表
# ==============================================================================
if "Phase 1" in active_phase:
    st.markdown(f"""
    <div style="background:#0F172A; padding:8px 16px; border-radius:6px; color:white; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div><b>💻 Phase 1：數位配方創作 (100% Jus 純原油設計)</b> ｜ 版本：<span class="mod-pill">{st.session_state.active_mod}</span></div>
        <div style="font-size:13px; color:#94A3B8;">配方總重：<b style="color:#FBBF24; font-size:15px;">{total_jus_g:.3f} g</b> ｜ 純香精淨重：<b style="color:#38BDF8;">{rt_calc['total_active_g']:.3f} g</b></div>
    </div>
    """, unsafe_allow_html=True)

    ph1_tab_edit, ph1_tab_print = st.tabs(["🎛️ 1-A：互動式三欄調香機艙", "📄 1-B：配方總表 (Print-ready Snapshot)"])

    with ph1_tab_edit:
        p_left, p_mid, p_right = st.columns([1.15, 2.25, 1.25])

        # 🟢 LEFT PANE: 智慧原料庫
        with p_left:
            st.markdown("#### 🟢 原料庫與採購清單")
            lib_search = st.text_input("🔍 搜尋 (名稱 / CAS / 廠商)：", placeholder="例如: 肖楠, 沐禾, 8007-75-8")
            c_f1, c_f2 = st.columns(2)
            note_filter = c_f1.selectbox("香階過濾", ["全部香階", "Top", "Mid", "Base"], label_visibility="collapsed")
            sup_filter = c_f2.selectbox("供應商", ["全部來源", "中興化工", "沐禾芳療", "精油好事多", "樸草園", "單體庫"], label_visibility="collapsed")

            filtered_keys = []
            for k, v in MASTER_LIBRARY.items():
                txt_ok = (lib_search.lower() in v["name_cn"].lower() or lib_search.lower() in k.lower()
                          or lib_search in v.get("cas", "") or lib_search in v.get("supplier", ""))
                note_ok = True if note_filter == "全部香階" else (note_filter in v.get("note", ""))
                sup_ok = True if sup_filter == "全部來源" else (sup_filter == v.get("supplier", ""))
                if txt_ok and note_ok and sup_ok:
                    filtered_keys.append(k)

            selected_lib_ing = st.selectbox(
                "選擇原料檢視資料卡：",
                filtered_keys if filtered_keys else list(MASTER_LIBRARY.keys()),
                format_func=lambda x: f"[{MASTER_LIBRARY[x].get('note', 'Mid')[:1]}] {MASTER_LIBRARY[x]['name_cn']}"
            )

            if selected_lib_ing:
                s_m = MASTER_LIBRARY[selected_lib_ing]
                tier_color = "#10B981" if "Top" in s_m.get("note", "") else ("#F59E0B" if "Mid" in s_m.get("note", "") else "#78350F")
                st.markdown(f"""
                <div class="mat-card" style="border-left: 4px solid {tier_color};">
                    <div style="font-weight:bold; font-size:14px; color:#0F172A;">{s_m['name_cn']}</div>
                    <div style="margin:4px 0;">
                        <span class="cas-badge">CAS: {s_m.get('cas', '-')}</span>
                        <span style="font-size:11px; color:#0284C7; font-weight:bold; margin-left:4px;">{s_m.get('supplier', '-')}</span>
                    </div>
                    <div style="font-size:12px; color:#475569; margin-top:4px;">
                        • 香階：<b>{s_m.get('note', '-')}</b> ({s_m.get('family', '-')})<br>
                        • 比重 ρ：<b>{s_m.get('sg', 1.0)}</b> ｜ 純油單價：<b>NT$ {s_m.get('cost_per_g', 0.0)}/g</b><br>
                        • IFRA Cat.4 上限：<b>{s_m.get('ifra_cat4_max', 100.0)}%</b>
                    </div>
                    <div style="font-size:12px; color:#334155; font-style:italic; margin-top:6px; padding-top:6px; border-top:1px dashed #CBD5E1;">
                        "{s_m.get('poetic', '')}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("➕ 加入當前配方表", use_container_width=True, type="primary"):
                    if selected_lib_ing not in current_formula:
                        st.session_state.mods[st.session_state.active_mod][selected_lib_ing] = {
                            "gross_g": 0.200, "dilution_pct": s_m.get("default_dilution", 50.0), "solvent": s_m.get("default_solvent", "DPG (二丙二醇)")
                        }
                        st.rerun()
                    else:
                        st.warning("⚠️ 此原料已在配方中。")

            with st.expander("🤖 AI 靈感骨架助理 (選用)"):
                st.caption("沒有靈感時，可生成 5.000g 起手骨架（將覆蓋當前 Mod）：")
                w_citrus = st.slider("🍊 柑橘清新", 0, 100, 25, 5)
                w_floral = st.slider("🌸 優雅花香", 0, 100, 25, 5)
                w_woody = st.slider("🌲 沉穩木質", 0, 100, 35, 5)
                w_spicy = st.slider("🌶️ 辛香草本", 0, 100, 10, 5)
                w_sweet = st.slider("🍦 溫潤樹脂", 0, 100, 5, 5)
                if st.button("✨ 生成並覆蓋當前 Mod", use_container_width=True):
                    s_dict = {"Citrus": w_citrus, "Floral": w_floral, "Woody": w_woody, "Spicy": w_spicy, "Sweet": w_sweet}
                    st.session_state.mods[st.session_state.active_mod] = core.synthesize_canvas_formula(s_dict, selected_lib_ing, 5.0, MASTER_LIBRARY)
                    st.rerun()

        # 🔵 CENTER PANE: 配方矩陣
        with p_mid:
            c_title, c_tools = st.columns([1.4, 1.3])
            with c_title:
                st.markdown("#### 🔵 數位配方矩陣 (Formulation Grid)")
            with c_tools:
                t_col1, t_col2 = st.columns(2)
                with t_col1:
                    display_unit = st.selectbox("單位", ["克數 (g) + 佔比", "千分比 (PPT ‰)"], label_visibility="collapsed")
                with t_col2:
                    with st.popover("⚖️ 等比縮放"):
                        target_g = st.number_input("目標總克數 (g)", min_value=1.0, max_value=5000.0, value=max(5.0, round(total_jus_g, 2)), step=1.0)
                        if st.button("執行縮放", use_container_width=True) and total_jus_g > 0:
                            mult = target_g / total_jus_g
                            for k in current_formula:
                                current_formula[k]["gross_g"] = round(current_formula[k]["gross_g"] * mult, 3)
                            st.session_state.mods[st.session_state.active_mod] = current_formula
                            st.rerun()

            creation_rows = core.build_compounding_sheet(current_formula, dosage_ratio, MASTER_LIBRARY, sort_by_compounding=False)

            if not creation_rows:
                st.info("👈 當前配方為空。請從左側原料庫挑選原料加入。")
            else:
                for row in creation_rows:
                    ing_id = row["ing_id"]
                    with st.container(border=True):
                        r1, r2, r3, r4, r5 = st.columns([2.2, 1.1, 1.3, 1.4, 0.45])
                        r1.markdown(f"**{row['name_cn']}**<br><span class='cas-badge'>{row['note']}</span> <span style='font-size:11px; color:#64748B;'>純油價: ${row['cost']:.1f}</span>", unsafe_allow_html=True)
                        new_dil = r2.selectbox("濃度%", DILUTION_TIERS, index=DILUTION_TIERS.index(float(row["dilution_pct"])) if float(row["dilution_pct"]) in DILUTION_TIERS else 0, key=f"p1_dil_{st.session_state.active_mod}_{ing_id}", label_visibility="collapsed")
                        new_sol = r3.selectbox("溶劑", SOLVENT_CHOICES, index=SOLVENT_CHOICES.index(row["solvent"]) if row["solvent"] in SOLVENT_CHOICES else 0, key=f"p1_sol_{st.session_state.active_mod}_{ing_id}", label_visibility="collapsed")
                        new_g = r4.number_input("克數", min_value=0.001, max_value=1000.0, value=float(row["gross_g"]), step=0.010, format="%.3f", key=f"p1_g_{st.session_state.active_mod}_{ing_id}", label_visibility="collapsed")
                        if "PPT" in display_unit:
                            r4.caption(f"📊 **{row['ppt']:.1f} ‰** (純油 {row['active_g']:.3f}g)")
                        else:
                            r4.caption(f"📊 **{row['pct']:.1f}%** (約 {row['drops']} 滴)")

                        if r5.button("🗑️", key=f"p1_del_{st.session_state.active_mod}_{ing_id}"):
                            del st.session_state.mods[st.session_state.active_mod][ing_id]
                            st.rerun()

                        if abs(new_dil - row["dilution_pct"]) > 1e-4 or new_sol != row["solvent"] or abs(new_g - row["gross_g"]) > 1e-4:
                            st.session_state.mods[st.session_state.active_mod][ing_id] = {"gross_g": new_g, "dilution_pct": new_dil, "solvent": new_sol}
                            st.rerun()

        # 🟡 RIGHT PANE: 即時智慧探針
        with p_right:
            st.markdown("#### 🟡 即時智慧探針")
            probe_tab1, probe_tab2 = st.tabs(["🛡️ 金字塔與法規", "🎡 風味輪與揮發"])

            with probe_tab1:
                if mod_calc:
                    st.markdown("**嗅覺金字塔結構 (純油有效佔比)：**")
                    top_p, mid_p, base_p = mod_calc["notes_pct"]["Top"], mod_calc["notes_pct"]["Mid"], mod_calc["notes_pct"]["Base"]
                    st.caption(f"Top 前調: {top_p:.1f}%")
                    st.progress(min(1.0, top_p / 100.0))
                    st.caption(f"Heart 中調: {mid_p:.1f}%")
                    st.progress(min(1.0, mid_p / 100.0))
                    st.caption(f"Base 後調: {base_p:.1f}%")
                    st.progress(min(1.0, base_p / 100.0))

                st.divider()
                st.markdown(f"**IFRA 51st 合規雷達 ({region_info['code']} @ {dosage_ratio*100:.0f}%)：**")
                all_safe = True
                for ing_id, stat in rt_calc["ifra_status"].items():
                    if not stat["is_safe"]:
                        all_safe = False
                        st.error(f"❌ **{MASTER_LIBRARY[ing_id]['name_cn']}** 超標！殘留 {stat['finished_pct']:.2f}% > 限值 {stat['limit']}%")
                    elif stat["is_warn"]:
                        st.warning(f"⚠️ **{MASTER_LIBRARY[ing_id]['name_cn']}** 逼近警戒 ({stat['risk_ratio']*100:.0f}%)")
                if all_safe and current_formula:
                    st.success(f"✅ 符合 IFRA Cat.4 限值（最高安全賦香率上限：{rt_calc['max_safe_dosage_pct']:.1f}%）")

                allg_dict = rt_calc.get("allergen_summary", {})
                over_allg = {k: v for k, v in allg_dict.items() if v >= region_info["allergen_ppm_threshold"]}
                if over_allg:
                    st.markdown("**⚠️ 須外盒標示之致敏原 (>10 ppm)：**")
                    for a_k, a_v in sorted(over_allg.items(), key=lambda x: x[1], reverse=True):
                        st.caption(f"• `{a_k}`: **{a_v:.1f} ppm**")

            with probe_tab2:
                if mod_calc:
                    sb_items = [{"Family": v["family"], "Name": v["name_cn"], "ActiveWeight": v["active_pct"]} for v in mod_calc["norm_active"].values()]
                    if sb_items:
                        fig_sb = px.sunburst(pd.DataFrame(sb_items), path=["Family", "Name"], values="ActiveWeight", color="Family", color_discrete_map={"Woody": "#78350F", "Floral": "#EC4899", "Citrus": "#F59E0B", "Sweet": "#EF4444", "Spicy": "#B45309"}, height=240)
                        fig_sb.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                        st.plotly_chart(fig_sb, use_container_width=True)

                    st.caption("⏳ 24h 揮發動態模擬：")
                    fig_traj = px.line(mod_calc["trajectory"], x="Hour", y=["Top", "Mid", "Base"], color_discrete_map={"Top": "#10B981", "Mid": "#F59E0B", "Base": "#6B7280"}, height=200)
                    fig_traj.update_layout(margin=dict(l=0, r=0, t=0, b=0), hovermode="x unified", showlegend=True)
                    st.plotly_chart(fig_traj, use_container_width=True)

            st.divider()
            st.markdown("**📝 調香師版本筆記：**")
            c_n = st.session_state.mod_notes.get(st.session_state.active_mod, "")
            n_n = st.text_area("記錄此版調整思路：", value=c_n, height=85, label_visibility="collapsed")
            if n_n != c_n:
                st.session_state.mod_notes[st.session_state.active_mod] = n_n

        # 🏁 BOTTOM STATS BAR
        if mod_calc:
            est_cost = mod_calc.get("total_cost", 0.0)
            est_cost_per_10g = (est_cost / total_jus_g * 10.0) if total_jus_g > 0 else 0.0
            st.markdown(f"""
            <div class="stats-bar">
                <div>
                    <span style="color:#94A3B8; font-size:12px;">本批純油原料成本：</span>
                    <b style="color:#FBBF24; font-size:16px;">NT$ {est_cost:.1f}</b>
                    <span style="color:#64748B; font-size:12px; margin-left:8px;">(基準成本: NT$ {est_cost_per_10g:.1f} / 10g 原油)</span>
                </div>
                <div>
                    <span style="color:#94A3B8; font-size:12px;">純香精有效淨重 vs 載體溶劑：</span>
                    <b style="color:#38BDF8; font-size:15px;">{rt_calc['total_active_g']:.3f} g 純油</b>
                    <span style="color:#94A3B8; font-size:12px;"> + {rt_calc['total_carrier_g']:.3f} g 溶劑</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 1-B 配方總表 (Print-ready Snapshot) ---
    with ph1_tab_print:
        if not mod_calc or not current_formula:
            st.warning("⚠️ 當前配方為空，請先在 1-A 建立配方。")
        else:
            st.markdown(f"""
            <div class="doc-sheet">
                <div class="doc-title">
                    <h3 style="margin:0;">FORMULATION RECORD SHEET — {st.session_state.active_mod}</h3>
                    <div style="color:#64748B; font-size:13px; margin-top:4px;">Date: {datetime.now().strftime("%Y-%m-%d")} | Regulatory: {region_info['code']} | Design Dosage: {dosage_ratio*100:.0f}%</div>
                </div>
                <p style="margin:4px 0;"><b>Perfumer Notes:</b> {st.session_state.mod_notes.get(st.session_state.active_mod, 'N/A')}</p>
                <p style="margin:4px 0;">
                    <b>Total Jus Weight:</b> {total_jus_g:.3f} g &nbsp;|&nbsp;
                    <b>Pure Active Oil:</b> {rt_calc['total_active_g']:.3f} g &nbsp;|&nbsp;
                    <b>Carrier Solvent:</b> {rt_calc['total_carrier_g']:.3f} g &nbsp;|&nbsp;
                    <b>Est. Raw Cost:</b> NT$ {mod_calc['total_cost']:.1f} (NT$ {mod_calc['total_cost']/total_jus_g*10.0:.1f} / 10g)
                </p>
            </div>
            """, unsafe_allow_html=True)

            print_rows = core.build_compounding_sheet(current_formula, dosage_ratio, MASTER_LIBRARY, sort_by_compounding=True)
            df_print = pd.DataFrame([{
                "投料序": r["seq"],
                "香階": r["note"],
                "CAS": r["cas"],
                "原料名稱": r["name_cn"],
                "稀釋規格": f"{r['dilution_pct']:.0f}% in {r['solvent'].split(' ')[0]}" if r["dilution_pct"] < 100 else "100% Neat",
                "投料重 (g)": f"{r['gross_g']:.3f}",
                "純油淨重 (g)": f"{r['active_g']:.3f}",
                "佔比 (%)": f"{r['pct']:.2f}%",
                "千分比 (‰)": f"{r['ppt']:.1f}",
                "純油成本 (NT$)": f"{r['cost']:.1f}"
            } for r in print_rows])

            st.dataframe(df_print, use_container_width=True, hide_index=True)
            csv_f = df_print.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 下載配方總表 (CSV)", data=csv_f, file_name=f"Formula_Sheet_{st.session_state.active_mod}.csv", mime="text/csv", use_container_width=True)

# ==============================================================================
# PHASE 2: 實驗室實體放樣與投料單 (Lab Compounding & Dosing Sheet)
# ==============================================================================
elif "Phase 2" in active_phase:
    st.markdown(f"""
    <div style="background:#0F172A; padding:8px 16px; border-radius:6px; color:white; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div><b>⚖️ Phase 2：實驗室放樣與投料單</b> ｜ 執行版本：<span class="mod-pill">{st.session_state.active_mod}</span></div>
        <div style="font-size:13px; color:#94A3B8;">目標原油母液總重：<b style="color:#FBBF24; font-size:15px;">{total_jus_g:.3f} g</b></div>
    </div>
    """, unsafe_allow_html=True)

    p2_sub1, p2_sub2 = st.tabs([
        "⚖️ 2-A：天平放樣工作站與實驗室投料單 (100% Jus)",
        "🧪 2-B：多濃度成品取樣與熟成冷濾 (Phase B 酒精)"
    ])

    with p2_sub1:
        st.info("🛡️ **大廠放樣 SOP**：系統已自動將配方強制轉換為 **「後調定香 (Base) ➔ 中調 (Mid) ➔ 高揮發前調 (Top)」** 工業投料序。")
        bench_rows = core.build_compounding_sheet(current_formula, dosage_ratio, MASTER_LIBRARY, sort_by_compounding=True)

        if not bench_rows:
            st.warning("⚠️ 當前配方為空，請先至 Phase 1 建立配方。")
        else:
            current_checks = st.session_state.dosed_checklist.setdefault(st.session_state.active_mod, {})
            dosed_count = sum(1 for r in bench_rows if current_checks.get(r["ing_id"], False))
            dosed_weight = sum(r["gross_g"] for r in bench_rows if current_checks.get(r["ing_id"], False))

            c_prog, c_reset = st.columns([3.5, 1])
            with c_prog:
                st.progress(dosed_count / len(bench_rows) if len(bench_rows) > 0 else 0)
                st.caption(f"📊 天平累計進度：已完成 **{dosed_count}/{len(bench_rows)}** 項（已投 **{dosed_weight:.3f} g** / {total_jus_g:.3f} g）")
            with c_reset:
                if st.button("🔄 重置打勾記錄", use_container_width=True):
                    st.session_state.dosed_checklist[st.session_state.active_mod] = {}
                    st.rerun()

            for row in bench_rows:
                ing_id = row["ing_id"]
                is_done = current_checks.get(ing_id, False)
                with st.container(border=True):
                    b1, b2, b3, b4, b5 = st.columns([0.5, 0.7, 2.5, 1.5, 1.5])
                    chk = b1.checkbox("已投", value=is_done, key=f"bench_chk_{st.session_state.active_mod}_{ing_id}", label_visibility="collapsed")
                    current_checks[ing_id] = chk

                    b2.markdown(f"**#{row['seq']}**<br>`{row['note']}`", unsafe_allow_html=True)
                    name_css = "text-decoration: line-through; color: #94A3B8;" if chk else "font-weight: 700; color: #0F172A;"
                    sol_short = row["solvent"].split(" ")[0]
                    spec_txt = "100% 純原液" if row["dilution_pct"] >= 100 else f"{row['dilution_pct']:.0f}% in {sol_short}"
                    b3.markdown(f"<span style='{name_css}'>{row['name_cn']}</span><br><span class='cas-badge'>{spec_txt}</span> <span style='font-size:11px; color:#64748B;'>CAS: {row['cas']}</span>", unsafe_allow_html=True)
                    b4.markdown(f"本次淨投：<br><b style='font-size:16px; color:#0284C7;'>{row['gross_g']:.3f} g</b> <span style='font-size:12px; color:#64748B;'>({row['drops']} 滴)</span>", unsafe_allow_html=True)
                    b5.markdown(f"天平累計：<br><span class='scale-chip'>⚖️ {row['cumulative_g']:.3f} g</span>", unsafe_allow_html=True)

            st.divider()
            st.subheader("📋 實驗室標準投料單 (Lab Dosing / Compounding Sheet)")
            dosing_df = pd.DataFrame([{
                "投料序": r["seq"],
                "香階": r["note"],
                "CAS": r["cas"],
                "原料名稱": r["name_cn"],
                "稀釋與載體規格": f"{r['dilution_pct']:.0f}% in {r['solvent'].split(' ')[0]}" if r["dilution_pct"] < 100 else "100% 純原液",
                "本次淨投 (g)": r["gross_g"],
                "預估滴數": r["drops"],
                "天平累計 Tare (g)": r["cumulative_g"],
                "純油淨重 (g)": r["active_g"],
                "載體重 (g)": r["carrier_g"],
                "投料確認": "✅" if current_checks.get(r["ing_id"], False) else "⬜"
            } for r in bench_rows])
            st.dataframe(dosing_df, hide_index=True, use_container_width=True)
            dosing_csv = dosing_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 下載實驗室投料單 (Lab Dosing Sheet CSV)", data=dosing_csv, file_name=f"Lab_Dosing_Sheet_{st.session_state.active_mod}.csv", mime="text/csv", use_container_width=True)

    with p2_sub2:
        st.subheader("🧪 多濃度成品取樣計算機 & 熟成冷濾預測")
        st.caption("從調好的 Jus 中取出定量樣品，系統自動扣除載體並加入 3% 低溫冷濾損耗裕度。")

        if total_jus_g <= 0:
            st.warning("⚠️ 當前可用原油存量為 0g。")
        else:
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("#### 樣品 A：日常清新版 (預設 EdT)")
                s1_tier = st.selectbox("樣品 A 濃度", list(PERFUME_CONCENTRATION_PRESETS.keys()), index=1, key="p2_s1_tier")
                s1_bot = st.number_input("瓶數 (A)", 1, 50, 1, 1, key="p2_s1_bot")
                s1_vol = st.selectbox("單瓶容量 (A)", [5, 10, 15, 30, 50], index=1, key="p2_s1_vol")
                res_s1 = core.compute_sample_application(current_formula, PERFUME_CONCENTRATION_PRESETS[s1_tier], s1_bot, s1_vol, MASTER_LIBRARY)
                if res_s1:
                    st.markdown(f"""
                    <div class="sample-card" style="border-left:4px solid #10B981;">
                        <div style="font-size:12px; color:#64748B;">含 3% 冷濾損耗總投料：<b>{res_s1['overfill_total_g']:.2f} g</b></div>
                        <div style="margin-top:8px;">Phase A 取用原油：<b style="color:#10B981; font-size:16px;">{res_s1['req_jus_g']:.3f} g</b></div>
                        <div>Phase B 補入酒精：<b style="color:#3B82F6; font-size:16px;">{res_s1['net_alcohol_g']:.2f} g</b></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("✅ 定案採用樣品 A 濃度並送交 Phase 3 PIF", key="lock_s1", use_container_width=True):
                        st.session_state.selected_tier_key = s1_tier
                        st.session_state.locked_for_pif = True
                        st.rerun()

            with col_s2:
                st.markdown("#### 樣品 B：沙龍留香版 (預設 EdP)")
                s2_tier = st.selectbox("樣品 B 濃度", list(PERFUME_CONCENTRATION_PRESETS.keys()), index=2, key="p2_s2_tier")
                s2_bot = st.number_input("瓶數 (B)", 1, 50, 1, 1, key="p2_s2_bot")
                s2_vol = st.selectbox("單瓶容量 (B)", [5, 10, 15, 30, 50], index=1, key="p2_s2_vol")
                res_s2 = core.compute_sample_application(current_formula, PERFUME_CONCENTRATION_PRESETS[s2_tier], s2_bot, s2_vol, MASTER_LIBRARY)
                if res_s2:
                    st.markdown(f"""
                    <div class="sample-card" style="border-left:4px solid #3B82F6;">
                        <div style="font-size:12px; color:#64748B;">含 3% 冷濾損耗總投料：<b>{res_s2['overfill_total_g']:.2f} g</b></div>
                        <div style="margin-top:8px;">Phase A 取用原油：<b style="color:#10B981; font-size:16px;">{res_s2['req_jus_g']:.3f} g</b></div>
                        <div>Phase B 補入酒精：<b style="color:#3B82F6; font-size:16px;">{res_s2['net_alcohol_g']:.2f} g</b></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("✅ 定案採用樣品 B 濃度並送交 Phase 3 PIF", key="lock_s2", use_container_width=True):
                        st.session_state.selected_tier_key = s2_tier
                        st.session_state.locked_for_pif = True
                        st.rerun()

            if st.session_state.locked_for_pif:
                st.success(f"🔒 已將 **{st.session_state.active_mod}**（定案規格：**{st.session_state.selected_tier_key}**）同步至 Phase 3 PIF 審查中心！")

            total_req = (res_s1["req_jus_g"] if res_s1 else 0.0) + (res_s2["req_jus_g"] if res_s2 else 0.0)
            remaining = total_jus_g - total_req
            st.divider()

            c_bal, c_mac = st.columns([1.3, 1.2])
            with c_bal:
                st.markdown("##### 📊 原油母瓶庫存平衡結算：")
                if remaining >= 0:
                    st.success(f"✅ 兩款樣品共需取用原油 **{total_req:.3f} g**，母瓶尚餘 **{remaining:.3f} g**（可封存於深色玻璃瓶進行純油陳化對照）。")
                else:
                    st.error(f"🚨 原油母液不足！共需 **{total_req:.3f} g**，母瓶僅有 **{total_jus_g:.3f} g**（缺口 {-remaining:.3f} g）。請回 Phase 1 等比放大。")

            with c_mac:
                if mac_meta:
                    st.markdown(f"""
                    <div style="background:#F8FAFC; border:1px solid #CBD5E1; padding:12px; border-radius:8px; margin-bottom:8px;">
                        <div style="font-size:14px; font-weight:bold; color:#0F172A;">⏳ 雙階段熟成時鐘：<span style="color:#D97706; font-size:18px;">{mac_meta['maceration']['days']} 天</span></div>
                        <div style="font-size:12px; color:#475569; margin-top:4px;">{mac_meta['maceration']['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    for alert in mac_meta["alerts"]:
                        if alert["level"] == "danger":
                            st.error(alert["msg"])
                        else:
                            st.success(alert["msg"])

# ==============================================================================
# PHASE 3: PIF 產品資訊與合規證書 (含三方保密協議 NDA 直傳 SA 模式)
# ==============================================================================
elif "Phase 3" in active_phase:
    st.markdown(f"""
    <div style="background:#0F172A; padding:8px 16px; border-radius:6px; color:white; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div><b>📑 Phase 3：PIF 產品資訊與合規證書 (B2B / OEM / SA Compliance Dossier)</b> ｜ 標的：<span class="mod-pill">{st.session_state.active_mod}</span></div>
        <div style="font-size:13px; color:#38BDF8;">法規轄區：<b>{region_info['code']}</b> ｜ 成品賦香率：<b>{dosage_ratio*100:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)

    if not mod_calc or total_jus_g <= 0:
        st.warning("⚠️ 請先於 Phase 1 完成配方設計。")
    else:
        all_ifra_pass = all(stat["is_safe"] for stat in rt_calc["ifra_status"].values())
        over_10ppm_list = [a for a in mod_calc["declared_allergens"] if a["ppm"] >= region_info["allergen_ppm_threshold"]]

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("IFRA 51st 審查判定", "✅ PASS 通過" if all_ifra_pass else "❌ FAIL 超標")
        k2.metric("Cat.4 香水最高安全賦香率", f"{rt_calc['max_safe_dosage_pct']:.2f} %")
        k3.metric("須展開標示致敏原 (>10ppm)", f"{len(over_10ppm_list)} 項")
        k4.metric("原油混合比重 / 天然佔比", f"ρ {mod_calc['jus_sg']} / {mac_meta['natural_pct'] if mac_meta else 0}%")

        p3_t1, p3_t2, p3_t3, p3_t4, p3_t5 = st.tabs([
            "1️⃣ 香精全成分比例表 (100% Q&Q)",
            "2️⃣ 過敏原清單與 INCI 標籤",
            "3️⃣ IFRA 51st 符合性證書",
            "4️⃣ 物質安全資料表 (MSDS)",
            "🔒 5️⃣ 三方保密協議 (NDA) 直傳 SA 模式"
        ])

        pif_rows = []
        for ing_id, item in mod_calc["norm_active"].items():
            m = MASTER_LIBRARY[ing_id]
            pct_in_finished_active = (item["active_pct"] / 100.0) * dosage_ratio * 100.0
            pct_in_finished_carrier = (item["carrier_g"] / mod_calc["total_active_g"]) * dosage_ratio * 100.0 if mod_calc["total_active_g"] > 0 else 0.0
            pif_rows.append({
                "CAS No.": item["cas"],
                "成分名稱 (Material Name)": item["name_cn"],
                "成分類別": m.get("type", "-"),
                "供應來源": m.get("supplier", "-"),
                "稀釋規格": f"{item['dilution_pct']:.0f}% in {item['solvent'].split(' ')[0]}" if item["dilution_pct"] < 100 else "100% Pure",
                "純香精中佔比 (% in Pure Oil)": round(item["active_pct"], 3),
                f"成品中純香精佔比 (@{dosage_ratio*100:.0f}%)": round(pct_in_finished_active, 4),
                f"成品中帶入溶劑 (@{dosage_ratio*100:.0f}%)": round(pct_in_finished_carrier, 4)
            })
        df_pif_a = pd.DataFrame(pif_rows).sort_values(by="純香精中佔比 (% in Pure Oil)", ascending=False)

        carrier_incis = []
        for sol_name in mod_calc["batch"]["carrier_solvents"].keys():
            inci_s = SOLVENT_DATABASE.get(sol_name, {}).get("inci", "")
            if inci_s and inci_s not in carrier_incis:
                carrier_incis.append(inci_s)
        inci_allergens = [a["name"].upper() for a in over_10ppm_list]
        base_incis = ["ALCOHOL DENAT.", "PARFUM (FRAGRANCE)", "AQUA (WATER)"] + carrier_incis + inci_allergens
        inci_final_str = ", ".join(base_incis)
        cert_no = f"IFRA-51-{datetime.now().strftime('%Y%m%d')}-{st.session_state.active_mod.replace(' ', '')}"

        # --- PIF-1: 香精全成分比例表 ---
        with p3_t1:
            st.subheader("1. 香精全成分比例表 (100% Full Quantitative Composition)")
            st.caption("供安全評估人員（SA）進行毒理評估與衛生主管機關產品登錄（PIF Part A）使用，精確列出純香精有效成分與稀釋溶劑之比例。")
            st.dataframe(df_pif_a, hide_index=True, use_container_width=True)
            st.download_button(
                "📥 下載 100% 香精全成分比例表 (CSV)",
                data=df_pif_a.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"PIF_100pct_Composition_{st.session_state.active_mod}.csv",
                mime="text/csv"
            )

        # --- PIF-2: 過敏原清單與 INCI 外盒標籤 ---
        with p3_t2:
            st.subheader("2. 法定香精過敏原清單聲明書 (Fragrance Allergen Declaration)")
            st.caption(f"依據 **{st.session_state.selected_region_key}** 規範：駐留型產品超過 **{region_info['allergen_ppm_threshold']:.0f} ppm (0.001%)** 須於外包裝展開標示。")

            allg_summary = rt_calc.get("allergen_summary", {})
            allg_sources = rt_calc.get("allergen_sources", {})
            if allg_summary:
                allg_detail_rows = []
                for a_name, ppm in sorted(allg_summary.items(), key=lambda x: x[1], reverse=True):
                    is_declare = ppm >= region_info["allergen_ppm_threshold"]
                    allg_detail_rows.append({
                        "法定致敏原 (INCI Name)": a_name.upper(),
                        "主要來源原料": ", ".join(set(allg_sources.get(a_name, []))),
                        "純香精中含量 (%)": round((ppm / 10000.0) / dosage_ratio, 4) if dosage_ratio > 0 else 0.0,
                        "最終成品濃度 (%)": f"{ppm / 10000.0:.5f}%",
                        "最終成品濃度 (ppm)": round(ppm, 2),
                        "法規標示義務": "⚠️ 強制外盒標示 (>10 ppm)" if is_declare else "✅ 免標示 (<10 ppm)"
                    })
                df_allg = pd.DataFrame(allg_detail_rows)
                st.dataframe(df_allg, hide_index=True, use_container_width=True)
                st.download_button(
                    "📥 下載過敏原清單聲明書 (CSV)",
                    data=df_allg.to_csv(index=False).encode("utf-8-sig"),
                    file_name=f"PIF_Allergens_{st.session_state.active_mod}.csv",
                    mime="text/csv"
                )
            else:
                st.success("✅ 經 GC-MS 成分穿透計算，此配方在最終成品中未檢出任何法定致敏原。")

            st.divider()
            st.markdown("#### 🏷️ 外包裝法定 INCI 全成分展開標籤 (依含量降冪排列)")
            st.code(inci_final_str, language="text")

        # --- PIF-3: IFRA 51st 符合性證書 ---
        with p3_t3:
            st.subheader("3. IFRA 51st Amendment 符合性證書 (IFRA Conformity Certificate)")
            st.markdown(f"""
            <div class="cert-box">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #CBD5E1; padding-bottom:8px; margin-bottom:10px;">
                    <div>
                        <h4 style="margin:0; color:#0F172A;">CERTIFICATE OF CONFORMITY WITH IFRA STANDARDS (51st Amendment)</h4>
                        <span style="font-size:12px; color:#64748B;">Certificate No.: <code>{cert_no}</code> ｜ Issue Date: {datetime.now().strftime("%Y-%m-%d")}</span>
                    </div>
                    <div style="background:{'#DCFCE7' if all_ifra_pass else '#FEE2E2'}; color:{'#15803D' if all_ifra_pass else '#B91C1C'}; padding:4px 12px; border-radius:4px; font-weight:bold;">
                        {'CONFORMING (PASS)' if all_ifra_pass else 'EXCEEDS LIMIT (FAIL)'}
                    </div>
                </div>
                <div style="font-size:13px; color:#334155;">
                    茲證明配方 <b>{st.session_state.active_mod}</b> 經評估符合國際日用香料香精協會（IFRA）第 51 次修訂版標準。在針對不同終端產品類別（Category 1 至 Category 12）應用時，本純香精原油在最終成品中之<b>最高安全允許添加濃度（Maximum Allowable Concentration）</b>如下表所示：
                </div>
            </div>
            """, unsafe_allow_html=True)

            df_ifra_cats = pd.DataFrame(rt_calc["ifra_categories"])
            st.dataframe(df_ifra_cats, hide_index=True, use_container_width=True)

            with st.expander("🔍 檢視單體級 CAS 質量合併限制明細 (Ingredient-level IFRA Audit)"):
                ifra_rows = []
                for ing_id, stat in rt_calc["ifra_status"].items():
                    ifra_rows.append({
                        "原料名稱": MASTER_LIBRARY[ing_id]["name_cn"],
                        "CAS No.": stat["cas"],
                        "純油中佔比 (%)": f"{stat['active_share_pct']:.2f}%",
                        f"成品殘留 (@{dosage_ratio*100:.0f}%)": f"{stat['finished_pct']:.4f}%",
                        "IFRA Cat.4 限值 (%)": f"{stat['limit']:.2f}%",
                        "判定": "✅ PASS" if stat["is_safe"] else "❌ FAIL"
                    })
                st.dataframe(pd.DataFrame(ifra_rows), hide_index=True, use_container_width=True)

            st.download_button(
                "📥 下載 IFRA 51st 跨品類符合性證書表 (CSV)",
                data=df_ifra_cats.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"IFRA_51st_Certificate_{st.session_state.active_mod}.csv",
                mime="text/csv"
            )

        # --- PIF-4: 物質安全資料表 (MSDS / SDS) ---
        with p3_t4:
            st.subheader("4. 物質安全資料表摘要 (Material Safety Data Sheet — MSDS / SDS)")
            st.caption("依據全球化學品統一分類和標示制度（GHS）編製，供安全評估人員（SA）、代工廠收料與貨運安全評估使用。")

            c_sds1, c_sds2 = st.columns(2)
            with c_sds1:
                st.markdown(f"""
                <div class="doc-sheet">
                    <div class="doc-title"><h4 style="margin:0;">Section 1–3 & 9：辨識與理化特性</h4></div>
                    <ul style="font-size:13px; line-height:1.75;">
                        <li><b>產品名稱：</b>Fragrance Compound — {st.session_state.active_mod}</li>
                        <li><b>外觀與氣味：</b>淡黃色至琥珀色透明油狀液體，具特徵性芳香氣味。</li>
                        <li><b>相對密度 (20°C)：</b>ρ = <b>{mod_calc['jus_sg']}</b> g/cm³</li>
                        <li><b>水溶性：</b>不溶於水，可與 95% 變性乙醇、DPG、TEC、IPM 完全互溶。</li>
                        <li><b>閃火點 (Flash Point)：</b>純原油約 68°C（閉杯）；稀釋為 {dosage_ratio*100:.0f}% 成品香水後約 <b>14°C</b>（高度易燃）。</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with c_sds2:
                st.markdown(f"""
                <div class="doc-sheet">
                    <div class="doc-title"><h4 style="margin:0;">Section 2, 7 & 10：GHS 危害分類與操作儲存</h4></div>
                    <ul style="font-size:13px; line-height:1.75;">
                        <li><b>GHS 危害分類：</b>易燃液體第 2 類（成品香水）、皮膚過敏物質第 1 類（H317）、水環境之危害物質慢性第 2 類（H411）。</li>
                        <li><b>安全處置 (Section 7)：</b>操作時建議配戴丁腈手套與護目鏡，遠離火源、火花及熱表面。</li>
                        <li><b>儲存與熟成條件：</b>避光密封儲存於 15–20°C 陰涼通風處；建議熟成 <b>{mac_meta['maceration']['days'] if mac_meta else 14} 天</b> 並於 -4°C 冷藏後 0.45μm 過濾。</li>
                        <li><b>光敏性特別提示：</b>{"⚠️ 含未去光敏佛手柑，成品上限 0.4%。" if (mac_meta and mac_meta["has_bergamot_phototoxic"]) else "✅ 未檢出高風險光敏性原料。"}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        # --- PIF-5: 三方保密協議 (NDA) 直傳 SA 模式 ---
        with p3_t5:
            st.subheader("🔒 三方保密協議（Tri-Party NDA）直傳安全評估人員（SA）模式")
            st.markdown("""
            <div class="nda-box">
                <h4 style="margin:0 0 6px 0; color:#92400E;">🛡️ 智慧財產權隔離保護機制（IP Protection Protocol）</h4>
                <div style="font-size:13px; line-height:1.6;">
                    依據歐盟 EC 1223/2009 與台灣 TFDA 化粧品 PIF 規範，安全評估人員（Safety Assessor, SA）簽署安全資料評估報告（CPSR）前，必須審閱<b>香精 100% 完整成分比例表</b>。<br>
                    為避免核心配方機密在品牌商或代工廠端外流，請啟用本模式：由<b>調香室／香精廠 × 品牌委託方 × 獨立安全評估人員（SA）</b>簽署三方保密協議（NDA）後，將本系統產出之<b>「SA 機密直傳專包（100% 成分表 + MSDS + IFRA 51st 證書）」</b>直接加密寄送予 SA，品牌商與代工廠端僅需留存過敏原聲明與 INCI 標籤即可完成合規。
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_nda1, c_nda2 = st.columns(2)
            with c_nda1:
                nda_perfumer = st.text_input("① 揭露方（調香室 / 香精供應商）", value="Nanmen Scent Lab (南門調香實驗室)", key="nda_perfumer")
                nda_brand = st.text_input("② 委託方（品牌商 / 產品登錄人）", value="", placeholder="輸入委託品牌商名稱（空白欄位）...", key="nda_brand")
            with c_nda2:
                nda_sa_name = st.text_input("③ 接收方（委託安全評估人員 SA 姓名 / 機構）", value="", placeholder="輸入 SA 姓名、資格證號或評估機構...", key="nda_sa_name")
                nda_ref_no = st.text_input("④ 三方保密協議編號 / 簽署日期", value=f"NDA-{datetime.now().strftime('%Y%m%d')}-01", key="nda_ref_no")

            nda_confirmed = st.checkbox("✅ 確認三方保密協議（Tri-Party NDA）已簽署生效，授權生成含 100% 商業機密成分之 SA 直傳文件包", key="nda_chk")

            allergen_lines = "\n".join([f"- {a['name'].upper()}: {a['ppm']} ppm ({a['pct_finished']}%)" for a in over_10ppm_list]) if over_10ppm_list else "- None above 10 ppm threshold."
            ifra_cat_lines = "\n".join([f"- {c['IFRA 類別']} ({c['適用產品應用範圍']}): Max {c['純香精最高允許濃度 (%)']}" for c in rt_calc["ifra_categories"]])
            comp_lines_100 = "\n".join([
                f"- [CAS: {r['CAS No.']}] {r['成分名稱 (Material Name)']} | 純油佔比: {r['純香精中佔比 (% in Pure Oil)']}% | 成品佔比: {r[f'成品中純香精佔比 (@{dosage_ratio*100:.0f}%)']}% | 稀釋規格: {r['稀釋規格']}"
                for r in pif_rows
            ])

            sa_confidential_dossier = f"""# STRICTLY CONFIDENTIAL — DIRECT-TO-SAFETY ASSESSOR (SA) PIF PACKAGE
## UNDER TRI-PARTY NON-DISCLOSURE AGREEMENT (NDA)

- **NDA Reference No.**: {nda_ref_no}
- **Disclosing Party (Fragrance Creator)**: {nda_perfumer}
- **Commissioning Party (Brand Owner)**: {nda_brand if nda_brand else '[Pending Brand Name]'}
- **Receiving Party (Authorized Safety Assessor / SA)**: {nda_sa_name if nda_sa_name else '[Pending SA Name]'}
- **Issue Date**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
- **Formula / Mod Code**: {st.session_state.active_mod}
- **Target Product Application & Dosage**: {st.session_state.selected_tier_key} ({dosage_ratio*100:.1f}%)
- **Regulatory Framework**: {st.session_state.selected_region_key}

> **CONFIDENTIALITY NOTICE**: This document contains 100% proprietary fragrance formulation data disclosed solely to the designated Safety Assessor (SA) under the executed Tri-Party NDA ({nda_ref_no}) for toxicological safety evaluation (CPSR / PIF) purposes only. Do not forward or disclose Section 1 to third parties, OEMs, or brand marketing personnel.

---

## PART 1: 100% FULL QUANTITATIVE FRAGRANCE COMPOSITION (PROPRIETARY)
- **Pure Active Fragrance Concentrate Share in Jus**: {round(mod_calc['total_active_g'] / mod_calc['total_gross_g'] * 100.0, 2)}%
- **Carrier Solvent Share in Jus**: {round(mod_calc['total_carrier_g'] / mod_calc['total_gross_g'] * 100.0, 2)}%

{comp_lines_100}

---

## PART 2: IFRA 51st AMENDMENT CONFORMITY CERTIFICATE ({cert_no})
- **Overall Compliance Status**: {'CONFORMING (PASS)' if all_ifra_pass else 'EXCEEDS LIMIT (FAIL)'}
- **Maximum Allowable Concentration in Cat. 4 (Fine Fragrance)**: {rt_calc['max_safe_dosage_pct']:.2f}%

{ifra_cat_lines}

---

## PART 3: MATERIAL SAFETY DATA SHEET (MSDS / GHS SUMMARY)
- **Product Identification**: Fragrance Compound — {st.session_state.active_mod}
- **Appearance & Odor**: Pale yellow to amber clear oily liquid, characteristic aromatic odor.
- **Relative Density (20°C)**: {mod_calc['jus_sg']} g/cm3
- **Flash Point**: ~68°C (Pure Jus, closed cup) / ~14°C (Finished alcoholic perfume at {dosage_ratio*100:.0f}%)
- **GHS Classification**: Flammable Liquid Cat. 2 (H225 - finished product), Skin Sensitization Cat. 1 (H317), Aquatic Chronic Cat. 2 (H411).
- **Recommended Maceration & Filtration**: {mac_meta['maceration']['days'] if mac_meta else 14} days maturation; -4°C chilling followed by 0.45μm filtration.

---

## PART 4: REGULATED ALLERGEN DECLARATION & INCI LABELING
- **Official INCI String**: {inci_final_str}
- **Allergens > 10 ppm in Finished Product**:
{allergen_lines}
"""

            if nda_confirmed:
                c_dl1, c_dl2 = st.columns(2)
                c_dl1.download_button(
                    "🔒 下載【NDA 直傳 SA 完整合規技術書】(100% 成分 + MSDS + IFRA 證書)",
                    data=sa_confidential_dossier.encode("utf-8"),
                    file_name=f"CONFIDENTIAL_SA_PIF_{st.session_state.active_mod}_{nda_ref_no}.md",
                    mime="text/markdown",
                    type="primary",
                    use_container_width=True
                )
                c_dl2.download_button(
                    "📊 下載【NDA 直傳 SA 100% 成分明細表】(CSV)",
                    data=df_pif_a.to_csv(index=False).encode("utf-8-sig"),
                    file_name=f"CONFIDENTIAL_SA_100pct_Formula_{st.session_state.active_mod}_{nda_ref_no}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("☝️ 請先勾選上方「確認三方保密協議（Tri-Party NDA）已簽署生效」，即可解鎖下載直傳給 SA 的 100% 機密完整文件包。")

# ==============================================================================
# PHASE 4: 商業量產與投遞框架 (BMR Dosing Sheet & Blank Landed Cost Framework)
# ==============================================================================
elif "Phase 4" in active_phase:
    st.markdown(f"""
    <div style="background:#0F172A; padding:8px 16px; border-radius:6px; color:white; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div><b>🏭 Phase 4：商業量產工單與落地成本框架</b> ｜ 定案版本：<span class="mod-pill">{st.session_state.active_mod}</span></div>
        <div style="font-size:13px; color:#38BDF8;">交付賦香率：<b>{dosage_ratio*100:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)

    if not mod_calc or total_jus_g <= 0:
        st.warning("⚠️ 請先於 Phase 1 完成配方設計。")
    else:
        st.subheader("1. 量產批次規模與工單表頭 (Batch Sizing & Dispatch Info)")
        c_b1, c_b2, c_b3 = st.columns(3)
        target_bottles = c_b1.number_input("首批量產瓶數 (Bottles)", min_value=50, max_value=50000, value=500, step=50)
        target_vol = c_b2.selectbox("單瓶容量規格 (ml)", [10, 15, 30, 50, 100], index=2)
        overfill_pct = c_b3.number_input("冷濾與灌裝損耗裕度 (%)", min_value=0.0, max_value=15.0, value=3.0, step=0.5)

        c_d1, c_d2 = st.columns(2)
        dispatch_target = c_d1.text_input("投遞 / 生產單位名稱（空白欄位）", value="", placeholder="未來可填寫代工廠或調香室名稱...")
        dispatch_batch_no = c_d2.text_input("生產批號 / 工單編號（空白欄位）", value="", placeholder="例如: BMR-2026-001...")

        scale_calc = core.calculate_mod_profile(
            current_formula, dosage_ratio,
            {"bottles": target_bottles, "vol_ml": target_vol},
            MASTER_LIBRARY, overfill_pct=overfill_pct
        )
        b_info = scale_calc["batch"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("成品總預投料重 (含損耗)", f"{b_info['total_g']:,.1f} g")
        m2.metric("Phase A 調香室投料重 (Jus)", f"{b_info['target_jus_g']:,.1f} g")
        m3.metric("Phase B 95% 酒精淨投重", f"{b_info['alcohol_g']:,.1f} g")
        m4.metric("本批次純香精內料基準成本", f"NT$ {b_info['batch_fragrance_cost']:,.0f}")

        st.divider()

        st.subheader("2. 工廠生產投料與投遞工單 (Factory BMR Dosing & Dispatch Sheet)")
        st.caption("同時列出「調香室實際投料重（含溶劑）」與「100% 純精油採購淨重」，可直接匯出作為工廠生產投料單或原料發料投遞單。")

        bmr_df = pd.DataFrame([{
            "工單編號": dispatch_batch_no if dispatch_batch_no else "-",
            "投遞對象": dispatch_target if dispatch_target else "-",
            "投料序": r["seq"],
            "投料階段": r["phase"],
            "CAS No.": r["cas"],
            "原料名稱": r["name"],
            "稀釋規格": r["spec"],
            "純油佔比 (%)": r["active_w_pct"],
            "100% 純原液淨重 (g)": r["pure_active_g"],
            "實際投料 / 發料重 (g)": r["target_batch_g"],
            "複核簽章": "⬜"
        } for r in scale_calc["bmr_rows"]])

        st.dataframe(bmr_df, hide_index=True, use_container_width=True)
        bmr_csv = bmr_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 下載工廠投料與投遞工單 (Factory BMR & Dispatch Sheet CSV)",
            data=bmr_csv,
            file_name=f"Factory_BMR_Dispatch_{st.session_state.active_mod}_{target_bottles}pcs.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

        st.divider()

        st.subheader("3. 單瓶落地成本框架 (Unit Landed Cost / COGS Framework)")
        st.info("💡 **架構預留說明**：此區塊僅建立落地成本結構框架，**不設任何預設單位價格、不作假設性加總計算**。所有項目名稱、廠商與報價備註皆保留為空白欄位，待未來洽談廠商後再行納入系統。")

        fragrance_cost_per_bottle = b_info["batch_fragrance_cost"] / target_bottles if target_bottles > 0 else 0.0

        with st.container(border=True):
            st.markdown(f"**[已建檔項目] 香精內料單瓶基準成本**（由 Phase 1 原料庫自動換算）：**`NT$ {fragrance_cost_per_bottle:.2f} / 瓶`**")
            st.divider()
            st.markdown("**[未來廠商對接空白框架] 自訂成本項目與廠商名稱欄位：**")

            for idx in range(1, 7):
                fc1, fc2, fc3 = st.columns([1.4, 1.4, 1.0])
                fc1.text_input(f"成本項目名稱 #{idx}", value="", placeholder=f"空白欄位 #{idx}（例如：玻璃瓶器 / 噴頭 / 酒精 / OEM 灌裝...）", key=f"cogs_name_{idx}")
                fc2.text_input(f"合作廠商與規格 #{idx}", value="", placeholder="空白欄位（廠商名稱 / MOQ / 交期條件）", key=f"cogs_vendor_{idx}")
                fc3.text_input(f"單位報價欄位 #{idx}", value="", placeholder="待廠商報價（不設預設值）", key=f"cogs_quote_{idx}")
