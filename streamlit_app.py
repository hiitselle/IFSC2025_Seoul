import streamlit as st
import pandas as pd
import requests
from io import StringIO
import time
from datetime import datetime, timedelta
import logging
import re
import os
import unicodedata
from typing import Dict, Tuple, List, Optional, Any, Callable
import hashlib
import hmac
from collections import defaultdict, deque
from functools import wraps
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
from concurrent.futures import ThreadPoolExecutor
import json


# Multi-language support module - Add this to your existing streamlit_app.py

# Language translations dictionary
# Multi-language support module - Add this to your existing streamlit_app.py

# Language translations dictionary
LANGUAGES = {
    "🇺🇸 English": {
        "app_title": "🧗‍♂️ IFSC 2025 World Championships",
        "app_subtitle": "Live Competition Results Dashboard",
        "app_description": "Real-time climbing competition tracking - Auto-refreshing every 2 seconds",
        "dashboard_controls": "🎯 Dashboard Controls",
        "refresh_settings": "🔄 Refresh Settings",
        "auto_refresh_status": "Auto-refresh is ALWAYS ON - Every 2 seconds",
        "manual_refresh": "🔄 Manual Refresh",
        "clear_cache": "🗑️ Clear Cache",
        "last_refresh": "🕒 Last refresh: {}s ago",
        "next_refresh": "⚡ Next refresh in: {}s",
        "competition_filters": "🎯 Competition Filters",
        "discipline": "⛰️ Discipline",
        "gender": "👤 Gender",
        "round": "🎯 Round",
        "competition_overview": "🚀 Competition Overview",
        "total": "🏆 Total",
        "live": "🔴 Live",
        "completed": "✅ Completed",
        "upcoming": "🔄 Upcoming",
        "live_results": "📊 Live Results",
        "current_standings": "📋 Current Standings",
        "athletes": "👥 Athletes",
        "problems_completed": "🧗‍♂️ Problems Completed",
        "avg_score": "📊 Avg Score",
        "leader": "🥇 Leader",
        "qualification_thresholds": "🎯 Qualification Thresholds",
        "no_data": "⚠️ No data available",
        "no_competitions_found": "⚠️ No Competitions Found",
        "adjust_filters": "No competitions match your current filters. Please adjust your selection.",
        "loading": "Loading {}...",
        "last_updated": "📡 Last updated: {}",
        "refreshed": "✅ Refreshed!",
        "cache_cleared": "✅ Cache cleared!",
        "all": "All",
        "boulder": "Boulder",
        "lead": "Lead",
        "male": "Male",
        "female": "Female",
        "semis": "Semis",
        "final": "Final",
          "live_upper": "LIVE",
        "completed_upper": "COMPLETED", 
        "upcoming_upper": "UPCOMING",
        "name": "Name",
        "score": "Score", 
        "status": "Status",
        "awaiting_result": "Awaiting Result",
        "progress": "Progress",
        "boulder_remaining": "boulder remaining",
        "targets": "Targets",
        "strategy": "Strategy",
        "for_1st_hold": "For 1st Hold",
        "for_2nd_hold": "For 2nd Hold", 
        "for_3rd_hold": "For 3rd Hold",
        "for_8th_hold": "For 8th Hold",
        "for_8th_points": "For 8th Points",
        "worst_finish": "Worst Finish",
        "unknown": "Unknown",
        "no_boulder_data": "No boulder data",
        "raw_data": "Raw Data",
        "data_validation_failed": "Data validation failed",
        "name_column_not_found": "Name column not found in data",
        "application_error": "Application Error",
        "refresh_page": "Please refresh the page or contact support if the issue persists.",
        "debug_information": "Debug Information",
        "help_discipline": "Filter by climbing discipline",
        "help_gender": "Filter by gender category", 
        "help_round": "Filter by competition round",
        "ifsc_world_championships": "IFSC World Championships 2025",
        "real_time_results": "Real-time Results",
        "auto_refresh_always_on": "Auto-refresh: ALWAYS ON (2s)",
    },
    "🇫🇷 Français": {
        "app_title": "🧗‍♂️ Championnats du Monde IFSC 2025",
        "app_subtitle": "Tableau de Bord des Résultats en Direct",
        "app_description": "Suivi en temps réel des compétitions d'escalade - Actualisation automatique toutes les 2 secondes",
        "dashboard_controls": "🎯 Contrôles du Tableau de Bord",
        "refresh_settings": "🔄 Paramètres d'Actualisation",
        "auto_refresh_status": "L'actualisation automatique est TOUJOURS ACTIVÉE - Toutes les 2 secondes",
        "manual_refresh": "🔄 Actualisation Manuelle",
        "clear_cache": "🗑️ Vider le Cache",
        "last_refresh": "🕒 Dernière actualisation : il y a {}s",
        "next_refresh": "⚡ Prochaine actualisation dans : {}s",
        "competition_filters": "🎯 Filtres de Compétition",
        "discipline": "⛰️ Discipline",
        "gender": "👤 Genre",
        "round": "🎯 Manche",
        "competition_overview": "🚀 Aperçu de la Compétition",
        "total": "🏆 Total",
        "live": "🔴 En Direct",
        "completed": "✅ Terminé",
        "upcoming": "🔄 À Venir",
        "live_results": "📊 Résultats en Direct",
        "current_standings": "📋 Classement Actuel",
        "athletes": "👥 Athlètes",
        "problems_completed": "🧗‍♂️ Problèmes Résolus",
        "avg_score": "📊 Score Moyen",
        "leader": "🥇 Leader",
        "qualification_thresholds": "🎯 Seuils de Qualification",
        "no_data": "⚠️ Aucune donnée disponible",
        "no_competitions_found": "⚠️ Aucune Compétition Trouvée",
        "adjust_filters": "Aucune compétition ne correspond à vos filtres actuels. Veuillez ajuster votre sélection.",
        "loading": "Chargement de {}...",
        "last_updated": "📡 Dernière mise à jour : {}",
        "refreshed": "✅ Actualisé !",
        "cache_cleared": "✅ Cache vidé !",
        "all": "Tous",
        "boulder": "Bloc",
        "lead": "Difficulté",
        "male": "Hommes",
        "female": "Femmes",
        "semis": "Demi-finales",
        "final": "Finale",
        "live_upper": "EN DIRECT",
        "completed_upper": "TERMINÉ",
        "upcoming_upper": "À VENIR",
        "name": "Nom",
        "score": "Score",
        "status": "Statut", 
        "awaiting_result": "En Attente du Résultat",
        "progress": "Progrès",
        "boulder_remaining": "bloc restant",
        "targets": "Objectifs",
        "strategy": "Stratégie",
        "for_1st_hold": "Pour 1ère Place",
        "for_2nd_hold": "Pour 2ème Place",
        "for_3rd_hold": "Pour 3ème Place", 
        "for_8th_hold": "Pour 8ème Place",
        "for_8th_points": "Pour 8ème Points",
        "worst_finish": "Pire Classement",
        "unknown": "Inconnu",
        "no_boulder_data": "Aucune donnée de bloc",
        "raw_data": "Données Brutes",
        "data_validation_failed": "Validation des données échouée",
        "name_column_not_found": "Colonne nom non trouvée dans les données",
        "application_error": "Erreur d'Application",
        "refresh_page": "Veuillez actualiser la page ou contacter le support si le problème persiste.",
        "debug_information": "Informations de Débogage",
        "help_discipline": "Filtrer par discipline d'escalade",
        "help_gender": "Filtrer par catégorie de genre",
        "help_round": "Filtrer par manche de compétition", 
        "ifsc_world_championships": "Championnats du Monde IFSC 2025",
        "real_time_results": "Résultats en Temps Réel",
        "auto_refresh_always_on": "Actualisation automatique : TOUJOURS ACTIVE (2s)",
    },
    },
    "🇩🇪 Deutsch": {
        "app_title": "🧗‍♂️ IFSC Weltmeisterschaft 2025",
        "app_subtitle": "Live Wettkampfergebnis Dashboard",
        "app_description": "Echtzeit-Kletternwettkampf-Verfolgung - Automatische Aktualisierung alle 2 Sekunden",
        "dashboard_controls": "🎯 Dashboard-Steuerung",
        "refresh_settings": "🔄 Aktualisierungseinstellungen",
        "auto_refresh_status": "Automatische Aktualisierung ist IMMER EIN - Alle 2 Sekunden",
        "manual_refresh": "🔄 Manuelle Aktualisierung",
        "clear_cache": "🗑️ Cache Leeren",
        "last_refresh": "🕒 Letzte Aktualisierung: vor {}s",
        "next_refresh": "⚡ Nächste Aktualisierung in: {}s",
        "competition_filters": "🎯 Wettkampffilter",
        "discipline": "⛰️ Disziplin",
        "gender": "👤 Geschlecht",
        "round": "🎯 Runde",
        "competition_overview": "🚀 Wettkampfübersicht",
        "total": "🏆 Gesamt",
        "live": "🔴 Live",
        "completed": "✅ Abgeschlossen",
        "upcoming": "🔄 Anstehend",
        "live_results": "📊 Live-Ergebnisse",
        "current_standings": "📋 Aktuelle Rangliste",
        "athletes": "👥 Athleten",
        "problems_completed": "🧗‍♂️ Gelöste Probleme",
        "avg_score": "📊 Durchschnittswertung",
        "leader": "🥇 Führender",
        "qualification_thresholds": "🎯 Qualifikationsschwellen",
        "no_data": "⚠️ Keine Daten verfügbar",
        "no_competitions_found": "⚠️ Keine Wettkämpfe Gefunden",
        "adjust_filters": "Keine Wettkämpfe entsprechen Ihren aktuellen Filtern. Bitte passen Sie Ihre Auswahl an.",
        "loading": "Lade {}...",
        "last_updated": "📡 Zuletzt aktualisiert: {}",
        "refreshed": "✅ Aktualisiert!",
        "cache_cleared": "✅ Cache geleert!",
        "all": "Alle",
        "boulder": "Bouldern",
        "lead": "Vorstieg",
        "male": "Männer",
        "female": "Frauen",
        "semis": "Halbfinale",
        "final": "Finale",
    },
    "🇪🇸 Español": {
        "app_title": "🧗‍♂️ Campeonatos Mundiales IFSC 2025",
        "app_subtitle": "Panel de Resultados de Competición en Vivo",
        "app_description": "Seguimiento de competiciones de escalada en tiempo real - Actualización automática cada 2 segundos",
        "dashboard_controls": "🎯 Controles del Panel",
        "refresh_settings": "🔄 Configuración de Actualización",
        "auto_refresh_status": "La actualización automática está SIEMPRE ACTIVADA - Cada 2 segundos",
        "manual_refresh": "🔄 Actualización Manual",
        "clear_cache": "🗑️ Limpiar Caché",
        "last_refresh": "🕒 Última actualización: hace {}s",
        "next_refresh": "⚡ Próxima actualización en: {}s",
        "competition_filters": "🎯 Filtros de Competición",
        "discipline": "⛰️ Disciplina",
        "gender": "👤 Género",
        "round": "🎯 Ronda",
        "competition_overview": "🚀 Resumen de la Competición",
        "total": "🏆 Total",
        "live": "🔴 En Vivo",
        "completed": "✅ Completado",
        "upcoming": "🔄 Próximo",
        "live_results": "📊 Resultados en Vivo",
        "current_standings": "📋 Clasificación Actual",
        "athletes": "👥 Atletas",
        "problems_completed": "🧗‍♂️ Problemas Completados",
        "avg_score": "📊 Puntuación Media",
        "leader": "🥇 Líder",
        "qualification_thresholds": "🎯 Umbrales de Clasificación",
        "no_data": "⚠️ No hay datos disponibles",
        "no_competitions_found": "⚠️ No se Encontraron Competiciones",
        "adjust_filters": "Ninguna competición coincide con sus filtros actuales. Por favor, ajuste su selección.",
        "loading": "Cargando {}...",
        "last_updated": "📡 Última actualización: {}",
        "refreshed": "✅ ¡Actualizado!",
        "cache_cleared": "✅ ¡Caché limpiado!",
        "all": "Todos",
        "boulder": "Boulder",
        "lead": "Dificultad",
        "male": "Hombres",
        "female": "Mujeres",
        "semis": "Semifinales",
        "final": "Final",
    },
    "🇮🇹 Italiano": {
        "app_title": "🧗‍♂️ Campionati Mondiali IFSC 2025",
        "app_subtitle": "Dashboard dei Risultati di Gara in Diretta",
        "app_description": "Monitoraggio delle gare di arrampicata in tempo reale - Aggiornamento automatico ogni 2 secondi",
        "dashboard_controls": "🎯 Controlli Dashboard",
        "refresh_settings": "🔄 Impostazioni Aggiornamento",
        "auto_refresh_status": "L'aggiornamento automatico è SEMPRE ATTIVO - Ogni 2 secondi",
        "manual_refresh": "🔄 Aggiornamento Manuale",
        "clear_cache": "🗑️ Svuota Cache",
        "last_refresh": "🕒 Ultimo aggiornamento: {}s fa",
        "next_refresh": "⚡ Prossimo aggiornamento in: {}s",
        "competition_filters": "🎯 Filtri Competizione",
        "discipline": "⛰️ Disciplina",
        "gender": "👤 Genere",
        "round": "🎯 Round",
        "competition_overview": "🚀 Panoramica Competizione",
        "total": "🏆 Totale",
        "live": "🔴 In Diretta",
        "completed": "✅ Completato",
        "upcoming": "🔄 Prossimo",
        "live_results": "📊 Risultati in Diretta",
        "current_standings": "📋 Classifica Attuale",
        "athletes": "👥 Atleti",
        "problems_completed": "🧗‍♂️ Problemi Completati",
        "avg_score": "📊 Punteggio Medio",
        "leader": "🥇 Leader",
        "qualification_thresholds": "🎯 Soglie di Qualificazione",
        "no_data": "⚠️ Nessun dato disponibile",
        "no_competitions_found": "⚠️ Nessuna Gara Trovata",
        "adjust_filters": "Nessuna gara corrisponde ai tuoi filtri attuali. Si prega di regolare la selezione.",
        "loading": "Caricamento {}...",
        "last_updated": "📡 Ultimo aggiornamento: {}",
        "refreshed": "✅ Aggiornato!",
        "cache_cleared": "✅ Cache svuotata!",
        "all": "Tutti",
        "boulder": "Boulder",
        "lead": "Lead",
        "male": "Uomini",
        "female": "Donne",
        "semis": "Semifinali",
        "final": "Finale",
    },
    "🇯🇵 日本語": {
        "app_title": "🧗‍♂️ IFSC 2025世界選手権",
        "app_subtitle": "ライブ競技結果ダッシュボード",
        "app_description": "リアルタイムクライミング競技追跡 - 2秒ごとの自動更新",
        "dashboard_controls": "🎯 ダッシュボード制御",
        "refresh_settings": "🔄 更新設定",
        "auto_refresh_status": "自動更新は常にON - 2秒ごと",
        "manual_refresh": "🔄 手動更新",
        "clear_cache": "🗑️ キャッシュクリア",
        "last_refresh": "🕒 最終更新: {}秒前",
        "next_refresh": "⚡ 次の更新まで: {}秒",
        "competition_filters": "🎯 競技フィルター",
        "discipline": "⛰️ 種目",
        "gender": "👤 性別",
        "round": "🎯 ラウンド",
        "competition_overview": "🚀 競技概要",
        "total": "🏆 合計",
        "live": "🔴 ライブ",
        "completed": "✅ 完了",
        "upcoming": "🔄 予定",
        "live_results": "📊 ライブ結果",
        "current_standings": "📋 現在の順位",
        "athletes": "👥 選手",
        "problems_completed": "🧗‍♂️ 完登課題数",
        "avg_score": "📊 平均得点",
        "leader": "🥇 首位",
        "qualification_thresholds": "🎯 予選通過ライン",
        "no_data": "⚠️ データがありません",
        "no_competitions_found": "⚠️ 競技が見つかりません",
        "adjust_filters": "現在のフィルターに一致する競技がありません。選択を調整してください。",
        "loading": "{}を読み込み中...",
        "last_updated": "📡 最終更新: {}",
        "refreshed": "✅ 更新完了！",
        "cache_cleared": "✅ キャッシュクリア完了！",
        "all": "すべて",
        "boulder": "ボルダリング",
        "lead": "リード",
        "male": "男子",
        "female": "女子",
        "semis": "準決勝",
        "final": "決勝",
    },
    "🇰🇷 한국어": {
        "app_title": "🧗‍♂️ IFSC 2025 세계선수권대회",
        "app_subtitle": "실시간 경기 결과 대시보드",
        "app_description": "실시간 클라이밍 경기 추적 - 2초마다 자동 새로고침",
        "dashboard_controls": "🎯 대시보드 제어",
        "refresh_settings": "🔄 새로고침 설정",
        "auto_refresh_status": "자동 새로고침이 항상 켜져 있습니다 - 2초마다",
        "manual_refresh": "🔄 수동 새로고침",
        "clear_cache": "🗑️ 캐시 지우기",
        "last_refresh": "🕒 마지막 새로고침: {}초 전",
        "next_refresh": "⚡ 다음 새로고침까지: {}초",
        "competition_filters": "🎯 경기 필터",
        "discipline": "⛰️ 종목",
        "gender": "👤 성별",
        "round": "🎯 라운드",
        "competition_overview": "🚀 경기 개요",
        "total": "🏆 전체",
        "live": "🔴 라이브",
        "completed": "✅ 완료",
        "upcoming": "🔄 예정",
        "live_results": "📊 실시간 결과",
        "current_standings": "📋 현재 순위",
        "athletes": "👥 선수",
        "problems_completed": "🧗‍♂️ 완등한 문제 수",
        "avg_score": "📊 평균 점수",
        "leader": "🥇 선두",
        "qualification_thresholds": "🎯 통과 기준",
        "no_data": "⚠️ 데이터가 없습니다",
        "no_competitions_found": "⚠️ 경기를 찾을 수 없습니다",
        "adjust_filters": "현재 필터와 일치하는 경기가 없습니다. 선택을 조정해 주세요.",
        "loading": "{} 로딩 중...",
        "last_updated": "📡 마지막 업데이트: {}",
        "refreshed": "✅ 새로고침 완료!",
        "cache_cleared": "✅ 캐시 지우기 완료!",
        "all": "전체",
        "boulder": "볼더링",
        "lead": "리드",
        "male": "남자",
        "female": "여자",
        "semis": "준결승",
        "final": "결승",
    }
}

