#!/usr/bin/env python3
"""
Script to create missing directory structure for Skydog Sports website
"""

import os
from pathlib import Path

def create_windsurfing_structure():
    """Create missing A-Windsurfing year directories"""
    base = Path('A-Windsurfing')
    years = ['2009', '2010', '2013', '2014', '2015', '2017', '2018']
    
    for year in years:
        year_dir = base / year
        year_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created: {year_dir}")
        
        # Create Don-F subdirectory for 2018
        if year == '2018':
            don_f_dir = year_dir / 'Don-F'
            don_f_dir.mkdir(exist_ok=True)
            print(f"Created: {don_f_dir}")

def create_kayak_structure():
    """Create missing A-kayaks directories"""
    base = Path('A-kayaks')
    missing_dirs = [
        'Kayak-4', 'Kayak-5', 'Kayaks-3',
        '2020 Kilworth', '2021-Kayak'
    ]
    
    for dir_name in missing_dirs:
        dir_path = base / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")

def create_rc_structure():
    """Create missing RC directories"""
    base = Path('RC')
    missing_dirs = [
        '2017-RC', '2017-RC/June-01', '2017-RC/June-04',
        'r-c-2014', 'r-c-2014/16th'
    ]
    
    for dir_name in missing_dirs:
        dir_path = base / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")

def create_snowboard_structure():
    """Create missing A-SNOWBOARD directories"""
    base = Path('A-SNOWBOARD')
    missing_dirs = [
        '01-24-04', '05-3-img', '05-4-img', '05img'
    ]
    
    for dir_name in missing_dirs:
        dir_path = base / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")

def create_bike_structure():
    """Create missing bike directories"""
    base = Path('bike')
    missing_dirs = ['2014', '2015']
    
    for dir_name in missing_dirs:
        dir_path = base / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")

def create_major_missing_dirs():
    """Create the most critical missing directories identified"""
    
    print("=== CREATING MISSING DIRECTORY STRUCTURE ===")
    
    # Change to skydog directory
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    print("\n1. Creating A-Windsurfing year directories...")
    create_windsurfing_structure()
    
    print("\n2. Creating A-kayaks missing directories...")
    create_kayak_structure()
    
    print("\n3. Creating RC missing directories...")
    create_rc_structure()
    
    print("\n4. Creating A-SNOWBOARD missing directories...")
    create_snowboard_structure()
    
    print("\n5. Creating bike missing directories...")
    create_bike_structure()
    
    print("\n=== DIRECTORY CREATION COMPLETED ===")
    print("Note: This creates the most critical missing directories.")
    print("Some images may still need to be moved to appropriate locations.")

if __name__ == "__main__":
    create_major_missing_dirs()