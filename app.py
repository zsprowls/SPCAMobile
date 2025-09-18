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
    
    /* Kennel container styling */
    .kennel-container {
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 8px;
        margin: 4px;
        background: #f8f9fa;
        min-height: 80px;
    }
    
    .kennel-label {
        font-weight: bold;
        font-size: 0.9rem;
        color: #333;
        margin-bottom: 4px;
    }
    
    .kennel-animal-button {
        width: 100%;
        margin: 2px 0;
        font-size: 0.8rem;
        padding: 4px 8px;
        text-align: left;
    }
    
    /* Red status text in buttons */
    .stButton > button:contains("SX"), .stButton > button:contains("BEHA"), .stButton > button:contains("ADPT") {
        color: #dc3545;
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
    """Map stage to abbreviation"""
    for key in sorted(STATUS_MAP.keys(), key=len, reverse=True):
        abbr = STATUS_MAP[key]
        if stage.lower().startswith(key.lower()):
            return abbr
    if 'evaluate' in stage.lower():
        return STATUS_MAP['Evaluate']
    return ""

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

# Room definitions with correct layouts
ROOM_DEFINITIONS = {
    "Small Animals & Exotics": {
        "location": "Small Animals & Exotics",
        "type": "small_animals"
    },
    "Adoptions Lobby": {
        "location": "Adoptions Lobby", 
        "grid_map": [
            ["Feature Room 1", "Feature Room 2", "Rabbitat 1", "Rabbitat 2"]
        ],
        "grid_cols": 4
    },
    "Condo A": {
        "location": "Cat Adoption Condo Rooms",
        "sublocation": "Condo A",
        "grid_map": [["Condo A"]],
        "grid_cols": 1
    },
    "Condo B": {
        "location": "Cat Adoption Condo Rooms", 
        "sublocation": "Condo B",
        "grid_map": [["Condo B"]],
        "grid_cols": 1
    },
    "Condo C": {
        "location": "Cat Adoption Condo Rooms",
        "sublocation": "Condo C", 
        "grid_map": [["Condo C"]],
        "grid_cols": 1
    },
    "Condo D": {
        "location": "Cat Adoption Condo Rooms",
        "sublocation": "Condo D",
        "grid_map": [["Condo D"]],
        "grid_cols": 1
    },
    "Condo E": {
        "location": "Cat Adoption Condo Rooms",
        "sublocation": "Condo E",
        "grid_map": [["Condo E"]],
        "grid_cols": 1
    },
    "Condo F": {
        "location": "Cat Adoption Condo Rooms",
        "sublocation": "Condo F",
        "grid_map": [["Condo F"]],
        "grid_cols": 1
    },
    "Meet & Greet 109B": {
        "location": "Cat Adoption Condo Rooms",
        "sublocation": ["Room 109-B", "Meet & Greet 109B"],
        "grid_map": [["Meet & Greet 109B"]],
        "grid_cols": 1
    },
    "Cat Condo Rabbitats": {
        "location": "Cat Adoption Condo Rooms",
        "sublocation": ["Rabbitat 1", "Rabbitat 2"],
        "grid_map": [["Rabbitat 1", "Rabbitat 2"]],
        "grid_cols": 2
    },
    "Cat Adoption Room G": {
        "location": "Cat Adoption Room G",
        "grid_map": [
            [None, "03", "06"],
            ["01", "04", "07"],
            ["02", "05", "08"]
        ],
        "grid_cols": 3
    },
    "Cat Adoption Room H": {
        "location": "Cat Adoption Room H",
        "grid_map": [
            ["01", "04", None],
            ["02", "05", "07"],
            ["03", "06", "08"]
        ],
        "grid_cols": 3
    },
    "Cat Behavior Room I": {
        "location": "Cat Behavior Room I",
        "grid_map": [
            [None, "03", "06"],
            ["01", "04", "07"],
            ["02", "05", "08"]
        ],
        "grid_cols": 3
    },
    "Dog Adoptions A": {
        "location": "Dog Adoptions A",
        "grid_map": [["A"]],
        "grid_cols": 1
    },
    "Dog Adoptions B": {
        "location": "Dog Adoptions B", 
        "grid_map": [["B"]],
        "grid_cols": 1
    },
    "Dog Adoptions C": {
        "location": "Dog Adoptions C",
        "grid_map": [["C"]],
        "grid_cols": 1
    },
    "Dog Adoptions D": {
        "location": "Dog Adoptions D",
        "grid_map": [["D"]],
        "grid_cols": 1
    },
    "Foster Care Room": {
        "location": "Foster Care Room",
        "grid_map": [
            ["01", "02", "03", "04"],
            ["05", "06", "07", "08"]
        ],
        "grid_cols": 4
    }
}

def render_small_animals_layout(animals_df, memo_df):
    """Render Small Animals & Exotics layout exactly like RoundsMapp"""
    
    sa_df = animals_df[animals_df['Location'] == 'Small Animals & Exotics'].copy()
    
    # Birds section
    st.markdown("### Birds")
    bird_cages = ["Bird Cage 1", "Bird Cage 2", "Bird Cage 3", "Bird Cage 4"]
    bird_extra = "Bird Cage EXTRA"
    
    # Create bird kennels with proper grid layout
    cols = st.columns(2)
    
    # Bird cages 1-4 (single width)
    for i, cage in enumerate(bird_cages):
        with cols[i % 2]:
            cell_animals = sa_df[sa_df["SubLocation"] == cage]
            if not cell_animals.empty:
                for idx, (_, animal) in enumerate(cell_animals.iterrows()):
                    button_text = create_button_text(str(i+1), animal)
                    if st.button(button_text, key=f"bird_{cage}_{idx}"):
                        st.session_state.selected_animal = animal
                        st.session_state.show_modal = True
                        st.rerun()
            else:
                button_text = create_button_text(str(i+1), None, is_empty=True)
                st.button(button_text, key=f"bird_{cage}_empty", disabled=True)
    
    # Bird Extra (spans both columns)
    with cols[0]:
        cell_animals = sa_df[sa_df["SubLocation"] == bird_extra]
        if not cell_animals.empty:
            for idx, (_, animal) in enumerate(cell_animals.iterrows()):
                button_text = create_button_text("EXTRA", animal)
                if st.button(button_text, key=f"bird_{bird_extra}_{idx}"):
                    st.session_state.selected_animal = animal
                    st.session_state.show_modal = True
                    st.rerun()
        else:
            button_text = create_button_text("EXTRA", None, is_empty=True)
            st.button(button_text, key=f"bird_{bird_extra}_empty", disabled=True)
    
    # Small Animals section
    st.markdown("### Small Animals")
    sa_cages = [f"Small Animal {i}" for i in range(1,9)]
    
    # 3x3 grid for small animals
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            if row * 3 + col < len(sa_cages):
                cage = sa_cages[row * 3 + col]
                with cols[col]:
                    cell_animals = sa_df[sa_df["SubLocation"] == cage]
                    if not cell_animals.empty:
                        for idx, (_, animal) in enumerate(cell_animals.iterrows()):
                            button_text = create_button_text(str(row * 3 + col + 1), animal)
                            if st.button(button_text, key=f"sa_{cage}_{idx}"):
                                st.session_state.selected_animal = animal
                                st.session_state.show_modal = True
                                st.rerun()
                    else:
                        button_text = create_button_text(str(row * 3 + col + 1), None, is_empty=True)
                        st.button(button_text, key=f"sa_{cage}_empty", disabled=True)
    
    # Mammals section
    st.markdown("### Mammals")
    mammal_cages = [f"Mammal {i}" for i in range(1,5)]
    
    cols = st.columns(2)
    for i, cage in enumerate(mammal_cages):
        with cols[i % 2]:
            cell_animals = sa_df[sa_df["SubLocation"] == cage]
            if not cell_animals.empty:
                for idx, (_, animal) in enumerate(cell_animals.iterrows()):
                    button_text = create_button_text(str(i+1), animal)
                    if st.button(button_text, key=f"mammal_{cage}_{idx}"):
                        st.session_state.selected_animal = animal
                        st.session_state.show_modal = True
                        st.rerun()
            else:
                button_text = create_button_text(str(i+1), None, is_empty=True)
                st.button(button_text, key=f"mammal_{cage}_empty", disabled=True)
    
    # Reptiles section
    st.markdown("### Reptiles")
    reptile_cages = [f"Reptile {i}" for i in range(1,6)]
    
    # 2x3 grid for reptiles
    for row in range(2):
        cols = st.columns(2)
        for col in range(2):
            if row * 2 + col < 4:  # First 4 reptiles
                cage = reptile_cages[row * 2 + col]
                with cols[col]:
                    cell_animals = sa_df[sa_df["SubLocation"] == cage]
                    if not cell_animals.empty:
                        for idx, (_, animal) in enumerate(cell_animals.iterrows()):
                            button_text = create_button_text(str(row * 2 + col + 1), animal)
                            if st.button(button_text, key=f"reptile_{cage}_{idx}"):
                                st.session_state.selected_animal = animal
                                st.session_state.show_modal = True
                                st.rerun()
                    else:
                        button_text = create_button_text(str(row * 2 + col + 1), None, is_empty=True)
                        st.button(button_text, key=f"reptile_{cage}_empty", disabled=True)
    
    # Reptile 5 (spans both columns)
    cage = reptile_cages[4]  # Reptile 5
    cell_animals = sa_df[sa_df["SubLocation"] == cage]
    if not cell_animals.empty:
        for idx, (_, animal) in enumerate(cell_animals.iterrows()):
            button_text = create_button_text("5", animal)
            if st.button(button_text, key=f"reptile_5_{idx}"):
                st.session_state.selected_animal = animal
                st.session_state.show_modal = True
                st.rerun()
    else:
        button_text = create_button_text("5", None, is_empty=True)
        st.button(button_text, key="reptile_5_empty", disabled=True)
    
    # Countertop Cages section
    st.markdown("### Countertop Cages")
    counter_cages = [f"Countertop Cage {i}" for i in range(1,3)]
    
    cols = st.columns(2)
    for i, cage in enumerate(counter_cages):
        with cols[i]:
            cell_animals = sa_df[sa_df["SubLocation"] == cage]
            if not cell_animals.empty:
                for idx, (_, animal) in enumerate(cell_animals.iterrows()):
                    button_text = create_button_text(str(i+1), animal)
                    if st.button(button_text, key=f"counter_{cage}_{idx}"):
                        st.session_state.selected_animal = animal
                        st.session_state.show_modal = True
                        st.rerun()
            else:
                button_text = create_button_text(str(i+1), None, is_empty=True)
                st.button(button_text, key=f"counter_{cage}_empty", disabled=True)
    
    # Show animals not assigned to kennels
    all_sublocations = bird_cages + [bird_extra] + sa_cages + [f"Mammal {i}" for i in range(1,5)] + reptile_cages + [f"Countertop Cage {i}" for i in range(1,3)]
    unassigned = sa_df[~sa_df['SubLocation'].isin(all_sublocations)]
    if not unassigned.empty:
        st.markdown("### Animals Not in Kennel Spaces")
        for _, animal in unassigned.iterrows():
            button_text = create_button_text("•", animal)
            if st.button(button_text, key=f"unassigned_{animal['AnimalNumber']}"):
                st.session_state.selected_animal = animal
                st.session_state.show_modal = True
                st.rerun()

def render_room_layout(room_name, animals_df, memo_df):
    """Render a room layout with consistent button sizing"""
    
    if room_name not in ROOM_DEFINITIONS:
        st.error(f"Room {room_name} not defined")
        return
    
    room_config = ROOM_DEFINITIONS[room_name]
    
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
    else:
        room_animals = animals_df[animals_df['Location'] == location].copy()
    
    # Ensure SubLocation is zero-padded string for numeric sublocations
    if room_name in ["Cat Adoption Room G", "Cat Adoption Room H", "Cat Behavior Room I", "Foster Care Room"]:
        room_animals["SubLocation"] = room_animals["SubLocation"].astype(str).str.zfill(2)
    
    # Create mapping of sublocation to animals
    sublocation_to_animals = {}
    for _, animal in room_animals.iterrows():
        subloc = animal.get('SubLocation', '')
        if pd.notna(subloc) and subloc != '':
            if subloc not in sublocation_to_animals:
                sublocation_to_animals[subloc] = []
            sublocation_to_animals[subloc].append(animal)
    
    st.markdown(f"### {room_name}")
    
    # Create grid layout using Streamlit columns with HTML-like styling
    for row_idx, row in enumerate(grid_map):
        cols = st.columns(grid_cols, gap="small")
        for col_idx, subloc in enumerate(row):
            if subloc is None:
                with cols[col_idx]:
                    st.write("")  # Empty space
            else:
                with cols[col_idx]:
                    animals = sublocation_to_animals.get(subloc, [])
                    
                    # Convert subloc to display number for numeric sublocations
                    display_label = subloc
                    if subloc.isdigit():
                        display_label = str(int(subloc))
                    
                    # Create a container that looks like a kennel box
                    st.markdown(f'<div class="kennel-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="kennel-label">{display_label}</div>', unsafe_allow_html=True)
                    
                    if animals:
                        # Show all animals in this kennel as clickable buttons
                        for idx, animal in enumerate(animals):
                            name = str(animal.get('AnimalName', 'Unknown'))
                            if pd.isna(name) or name.lower() == 'nan':
                                name = str(animal.get('AnimalNumber', 'Unknown'))
                            
                            # Get status abbreviation
                            stage = str(animal.get('Stage', ''))
                            abbr = map_status(stage)
                            
                            # Create display text with red status if present
                            if abbr:
                                display_text = f'{name} <span style="color: #dc3545; font-weight: bold;">{abbr}</span>'
                            else:
                                display_text = name
                            
                            if st.button(display_text, key=f"kennel_{room_name}_{subloc}_{idx}"):
                                st.session_state.selected_animal = animal
                                st.session_state.show_modal = True
                                st.rerun()
                    else:
                        # Empty kennel
                        st.button("-", key=f"kennel_{room_name}_{subloc}_empty", disabled=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
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

def render_animal_modal(animal, memo_df):
    """Render animal details modal with swipe functionality for multiple animals"""
    st.markdown("---")
    st.markdown("### Animal Details")
    
    # Close button
    if st.button("✕ Close", key="close_modal"):
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
    
    # Define room order
    room_order = [
        "Small Animals & Exotics",
        "Adoptions Lobby", 
        "Condo A", "Condo B", "Condo C", "Condo D", "Condo E", "Condo F",
        "Meet & Greet 109B",
        "Cat Condo Rabbitats",
        "Cat Adoption Room G", "Cat Adoption Room H", "Cat Behavior Room I",
        "Foster Care Room",
        "Dog Adoptions A", "Dog Adoptions B", "Dog Adoptions C", "Dog Adoptions D"
    ]
    
    # Get available rooms in the specified order
    available_rooms = []
    for room_name in room_order:
        if room_name in ROOM_DEFINITIONS:
            room_config = ROOM_DEFINITIONS[room_name]
            location = room_config["location"]
            
            if room_config.get("type") == "small_animals":
                room_animals = inventory_df[inventory_df['Location'] == location]
            elif "sublocation" in room_config:
                if isinstance(room_config["sublocation"], list):
                    room_animals = inventory_df[(inventory_df['Location'] == location) & (inventory_df['SubLocation'].isin(room_config["sublocation"]))]
                else:
                    room_animals = inventory_df[(inventory_df['Location'] == location) & (inventory_df['SubLocation'] == room_config["sublocation"])]
            else:
                room_animals = inventory_df[inventory_df['Location'] == location]
            
            if not room_animals.empty:
                available_rooms.append(room_name)
    
    if not available_rooms:
        st.error("No data found for the target rooms.")
        return
    
    # Add tabs for different views
    tab1, tab2, tab3 = st.tabs(["🏠 Room View", "🏗️ Layout Builder", "📊 Analytics"])
    
    with tab1:
        # Room navigation
        current_room = available_rooms[st.session_state.current_room]
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous", key="prev_room"):
                st.session_state.current_room = (st.session_state.current_room - 1) % len(available_rooms)
                st.rerun()
        
        with col2:
            st.markdown(f"### {current_room}")
            st.markdown(f"**Room {st.session_state.current_room + 1} of {len(available_rooms)}**")
        
        with col3:
            if st.button("Next ➡️", key="next_room"):
                st.session_state.current_room = (st.session_state.current_room + 1) % len(available_rooms)
                st.rerun()
        
        # Room selector
        selected_room = st.selectbox("Or select room directly:", available_rooms, index=st.session_state.current_room, key="room_selector")
        if selected_room != current_room:
            st.session_state.current_room = available_rooms.index(selected_room)
            st.rerun()
        
        # Render current room
        render_room_layout(current_room, inventory_df, memo_df)
        
        # Show room statistics
        room_config = ROOM_DEFINITIONS[current_room]
        location = room_config["location"]
        
        if room_config.get("type") == "small_animals":
            room_animals = inventory_df[inventory_df['Location'] == location]
        elif "sublocation" in room_config:
            if isinstance(room_config["sublocation"], list):
                room_animals = inventory_df[(inventory_df['Location'] == location) & (inventory_df['SubLocation'].isin(room_config["sublocation"]))]
            else:
                room_animals = inventory_df[(inventory_df['Location'] == location) & (inventory_df['SubLocation'] == room_config["sublocation"])]
        else:
            room_animals = inventory_df[inventory_df['Location'] == location]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            ready_count = len(room_animals[room_animals['Stage'].str.contains('Available', na=False)])
            st.metric("Ready", ready_count)
        with col2:
            hold_count = len(room_animals[room_animals['Stage'].str.contains('Hold', na=False)])
            st.metric("On Hold", hold_count)
        with col3:
            total_count = len(room_animals)
            st.metric("Total", total_count)
        with col4:
            avg_los = room_animals['LOSInDays'].mean() if 'LOSInDays' in room_animals.columns else 0
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