def get_text(key: str, language: str = None) -> str:
    """Get localized text for the given key"""
    if language is None:
        language = st.session_state.get('selected_language', '🇺🇸 English')
    
    # Fallback to English if key not found in selected language
    text = LANGUAGES.get(language, {}).get(key)
    if text is None:
        text = LANGUAGES['🇺🇸 English'].get(key, key)
    
    return text

def language_selector():
    """Display language selector at the top of the app"""
    # Add language selector CSS
    st.markdown("""
    <style>
        .language-selector {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 0.5rem 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            text-align: center;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="language-selector">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            selected_language = st.selectbox(
                "🌐 Language / Langue / Sprache / Idioma / Lingua / 言語",
                list(LANGUAGES.keys()),
                index=list(LANGUAGES.keys()).index(st.session_state.get('selected_language', '🇺🇸 English')),
                key="language_selector"
            )
            
            if selected_language != st.session_state.get('selected_language'):
                st.session_state.selected_language = selected_language
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the page
st.set_page_config(
    page_title="🧗‍♂️ IFSC 2025 World Championships",
    page_icon="🧗‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with better mobile responsiveness
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
        color: white;
        margin-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive athlete cards */
    .athlete-row {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        font-weight: 500;
        border: 2px solid transparent;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .athlete-row:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .athlete-row strong {
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .athlete-row small {
        font-size: 0.9rem;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    .athlete-row .targets {
        background-color: rgba(0, 0, 0, 0.15);
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin-top: 0.6rem;
        display: inline-block;
        font-weight: 600;
        border: 2px solid rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(5px);
        font-size: 0.85rem;
    }
    
    /* Status-based styling - FIXED */
    .athlete-row.podium-position {
        background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
    }
    
    .athlete-row.qualified {
        background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
    }
    
    .athlete-row.podium-contention {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7) !important;
        border: 2px solid #ffc107 !important;
        color: #856404 !important;
    }
    
    .athlete-row.eliminated,
    .athlete-row.no-podium {
        background: linear-gradient(135deg, #f8d7da, #f1b0b7) !important;
        border: 2px solid #dc3545 !important;
        color: #721c24 !important;
    }
    
    .athlete-row.awaiting-result {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef) !important;
        border: 2px solid #6c757d !important;
        color: #495057 !important;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, white, #f8f9fa);
        padding: 1.5rem 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        color: #333333;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card h4 {
        color: #666666;
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card h2 {
        color: #333333;
        margin: 0;
        font-size: 1.6rem;
        font-weight: bold;
        text-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 0.5rem;
    }
    
    .badge-live {
        background: linear-gradient(45deg, #ff4757, #ff6b6b);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .badge-completed {
        background: linear-gradient(45deg, #2ed573, #7bed9f);
        color: white;
    }
    
    .badge-upcoming {
        background: linear-gradient(45deg, #ffa502, #ff6348);
        color: white;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Threshold and error cards */
    .threshold-card {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #0d47a1;
    }
    
    .error-card {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #c62828;
    }
    
    /* Progress bar */
    .progress-bar {
        width: 100%;
        height: 6px;
        background-color: #e9ecef;
        border-radius: 3px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem 0.5rem;
        }
        
        .metric-card h2 {
            font-size: 1.4rem;
        }
        
        .athlete-row {
            padding: 0.8rem;
        }
        
        .athlete-row strong {
            font-size: 1rem;
        }
        
        .athlete-row .targets {
            font-size: 0.8rem;
            padding: 0.5rem 0.6rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Configuration with updated auto-refresh settings
class Config:
    CACHE_TTL = 2  # Reduced cache time to 2 seconds
    AUTO_REFRESH_INTERVAL = 2  # Refresh every 2 seconds
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 15
    MAX_ATHLETES_DISPLAY = 50
    
    # Google Sheets URLs
    SHEETS_URLS = {
        "Male Boulder Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=911620167",
        "Female Boulder Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=920221506",
        "Male Boulder Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=1415967322",
        "Female Boulder Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=299577805",
        "Male Lead Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=0",
        "Female Lead Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=352924417",
        "Male Lead Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=1091240908",
        "Female Lead Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=528108640"
    }

class DataProcessor:
    """Enhanced data processing utilities"""
    
    @staticmethod
    def safe_numeric_conversion(value, default=0) -> float:
        """Safely convert value to numeric with proper error handling"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return default
            return pd.to_numeric(value, errors='coerce')
        except Exception as e:
            logger.warning(f"Error converting {value} to numeric: {e}")
            return default

    @staticmethod
    def clean_text(text) -> str:
        """Enhanced text cleaning with better Unicode handling"""
        if not isinstance(text, str):
            return str(text) if text is not None else ""
        
        try:
            # Better Unicode handling
            cleaned = text.encode('utf-8', 'ignore').decode('utf-8')
            
            # Remove common problematic characters and encoding artifacts
            cleaned = cleaned.replace('â', '')  # Remove the specific problematic character
            cleaned = cleaned.replace('Â', '')  # Remove capital version too
            
            # Remove other common encoding artifacts
            cleaned = re.sub(r'[^\w\s\-\.\,\(\)]+', '', cleaned)
            
            # Remove extra whitespace
            cleaned = ' '.join(cleaned.split())
            
            return cleaned.strip()
        except Exception as e:
            logger.warning(f"Error cleaning text '{text}': {e}")
            return str(text) if text is not None else ""
        
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, expected_columns: List[str]) -> Tuple[bool, List[str]]:
        """Enhanced DataFrame validation"""
        if df.empty:
            return False, ["DataFrame is empty"]
        
        issues = []
        missing_cols = [col for col in expected_columns if col not in df.columns]
        
        if missing_cols:
            issues.append(f"Missing columns: {', '.join(missing_cols)}")
        
        # Check for minimum data requirements
        if len(df) < 1:
            issues.append("Insufficient data rows")
        
        return len(issues) == 0, issues

