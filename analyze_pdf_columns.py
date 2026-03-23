"""
Deep analysis of PDF table structure to understand field mapping correctly.
"""
import pdfplumber

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]  # First page
    tables = page.extract_tables()
    
    if tables:
        table = tables[0]
        
        print("DETAILED PDF TABLE STRUCTURE ANALYSIS")
        print("=" * 80)
        print(f"Table dimensions: {len(table)} rows × {len(table[0])} columns\n")
        
        # Analyze header rows
        print("ROW 0 (Main Header):")
        for col_idx, cell in enumerate(table[0][:12]):
            print(f"  Col {col_idx:2d}: {str(cell)[:50] if cell else '(empty)'}")
        
        print("\nROW 1 (Sub-header):")
        for col_idx, cell in enumerate(table[1][:12]):
            print(f"  Col {col_idx:2d}: {str(cell)[:50] if cell else '(empty)'}")
        
        print("\nROW 2 (First data row - Sample):")
        for col_idx, cell in enumerate(table[2][:12]):
            cell_str = str(cell)[:100] if cell else "(empty)"
            if '\n' in cell_str:
                lines = cell_str.split('\n')
                print(f"  Col {col_idx:2d}: {lines[0]}... ({len(cell_str.split(chr(10)))} lines)")
            else:
                print(f"  Col {col_idx:2d}: {cell_str}")
        
        # Analyze column structure
        print("\n" + "=" * 80)
        print("COLUMN STRUCTURE ANALYSIS:")
        print("=" * 80)
        
        # Get all columns from row 1 (headers)
        for col_idx in range(len(table[0])):
            if table[1][col_idx]:
                header = str(table[1][col_idx]).strip()
                print(f"\nColumn {col_idx}: {header[:60]}")
                
                # Show sample from data row
                if col_idx < len(table[2]):
                    sample = table[2][col_idx]
                    if sample:
                        sample_str = str(sample)[:100]
                        lines = sample_str.split('\n')
                        print(f"  Sample data (first item): {lines[0]}")
                        if len(lines) > 1:
                            print(f"  Sample data (second item): {lines[1]}")
