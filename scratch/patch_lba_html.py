import re, sys

sys.stdout.reconfigure(encoding='utf-8')

# Read full file
with open('LbaAssessment.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect the markup between <div class="flex flex-col gap-4 w-full print-container"> and </section>
pattern = r'<!-- Actions & Edit Control Bar -->[\s\S]*?<!-- Filter Bar -->'

new_toolbar = """<!-- Actions & Edit Control Bar -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-2 bg-slate-50 dark:bg-slate-900 p-3 rounded-2xl border border-slate-200 dark:border-slate-800 no-print text-xs font-semibold">
            <!-- View Mode Switcher -->
            <div class="flex items-center gap-1 p-1 bg-slate-200/70 dark:bg-slate-800 rounded-xl w-fit">
              <button id="btn-view-cards" onclick="setViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
                <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವೀಕ್ಷಣೆ (Cards)</span>
              </button>
              <button id="btn-view-table" onclick="setViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent">
                <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ (Table)</span>
              </button>
            </div>
            
            <!-- Actions -->
            <div class="flex flex-wrap items-center gap-1.5">
              <!-- Edit/Save/Cancel -->
              <button id="btn-edit" onclick="enableEditing()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-3.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition shadow-xs border-0 cursor-pointer hidden">
                <i class="fa-solid fa-pen-to-square"></i> ತಿದ್ದುಪಡಿ / Edit
              </button>
              <button id="btn-save" onclick="saveData()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition shadow-xs border-0 cursor-pointer hidden">
                <i class="fa-solid fa-floppy-disk"></i> ಉಳಿಸಿ / Save
              </button>
              <button id="btn-cancel" onclick="cancelEditing()" class="bg-slate-200 hover:bg-slate-300 text-slate-700 px-3.5 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition border-0 cursor-pointer hidden">
                <i class="fa-solid fa-xmark"></i> ರದ್ದು / Cancel
              </button>
              
              <span class="border-l border-slate-300 dark:border-slate-700 h-5 mx-0.5"></span>
              
              <!-- Settings -->
              <button onclick="toggleSettingsPanel()" title="ಪಾಠಗಳ ಸೆಟ್ಟಿಂಗ್ಸ್ / Lesson Settings" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition border-0 bg-transparent cursor-pointer">
                <i class="fa-solid fa-gear text-amber-600 text-base"></i>
              </button>
              <!-- Print -->
              <button id="btn-print-report" onclick="triggerPrint()" title="ಮುದ್ರಿಸು / Print" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition border-0 bg-transparent cursor-pointer hidden">
                <i class="fa-solid fa-print text-slate-700 dark:text-slate-300 text-base"></i>
              </button>
              <!-- Excel -->
              <button id="btn-export-excel" onclick="exportToExcel()" title="Excel ರಫ್ತು" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition border-0 bg-transparent cursor-pointer hidden">
                <i class="fa-solid fa-file-excel text-emerald-600 text-base"></i>
              </button>
              <!-- CSV Export -->
              <button id="btn-export-csv" onclick="exportToCSV()" title="CSV ರಫ್ತು" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition border-0 bg-transparent cursor-pointer hidden">
                <i class="fa-solid fa-file-csv text-teal-600 text-base"></i>
              </button>
              <!-- CSV Template -->
              <button onclick="downloadCSVTemplate()" title="CSV ನಮೂನೆ ಡೌನ್‌ಲೋಡ್" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition border-0 bg-transparent cursor-pointer">
                <i class="fa-solid fa-file-arrow-down text-slate-500 text-base"></i>
              </button>
              <!-- CSV Upload -->
              <input type="file" id="csvFileInput" class="hidden" accept=".csv" onchange="handleCSVUpload(event)">
              <button id="btn-import-csv" onclick="document.getElementById('csvFileInput').click()" title="CSV ಆಮದು" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition border-0 bg-transparent cursor-pointer hidden">
                <i class="fa-solid fa-file-import text-blue-600 text-base"></i>
              </button>
            </div>
          </div>

          <!-- Filter Bar -->"""

html = re.sub(pattern, new_toolbar, html)

# Next, add search and filter bar right above table-container and add student-cards-container inside table-container
table_container_old = """            <div class="flex-grow overflow-auto custom-scrollbar relative p-4 bg-white min-h-[350px]" id="table-container">"""

table_container_new = """            <!-- Search & Quick Filter Bar -->
            <div id="search-filter-bar" class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3 bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 hidden no-print">
              <div class="relative flex-1">
                <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                <input type="text" id="search-student-input" oninput="applyFiltersAndRender()" placeholder="ವಿದ್ಯಾರ್ಥಿಯ ಹೆಸರು / STS ಸಂಖ್ಯೆ ಹುಡುಕಿ..." class="w-full pl-8 pr-3 py-2 text-xs bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800 dark:text-slate-100 placeholder-slate-400">
              </div>
              <div class="flex items-center gap-1.5 self-end sm:self-auto">
                <button type="button" onclick="setGenderFilter('')" id="gen-btn-all" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer">ಎಲ್ಲಾ</button>
                <button type="button" onclick="setGenderFilter('Boy')" id="gen-btn-boy" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👦 ಬಾಲಕರು</button>
                <button type="button" onclick="setGenderFilter('Girl')" id="gen-btn-girl" class="px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer">👧 ಬಾಲಕಿಯರು</button>
              </div>
            </div>

            <div class="flex-grow overflow-auto custom-scrollbar relative p-4 bg-white min-h-[350px]" id="table-container">
              <!-- Cards View Container -->
              <div id="student-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>"""

html = html.replace(table_container_old, table_container_new)

with open('LbaAssessment.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated HTML structure for Card View and Toolbar in LbaAssessment.html")