class CompetitionStatusDetector:
    """Enhanced competition status detection"""
    
    @staticmethod
    def get_competition_status(df: pd.DataFrame, competition_name: str) -> Tuple[str, str]:
        """Determine competition status with improved logic"""
        if df.empty:
            return "upcoming", "📄"
        
        try:
            if "Boulder" in competition_name:
                return CompetitionStatusDetector._get_boulder_status(df)
            elif "Lead" in competition_name:
                return CompetitionStatusDetector._get_lead_status(df)
        except Exception as e:
            logger.warning(f"Error determining status for {competition_name}: {e}")
        
        return "upcoming", "📄"
    
    @staticmethod
    def _get_boulder_status(df: pd.DataFrame) -> Tuple[str, str]:
        """Determine boulder competition status"""
        score_cols = [col for col in df.columns if 'Score' in str(col)]
        if not score_cols:
            return "upcoming", "📄"
        
        has_scores = df[score_cols].notna().any().any()
        if not has_scores:
            return "upcoming", "📄"
        
        total_athletes = len(df[df.iloc[:, 0].notna() & (df.iloc[:, 0] != '')])
        completed_athletes = len(df[df[score_cols].notna().any(axis=1)])
        
        completion_rate = completed_athletes / max(total_athletes, 1)
        
        if completion_rate >= 0.9:
            return "completed", "✅"
        elif completion_rate >= 0.1:
            return "live", "🔴"
        else:
            return "upcoming", "📄"
    
    @staticmethod
    def _get_lead_status(df: pd.DataFrame) -> Tuple[str, str]:
        """Determine lead competition status"""
        if 'Manual Score' not in df.columns:
            return "upcoming", "📄"
        
        has_scores = df['Manual Score'].notna().any()
        if not has_scores:
            return "upcoming", "📄"
        
        total_athletes = len(df[df['Name'].notna() & (df['Name'] != '')])
        completed_athletes = len(df[df['Manual Score'].notna()])
        
        completion_rate = completed_athletes / max(total_athletes, 1)
        
        if completion_rate >= 0.9:
            return "completed", "✅"
        elif completion_rate >= 0.1:
            return "live", "🔴"
        else:
            return "upcoming", "📄"

