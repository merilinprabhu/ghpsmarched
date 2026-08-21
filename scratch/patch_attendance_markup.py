import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance.html', 'r', encoding='utf-8') as f:
    att_code = f.read()

# 1. Add view mode switcher & cards container in tab-content-entry
# Let's find #daily-batch-actions
old_actions = """          <!-- Batch Actions for Daily Attendance -->
          <div id="daily-batch-actions" class="flex flex-wrap items-center gap-2 text-[10px] font-bold">"""

new_actions = """          <!-- View Mode Switcher -->
          <div class="flex items-center gap-1 p-1 bg-slate-200/70 dark:bg-slate-800 rounded-xl w-fit">
            <button type="button" id="btn-att-view-cards" onclick="setAttViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
              <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವ್ಯೂ</span>
            </button>
            <button type="button" id="btn-att-view-table" onclick="setAttViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent">
              <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ</span>
            </button>
          </div>

          <!-- Batch Actions for Daily Attendance -->
          <div id="daily-batch-actions" class="flex flex-wrap items-center gap-2 text-[10px] font-bold">"""

att_code = att_code.replace(old_actions, new_actions, 1)

# Add search/filter bar and student-cards-container above entry-grid-container
old_grid_container = """        <div id="entry-grid-container" class="hidden sticky-table-container border border-slate-200/80 dark:border-slate-800 rounded-2xl custom-scrollbar shadow-inner bg-slate-50/20">"""

new_grid_container = """        <!-- Search & Filter Bar for Entry -->
        <div id="att-search-filter-bar" class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3 bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-800 rounded-2xl hidden no-print">
          <div class="relative flex-1">
            <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
            <input type="text" id="att-search-input" oninput="applyAttFiltersAndRender()" placeholder="ವಿದ್ಯಾರ್ಥಿಯ ಹೆಸರು / STS ಹುಡುಕಿ..." class="w-full pl-8 pr-3 py-2 text-xs bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800 dark:text-slate-100 placeholder-slate-400">
          </div>
          <div class="flex items-center gap-1.5 self-end sm:self-auto">
            <button type="button" onclick="setAttGenderFilter('')" id="att-gen-all" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer">ಎಲ್ಲಾ</button>
            <button type="button" onclick="setAttGenderFilter('Boy')" id="att-gen-boy" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👦 ಬಾಲಕರು</button>
            <button type="button" onclick="setAttGenderFilter('Girl')" id="att-gen-girl" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👧 ಬಾಲಕಿಯರು</button>
          </div>
        </div>

        <!-- Mobile Cards View for Attendance -->
        <div id="att-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>

        <div id="entry-grid-container" class="hidden sticky-table-container border border-slate-200/80 dark:border-slate-800 rounded-2xl custom-scrollbar shadow-inner bg-slate-50/20">"""

att_code = att_code.replace(old_grid_container, new_grid_container, 1)

# Now add JavaScript functions for attendance card view
js_insert_target = "    let isSupabaseAttendanceAvailable = true;"
js_insert_code = """    let isSupabaseAttendanceAvailable = true;
    let currentAttViewMode = localStorage.getItem('attendance_view_mode') || 'cards';
    let attGenderFilter = '';
    let attSearchQuery = '';
    let currentLoadedStudents = [];"""

att_code = att_code.replace(js_insert_target, js_insert_code, 1)

with open('Attendance.html', 'w', encoding='utf-8') as f:
    f.write(att_code)

print("Updated Attendance.html markup for Cards View")
