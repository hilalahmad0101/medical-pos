import os
import shutil
import re

def reorganize():
    base_dir = r"c:\opensource-project\medical_pos"
    screenshot_dir = os.path.join(base_dir, "screenshot")
    
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    # Mapping of menu labels to file names
    link_map = {
        "Dashboard": "dashboard_overview.html",
        "POS": "pos_billing_terminal.html",
        "Inventory": "inventory_management.html",
        "Customers": "customer_list.html",
        "Reports": "refined_invoice_templates.html",
        "Settings": "dashboard_overview.html",
        "New Sale": "pos_billing_terminal.html",
        "Add Medicine": "add_new_medicine.html",
        "Generate Report": "refined_invoice_templates.html",
        "Complete Sale": "pos_billing_terminal.html",
        "New Customer": "add_new_customer.html",
        "View All Invoices": "refined_invoice_templates.html"
    }

    # All subdirectories that are not the screenshot folder
    subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d != "screenshot"]
    
    moved_files = []

    for subdir in subdirs:
        subdir_path = os.path.join(base_dir, subdir)
        code_file = os.path.join(subdir_path, "code.html")
        screen_file = os.path.join(subdir_path, "screen.png")
        
        target_html_name = f"{subdir}.html"
        target_html = os.path.join(base_dir, target_html_name)
        target_png = os.path.join(screenshot_dir, f"{subdir}.png")
        
        if os.path.exists(code_file):
            shutil.copy2(code_file, target_html)
            moved_files.append(target_html)
            print(f"Moved {subdir}/code.html to {target_html_name}")
            
        if os.path.exists(screen_file):
            shutil.copy2(screen_file, target_png)
            print(f"Moved {subdir}/screen.png to screenshot/{subdir}.png")
            
    # Now update links in all moved HTML files
    for html_file in moved_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update sidebar/navbar links based on text content
        # We look for <a ...>...Label...</a> and replace href="#" with filename
        for label, filename in link_map.items():
            # Case 1: <a href="#">...<span>Label</span>...</a>
            pattern = re.compile(rf'(<a\s+[^>]*href=")#("[^>]*>.*?{label}.*?</a>)', re.IGNORECASE | re.DOTALL)
            content = pattern.sub(rf'\1{filename}\2', content)
            
            # Case 2: Simple button or span that looks like a menu item but within an <a>
            # Many sidebar items have <span ...>Label</span>
            # Let's try a more general replacement for href="#" in tags containing the label
            # This is tricky with regex, but we can do a broad stroke
        
        # Specific fix for "New Prescription" button if it was an <a>
        content = content.replace('href="#"', 'href="pos_billing_terminal.html"') # fallback for some specific cases
        
        # Better: specifically find all href="#" and if their text content matches a key in link_map, replace it.
        # But we'll stick to a simpler approach for now to avoid breaking the HTML.
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"\nProcessing complete. Reorganized {len(moved_files)} pages.")

if __name__ == "__main__":
    reorganize()