class DataLoader:
    """Enhanced data loading with better error handling and caching"""
    
    @staticmethod
    @st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
    def load_sheet_data(url: str, retries: int = 0) -> pd.DataFrame:
        """Load data from Google Sheets with enhanced error handling"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/csv,text/plain,*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            response = requests.get(
                url, 
                timeout=Config.REQUEST_TIMEOUT,
                headers=headers,
                stream=True
            )
            response.raise_for_status()
            
            # Read CSV data with better encoding handling
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data, encoding='utf-8', low_memory=False)
            
            # Enhanced data cleaning
            df = DataLoader._clean_dataframe(df)
            
            logger.info(f"Successfully loaded data: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            
            if retries < Config.MAX_RETRIES:
                logger.info(f"Retrying... attempt {retries + 1}")
                time.sleep(2 ** retries)
                return DataLoader.load_sheet_data(url, retries + 1)
            
            st.error(f"🚫 {error_msg}")
            return pd.DataFrame()
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            st.error(f"🚫 {error_msg}")
            return pd.DataFrame()
    
    @staticmethod
    def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced DataFrame cleaning"""
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove unnamed columns
        unnamed_cols = [col for col in df.columns if str(col).startswith('Unnamed')]
        df = df.drop(columns=unnamed_cols, errors='ignore')
        
        # Clean text data
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(DataProcessor.clean_text)
        
        return df

class MetricsCalculator:
    """Enhanced metrics calculation"""
    
    @staticmethod
    def calculate_boulder_metrics(df: pd.DataFrame) -> Dict[str, any]:
        """Calculate boulder competition metrics"""
        try:
            total_athletes = len(df[df['Athlete Name'].notna() & (df['Athlete Name'] != '')])
            
            boulder_cols = [col for col in df.columns if 'Boulder' in str(col) and 'Score' in str(col)]
            completed_problems = sum(df[col].notna().sum() for col in boulder_cols) if boulder_cols else 0
            
            # Find total score column
            score_col = next((col for col in df.columns if 'Total Score' in str(col)), None)
            
            avg_score = 0
            if score_col:
                numeric_scores = pd.to_numeric(df[score_col], errors='coerce')
                avg_score = numeric_scores.mean() if not numeric_scores.isna().all() else 0
            
            # Find leader
            leader = "TBD"
            if 'Current Position/Rank' in df.columns:
                try:
                    leader_mask = pd.to_numeric(df['Current Position/Rank'], errors='coerce') == 1
                    if leader_mask.any():
                        leader = DataProcessor.clean_text(df.loc[leader_mask, 'Athlete Name'].iloc[0])
                except:
                    pass
            
            return {
                'total_athletes': total_athletes,
                'completed_problems': completed_problems,
                'avg_score': avg_score,
                'leader': leader
            }
        except Exception as e:
            logger.error(f"Error calculating boulder metrics: {e}")
            return {'total_athletes': 0, 'completed_problems': 0, 'avg_score': 0, 'leader': 'TBD'}
    
    @staticmethod
    def calculate_lead_metrics(df: pd.DataFrame) -> Dict[str, any]:
        """Calculate lead competition metrics"""
        try:
            # Filter active athletes
            active_df = df[
                df['Name'].notna() & 
                (df['Name'] != '') & 
                (~df['Name'].astype(str).str.contains('Hold for', na=False)) &
                (~df['Name'].astype(str).str.contains('Min to', na=False))
            ]
            
            total_athletes = len(active_df)
            completed = len(active_df[active_df['Manual Score'].notna() & (active_df['Manual Score'] != '')])
            
            # Calculate average score
            avg_score = 0
            if 'Manual Score' in active_df.columns:
                scores = pd.to_numeric(active_df['Manual Score'], errors='coerce')
                avg_score = scores.mean() if not scores.isna().all() else 0
            
            # Find leader
            leader = "TBD"
            if 'Current Rank' in active_df.columns:
                try:
                    leader_idx = pd.to_numeric(active_df['Current Rank'], errors='coerce') == 1
                    if leader_idx.any():
                        leader = DataProcessor.clean_text(active_df.loc[leader_idx, 'Name'].iloc[0])
                except:
                    pass
            
            return {
                'total_athletes': total_athletes,
                'completed': completed,
                'avg_score': avg_score,
                'leader': leader
            }
        except Exception as e:
            logger.error(f"Error calculating lead metrics: {e}")
            return {'total_athletes': 0, 'completed': 0, 'avg_score': 0, 'leader': 'TBD'}

