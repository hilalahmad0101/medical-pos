import os
import shutil
import re

def fix_all_pages():
    base_dir = r"c:\opensource-project\medical_pos"
    files = [f for f in os.listdir(base_dir) if f.endswith(".html")]
    
    link_map = {
        "Dashboard": "dashboard_overview.html",
        "POS": "pos_billing_terminal.html",
        "Inventory": "inventory_management.html",
        "Customers": "customer_list.html",
        "Reports": "refined_invoice_templates.html",
        "Settings": "dashboard_overview.html",
        "New Prescription": "pos_billing_terminal.html",
        "New Sale": "pos_billing_terminal.html",
        "Add Medicine": "add_new_medicine.html",
        "Sales": "refined_invoice_templates.html",
        "Stock": "inventory_management.html",
        "Users": "customer_list.html",
        "Home": "dashboard_overview.html",
        "More": "dashboard_overview.html"
    }

    for filename in files:
        file_path = os.path.join(base_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Update existing <a> tags with href="#" or update links
        for label, target in link_map.items():
            pattern = re.compile(rf'(<a\s+[^>]*href=")([^"]*)("[^>]*>.*?{label}.*?</a>)', re.IGNORECASE | re.DOTALL)
            def repl(m):
                # Only replace if href is # or empty or we want to force it
                if m.group(2) == "#" or m.group(2) == "":
                    return f'{m.group(1)}{target}{m.group(3)}'
                return m.group(0)
            content = pattern.sub(repl, content)

        # 2. Convert div-based menu items to a-based
        for label, target in link_map.items():
             # Pattern for <div ... cursor-pointer ...> ... Label ... </div>
            content = re.sub(
                rf'<div([^>]*class="[^"]*cursor-pointer[^"]*"[^>]*)>\s*(<span[^>]*>.*?</span>\s*<span[^>]*>{label}</span>)\s*</div>',
                rf'<a\1 href="{target}">\2</a>',
                content, flags=re.DOTALL | re.IGNORECASE
            )
            content = re.sub(
                rf'<div([^>]*class="[^"]*cursor-pointer[^"]*"[^>]*)>\s*(<span[^>]*>{label}</span>)\s*</div>',
                rf'<a\1 href="{target}">\2</a>',
                content, flags=re.DOTALL | re.IGNORECASE
            )

        # 3. Handle mobile nav (button instead of a)
        for label, target in link_map.items():
            content = re.sub(
                rf'<button([^>]*class="[^"]*flex flex-col items-center[^"]*"[^>]*)>\s*(<span[^>]*>.*?</span>\s*<span[^>]*>.*?{label}.*?</span>)\s*</button>',
                rf'<a\1 href="{target}">\2</a>',
                content, flags=re.DOTALL | re.IGNORECASE
            )

        # 4. Specific fix for "New Prescription" and "New Sale" buttons
        # Wrap them in <a> if they are buttons
        content = re.sub(
            r'<button([^>]*class="[^"]*bg-primary[^"]*"[^>]*)>\s*(<span[^>]*>.*?</span>\s*New (?:Prescription|Sale))\s*</button>',
            r'<a\1 href="pos_billing_terminal.html" style="display:flex; justify-content:center; align-items:center;">\2</a>',
            content, flags=re.DOTALL | re.IGNORECASE
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Final link fixes completed.")

def cleanup():
    base_dir = r"c:\opensource-project\medical_pos"
    protected = ["screenshot", ".gemini", ".git", "node_modules"]
    subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d not in protected]
    for subdir in subdirs:
        try:
            shutil.rmtree(os.path.join(base_dir, subdir))
            print(f"Removed directory: {subdir}")
        except Exception as e:
            print(f"Error removing {subdir}: {e}")

if __name__ == "__main__":
    fix_all_pages()
    cleanup()
