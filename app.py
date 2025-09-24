import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

# Page configuration for mobile-first design
st.set_page_config(
    page_title="SPCA Mobile Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-first design
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Mobile navigation */
    .mobile-nav {
        position: sticky;
        top: 0;
        z-index: 100;
        background: white;
        padding: 0.5rem;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    /* Room navigation */
    .room-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0;
        padding: 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .room-nav-button {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        background: #007bff;
        color: white;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .room-nav-button:hover {
        background: #0056b3;
        transform: translateY(-1px);
    }
    
    .room-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
    }
    
    /* Kennel grid container */
    .kennel-grid-container {
        width: 98vw;
        max-width: 1400px;
        aspect-ratio: 4 / 3;
        margin: 0 auto 32px auto;
        display: grid;
        gap: 12px;
        border: 2px solid #333;
        background: #eee;
        box-sizing: border-box;
        align-items: stretch;
        justify-items: stretch;
    }
    
    .kennel-block {
        background: #f9f9f9;
        border: 1.5px solid #333;
        border-radius: 6px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        min-width: 0;
        min-height: 0;
        width: 100%;
        height: 100%;
        padding: 8px;
        box-sizing: border-box;
        overflow: hidden;
        position: relative;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .kennel-block:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .kennel-label-small {
        position: absolute;
        top: 6px;
        left: 10px;
        font-size: 0.95em;
        color: #333;
        font-weight: 600;
        opacity: 0.95;
        z-index: 2;
        pointer-events: none;
    }
    
    .kennel-animal-list {
        margin-top: 2.2em;
        width: 100%;
        max-height: 100%;
        overflow-y: auto;
        container-type: inline-size;
    }
    
    .kennel-animal {
        color: #222;
        font-size: 1em;
        margin: 0;
        padding: 0;
        line-height: 1.1em;
        word-break: break-word;
        font-stretch: ultra-condensed;
        white-space: normal;
    }
    
    .stage-abbr {
        color: #c00;
        font-weight: bold;
        text-transform: uppercase;
        margin-left: 0.25em;
    }
    
    /* Link-style buttons for sublocations */
    .stButton > button[data-testid*="list_"] {
        background: transparent !important;
        border: none !important;
        color: #007bff !important;
        text-decoration: underline !important;
        padding: 4px 0 !important;
        margin: 2px 0 !important;
        text-align: left !important;
        font-size: 1rem !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        width: auto !important;
        height: auto !important;
        min-height: auto !important;
    }
    
    .stButton > button[data-testid*="list_"]:hover {
        background: #f8f9fa !important;
        color: #0056b3 !important;
    }
    
    /* Empty sublocation styling */
    .empty-sublocation {
        color: #6c757d;
        font-style: italic;
        padding: 4px 0;
        margin: 2px 0;
    }
    
    /* Make invisible buttons completely invisible */
    .stButton > button[data-testid*="click_"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        background: none !important;
    }
    
    /* Make buttons look like plain text and take full width */
    .stButton > button {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        min-height: auto !important;
        padding: 4px 0 !important;
        margin: 2px 0 !important;
        border: none !important;
        border-radius: 0 !important;
        background: transparent !important;
        color: #333 !important;
        font-size: 1rem !important;
        text-align: left !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.4 !important;
        box-shadow: none !important;
        cursor: pointer !important;
        font-family: inherit !important;
        font-weight: normal !important;
        text-decoration: none !important;
        outline: none !important;
        transition: color 0.2s !important;
        display: block !important;
    }
    
    /* Make small "View Details" buttons look clean */
    .stButton > button {
        width: auto !important;
        min-width: auto !important;
        max-width: auto !important;
        height: 28px !important;
        min-height: 28px !important;
        padding: 4px 12px !important;
        margin: 2px 0 !important;
        border: 1px solid #ddd !important;
        border-radius: 4px !important;
        background: white !important;
        color: #007bff !important;
        font-size: 0.8rem !important;
        text-align: center !important;
        white-space: nowrap !important;
        box-shadow: none !important;
        cursor: pointer !important;
        font-family: inherit !important;
        font-weight: normal !important;
        text-decoration: none !important;
        outline: none !important;
        transition: all 0.2s !important;
        display: inline-block !important;
    }
    
    .stButton > button:hover {
        background: #f8f9fa !important;
        border-color: #007bff !important;
        color: #0056b3 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transform: none !important;
        text-decoration: none !important;
    }
    
    /* Red text for stage names */
    .stage-red {
        color: #dc3545 !important;
        font-weight: bold !important;
    }
    
    .stButton > button:hover {
        background: transparent !important;
        border: none !important;
        color: #007bff !important;
        box-shadow: none !important;
        transform: none !important;
        text-decoration: underline !important;
    }
    
    .stButton > button:focus {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stButton > button:active {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        transform: none !important;
    }
    
    .photo-indicator {
        color: #ff6b35;
        font-weight: bold;
        font-size: 0.8em;
        text-transform: uppercase;
        margin-top: 2px;
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 3px;
        padding: 1px 4px;
        display: inline-block;
        text-align: center;
    }
    
    .photo-count {
        color: #666;
        font-weight: normal;
        font-style: italic;
        margin-top: 1px;
        display: inline-block;
        text-align: center;
    }
    
    /* Small Animals & Exotics specific styling */
    .sa-block {
        margin-bottom: 1rem;
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sa-heading {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sa-bird-grid, .sa-sa-grid, .sa-mammal1-grid, .sa-mammal2-grid, .sa-reptile-grid, .sa-counter-grid {
        display: grid;
        gap: 8px;
        margin-bottom: 1rem;
    }
    
    .sa-bird-grid {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
    }
    
    .sa-sa-grid {
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
    }
    
    .sa-mammal1-grid, .sa-mammal2-grid {
        grid-template-columns: 1fr;
        grid-template-rows: 1fr 1fr;
    }
    
    .sa-reptile-grid {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
    }
    
    .sa-counter-grid {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr;
    }
    
    /* Consistent button sizing - fill available space properly */
    .stButton > button {
        width: 100% !important;
        height: 80px !important;
        font-size: 0.8rem;
        white-space: pre-wrap;
        text-align: center;
        padding: 0.3rem;
        border-radius: 6px;
        border: 2px solid #ddd;
        background: #f8f9fa;
        transition: all 0.2s;
        margin: 0 !important;
        min-height: 80px !important;
        max-width: none !important;
        flex: 1 !important;
    }
    
    /* Ensure columns fill space properly */
    .stColumn {
        padding: 0 2px !important;
        flex: 1 !important;
    }
    
    /* Remove gaps between buttons */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    /* Force columns to use full width */
    .stColumns {
        gap: 4px !important;
        width: 100% !important;
    }
    
    /* Ensure buttons fill their containers */
    .stButton {
        width: 100% !important;
        flex: 1 !important;
    }
    
    /* Red text for status abbreviations */
    .status-red {
        color: #dc3545 !important;
        font-weight: bold !important;
    }
    
        /* Kennel grid container - like RoundsMapp */
        .kennel-grid-container {
            width: 100% !important;
            display: grid !important;
            gap: 4px !important;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
            margin: 0 auto !important;
        }
        
        .kennel-block {
            background: #f9f9f9 !important;
            border: 1.5px solid #333 !important;
            border-radius: 6px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            justify-content: flex-start !important;
            min-width: 0 !important;
            min-height: 0 !important;
            width: 100% !important;
            height: 120px !important;
            padding: 0 !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
            position: relative !important;
        }
        
        .kennel-block .stButton {
            width: 100% !important;
            height: 100% !important;
            margin: 0 !important;
        }
        
        .kennel-block .stButton > button {
            width: 100% !important;
            height: 100% !important;
            background: transparent !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 8px !important;
            margin: 0 !important;
            text-align: left !important;
            font-size: 0.8rem !important;
            line-height: 1.2em !important;
            white-space: pre-wrap !important;
            overflow-y: auto !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-start !important;
            align-items: flex-start !important;
            box-sizing: border-box !important;
        }
        
        .kennel-label {
            position: absolute !important;
            top: 6px !important;
            left: 10px !important;
            font-size: 0.95em !important;
            color: #333 !important;
            font-weight: 600 !important;
            opacity: 0.95 !important;
            z-index: 2 !important;
            pointer-events: none !important;
        }
        
        .kennel-animal-list {
            margin-top: 2.2em !important;
            width: 100% !important;
            max-height: 100% !important;
            overflow-y: auto !important;
            color: #222 !important;
            font-size: 0.9em !important;
            line-height: 1.2em !important;
            word-break: break-word !important;
            white-space: normal !important;
        }
        
        /* Make navigation buttons small */
        .stButton > button:not([data-testid*="kennel"]) {
            height: 30px !important;
            width: auto !important;
            min-width: 50px !important;
            max-width: 100px !important;
        }
        
        /* Force columns to fill space with no gaps */
        .stColumn {
            flex: 1 !important;
            min-width: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove gaps between columns */
        .stColumns {
            gap: 0 !important;
            width: 100% !important;
        }
        
        /* Desktop mode - smaller buttons, more columns */
        .desktop-mode .stButton > button {
            height: 100px !important;
            font-size: 0.7rem !important;
        }
        
        /* Dog adoptions - 2 column layout */
        .dog-adoptions .stColumns {
            display: flex !important;
            flex-direction: row !important;
        }
        
        .dog-adoptions .stColumn {
            flex: 1 !important;
            min-width: 0 !important;
            padding: 2px !important;
        }
        
        
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .stButton > button[data-testid*="kennel"] {
                height: 160px !important;
                font-size: 0.7rem !important;
            }
            .stColumn {
                padding: 1px !important;
            }
            .stColumns {
                gap: 2px !important;
            }
        }
        
        /* Red status text styling */
        .status-red {
            color: #dc3545 !important;
            font-weight: bold !important;
        }
        
        /* Target navigation buttons by their specific keys */
        button[data-testid*="prev_room"],
        button[data-testid*="next_room"],
        button[data-testid*="prev_animal"],
        button[data-testid*="next_animal"],
        button[data-testid*="close_modal"] {
            height: 30px !important;
            min-height: 30px !important;
            width: 50px !important;
            min-width: 50px !important;
            max-width: 50px !important;
            padding: 4px 8px !important;
            font-size: 0.8rem !important;
        }
        
        /* Force all buttons to be small except kennel buttons */
        .stButton > button:not([data-testid*="kennel"]) {
            height: 30px !important;
            min-height: 30px !important;
            width: auto !important;
            min-width: 50px !important;
            max-width: 100px !important;
            padding: 4px 8px !important;
            font-size: 0.8rem !important;
        }
        
        /* Reduce spacing in modals */
        .element-container {
            margin-bottom: 0.5rem !important;
        }
        
        /* Compact room headers */
        h3 {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Reduce padding in main content */
        .main .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
    
    .stButton > button:hover {
        border-color: #007bff;
        background: #e3f2fd;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:disabled {
        background: #f8f9fa;
        border-color: #e9ecef;
        color: #6c757d;
    }
    
    /* Remove gaps between buttons */
    .element-container {
        margin-bottom: 0;
    }
    
    /* Ensure buttons fill their containers */
    .stButton {
        width: 100%;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .kennel-grid-container {
            width: 95vw;
            gap: 8px;
        }
        
        .kennel-block {
            padding: 6px;
        }
        
        .kennel-animal {
            font-size: 0.8em;
        }
        
        .room-nav-button {
            padding: 1rem 1.5rem;
            font-size: 1.1rem;
        }
        
        .stButton > button {
            height: 70px;
            font-size: 0.75rem;
            padding: 0.2rem;
        }
    }
    
    /* Container queries for text scaling */
    @container (max-width: 200px) {
        .kennel-animal {
            font-size: 0.8em;
        }
    }
    @container (max-width: 150px) {
        .kennel-animal {
            font-size: 0.7em;
        }
    }
    @container (max-width: 100px) {
        .kennel-animal {
            font-size: 0.6em;
        }
    }
</style>
""", unsafe_allow_html=True)

# Data loading functions
@st.cache_data
def load_animal_inventory():
    """Load animal inventory data"""
    try:
        df = pd.read_csv('AnimalInventory.csv', skiprows=3, on_bad_lines='skip', encoding='utf-8', low_memory=False)
        df.columns = df.columns.str.strip()
        df = df.dropna(how='all')
        
        # Clean up data
        for col in ["AnimalName", "Stage", "Location", "SubLocation"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error loading AnimalInventory.csv: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_behavior_memos():
    """Load behavior memo data"""
    try:
        df = pd.read_csv('AnimalInventoryMemo.csv', skiprows=3, on_bad_lines='skip', encoding='utf-8', low_memory=False)
        df.columns = df.columns.str.strip()
        df = df.dropna(how='all')
        
        # Filter for Behavior/Adoption Info memos
        if 'AnimalMemoType' in df.columns and 'AnimalMemoSubType' in df.columns:
            df = df[(df['AnimalMemoType'].str.strip() == 'Behavior') & (df['AnimalMemoSubType'].str.strip() == 'Adoption Info')]
        
        return df
    except Exception as e:
        st.error(f"Error loading AnimalInventoryMemo.csv: {str(e)}")
        return pd.DataFrame()

# Status mapping (from RoundsMapp)
STATUS_MAP = {
    'Evaluate': 'EVAL',
    'Hold - Adopted!': 'ADPT',
    'Hold - Behavior': 'BEHA',
    'Hold - Behavior Foster': 'BFOS',
    'Hold - Behavior Mod.': 'BMOD',
    'Hold - Bite/Scratch': 'B/S',
    'Hold - Canisus Program': 'CANISUS',
    'Hold - Complaint': 'COMP',
    'Hold - Cruelty Foster': 'CF',
    'Hold - Dental': 'DENT',
    'Hold - Doc': 'DOC',
    'Hold - Evidence!': 'EVID',
    'Hold - For RTO': 'RTO',
    'Hold - Foster': 'FOST',
    'Hold - Legal Notice': 'LEGAL',
    'Hold - Media!': 'MEDIA',
    'Hold - Meet and Greet': 'M+G',
    'Hold - Offsite': 'OFFSITE',
    'Hold - Possible Adoption': 'PADPT',
    'Hold - Pups at the Pen!': 'PEN',
    'Hold - Rescue': 'RESC',
    'Hold – SAFE Foster': 'SAFE',
    'Hold - Special Event': 'SPEC',
    'Hold - Stray': 'STRAY',
    'Hold - Surgery': 'SX',
    'Available - Behind the Scenes': 'BTS',
    'Available - ITFF Medical': 'ITFF MED',
    'Available - ITFF Behavior': 'ITFF BEH',
    'Pending Foster Pickup': 'PFP'
}

def map_status(stage):
    """Map stage to full name or None if Available"""
    if pd.isna(stage) or stage == '':
        return None
    
    stage = str(stage).strip()
    
    # Don't show Available status at all
    if 'Available' in stage:
        return None
    
    # Return the full stage name for everything else
    return stage

def create_button_text(display_label, animal, is_empty=False):
    """Create button text with red status abbreviations"""
    if is_empty:
        return f"{display_label}\n-"
    
    # Create clean display text
    name = str(animal.get('AnimalName', 'Unknown'))
    if pd.isna(name) or name.lower() == 'nan':
        name = str(animal.get('AnimalNumber', 'Unknown'))
    
    # Get status abbreviation
    stage = str(animal.get('Stage', ''))
    abbr = map_status(stage)
    
    # Create display text with red status if present
    if abbr:
        # Use a special character or formatting to indicate red text
        display_text = f"{display_label}\n{name} 🔴{abbr}"
    else:
        display_text = f"{display_label}\n{name}"
    
    return display_text

def format_display_line(row):
    """Format animal display line (from RoundsMapp)"""
    name = row["AnimalName"]
    if name.lower() == 'nan' or name.strip() == '' or pd.isna(name):
        animal_number = str(row.get("AnimalNumber", ""))
        name = animal_number[-8:] if len(animal_number) >= 8 else animal_number
    name = name.title()
    stage = row["Stage"]
    abbr = map_status(stage)
    
    # Build the display line
    display_parts = []
    display_parts.append(name)
    
    if abbr:
        display_parts.append(f'<span class="stage-abbr">{abbr}</span>')
    
    display_line = ' '.join(display_parts)
    
    return display_line

# Room definitions - only define sublocations for specific rooms
ROOM_DEFINITIONS = {
    "Adoptions Lobby": {
        "location": ["Adoptions Lobby", "Feature Room 1", "Feature Room 2"]
        # No sublocation defined - will pull from data
    },
    "Cat Adoption Condo Rooms": {
        "location": "Cat Adoption Condo Rooms",
        "sublocation": ["Catiat 1", "Catiat 2", "Catiat 3", "Catiat 4", "Catiat 5", "Condo A", "Condo B", "Condo C", "Condo D", "Condo E", "Condo F", "Counselling Room 110", "Ferret Cage", "Meet & Greet 109A", "Meet & Greet 109B", "Rabbitat 1", "Rabbitat 2", "Cat Behavior 174"]
    },
    "Cat Adoption Room G": {
        "location": "Cat Adoption Room G",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08"]
    },
    "Cat Adoption Room H": {
        "location": "Cat Adoption Room H",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08"]
    },
    "Cat Behavior Room I": {
        "location": "Cat Behavior Room I",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08"]
    },
    "Foster Care Room": {
        "location": "Foster Care Room",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08", "Foster Care Room"]
    },
    "Cat Treatment": {
        "location": "Cat Treatment"
        # No sublocation defined - will pull from data
    },
    "Cat Isolation 230": {
        "location": "Cat Isolation 230",
        "sublocation": ["Cage 1", "Cage 2", "Cage 3", "Cage 4", "Cage 5"]
    },
    "Cat Isolation 231": {
        "location": "Cat Isolation 231",
        "sublocation": ["Cage 1", "Cage 2", "Cage 3", "Cage 4", "Cage 5", "Cage 6", "Cage 7", "Cage 8", "Cage 9"]
    },
    "Cat Isolation 232": {
        "location": "Cat Isolation 232",
        "sublocation": ["Cage 1", "Cage 2", "Cage 3", "Cage 4", "Cage 5", "Cage 6"]
    },
    "Cat Isolation 233": {
        "location": "Cat Isolation 233",
        "sublocation": ["Cage 1", "Cage 2", "Cage 3", "Cage 4", "Cage 5", "Cage 6"]
    },
    "Cat Isolation 234": {
        "location": "Cat Isolation 234",
        "sublocation": ["Cage 1", "Cage 2", "Cage 3", "Cage 4", "Cage 5", "Cage 6"]
    },
    "Cat Isolation 235": {
        "location": "Cat Isolation 235",
        "sublocation": ["Cage 1", "Cage 2", "Cage 3", "Cage 4", "Cage 5", "Cage 6", "Cage 7", "Cage 8", "Cage 9"]
    },
    "Dog Adoptions A": {
        "location": "Dog Adoptions A",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    },
    "Dog Adoptions B": {
        "location": "Dog Adoptions B",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    },
    "Dog Adoptions C": {
        "location": "Dog Adoptions C",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    },
    "Dog Adoptions D": {
        "location": "Dog Adoptions D",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
    },
    "Dog Holding E": {
        "location": "Dog Holding E",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    },
    "Dog Holding F": {
        "location": "Dog Holding F",
        "sublocation": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    },
    "ICU": {
        "location": "ICU"
        # No sublocation defined - will pull from data
    },
    "Multi-Animal Holding, Room 227": {
        "location": "Multi-Animal Holding, Room 227"
        # No sublocation defined - will pull from data
    },
    "Multi-Animal Holding, Room 229": {
        "location": "Multi-Animal Holding, Room 229"
        # No sublocation defined - will pull from data
    },
    "Small Animals & Exotics": {
        "location": "Small Animals & Exotics"
        # No sublocation defined - will pull from data
    }
}

def render_small_animals_layout(animals_df, memo_df):
    """Render Small Animals & Exotics layout with clean selectbox interface"""
    
    sa_df = animals_df[animals_df['Location'] == 'Small Animals & Exotics'].copy()
    
    # Birds section
    st.markdown("**Birds**")
    bird_cages = ["Bird Cage 1", "Bird Cage 2", "Bird Cage 3", "Bird Cage 4", "Bird Cage EXTRA"]
    
    # Create options for birds
    bird_options = []
    bird_data = {}
    
    for cage in bird_cages:
        cell_animals = sa_df[sa_df["SubLocation"] == cage]
        if not cell_animals.empty:
            # Show all animal names
            animal_names = []
            for _, animal in cell_animals.iterrows():
                name = str(animal.get('AnimalName', 'Unknown'))
                if pd.isna(name) or name.lower() == 'nan':
                    name = str(animal.get('AnimalNumber', 'Unknown'))
                
                stage = str(animal.get('Stage', ''))
                abbr = map_status(stage)
                
                if abbr:
                    animal_names.append(f'{name} {abbr}')
                else:
                    animal_names.append(name)
            
            display_text = f'{cage}: ' + ', '.join(animal_names)
            bird_options.append(display_text)
            bird_data[display_text] = cell_animals
        else:
            display_text = f'{cage}: -'
            bird_options.append(display_text)
            bird_data[display_text] = None
    
    # Display each bird cage directly
    for cage in bird_cages:
        cell_animals = sa_df[sa_df["SubLocation"] == cage]
        if not cell_animals.empty:
            # Show all animal names
            animal_names = []
            for _, animal in cell_animals.iterrows():
                name = str(animal.get('AnimalName', 'Unknown'))
                if pd.isna(name) or name.lower() == 'nan':
                    name = str(animal.get('AnimalNumber', 'Unknown'))
                
                stage = str(animal.get('Stage', ''))
                abbr = map_status(stage)
                
                if abbr:
                    animal_names.append(f'{name} {abbr}')
                else:
                    animal_names.append(name)
            
            display_text = f'{cage}: ' + ', '.join(animal_names)
            
            st.markdown(display_text, unsafe_allow_html=True)
            if st.button("View Details", key=f"view_bird_{cage}"):
                st.session_state.kennel_animals = cell_animals.to_dict('records')
                st.session_state.current_animal_idx = 0
                st.session_state.selected_animal = cell_animals.iloc[0].to_dict()
                st.session_state.show_modal = True
                st.rerun()
        else:
            pass  # Empty cage, don't show anything
    
    # Small Animals section
    st.markdown("**Small Animals**")
    sa_cages = [f"Small Animal {i}" for i in range(1,9)]
    
    # Display each small animal cage directly
    for cage in sa_cages:
        cell_animals = sa_df[sa_df["SubLocation"] == cage]
        if not cell_animals.empty:
            # Show all animal names
            animal_names = []
            for _, animal in cell_animals.iterrows():
                name = str(animal.get('AnimalName', 'Unknown'))
                if pd.isna(name) or name.lower() == 'nan':
                    name = str(animal.get('AnimalNumber', 'Unknown'))
                
                stage = str(animal.get('Stage', ''))
                abbr = map_status(stage)
                
                if abbr:
                    animal_names.append(f'{name} {abbr}')
                else:
                    animal_names.append(name)
            
            display_text = f'{cage}: ' + ', '.join(animal_names)
            
            if st.button(display_text, key=f"sa_{cage}"):
                st.session_state.kennel_animals = cell_animals.to_dict('records')
                st.session_state.current_animal_idx = 0
                st.session_state.selected_animal = cell_animals.iloc[0].to_dict()
                st.session_state.show_modal = True
                st.rerun()
        else:
            pass  # Empty cage, don't show anything
    
    # Mammals section
    st.markdown("**Mammals**")
    mammal_cages = [f"Mammal {i}" for i in range(1,5)]
    
    # Create options for mammals
    mammal_options = []
    mammal_data = {}
    
    for cage in mammal_cages:
        cell_animals = sa_df[sa_df["SubLocation"] == cage]
        if not cell_animals.empty:
            # Show all animal names
            animal_names = []
            for _, animal in cell_animals.iterrows():
                name = str(animal.get('AnimalName', 'Unknown'))
                if pd.isna(name) or name.lower() == 'nan':
                    name = str(animal.get('AnimalNumber', 'Unknown'))
                
                stage = str(animal.get('Stage', ''))
                abbr = map_status(stage)
                
                if abbr:
                    animal_names.append(f'{name} {abbr}')
                else:
                    animal_names.append(name)
            
            display_text = f'{cage}: ' + ', '.join(animal_names)
            mammal_options.append(display_text)
            mammal_data[display_text] = cell_animals
        else:
            display_text = f'{cage}: -'
            mammal_options.append(display_text)
            mammal_data[display_text] = None
    
    # Display each mammal cage directly
    for cage in mammal_cages:
        cell_animals = sa_df[sa_df["SubLocation"] == cage]
        if not cell_animals.empty:
            # Show all animal names
            animal_names = []
            for _, animal in cell_animals.iterrows():
                name = str(animal.get('AnimalName', 'Unknown'))
                if pd.isna(name) or name.lower() == 'nan':
                    name = str(animal.get('AnimalNumber', 'Unknown'))
                
                stage = str(animal.get('Stage', ''))
                abbr = map_status(stage)
                
                if abbr:
                    animal_names.append(f'{name} {abbr}')
                else:
                    animal_names.append(name)
            
            display_text = f'{cage}: ' + ', '.join(animal_names)
            
            if st.button(display_text, key=f"mammal_{cage}"):
                st.session_state.kennel_animals = cell_animals.to_dict('records')
                st.session_state.current_animal_idx = 0
                st.session_state.selected_animal = cell_animals.iloc[0].to_dict()
                st.session_state.show_modal = True
                st.rerun()
        else:
            pass  # Empty cage, don't show anything
    
    # Reptiles section
    st.markdown("**Reptiles**")
    reptile_cages = [f"Reptile {i}" for i in range(1,6)]
    
    # Display each reptile cage directly
    for cage in reptile_cages:
        cell_animals = sa_df[sa_df["SubLocation"] == cage]
        if not cell_animals.empty:
            # Show all animal names
            animal_names = []
            for _, animal in cell_animals.iterrows():
                name = str(animal.get('AnimalName', 'Unknown'))
                if pd.isna(name) or name.lower() == 'nan':
                    name = str(animal.get('AnimalNumber', 'Unknown'))
                
                stage = str(animal.get('Stage', ''))
                abbr = map_status(stage)
                
                if abbr:
                    animal_names.append(f'{name} {abbr}')
                else:
                    animal_names.append(name)
            
            display_text = f'{cage}: ' + ', '.join(animal_names)
            
            if st.button(display_text, key=f"reptile_{cage}"):
                st.session_state.kennel_animals = cell_animals.to_dict('records')
                st.session_state.current_animal_idx = 0
                st.session_state.selected_animal = cell_animals.iloc[0].to_dict()
                st.session_state.show_modal = True
                st.rerun()
        else:
            pass  # Empty cage, don't show anything
    
    # Countertop Cages section
    st.markdown("**Countertop Cages**")
    counter_cages = [f"Countertop Cage {i}" for i in range(1,3)]
    
    # Display each countertop cage directly
    for cage in counter_cages:
        cell_animals = sa_df[sa_df["SubLocation"] == cage]
        if not cell_animals.empty:
            # Show all animal names
            animal_names = []
            for _, animal in cell_animals.iterrows():
                name = str(animal.get('AnimalName', 'Unknown'))
                if pd.isna(name) or name.lower() == 'nan':
                    name = str(animal.get('AnimalNumber', 'Unknown'))
                
                stage = str(animal.get('Stage', ''))
                abbr = map_status(stage)
                
                if abbr:
                    animal_names.append(f'{name} {abbr}')
                else:
                    animal_names.append(name)
            
            display_text = f'{cage}: ' + ', '.join(animal_names)
            
            if st.button(display_text, key=f"counter_{cage}"):
                st.session_state.kennel_animals = cell_animals.to_dict('records')
                st.session_state.current_animal_idx = 0
                st.session_state.selected_animal = cell_animals.iloc[0].to_dict()
                st.session_state.show_modal = True
                st.rerun()
        else:
            pass  # Empty cage, don't show anything

def handle_sublocation_click(room_name, subloc, animals):
    """Handle click on a sublocation link"""
    # Store all animals for this sublocation and show modal for first one
    st.session_state.kennel_animals = animals.to_dict('records')
    st.session_state.current_animal_idx = 0
    st.session_state.selected_animal = animals.iloc[0].to_dict()
    st.session_state.show_modal = True
    st.rerun()

def render_room_list(room_name, animals_df, memo_df):
    """Render a room as a simple list organized by sublocation"""
    
    if room_name not in ROOM_DEFINITIONS:
        # Handle dynamically added rooms (locations not in ROOM_DEFINITIONS)
        st.markdown(f"**{room_name}**")
        
        # Get all animals for this location
        room_animals = animals_df[animals_df['Location'] == room_name]
        
        if room_animals.empty:
            st.write("No animals in this location.")
            return
        
        # Group by sublocation
        sublocations = sorted(room_animals['SubLocation'].unique())
        for subloc in sublocations:
            animals = room_animals[room_animals['SubLocation'] == subloc]
            
            if not animals.empty:
                # Show all animal names
                animal_names = []
                for _, animal in animals.iterrows():
                    name = str(animal.get('AnimalName', 'Unknown'))
                    if pd.isna(name) or name.lower() == 'nan':
                        name = str(animal.get('AnimalNumber', 'Unknown'))
                    
                    stage = str(animal.get('Stage', ''))
                    stage_display = map_status(stage)
                    
                    if stage_display:
                        animal_names.append(f'{name} <span class="stage-red">{stage_display}</span>')
                    else:
                        animal_names.append(name)
                
                display_text = f'{subloc}: ' + ', '.join(animal_names)
                
                # Show as HTML with red stage names
                st.markdown(f"""
                <div style="margin: 8px 0; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                    {display_text}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.write(f'{subloc}: -')
        return
    
    room_config = ROOM_DEFINITIONS[room_name]
    
    # Handle combined locations
    if isinstance(room_config["location"], list):
        location = room_config["location"]
        # Filter animals for combined locations
        room_animals = animals_df[animals_df['Location'].isin(location)]
    else:
        location = room_config["location"]
        room_animals = animals_df[animals_df['Location'] == location]
    
    
    # Don't filter by sublocation here - we want to show all sublocations even if empty
    
    st.markdown(f"**{room_name}**")
    
    # Get sublocations for this room
    if "sublocation" in room_config:
        # Use predefined sublocations
        sublocations = room_config["sublocation"]
        
        # If we have multiple locations, organize by location first
        if isinstance(location, list) and len(location) > 1:
            for loc in location:
                st.markdown(f"**{loc}**")
                loc_animals = room_animals[room_animals['Location'] == loc]
                
                # Only show sublocations that have animals
                actual_sublocs = sorted(loc_animals['SubLocation'].unique()) if not loc_animals.empty else []
                
                # Display each sublocation for this location
                for subloc in actual_sublocs:
                    animals = loc_animals[loc_animals['SubLocation'] == subloc]
                    
                    if not animals.empty:
                        # Show all animal names
                        animal_names = []
                        for _, animal in animals.iterrows():
                            name = str(animal.get('AnimalName', 'Unknown'))
                            if pd.isna(name) or name.lower() == 'nan':
                                name = str(animal.get('AnimalNumber', 'Unknown'))
                            
                            stage = str(animal.get('Stage', ''))
                            stage_display = map_status(stage)
                            
                            if stage_display:
                                animal_names.append(f'{name} <span class="stage-red">{stage_display}</span>')
                            else:
                                animal_names.append(name)
                        
                        display_text = f'{subloc}: ' + ', '.join(animal_names)
                        
                        # Show as HTML with red stage names
                        st.markdown(display_text, unsafe_allow_html=True)
                        if st.button("View Details", key=f"view_{room_name}_{loc}_{subloc}"):
                            st.session_state.kennel_animals = animals.to_dict('records')
                            st.session_state.current_animal_idx = 0
                            st.session_state.selected_animal = animals.iloc[0].to_dict()
                            st.session_state.show_modal = True
                            st.rerun()
        else:
            # Single location - display each sublocation directly
            # Only show sublocations that have animals
            actual_sublocs = sorted(room_animals['SubLocation'].unique()) if not room_animals.empty else []
            
            for subloc in actual_sublocs:
                animals = room_animals[room_animals['SubLocation'] == subloc]
                
                if not animals.empty:
                    # Show all animal names
                    animal_names = []
                    for _, animal in animals.iterrows():
                        name = str(animal.get('AnimalName', 'Unknown'))
                        if pd.isna(name) or name.lower() == 'nan':
                            name = str(animal.get('AnimalNumber', 'Unknown'))
                        
                        stage = str(animal.get('Stage', ''))
                        stage_display = map_status(stage)
                        
                        if stage_display:
                            animal_names.append(f'{name} <span class="stage-red">{stage_display}</span>')
                        else:
                            animal_names.append(name)
                    
                    display_text = f'{subloc}: ' + ', '.join(animal_names)
                    
                    # Show as plain text with a small button below
                    st.markdown(display_text, unsafe_allow_html=True)
                    if st.button("View Details", key=f"view_{room_name}_{subloc}"):
                        st.session_state.kennel_animals = animals.to_dict('records')
                        st.session_state.current_animal_idx = 0
                        st.session_state.selected_animal = animals.iloc[0].to_dict()
                        st.session_state.show_modal = True
                        st.rerun()
                else:
                    # Empty sublocation
                    st.write(f'{subloc}: -')
    else:
        # No predefined sublocations - pull from data
        if not room_animals.empty:
            sublocations = sorted(room_animals['SubLocation'].unique())
        else:
            sublocations = []
        
        # If we have multiple locations, organize by location first
        if isinstance(location, list) and len(location) > 1:
            for loc in location:
                st.markdown(f"**{loc}**")
                loc_animals = room_animals[room_animals['Location'] == loc]
                
                # Show all sublocations that exist in data for this location
                actual_sublocs = sorted(loc_animals['SubLocation'].unique()) if not loc_animals.empty else []
                
                # Display each sublocation for this location
                for subloc in actual_sublocs:
                    animals = loc_animals[loc_animals['SubLocation'] == subloc]
                    
                    if not animals.empty:
                        # Show all animal names
                        animal_names = []
                        for _, animal in animals.iterrows():
                            name = str(animal.get('AnimalName', 'Unknown'))
                            if pd.isna(name) or name.lower() == 'nan':
                                name = str(animal.get('AnimalNumber', 'Unknown'))
                            
                            stage = str(animal.get('Stage', ''))
                            stage_display = map_status(stage)
                            
                            if stage_display:
                                animal_names.append(f'{name} <span class="stage-red">{stage_display}</span>')
                            else:
                                animal_names.append(name)
                        
                        display_text = f'{subloc}: ' + ', '.join(animal_names)
                        
                        # Show as HTML with red stage names
                        st.markdown(f"""
                        <div style="margin: 8px 0; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                            {display_text}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write(f'{subloc}: -')
        else:
            # Single location - display each sublocation directly
            for subloc in sublocations:
                animals = room_animals[room_animals['SubLocation'] == subloc]
                
                if not animals.empty:
                    # Show all animal names
                    animal_names = []
                    for _, animal in animals.iterrows():
                        name = str(animal.get('AnimalName', 'Unknown'))
                        if pd.isna(name) or name.lower() == 'nan':
                            name = str(animal.get('AnimalNumber', 'Unknown'))
                        
                        stage = str(animal.get('Stage', ''))
                        stage_display = map_status(stage)
                        
                        if stage_display:
                            animal_names.append(f'{name} <span class="stage-red">{stage_display}</span>')
                        else:
                            animal_names.append(name)
                    
                    display_text = f'{subloc}: ' + ', '.join(animal_names)
                    
                    # Show as HTML with red stage names
                    st.markdown(f"""
                    <div style="margin: 8px 0; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                        {display_text}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write(f'{subloc}: -')

def render_room_layout(room_name, animals_df, memo_df, view_mode="Mobile"):
    """Render a room layout with consistent button sizing"""
    
    if room_name not in ROOM_DEFINITIONS:
        st.error(f"Room {room_name} not defined")
        return
    
    room_config = ROOM_DEFINITIONS[room_name]
    
    # Apply view mode styling
    if view_mode == "Desktop":
        st.markdown('<div class="desktop-mode">', unsafe_allow_html=True)
    
    # Apply dog adoptions styling
    if "Dog Adoptions" in room_name:
        st.markdown('<div class="dog-adoptions">', unsafe_allow_html=True)
    
    # Special handling for Small Animals & Exotics
    if room_config.get("type") == "small_animals":
        render_small_animals_layout(animals_df, memo_df)
        return
    
    location = room_config["location"]
    grid_map = room_config["grid_map"]
    grid_cols = room_config["grid_cols"]
    
    # Filter animals for this room
    if "sublocation" in room_config:
        if isinstance(room_config["sublocation"], list):
            room_animals = animals_df[(animals_df['Location'] == location) & (animals_df['SubLocation'].isin(room_config["sublocation"]))].copy()
        else:
            room_animals = animals_df[(animals_df['Location'] == location) & (animals_df['SubLocation'] == room_config["sublocation"])].copy()
    elif isinstance(location, list):
        # Handle combined rooms like Dog Adoptions A & B
        room_animals = animals_df[animals_df['Location'].isin(location)].copy()
    else:
        room_animals = animals_df[animals_df['Location'] == location].copy()
    
    # Ensure SubLocation is zero-padded string for numeric sublocations
    if room_name in ["Cat Adoption Room G", "Cat Adoption Room H", "Cat Behavior Room I", "Foster Care Room", "Dog Adoptions A & B", "Dog Adoptions C & D"]:
        room_animals["SubLocation"] = room_animals["SubLocation"].astype(str).str.zfill(2)
    
    # Create mapping of sublocation to animals
    sublocation_to_animals = {}
    for _, animal in room_animals.iterrows():
        subloc = animal.get('SubLocation', '')
        location = animal.get('Location', '')
        if pd.notna(subloc) and subloc != '':
            # For combined dog adoptions, create prefixed sublocation
            if room_name in ["Dog Adoptions A & B", "Dog Adoptions C & D"]:
                if "Dog Adoptions A" in location:
                    prefixed_subloc = f"A{subloc}"
                elif "Dog Adoptions B" in location:
                    prefixed_subloc = f"B{subloc}"
                elif "Dog Adoptions C" in location:
                    prefixed_subloc = f"C{subloc}"
                elif "Dog Adoptions D" in location:
                    prefixed_subloc = f"D{subloc}"
                else:
                    prefixed_subloc = subloc
                
                if prefixed_subloc not in sublocation_to_animals:
                    sublocation_to_animals[prefixed_subloc] = []
                sublocation_to_animals[prefixed_subloc].append(animal)
            else:
                if subloc not in sublocation_to_animals:
                    sublocation_to_animals[subloc] = []
                sublocation_to_animals[subloc].append(animal)
    
    st.markdown(f"**{room_name}**")
    
    # Create kennel grid using Streamlit columns but with RoundsMapp styling
    for row_idx, row in enumerate(grid_map):
        cols = st.columns(grid_cols, gap="small")
        for col_idx, subloc in enumerate(row):
            if subloc is None:
                with cols[col_idx]:
                    st.write("")  # Empty space
            else:
                with cols[col_idx]:
                    animals = sublocation_to_animals.get(subloc, [])
                    # For combined dog adoptions, show just the number part
                    if room_name in ["Dog Adoptions A & B", "Dog Adoptions C & D"]:
                        display_label = subloc[1:] if len(subloc) > 1 else subloc
                    else:
                        display_label = subloc
                        if subloc.isdigit():
                            display_label = str(int(subloc))
                    
                    # Build animal list for button text
                    if animals:
                        animal_names = []
                        for animal in animals:
                            name = str(animal.get('AnimalName', 'Unknown'))
                            if pd.isna(name) or name.lower() == 'nan':
                                name = str(animal.get('AnimalNumber', 'Unknown'))
                            
                            stage = str(animal.get('Stage', ''))
                            abbr = map_status(stage)
                            
                            if abbr:
                                animal_names.append(f'{name} {abbr}')
                            else:
                                animal_names.append(name)
                        
                        # Truncate if too many animals to fit
                        if len(animal_names) > 4:
                            display_names = animal_names[:3] + [f'... +{len(animal_names)-3} more']
                        else:
                            display_names = animal_names
                        
                        display_text = f'{display_label}\n' + '\n'.join(display_names)
                        
                        # Create kennel block with button inside
                        st.markdown(f'''
                        <div class="kennel-block">
                            <div class="kennel-label">{display_label}</div>
                            <div class="kennel-animal-list">
                        ''', unsafe_allow_html=True)
                        
                        if st.button(display_text, key=f"kennel_{room_name}_{subloc}"):
                            # Store all animals for this kennel and show modal for first one
                            st.session_state.kennel_animals = animals
                            st.session_state.current_animal_idx = 0
                            st.session_state.selected_animal = animals[0]
                            st.session_state.show_modal = True
                            st.rerun()
                        
                        st.markdown('</div></div>', unsafe_allow_html=True)
                    else:
                        # Empty kennel
                        st.markdown(f'''
                        <div class="kennel-block">
                            <div class="kennel-label">{display_label}</div>
                            <div class="kennel-animal-list">-</div>
                        </div>
                        ''', unsafe_allow_html=True)
    
    # Show animals not assigned to kennels (for rooms with specific sublocations)
    if "sublocation" in room_config:
        all_sublocations = [subloc for row in grid_map for subloc in row if subloc is not None]
        unassigned = room_animals[~room_animals['SubLocation'].isin(all_sublocations)]
        if not unassigned.empty:
            st.markdown("### Animals Not in Kennel Spaces")
            for _, animal in unassigned.iterrows():
                name = str(animal.get('AnimalName', 'Unknown'))
                if pd.isna(name) or name.lower() == 'nan':
                    name = str(animal.get('AnimalNumber', 'Unknown'))
                
                stage = str(animal.get('Stage', ''))
                abbr = map_status(stage)
                
                display_text = name
                if abbr:
                    display_text += f" {abbr}"
                
                if st.button(f"• {display_text}", key=f"unassigned_{room_name}_{animal['AnimalNumber']}"):
                    st.session_state.selected_animal = animal
                    st.session_state.show_modal = True
                    st.rerun()
    
    # Close styling divs
    if "Dog Adoptions" in room_name:
        st.markdown('</div>', unsafe_allow_html=True)
    
    if view_mode == "Desktop":
        st.markdown('</div>', unsafe_allow_html=True)

def render_animal_modal(animal, memo_df):
    """Render animal details modal with navigation for multiple animals"""
    st.markdown("---")
    st.markdown("**Animal Details**")
    
    # Get all animals in this kennel
    kennel_animals = st.session_state.get('kennel_animals', [animal])
    current_idx = st.session_state.get('current_animal_idx', 0)
    
    # Compact navigation buttons if multiple animals
    if len(kennel_animals) > 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("←", key="prev_animal"):
                new_idx = (current_idx - 1) % len(kennel_animals)
                st.session_state.current_animal_idx = new_idx
                st.session_state.selected_animal = kennel_animals[new_idx]
                st.rerun()
        with col2:
            st.markdown(f"**{current_idx + 1}/{len(kennel_animals)}**")
        with col3:
            if st.button("→", key="next_animal"):
                new_idx = (current_idx + 1) % len(kennel_animals)
                st.session_state.current_animal_idx = new_idx
                st.session_state.selected_animal = kennel_animals[new_idx]
                st.rerun()
    
    # Close button
    if st.button("✕", key="close_modal"):
        st.session_state.show_modal = False
        st.rerun()
    
    # Animal name and AID at top with clickable links
    animal_name = animal.get('AnimalName', 'Unknown')
    animal_id = str(animal.get('AnimalNumber', 'Unknown'))
    
    # Extract non-zero digits from animal_id for PetPoint link (same as RoundsMapp)
    petpoint_id = ''.join(filter(str.isdigit, animal_id))
    
    # Create PetPoint profile link for name only
    if petpoint_id:
        petpoint_profile_url = f"https://sms.petpoint.com/sms3/enhanced/animal/{petpoint_id}"  # Regular PetPoint profile
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** [{animal_name}]({petpoint_profile_url})")
        with col2:
            st.markdown(f"**AID:** {animal_id}")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** {animal_name}")
        with col2:
            st.markdown(f"**AID:** {animal_id}")
    
    st.markdown("---")
    
    # Animal details
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Species:** {animal.get('Species', 'Unknown')}")
        st.markdown(f"**Breed:** {animal.get('PrimaryBreed', 'Unknown')}")
        st.markdown(f"**Age:** {animal.get('Age', 'Unknown')}")
        st.markdown(f"**Sex:** {animal.get('Sex', 'Unknown')}")
    with col2:
        st.markdown(f"**Stage:** {animal.get('Stage', 'Unknown')}")
        st.markdown(f"**Location:** {animal.get('Location', 'Unknown')}")
        st.markdown(f"**SubLocation:** {animal.get('SubLocation', 'Unknown')}")
        st.markdown(f"**Weight:** {animal.get('AnimalWeight', 'Unknown')}")
    
    # Behavior memo
    st.markdown("### Behavior Memo")
    animal_memos = memo_df[memo_df['AnimalNumber_1'] == animal.get('AnimalNumber', '')]
    
    if not animal_memos.empty:
        latest_memo = animal_memos.iloc[-1]
        memo_text = latest_memo.get('AnimalMemo_1', 'No memo available')
        memo_date = latest_memo.get('DateCreated_1', 'Unknown date')
        
        st.markdown(f"**Date:** {memo_date}")
        st.markdown(f"""
        <div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 1rem; font-family: monospace; white-space: pre-wrap; max-height: 300px; overflow-y: auto;">
        {memo_text}
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.info("No behavior memo available for this animal.")

# Main app
def main():
    # Load data
    inventory_df = load_animal_inventory()
    memo_df = load_behavior_memos()
    
    if inventory_df.empty:
        st.error("No animal inventory data available. Please check your data files.")
        return
    
    # Initialize session state
    if 'current_room' not in st.session_state:
        st.session_state.current_room = 0
    if 'show_modal' not in st.session_state:
        st.session_state.show_modal = False
    
    # Modal for animal details (show at top if active)
    if st.session_state.get('show_modal', False) and 'selected_animal' in st.session_state:
        render_animal_modal(st.session_state.selected_animal, memo_df)
        return  # Don't show main content when modal is open
    
    # Mobile navigation header
    st.markdown("""
    <div class="mobile-nav">
        <h1 style="margin: 0; font-size: 1.5rem;">🏠 SPCA Mobile Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Define room order based on user's requested order
    room_order = [
        "Adoptions Lobby",
        "Cat Adoption Condo Rooms",
        "Cat Adoption Room G",
        "Cat Adoption Room H",
        "Cat Behavior Room I",
        "Foster Care Room",
        "Cat Treatment",
        "ICU",
        "Multi-Animal Holding, Room 227",
        "Multi-Animal Holding, Room 229",
        "Cat Isolation 230",
        "Cat Isolation 231",
        "Cat Isolation 232",
        "Cat Isolation 233",
        "Cat Isolation 234",
        "Cat Isolation 235",
        "Dog Adoptions A",
        "Dog Adoptions B",
        "Dog Adoptions C",
        "Dog Adoptions D",
        "Dog Holding E",
        "Dog Holding F",
        "Small Animals & Exotics"
    ]
    
    # Rooms that should always be shown (even if empty)
    always_show_rooms = set(room_order)
    
    # Locations to exclude when empty
    exclude_when_empty = {
        "At the Emergency Clinic",
        "At the Veterinarian", 
        "Boarding Facility",
        "Cooler",
        "Farm",
        "Foster Home",
        "Humane Education Offices",
        "If The Fur Fits",
        "Receiving"
    }
    
    # Get available rooms in the specified order
    available_rooms = []
    
    # First, add all requested rooms (always show them)
    for room_name in room_order:
        if room_name in ROOM_DEFINITIONS:
            available_rooms.append(room_name)
    
    # Then, add any other rooms that have animals (except excluded ones)
    all_locations = inventory_df['Location'].unique()
    for location in all_locations:
        if location not in exclude_when_empty:
            # Check if this location is already covered by our room definitions
            already_covered = False
            for room_name, room_config in ROOM_DEFINITIONS.items():
                if isinstance(room_config["location"], list):
                    if location in room_config["location"]:
                        already_covered = True
                        break
                else:
                    if location == room_config["location"]:
                        already_covered = True
                        break
            
            if not already_covered:
                # Create a room name from the location
                room_name = location
                if room_name not in available_rooms:
                    available_rooms.append(room_name)
    
    if not available_rooms:
        st.error("No data found for the target rooms.")
        return
    
    # Add view mode toggle in sidebar
    with st.sidebar:
        st.markdown("### View Settings")
        view_mode = st.radio("Display Mode", ["Mobile", "Desktop"], index=0)
        st.markdown("---")
    
    # Add tabs for different views
    tab1, tab2, tab3 = st.tabs(["🏠 Room View", "🏗️ Layout Builder", "📊 Analytics"])
    
    with tab1:
        # Get current room first
        current_room = available_rooms[st.session_state.current_room]
        
        # Room selector at the top
        selected_room = st.selectbox("Select Room", available_rooms, index=st.session_state.current_room, key="room_selector")
        if selected_room != current_room:
            st.session_state.current_room = available_rooms.index(selected_room)
            st.rerun()
        
        # Compact room navigation
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️", key="prev_room"):
                st.session_state.current_room = (st.session_state.current_room - 1) % len(available_rooms)
                st.rerun()
        
        with col2:
            st.markdown(f"### {current_room}")
        
        with col3:
            if st.button("➡️", key="next_room"):
                st.session_state.current_room = (st.session_state.current_room + 1) % len(available_rooms)
                st.rerun()
        
        # Render current room as a simple list
        render_room_list(current_room, inventory_df, memo_df)
        
        # Show room statistics
        if current_room in ROOM_DEFINITIONS:
            room_config = ROOM_DEFINITIONS[current_room]
            location = room_config["location"]
            
            if room_config.get("type") == "small_animals":
                if isinstance(location, list):
                    room_animals = inventory_df[inventory_df['Location'].isin(location)]
                else:
                    room_animals = inventory_df[inventory_df['Location'] == location]
            elif "sublocation" in room_config:
                if isinstance(room_config["sublocation"], list):
                    if isinstance(location, list):
                        room_animals = inventory_df[(inventory_df['Location'].isin(location)) & (inventory_df['SubLocation'].isin(room_config["sublocation"]))]
                    else:
                        room_animals = inventory_df[(inventory_df['Location'] == location) & (inventory_df['SubLocation'].isin(room_config["sublocation"]))]
                else:
                    if isinstance(location, list):
                        room_animals = inventory_df[(inventory_df['Location'].isin(location)) & (inventory_df['SubLocation'] == room_config["sublocation"])]
                    else:
                        room_animals = inventory_df[(inventory_df['Location'] == location) & (inventory_df['SubLocation'] == room_config["sublocation"])]
            else:
                if isinstance(location, list):
                    room_animals = inventory_df[inventory_df['Location'].isin(location)]
                else:
                    room_animals = inventory_df[inventory_df['Location'] == location]
        else:
            # Handle dynamically added rooms
            room_animals = inventory_df[inventory_df['Location'] == current_room]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if not room_animals.empty and 'Stage' in room_animals.columns:
                ready_count = len(room_animals[room_animals['Stage'].str.contains('Available', na=False)])
            else:
                ready_count = 0
            st.metric("Ready", ready_count)
        with col2:
            if not room_animals.empty and 'Stage' in room_animals.columns:
                hold_count = len(room_animals[room_animals['Stage'].str.contains('Hold', na=False)])
            else:
                hold_count = 0
            st.metric("On Hold", hold_count)
        with col3:
            total_count = len(room_animals)
            st.metric("Total", total_count)
        with col4:
            if not room_animals.empty and 'LOSInDays' in room_animals.columns:
                avg_los = room_animals['LOSInDays'].mean()
            else:
                avg_los = 0
            st.metric("Avg LOS", f"{avg_los:.1f}d")
    
    with tab2:
        # Room Layout Builder
        st.markdown("### 🏗️ Room Layout Builder")
        st.markdown("Select a room to edit its layout:")
        
        builder_room = st.selectbox("Select Room to Edit:", available_rooms, key="builder_room")
        
        if st.button("Edit Layout", key="edit_layout"):
            st.session_state.edit_mode = builder_room
            st.rerun()
        
        if st.session_state.get('edit_mode'):
            st.markdown(f"### Editing: {st.session_state.edit_mode}")
            st.info("Layout editing functionality will be added here. For now, layouts are predefined based on RoundsMapp.")
            
            if st.button("Save Layout", key="save_layout"):
                st.success("Layout saved!")
                st.session_state.edit_mode = None
                st.rerun()
            
            if st.button("Cancel", key="cancel_edit"):
                st.session_state.edit_mode = None
                st.rerun()
    
    with tab3:
        # Analytics
        st.markdown("### 📊 Analytics")
        
        # Overall stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_animals = len(inventory_df)
            st.metric("Total Animals", total_animals)
        with col2:
            ready_count = len(inventory_df[inventory_df['Stage'].str.contains('Available', na=False)])
            st.metric("Available", ready_count)
        with col3:
            hold_count = len(inventory_df[inventory_df['Stage'].str.contains('Hold', na=False)])
            st.metric("On Hold", hold_count)
        with col4:
            avg_los = inventory_df['LOSInDays'].mean() if 'LOSInDays' in inventory_df.columns else 0
            st.metric("Avg LOS", f"{avg_los:.1f}d")
        
        # Species breakdown
        st.markdown("#### Species Breakdown")
        species_counts = inventory_df['Species'].value_counts()
        st.bar_chart(species_counts)
        
        # Location occupancy
        st.markdown("#### Location Occupancy")
        location_counts = inventory_df['Location'].value_counts()
        st.bar_chart(location_counts)

if __name__ == "__main__":
    main()