def display_enhanced_metrics(df: pd.DataFrame, competition_name: str):
    """Display enhanced metrics with progress indicators"""
    col1, col2, col3, col4 = st.columns(4)
    
    if "Boulder" in competition_name:
        metrics = MetricsCalculator.calculate_boulder_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>👥 Athletes</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🧗‍♂️ Problems Completed</h4>
                <h2>{metrics["completed_problems"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>📊 Avg Score</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🥇 Leader</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)
    
    elif "Lead" in competition_name:
        metrics = MetricsCalculator.calculate_lead_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>👥 Athletes</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            completion_rate = (metrics["completed"] / max(metrics["total_athletes"], 1)) * 100
            st.markdown(f'''
            <div class="metric-card">
                <h4>✅ Completed</h4>
                <h2>{metrics["completed"]}</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion_rate}%"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>📊 Avg Score</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>🥇 Leader</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)

def determine_athlete_status(rank: any, total_score: any, boulder_info: Dict, competition_name: str, row: pd.Series = None) -> Tuple[str, str]:
    """Determine athlete status and appropriate styling - FIXED"""
    try:
        rank_num = DataProcessor.safe_numeric_conversion(rank)
        completed_boulders = boulder_info['completed_boulders']
        worst_finish_display = boulder_info['worst_finish_display']
        
        # If no valid rank, return gray
        if rank_num <= 0:
            return "awaiting-result", "⏳"
        
        # BOULDER FINALS - Check if all podium positions are impossible
        if "Boulder" in competition_name and "Final" in competition_name:
            # Check if all podium positions are impossible (regardless of completion status)
            if row is not None and check_all_podium_impossible(row):
                return "no-podium", "❌"  # RED - All podium positions impossible
            
            if completed_boulders < 4:
                # Still competing - yellow for everyone (unless impossible above)
                return "podium-contention", "⚠️"
            else:
                # All 4 boulders completed - check rank AND worst finish for podium
                if rank_num <= 3:
                    # Extract worst finish number from the display string
                    worst_finish_num = extract_worst_finish_number(boulder_info)
                    if worst_finish_num is not None and worst_finish_num <= 3:
                        return "podium-position", "🏆"  # GREEN - Top 3 with worst finish 1, 2, or 3
                    else:
                        return "podium-contention", "⚠️"  # YELLOW - Top 3 but worst finish > 3
                else:
                    return "no-podium", "❌"  # RED - Not in top 3
        
        # BOULDER SEMIS - Check worst finish
        elif "Boulder" in competition_name and "Semis" in competition_name:
            if completed_boulders < 4:
                # Still competing - yellow for everyone
                return "podium-contention", "⚠️"
            else:
                # All 4 boulders completed - check rank AND worst finish
                if rank_num <= 8:
                    # Extract worst finish number from the display string
                    worst_finish_num = extract_worst_finish_number(boulder_info)
                    if worst_finish_num is not None and worst_finish_num < 8:
                        return "qualified", "✅"  # GREEN - Top 8 with good worst finish
                    else:
                        return "podium-contention", "⚠️"  # YELLOW - Top 8 but bad worst finish
                else:
                    return "eliminated", "❌"  # RED - Not in top 8
        
        # Default for all other cases
        else:
            if rank_num <= 3:
                return "podium-position", "🏆"  # GREEN
            elif rank_num <= 8:
                return "qualified", "✅"  # GREEN
            else:
                return "eliminated", "❌"  # RED
            
    except Exception as e:
        logger.warning(f"Error: {e}")
        return "awaiting-result", "⏳"


def extract_worst_finish_number(boulder_info: Dict) -> Optional[int]:
    """Extract the worst finish number from boulder info"""
    try:
        worst_finish_display = boulder_info.get('worst_finish_display', '')
        if worst_finish_display:
            # Look for patterns like "Worst Finish: 9.0" or "Worst Finish: 7"
            import re
            match = re.search(r'Worst Finish:\s*(\d+(?:\.\d+)?)', worst_finish_display)
            if match:
                return int(float(match.group(1)))
    except Exception as e:
        logger.warning(f"Error extracting worst finish number: {e}")
    return None

def check_all_podium_impossible(row: pd.Series) -> bool:
    """Check if all podium positions (1st, 2nd, 3rd) are impossible - ONLY for finals"""
    try:
        strategy_cols = ['1st Place Strategy', '2nd Place Strategy', '3rd Place Strategy']
        impossible_count = 0
        
        for col in strategy_cols:
            if col in row.index:
                strategy_value = row.get(col, '')
                if strategy_value and str(strategy_value) not in ['', 'nan', 'N/A']:
                    strategy_clean = str(strategy_value).upper()
                    if "IMPOSSIBLE" in strategy_clean:
                        impossible_count += 1
        
        # Return True if all three positions are impossible
        return impossible_count == 3
        
    except Exception as e:
        logger.warning(f"Error checking impossible podium positions: {e}")
        return False
    
def determine_lead_athlete_status(status: str, has_score: bool) -> Tuple[str, str]:
    """Determine lead athlete status - FIXED"""
    if not has_score:
        return "awaiting-result", "🔄"
    
    status_lower = str(status).lower()
    
    if "qualified" in status_lower and "contention" not in status_lower:
        return "qualified", "✅"
    elif "eliminated" in status_lower:
        return "eliminated", "❌"
    elif "podium" in status_lower and "no podium" not in status_lower and "contention" not in status_lower:
        return "podium-position", "🏆"
    elif "contention" in status_lower or "podium contention" in status_lower:
        return "podium-contention", "⚠️"  # YELLOW for podium contention
    elif "no podium" in status_lower:
        return "no-podium", "❌"
    else:
        return "podium-contention", "📊"

def main():
    """Enhanced main application function with forced auto-refresh"""
    
    # Initialize session state
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    if 'auto_refresh_enabled' not in st.session_state:
        st.session_state.auto_refresh_enabled = True  # Always enabled
    if 'selected_competitions' not in st.session_state:
        st.session_state.selected_competitions = []
    if 'selected_language' not in st.session_state:
       st.session_state.selected_language = '🇺🇸 English'

    language_selector()
    
    # Enhanced header - ALREADY TRANSLATED ✅
    st.markdown(f"""
   <div class="main-header">
       <h1>{get_text("app_title")}</h1>
       <h3>{get_text("app_subtitle")}</h3>
       <p style="margin: 0; opacity: 0.9;">{get_text("app_description")}</p>
   </div>
   """, unsafe_allow_html=True)
    
    # Enhanced sidebar - FIX: Use get_text() here
    st.sidebar.title(get_text("dashboard_controls"))
    
    # Auto-refresh section - FIX: Use get_text() here
    with st.sidebar.expander(get_text("refresh_settings"), expanded=True):
        st.markdown(f"**{get_text('auto_refresh_status')}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(get_text("manual_refresh"), type="primary", use_container_width=True):
                st.cache_data.clear()
                st.session_state.last_refresh = datetime.now()
                st.success(get_text("refreshed"))
                time.sleep(0.5)
                st.rerun()
        
        with col2:
            if st.button(get_text("clear_cache"), use_container_width=True):
                st.cache_data.clear()
                st.success(get_text("cache_cleared"))
        
        # Show refresh status - FIX: Use get_text() here
        time_since = (datetime.now() - st.session_state.last_refresh).seconds
        st.caption(get_text("last_refresh").format(time_since))
        st.caption(get_text("next_refresh").format(2 - (time_since % 2)))
    
    # Competition filters - FIX: Use get_text() here
    with st.sidebar.expander(get_text("competition_filters"), expanded=True):
        competition_type = st.selectbox(
            get_text("discipline"),
            [get_text("all"), get_text("boulder"), get_text("lead")],
            help="Filter by climbing discipline"
        )
        
        gender_filter = st.selectbox(
            get_text("gender"),
            [get_text("all"), get_text("male"), get_text("female")],
            help="Filter by gender category"
        )
        
        round_filter = st.selectbox(
            get_text("round"),
            [get_text("all"), get_text("semis"), get_text("final")],
            help="Filter by competition round"
        )
    
    # Filter competitions - Need to map translated selections back to English
    # Convert translated selections back to English for filtering
    competition_type_en = map_to_english(competition_type, ["All", "Boulder", "Lead"])
    gender_filter_en = map_to_english(gender_filter, ["All", "Male", "Female"])
    round_filter_en = map_to_english(round_filter, ["All", "Semis", "Final"])
    
    filtered_competitions = get_filtered_competitions(competition_type_en, gender_filter_en, round_filter_en)
    
    if not filtered_competitions:
        st.markdown(f"""
        <div class="error-card">
            <h3>{get_text("no_competitions_found")}</h3>
            <p>{get_text("adjust_filters")}</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Competition overview - FIX: Use get_text() here
    st.markdown(f"### {get_text('competition_overview')}")
    
    # Calculate overview metrics with progress
    overview_metrics = calculate_overview_metrics(filtered_competitions)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h4>{get_text("total")}</h4>
            <h2>{overview_metrics["total"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <h4>{get_text("live")}</h4>
            <h2>{overview_metrics["live"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <h4>{get_text("completed")}</h4>
            <h2>{overview_metrics["completed"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <h4>{get_text("upcoming")}</h4>
            <h2>{overview_metrics["upcoming"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    # Display results - FIX: Use get_text() here
    st.markdown(f"### {get_text('live_results')}")
    
    if len(filtered_competitions) > 1:
        # Create tabs for multiple competitions
        tab_names = list(filtered_competitions.keys())
        tabs = st.tabs(tab_names)
        
        for i, (comp_name, url) in enumerate(filtered_competitions.items()):
            with tabs[i]:
                display_competition_results(comp_name, url)
    else:
        # Single competition view
        comp_name, url = list(filtered_competitions.items())[0]
        display_competition_results(comp_name, url)
    
    # Enhanced footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**⛰️ IFSC World Championships 2025**")
    with col2:
        st.markdown("**📊 Real-time Results**")
    with col3:
        st.markdown("**🔄 Auto-refresh: ALWAYS ON (2s)**")
    
    # FORCED Auto-refresh logic - ALWAYS ACTIVE
    time_since_last = (datetime.now() - st.session_state.last_refresh).total_seconds()
    if time_since_last >= Config.AUTO_REFRESH_INTERVAL:
        st.session_state.last_refresh = datetime.now()
        st.cache_data.clear()  # Clear cache on each refresh
        st.rerun()


def map_to_english(translated_value: str, english_options: List[str]) -> str:
    """Map translated filter values back to English for backend processing"""
    current_lang = st.session_state.get('selected_language', '🇺🇸 English')
    
    # If already in English, return as-is
    if current_lang == '🇺🇸 English':
        return translated_value
    
    # Create reverse mapping
    mapping = {
        get_text("all"): "All",
        get_text("boulder"): "Boulder", 
        get_text("lead"): "Lead",
        get_text("male"): "Male",
        get_text("female"): "Female", 
        get_text("semis"): "Semis",
        get_text("final"): "Final"
    }
    
    return mapping.get(translated_value, translated_value)


def display_enhanced_metrics(df: pd.DataFrame, competition_name: str):
    """Display enhanced metrics with progress indicators - TRANSLATED"""
    col1, col2, col3, col4 = st.columns(4)
    
    if "Boulder" in competition_name:
        metrics = MetricsCalculator.calculate_boulder_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>{get_text("athletes")}</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h4>{get_text("problems_completed")}</h4>
                <h2>{metrics["completed_problems"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>{get_text("avg_score")}</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>{get_text("leader")}</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)
    
    elif "Lead" in competition_name:
        metrics = MetricsCalculator.calculate_lead_metrics(df)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h4>{get_text("athletes")}</h4>
                <h2>{metrics["total_athletes"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            completion_rate = (metrics["completed"] / max(metrics["total_athletes"], 1)) * 100
            st.markdown(f'''
            <div class="metric-card">
                <h4>✅ {get_text("completed")}</h4>
                <h2>{metrics["completed"]}</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion_rate}%"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h4>{get_text("avg_score")}</h4>
                <h2>{metrics["avg_score"]:.1f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h4>{get_text("leader")}</h4>
                <h2>{metrics["leader"][:15]}{"..." if len(metrics["leader"]) > 15 else ""}</h2>
            </div>
            ''', unsafe_allow_html=True)


def display_competition_results(comp_name: str, url: str):
    """Display results for a single competition - TRANSLATED"""
    with st.spinner(get_text("loading").format(comp_name)):
        df = DataLoader.load_sheet_data(url)
    
    current_time = datetime.now().strftime("%H:%M:%S")
    st.caption(get_text("last_updated").format(current_time))
    
    if "Boulder" in comp_name:
        display_boulder_results(df, comp_name)
    elif "Lead" in comp_name:
        display_lead_results(df, comp_name)
    else:
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown(f'<div class="error-card">{get_text("no_data")}</div>', unsafe_allow_html=True)


def display_boulder_results(df: pd.DataFrame, competition_name: str):
    """Enhanced boulder competition results display - TRANSLATED"""
    status, status_emoji = CompetitionStatusDetector.get_competition_status(df, competition_name)
    status_class = f"badge-{status}"
    
    st.markdown(f"""
    ### 🪨 {competition_name} 
    <span class="status-badge {status_class}">{status_emoji} {status.upper()}</span>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.markdown(f'<div class="error-card">{get_text("no_data")}</div>', unsafe_allow_html=True)
        return
    
    # Validate required columns
    required_cols = ['Athlete Name', 'Current Position/Rank']
    is_valid, issues = DataProcessor.validate_dataframe(df, required_cols)
    
    if not is_valid:
        st.markdown(f'<div class="error-card">⚠️ Data validation failed: {"; ".join(issues)}</div>', unsafe_allow_html=True)
        with st.expander("🔍 Raw Data"):
            st.dataframe(df, use_container_width=True, hide_index=True)
        return
    
    # Display enhanced metrics
    display_enhanced_metrics(df, competition_name)
    
    st.markdown(f"#### {get_text('current_standings')}")
    
    # Find the total score column
    score_col = next((col for col in df.columns if 'Total Score' in str(col)), None)
    
    # Sort and prepare data
    df_sorted = df.copy()
    
    # Convert rank to numeric
    if 'Current Position/Rank' in df.columns:
        df_sorted['Current Position/Rank'] = pd.to_numeric(df_sorted['Current Position/Rank'], errors='coerce')
    
    # Convert score to numeric if available
    if score_col is not None:
        df_sorted[score_col] = pd.to_numeric(df_sorted[score_col], errors='coerce')
    
    # Sort by position
    try:
        if 'Current Position/Rank' in df_sorted.columns:
            df_sorted = df_sorted.sort_values('Current Position/Rank', ascending=True).reset_index(drop=True)
        elif score_col is not None:
            df_sorted = df_sorted.sort_values(score_col, ascending=False).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort data: {e}")
        df_sorted = df.copy()
    
    # Display results with enhanced athlete cards
    display_boulder_athlete_cards(df_sorted, score_col, competition_name)


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available - TRANSLATED"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>{get_text("qualification_thresholds")}</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_results(df: pd.DataFrame, competition_name: str):
    """Enhanced lead competition results display - TRANSLATED"""
    status, status_emoji = CompetitionStatusDetector.get_competition_status(df, competition_name)
    status_class = f"badge-{status}"
    
    st.markdown(f"""
    ### 🧗‍♀️ {competition_name}
    <span class="status-badge {status_class}">{status_emoji} {get_text(f"{status}_upper")}</span>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.markdown(f'<div class="error-card">{get_text("no_data")}</div>', unsafe_allow_html=True)
        return
    
    if 'Name' not in df.columns:
        st.markdown('<div class="error-card">⚠️ Name column not found in data</div>', unsafe_allow_html=True)
        return
    
    # Extract qualification info and filter active athletes
    qualification_info = extract_qualification_info(df)
    active_df = filter_active_athletes(df, competition_name)
    
    # Display enhanced metrics
    display_enhanced_metrics(active_df, competition_name)
    
    st.markdown(f"#### {get_text('current_standings')}")
    
    # Show qualification thresholds
    display_qualification_thresholds(qualification_info)
    
    # Sort and display athletes
    display_lead_athletes(active_df, qualification_info)


def get_filtered_competitions(competition_type: str, gender_filter: str, round_filter: str) -> Dict[str, str]:
    """Get filtered competitions based on user selection"""
    filtered_competitions = {}
    
    for name, url in Config.SHEETS_URLS.items():
        include = True
        
        if competition_type != "All" and competition_type.lower() not in name.lower():
            include = False
        
        if gender_filter != "All" and gender_filter.lower() not in name.lower():
            include = False
                
        if round_filter != "All" and round_filter.lower() not in name.lower():
            include = False
        
        if include:
            filtered_competitions[name] = url
    
    return filtered_competitions


def calculate_overview_metrics(filtered_competitions: Dict[str, str]) -> Dict[str, int]:
    """Calculate overview metrics for all competitions"""
    metrics = {"total": 0, "live": 0, "completed": 0, "upcoming": 0}
    
    for comp_name, url in filtered_competitions.items():
        try:
            df = DataLoader.load_sheet_data(url)
            status, _ = CompetitionStatusDetector.get_competition_status(df, comp_name)
            metrics["total"] += 1
            metrics[status] += 1
        except Exception as e:
            logger.warning(f"Error calculating metrics for {comp_name}: {e}")
            metrics["total"] += 1
            metrics["upcoming"] += 1
    
    return metrics


def display_competition_results(comp_name: str, url: str):
    """Display results for a single competition"""
    with st.spinner(f"Loading {comp_name}..."):
        df = DataLoader.load_sheet_data(url)
    
    current_time = datetime.now().strftime("%H:%M:%S")
    st.caption(f"📡 Last updated: {current_time}")
    
    if "Boulder" in comp_name:
        display_boulder_results(df, comp_name)
    elif "Lead" in comp_name:
        display_lead_results(df, comp_name)
    else:
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="error-card">⚠️ No data available</div>', unsafe_allow_html=True)


def display_boulder_results(df: pd.DataFrame, competition_name: str):
    """Enhanced boulder competition results display"""
    status, status_emoji = CompetitionStatusDetector.get_competition_status(df, competition_name)
    status_class = f"badge-{status}"
    
    st.markdown(f"""
    ### 🪨 {competition_name} 
    <span class="status-badge {status_class}">{status_emoji} {get_text(f"{status}_upper")}</span>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.markdown('<div class="error-card">⚠️ No data available for this competition</div>', unsafe_allow_html=True)
        return
    
    # Validate required columns
    required_cols = ['Athlete Name', 'Current Position/Rank']
    is_valid, issues = DataProcessor.validate_dataframe(df, required_cols)
    
    if not is_valid:
        st.markdown(f'<div class="error-card">⚠️ Data validation failed: {"; ".join(issues)}</div>', unsafe_allow_html=True)
        with st.expander("🔍 Raw Data"):
            st.dataframe(df, use_container_width=True, hide_index=True)
        return
    
    # Display enhanced metrics
    display_enhanced_metrics(df, competition_name)
    
    st.markdown("#### 📋 Current Standings")
    
    # Find the total score column
    score_col = next((col for col in df.columns if 'Total Score' in str(col)), None)
    
    # Sort and prepare data
    df_sorted = df.copy()
    
    # Convert rank to numeric
    if 'Current Position/Rank' in df.columns:
        df_sorted['Current Position/Rank'] = pd.to_numeric(df_sorted['Current Position/Rank'], errors='coerce')
    
    # Convert score to numeric if available
    if score_col is not None:
        df_sorted[score_col] = pd.to_numeric(df_sorted[score_col], errors='coerce')
    
    # Sort by position
    try:
        if 'Current Position/Rank' in df_sorted.columns:
            df_sorted = df_sorted.sort_values('Current Position/Rank', ascending=True).reset_index(drop=True)
        elif score_col is not None:
            df_sorted = df_sorted.sort_values(score_col, ascending=False).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort data: {e}")
        df_sorted = df.copy()
    
    # Display results with enhanced athlete cards
    display_boulder_athlete_cards(df_sorted, score_col, competition_name)


def display_boulder_athlete_cards(df_sorted: pd.DataFrame, score_col: Optional[str], competition_name: str):
    """Display enhanced athlete cards for boulder competitions"""
    
    for idx, row in df_sorted.iterrows():
        if pd.isna(row.get('Athlete Name')) or row.get('Athlete Name') == '':
            continue
            
        rank = row.get('Current Position/Rank', 'N/A')
        athlete = DataProcessor.clean_text(str(row.get('Athlete Name', 'Unknown')))
        total_score = row.get(score_col, 'N/A') if score_col else 'N/A'
        
        # Calculate boulder completion
        boulder_info = calculate_boulder_completion(row)
        
        # Determine athlete status and styling - PASS THE ROW DATA
        card_class, position_emoji = determine_athlete_status(
            rank, total_score, boulder_info, competition_name, row
        )
        
        # Create strategy display if applicable
        strategy_display = create_strategy_display(row, boulder_info, competition_name)
        
        # Create the athlete card
        create_athlete_card(
            position_emoji, athlete, total_score, boulder_info, 
            strategy_display, card_class
        )


def calculate_boulder_completion(row: pd.Series) -> Dict[str, any]:
    """Calculate boulder completion information for an athlete"""
    boulder_scores = []
    completed_boulders = 0
    
    for i in range(1, 5):
        col_name = f'Boulder {i} Score (0-25)'
        if col_name in row.index:
            score = row.get(col_name, '-')
            if pd.notna(score) and str(score) != '-' and str(score) != '':
                boulder_scores.append(f"B{i}: {score}")
                completed_boulders += 1
            else:
                boulder_scores.append(f"B{i}: -")
    
    boulder_display = " | ".join(boulder_scores) if boulder_scores else "No boulder data"
    
    # Check for worst finish information
    worst_finish_display = ""
    if completed_boulders == 4:
        detail_text = f"{get_text('total')}: {total_score} | {boulder_display}{worst_finish_display}"
    elif completed_boulders == 3:
        detail_text = f"{get_text('total')}: {total_score} | {boulder_display} | 1 {get_text('boulder_remaining')}"
    else:
        detail_text = f"{get_text('total')}: {total_score} | {boulder_display} | {get_text('progress')}: {completed_boulders}/4"
        
        if worst_finish_col:
            worst_finish = row.get(worst_finish_col, 'N/A')
            if worst_finish not in ['N/A', '', None] and not pd.isna(worst_finish):
                worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
                if worst_finish_clean and worst_finish_clean != '-':
                    worst_finish_display = f" | Worst Finish: {worst_finish_clean}"
    
    return {
        'boulder_scores': boulder_scores,
        'completed_boulders': completed_boulders,
        'boulder_display': boulder_display,
        'worst_finish_display': worst_finish_display
    }


def create_strategy_display(row: pd.Series, boulder_info: Dict, competition_name: str) -> str:
    """Create strategy display for boulder competitions"""
    strategy_display = ""
    completed_boulders = boulder_info['completed_boulders']
    
    if ("Semis" in competition_name or "Final" in competition_name) and completed_boulders == 3:
        strategy_cols = {}
        for col in row.index:
            col_str = str(col)
            if '1st Place Strategy' in col_str:
                strategy_cols['1st'] = col
            elif '2nd Place Strategy' in col_str:
                strategy_cols['2nd'] = col
            elif '3rd Place Strategy' in col_str:
                strategy_cols['3rd'] = col
            elif 'Points Needed for Top 8' in col_str:
                strategy_cols['top8'] = col
        
        if strategy_cols:
            strategies = []
            has_impossible_top8 = False
            
            for place, col in strategy_cols.items():
                strategy_value = row.get(col, '')
                if strategy_value and str(strategy_value) not in ['', 'nan', 'N/A']:
                    strategy_clean = DataProcessor.clean_text(str(strategy_value))
                    if strategy_clean:
                        if place == '1st':
                            strategies.append(f"🥇 1st: {strategy_clean}")
                        elif place == '2nd':
                            strategies.append(f"🥈 2nd: {strategy_clean}")
                        elif place == '3rd':
                            strategies.append(f"🥉 3rd: {strategy_clean}")
                        elif place == 'top8' and "Semis" in competition_name:
                            strategies.append(f"🎯 Top 8: {strategy_clean}")
                            if "IMPOSSIBLE" in strategy_clean.upper():
                                has_impossible_top8 = True
            
            if strategies:
                comp_type = "Final" if "Final" in competition_name else "Semi"
                strategy_display = f"<br><div class='targets'><strong>{comp_type} Strategy:</strong> {' | '.join(strategies)}</div>"
                
                if has_impossible_top8 and "Semis" in competition_name:
                    return strategy_display, "eliminated"
    
    return strategy_display


def create_athlete_card(position_emoji: str, athlete: str, total_score: any, 
                       boulder_info: Dict, strategy_display: str, card_class: str):
    """Create and display an athlete card"""
    completed_boulders = boulder_info['completed_boulders']
    boulder_display = boulder_info['boulder_display']
    worst_finish_display = boulder_info['worst_finish_display']
    
    # Ensure card_class is never empty
    if not card_class or card_class.strip() == "":
        card_class = "awaiting-result"
    
    # Check if strategy display indicates impossible Top 8
    if isinstance(strategy_display, tuple):
        strategy_display, override_class = strategy_display
        if override_class == "eliminated":
            card_class = "eliminated"
            position_emoji = "❌"
    
    # Create detail text based on completion status
    if completed_boulders == 4:
        detail_text = f"Total: {total_score} | {boulder_display}{worst_finish_display}"
    elif completed_boulders == 3:
        detail_text = f"Total: {total_score} | {boulder_display} | 1 boulder remaining"
    else:
        detail_text = f"Total: {total_score} | {boulder_display} | Progress: {completed_boulders}/4"
    
    st.markdown(f"""
    <div class="athlete-row {card_class}">
        <strong>{position_emoji} - {athlete}</strong><br>
        <small>{detail_text}</small>{strategy_display}
    </div>
    """, unsafe_allow_html=True)


def display_lead_results(df: pd.DataFrame, competition_name: str):
    """Enhanced lead competition results display"""
    status, status_emoji = CompetitionStatusDetector.get_competition_status(df, competition_name)
    status_class = f"badge-{status}"
    
    st.markdown(f"""
    ### 🧗‍♀️ {competition_name}
    <span class="status-badge {status_class}">{status_emoji} {status.upper()}</span>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.markdown('<div class="error-card">⚠️ No data available for this competition</div>', unsafe_allow_html=True)
        return
    
    if 'Name' not in df.columns:
        st.markdown('<div class="error-card">⚠️ Name column not found in data</div>', unsafe_allow_html=True)
        return
    
    # Extract qualification info and filter active athletes
    qualification_info = extract_qualification_info(df)
    active_df = filter_active_athletes(df, competition_name)
    
    # Display enhanced metrics
    display_enhanced_metrics(active_df, competition_name)
    
    st.markdown("#### 📋 Current Standings")
    
    # Show qualification thresholds
    display_qualification_thresholds(qualification_info)
    
    # Sort and display athletes
    display_lead_athletes(active_df, qualification_info)


def extract_qualification_info(df: pd.DataFrame) -> Dict[str, str]:
    """Extract qualification threshold information from dataframe"""
    qualification_info = {}
    try:
        threshold_cols = ['Hold for 1st', 'Hold for 2nd', 'Hold for 3rd', 'Hold to Qualify', 'Min to Qualify']
        for _, row in df.iterrows():
            if pd.isna(row.get('Name')) or row.get('Name') == '':
                continue
            for col in threshold_cols:
                if col in df.columns and pd.notna(row.get(col)):
                    qualification_info[col] = DataProcessor.clean_text(str(row.get(col)))
    except Exception as e:
        logger.warning(f"Error extracting qualification thresholds: {e}")
    return qualification_info


def filter_active_athletes(df: pd.DataFrame, competition_name: str) -> pd.DataFrame:
    """Filter out reference rows to get only active athletes"""
    try:
        active_df = df[
            df['Name'].notna() & 
            (df['Name'] != '') & 
            (~df['Name'].astype(str).str.isdigit()) &
            (~df['Name'].astype(str).str.contains('Hold for', na=False)) &
            (~df['Name'].astype(str).str.contains('Min to', na=False)) &
            (~df['Name'].astype(str).str.contains('TBD|TBA|Qualification|Threshold|Zone|Top', na=False, case=False)) &
            (~df['Name'].astype(str).str.startswith(('Hold', 'Min', '#'), na=False)) &
            (~df['Name'].apply(is_placeholder_athlete))
        ]
        
        # Set expected athlete counts based on competition type
        if "Lead Semis" in competition_name:
            expected_max = 24
        elif "Boulder Semis" in competition_name:
            expected_max = 20
        elif "Final" in competition_name:
            expected_max = 8
        else:
            expected_max = 999
        
        if "Lead Semis" in competition_name:
            if len(active_df) >= 24:
                active_df = active_df.head(24)
                logger.info(f"{competition_name}: Using first 24 athletes")
            else:
                logger.warning(f"{competition_name}: Only found {len(active_df)} athletes, expected 24")
        
        elif expected_max < 999 and len(active_df) > expected_max and 'Current Rank' in active_df.columns:
            active_df['temp_rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            
            rank_filtered = active_df[
                (active_df['temp_rank'].notna()) & 
                (active_df['temp_rank'] >= 1) & 
                (active_df['temp_rank'] <= expected_max)
            ]
            
            if len(rank_filtered) == expected_max:
                active_df = rank_filtered.drop('temp_rank', axis=1)
            else:
                active_df = active_df.drop('temp_rank', axis=1).head(expected_max)
        
        elif expected_max < 999 and len(active_df) > expected_max:
            active_df = active_df.head(expected_max)
        
        return active_df
        
    except Exception as e:
        logger.error(f"Error filtering athletes: {e}")
        fallback_df = df[
            df['Name'].notna() & 
            (df['Name'] != '') &
            (~df['Name'].astype(str).str.contains('Hold for', na=False))
        ]
        
        if "Lead Semis" in competition_name:
            fallback_df = fallback_df.head(24)
        elif "Final" in competition_name:
            fallback_df = fallback_df.head(8)
            
        return fallback_df


def is_placeholder_athlete(name: str) -> bool:
    """Check if name is a placeholder like 'Athlete 1', 'Athlete 23', etc."""
    name_str = str(name).strip()
    if name_str.startswith('Athlete '):
        remaining = name_str[8:].strip()
        return remaining.isdigit()
    return False


def display_qualification_thresholds(qualification_info: Dict[str, str]):
    """Display qualification thresholds if available"""
    if qualification_info:
        threshold_items = []
        threshold_mapping = {
            'Hold for 1st': ('🥇 1st', '#FFD700'),
            'Hold for 2nd': ('🥈 2nd', '#C0C0C0'),
            'Hold for 3rd': ('🥉 3rd', '#CD7F32'),
            'Hold to Qualify': ('✅ Qualify', '#28a745'),
            'Min to Qualify': ('⚠️ Min', '#ffc107')
        }
        
        for key, value in qualification_info.items():
            if key in threshold_mapping:
                label, color = threshold_mapping[key]
                threshold_items.append(f'<span style="color: {color}; font-weight: bold;">{label}: {value}</span>')
        
        if threshold_items:
            st.markdown(f"""
            <div class="threshold-card">
                <h5>🎯 Qualification Thresholds</h5>
                {' | '.join(threshold_items)}
            </div>
            """, unsafe_allow_html=True)


def display_lead_athletes(active_df: pd.DataFrame, qualification_info: Dict[str, str]):
    """Display lead competition athletes with enhanced formatting"""
    try:
        if 'Current Rank' in active_df.columns:
            active_df['Current Rank'] = pd.to_numeric(active_df['Current Rank'], errors='coerce')
            active_df = active_df.sort_values('Current Rank', ascending=True).reset_index(drop=True)
    except Exception as e:
        logger.warning(f"Could not sort by rank: {e}")
    
    for _, row in active_df.iterrows():
        name = DataProcessor.clean_text(str(row.get('Name', 'Unknown')))
        score = row.get('Manual Score', 'N/A')
        rank = row.get('Current Rank', 'N/A')
        status = DataProcessor.clean_text(str(row.get('Status', 'Unknown')))
        worst_finish = row.get('Worst Finish', 'N/A')
        
        has_score = score not in ['N/A', '', None] and not pd.isna(score)
        
        threshold_display = create_threshold_display(has_score, qualification_info)
        
        card_class, status_emoji = determine_lead_athlete_status(status, has_score)
        
        position_emoji = get_lead_position_emoji(rank, has_score, card_class, status_emoji)
        
        score_display = score if has_score else get_text('awaiting_result')
        worst_finish_display = format_worst_finish(worst_finish, has_score)
        
        st.markdown(f"""
        <div class="athlete-row {card_class}">
            <strong>{position_emoji} #{rank} - {name}</strong><br>
            <small>{get_text('score')}: {score_display} | {get_text('status')}: {status}{worst_finish_display}</small>{threshold_display}
        </div>
        """, unsafe_allow_html=True)


def create_threshold_display(has_score: bool, qualification_info: Dict[str, str]) -> str:
    """Create threshold display for athletes without scores"""
    if has_score or not qualification_info:
        return ""
    
    thresholds = []
    for key, value in qualification_info.items():
        if key == 'Hold for 1st':
            thresholds.append(f'🥇 For 1st Hold: {get_text("for_1st_hold")}: {value}')
        elif key == 'Hold for 2nd':
            thresholds.append(f'🥈 For 2nd Hold: {get_text("for_2nd_hold")}: {value}')
        elif key == 'Hold for 3rd':
            thresholds.append(f'🥉 For 3rd Hold: {get_text("for_3rd_hold")}: {value}')
        elif key == 'Hold to Qualify':
            thresholds.append(f'🎯 For 8th Hold: {get_text("for_8th_hold")}: {value}')
        elif key == 'Min to Qualify':
            thresholds.append(f'📊 For 8th Points: {get_text("for_8th_points")}: {value}')
    
    if thresholds:
        return f"<br><div class='targets'><strong>Targets:</strong><br>{' | '.join(thresholds)}</div>"
    return ""


def get_lead_position_emoji(rank: any, has_score: bool, card_class: str, status_emoji: str) -> str:
    """Get position emoji for lead athletes"""
    rank_num = DataProcessor.safe_numeric_conversion(rank)
    if rank_num > 0:
        return status_emoji if has_score and card_class else f"#{rank_num}"
    return "📄"


def format_worst_finish(worst_finish: any, has_score: bool) -> str:
    """Format worst finish display"""
    if not has_score or worst_finish in ['N/A', '', None] or pd.isna(worst_finish):
        return ""
    
    worst_finish_clean = DataProcessor.clean_text(str(worst_finish))
    return f" | Worst Finish: {worst_finish_clean}" if worst_finish_clean and worst_finish_clean != '-' else ""


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"🚫 Application Error: {e}")
        st.markdown("Please refresh the page or contact support if the issue persists.")
        
        with st.expander("🔧 Debug Information"):
            st.code(f"Error: {e}")
            st.code(f"Time: {datetime.now()}")
            import traceback
            st.code(traceback.format_exc())
