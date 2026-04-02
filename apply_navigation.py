import os
import re

def apply_navigation():
    base_dir = r"c:\opensource-project\medical_pos"
    
    # Define our consistent components
    overlay = '<div id="sidebar-overlay" class="fixed inset-0 bg-black/50 z-40 hidden lg:hidden transition-opacity backdrop-blur-sm"></div>'
    
    sidebar_template = """
<aside id="sidebar" class="fixed lg:sticky left-0 top-0 h-screen w-64 bg-slate-100 dark:bg-slate-900 border-none z-50 transform -translate-x-full lg:translate-x-0 transition-transform duration-300 flex flex-col">
<div class="p-6 flex items-center justify-between">
<div>
<h1 class="text-xl font-black text-blue-700 dark:text-blue-500 tracking-tight font-headline">Precision Rx</h1>
<p class="text-[10px] uppercase tracking-[0.2em] text-slate-500 font-bold mt-1">Lead Pharmacist</p>
</div>
<button id="mobile-sidebar-close" class="lg:hidden p-2 text-slate-500 hover:text-blue-600 transition-colors">
<span class="material-symbols-outlined">close</span>
</button>
</div>
<nav class="flex-1 px-3 space-y-1">
<!-- Dashboard -->
<a id="nav-dashboard" class="flex items-center px-4 py-3 text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors rounded-xl group" href="dashboard_overview.html">
<span class="material-symbols-outlined mr-3" data-icon="dashboard">dashboard</span>
<span class="font-inter text-sm font-medium">Dashboard</span>
</a>
<!-- POS -->
<a id="nav-pos" class="flex items-center px-4 py-3 text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors rounded-xl group" href="pos_billing_terminal.html">
<span class="material-symbols-outlined mr-3" data-icon="point_of_sale">point_of_sale</span>
<span class="font-inter text-sm font-medium">POS</span>
</a>
<!-- Inventory -->
<a id="nav-inventory" class="flex items-center px-4 py-3 text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors rounded-xl group" href="inventory_management.html">
<span class="material-symbols-outlined mr-3" data-icon="inventory_2">inventory_2</span>
<span class="font-inter text-sm font-medium">Inventory</span>
</a>
<!-- Customers -->
<a id="nav-customers" class="flex items-center px-4 py-3 text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors rounded-xl group" href="customer_list.html">
<span class="material-symbols-outlined mr-3" data-icon="group">group</span>
<span class="font-inter text-sm font-medium">Customers</span>
</a>
<!-- Reports -->
<a id="nav-reports" class="flex items-center px-4 py-3 text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors rounded-xl group" href="refined_invoice_templates.html">
<span class="material-symbols-outlined mr-3" data-icon="assessment">assessment</span>
<span class="font-inter text-sm font-medium">Reports</span>
</a>
</nav>
<div class="p-4 mt-auto">
<div class="flex items-center p-3 rounded-xl bg-white/50 dark:bg-slate-800/50">
<img class="w-10 h-10 rounded-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuD5AId7SvtNsigOTVepQ0GLyv16GHLBa0N1BiVn6q8PK6ImiPcOYuK90ZYZc707Tl-J9st8uo1JuV_G8WShO7qzOTQZ2QVQfuufsSV1MoQS-h2PkcHcXZqXjXlOyQmZUaubuTr4JbAWovgNUgeYSMn073MJJ3KjMds5xSTwGepjblmIhgXuVSLKsPH2KouQcFSfmemy0I14Js8NXVNZkywKsTU1qsuoV_ugKysChJsECd5i7-cA3CyTrOApQt-1x6vNyjIx2vz684c"/>
<div class="ml-3 overflow-hidden">
<p class="text-xs font-bold text-slate-900 dark:text-white truncate">Pharmacist Profile</p>
<p class="text-[10px] text-slate-500 truncate">Lead Administrator</p>
</div>
</div>
</div>
</aside>
"""

    navbar = """
<header class="flex items-center justify-between px-6 w-full h-16 sticky top-0 z-40 bg-white/80 dark:bg-slate-950/80 backdrop-blur-md border-b border-slate-200/50 dark:border-slate-800/50">
<div class="flex items-center gap-4 flex-1">
<button id="mobile-menu-open" class="lg:hidden p-2 -ml-2 text-slate-600 dark:text-slate-400 hover:text-blue-600 transition-colors">
<span class="material-symbols-outlined">menu</span>
</button>
<div class="relative w-full max-w-xl group hidden md:block">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-sm" data-icon="search">search</span>
<input class="w-full bg-surface-container-high border-none rounded-xl pl-10 pr-4 py-2 text-sm focus:ring-2 focus:ring-primary/20 transition-all outline-none" placeholder="Search medications, batch no, or category..." type="text"/>
</div>
</div>
<div class="flex items-center gap-4">
<button class="text-slate-600 dark:text-slate-400 hover:text-blue-600 transition-opacity p-2">
<span class="material-symbols-outlined" data-icon="notifications">notifications</span>
</button>
<button class="text-slate-600 dark:text-slate-400 hover:text-blue-600 transition-opacity p-2">
<span class="material-symbols-outlined" data-icon="inventory_2">inventory_2</span>
</button>
<button class="text-slate-600 dark:text-slate-400 hover:text-blue-600 transition-opacity p-2">
<span class="material-symbols-outlined" data-icon="history">history</span>
</button>
<div class="h-6 w-[1px] bg-slate-200 dark:bg-slate-800 mx-2"></div>
<button class="bg-primary text-on-primary px-4 py-2 rounded-lg text-sm font-semibold hover:opacity-90 transition-opacity flex items-center gap-2">
<span class="material-symbols-outlined text-sm" data-icon="shopping_cart">shopping_cart</span>
Complete Sale
</button>
</div>
</header>
"""

    js_logic = """
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        const openBtn = document.getElementById('mobile-menu-open');
        const closeBtn = document.getElementById('mobile-sidebar-close');

        const toggleSidebar = () => {
            sidebar.classList.toggle('-translate-x-full');
            overlay.classList.toggle('hidden');
            document.body.classList.toggle('overflow-hidden');
        };

        if (openBtn) openBtn.addEventListener('click', toggleSidebar);
        if (closeBtn) closeBtn.addEventListener('click', toggleSidebar);
        if (overlay) overlay.addEventListener('click', toggleSidebar);
    });
</script>
"""

    active_map = {
        "dashboard_overview.html": "nav-dashboard",
        "pos_billing_terminal.html": "nav-pos",
        "inventory_management.html": "nav-inventory",
        "customer_list.html": "nav-customers",
        "refined_invoice_templates.html": "nav-reports",
        "add_new_customer.html": "nav-customers",
        "add_new_medicine.html": "nav-inventory",
        "edit_customer_profile.html": "nav-customers",
        "edit_medicine.html": "nav-inventory",
        "invoice_templates_thermal_a4.html": "nav-reports",
        "barcode_generator.html": "nav-inventory",
        "stock_adjustment.html": "nav-inventory"
    }

    files = [f for f in os.listdir(base_dir) if f.endswith(".html")]

    for filename in files:
        file_path = os.path.join(base_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Clean-up old stuff
        content = re.sub(r'<div id="sidebar-overlay".*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<aside id="sidebar".*?</aside>', '', content, flags=re.DOTALL)
        content = re.sub(r'<header.*?</header>', '', content, flags=re.DOTALL)
        content = re.sub(r'<script>.*?sidebar\.classList\.toggle\(.-translate-x-full.\).*?</script>', '', content, flags=re.DOTALL)
        content = content.replace('<div class="flex-1 flex flex-col min-w-0">', '')
        content = re.sub(r'</main>\s*</div>', '</main>', content)

        # Body flex
        content = re.sub(r'(<body[^>]*class=")([^"]*)(")', lambda m: f'{m.group(1)}flex {m.group(2).replace("flex ", "").strip()}{m.group(3)}', content)

        # Prepare Sidebar with Active State
        current_sidebar = sidebar_template
        active_id = active_map.get(filename)
        if active_id:
            active_class = 'text-blue-700 dark:text-blue-400 font-bold border-r-4 border-blue-600 bg-blue-50/50 dark:bg-blue-900/20 translate-x-1 transition-transform rounded-l-xl'
            # Replace class for active id
            current_sidebar = current_sidebar.replace(f'id="{active_id}" class="flex items-center px-4 py-3 text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors rounded-xl group"', 
                                                       f'id="{active_id}" class="flex items-center px-4 py-3 {active_class}"')
            # Add Fill to icon
            pattern = rf'(id="{active_id}"[^>]*>.*?<span[^>]*data-icon="[^"]*")'
            current_sidebar = re.sub(pattern, r'\1 style="font-variation-settings: \'FILL\' 1;"', current_sidebar, flags=re.DOTALL)

        # Re-assemble
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + overlay + '\n' + current_sidebar, content)
        
        # Wrap main
        if '<main' in content:
            content = re.sub(r'(<main)', r'<div class="flex-1 flex flex-col min-w-0">\n' + navbar + r'\n\1', content)
            content = re.sub(r'(</main>)', r'\1\n</div>', content)
            content = re.sub(r'<main([^>]*)class="([^"]*)"', r'<main\1class="flex-1 min-w-0 pt-4 pb-20 lg:pb-8 min-h-screen overflow-y-auto"', content)
        
        # Bottom nav correction (if it exists)
        # Some files have fixed bottom nav, we should keep them but maybe update links?
        # For now let's just add the JS
        content = content.replace('</body>', js_logic + '\n</body>')

        # Formatting
        content = re.sub(r'\n\s*\n+', '\n', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Final Precision Navigation applied to all modules.")

if __name__ == "__main__":
    apply_navigation()
