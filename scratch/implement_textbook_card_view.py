import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TextbookDistribution.html', 'r', encoding='utf-8') as f:
    tb_code = f.read()

# Add view switcher into export buttons area
export_old = """        <!-- Export Buttons / Bulk Action -->
        <div class="flex gap-2 items-center flex-wrap">"""

export_new = """        <!-- Export Buttons / Bulk Action -->
        <div class="flex gap-2 items-center flex-wrap">
          <!-- View Mode Switcher -->
          <div class="flex items-center gap-1 p-1 bg-black/40 border border-white/5 rounded-xl">
            <button type="button" id="btn-tb-cards" onclick="setTextbookViewMode('cards')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0">
              <i class="fa-solid fa-grip-vertical"></i> <span>ಕಾರ್ಡ್ ವ್ಯೂ</span>
            </button>
            <button type="button" id="btn-tb-table" onclick="setTextbookViewMode('table')" class="px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent">
              <i class="fa-solid fa-table-cells"></i> <span>ಕೋಷ್ಟಕ</span>
            </button>
          </div>"""

tb_code = tb_code.replace(export_old, export_new, 1)

# Add cards container right above textbook-table container
table_cont_old = """      <!-- Main entry table -->
      <div class="glass-card rounded-3xl border border-white/5 shadow-xl overflow-hidden">"""

table_cont_new = """      <!-- Mobile Cards View for Textbook -->
      <div id="textbook-cards-container" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden no-print"></div>

      <!-- Main entry table -->
      <div id="textbook-table-container" class="glass-card rounded-3xl border border-white/5 shadow-xl overflow-hidden">"""

tb_code = tb_code.replace(table_cont_old, table_cont_new, 1)

# Add JS state variables
js_state_old = "    let entrySortCol = 'name_english';"
js_state_new = """    let entrySortCol = 'name_english';
    let currentTextbookViewMode = localStorage.getItem('textbook_view_mode') || 'cards';
    let currentTextbookStudents = [];
    let currentTextbookRecordsMap = {};"""

tb_code = tb_code.replace(js_state_old, js_state_new, 1)

# Replace renderTable with dual view engine
render_target = r'function renderTable\(students, recordsMap\)[\s\S]*?async function autoSaveRecord\(studentId\)'

render_replacement = """function setTextbookViewMode(mode, triggerRender = true) {
      currentTextbookViewMode = mode || 'cards';
      localStorage.setItem('textbook_view_mode', currentTextbookViewMode);

      const btnCards = document.getElementById('btn-tb-cards');
      const btnTable = document.getElementById('btn-tb-table');

      if (currentTextbookViewMode === 'cards') {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent';
      } else {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-400 hover:text-white border-0 bg-transparent';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
      }

      if (triggerRender) {
        renderActiveTextbookView();
      }
    }

    function renderActiveTextbookView() {
      const tableEl = document.getElementById('textbook-table-container');
      const cardsEl = document.getElementById('textbook-cards-container');

      if (currentTextbookViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderTextbookCards(currentTextbookStudents, currentTextbookRecordsMap);
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderTextbookTable(currentTextbookStudents, currentTextbookRecordsMap);
        }
      }
    }

    function renderTable(students, recordsMap) {
      currentTextbookStudents = students;
      currentTextbookRecordsMap = recordsMap;
      setTextbookViewMode(currentTextbookViewMode, false);
      renderActiveTextbookView();
    }

    function renderTextbookCards(students, recordsMap) {
      const container = document.getElementById('textbook-cards-container');
      if (!container) return;
      container.innerHTML = '';

      if (students.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold glass-card rounded-2xl border border-white/5"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-500"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      students.forEach((s, idx) => {
        const vals = recordsMap[s.id] || {};
        const cleanClass = normalizeClass(s.enroll_class);
        const books = defaultClassBooks[cleanClass] || [];
        const isGirl = s.gender && (s.gender.toLowerCase().includes('girl') || s.gender.toLowerCase().includes('female') || s.gender.includes('ಹೆಣ್ಣು'));
        const isBoy = !isGirl;

        let booksHtml = '';
        let receivedCount = 0;

        books.forEach((b, bIdx) => {
          const isDist = vals[`book_${bIdx}`] === true || vals[`book_${bIdx}`] === 'true';
          if (isDist) receivedCount++;

          booksHtml += `
            <button type="button" onclick="toggleTextbookItem('${s.id}', ${bIdx})" id="card-tb-${s.id}-${bIdx}" class="p-2 rounded-xl text-left transition cursor-pointer flex items-center justify-between gap-1.5 border-0 ${isDist ? 'bg-emerald-600 text-white shadow-xs' : 'bg-black/50 text-slate-400 border border-white/10'}">
              <span class="text-[10.5px] font-bold truncate max-w-[130px]" title="${b.title}">${b.title}</span>
              <span class="font-black text-xs">${isDist ? '✓' : '✗'}</span>
            </button>
          `;
        });

        const totalBooks = books.length;
        const allReceived = totalBooks > 0 && receivedCount === totalBooks;

        const cardHtml = `
          <div class="glass-card rounded-2xl p-4 border border-white/10 shadow-sm hover:shadow-md transition flex flex-col justify-between space-y-3.5" data-card-tb-id="${s.id}">
            <!-- Header -->
            <div class="flex items-start justify-between gap-2 border-b border-white/10 pb-2.5">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center font-black text-xs ${isBoy ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30' : 'bg-pink-600/20 text-pink-400 border border-pink-500/30'}">
                  ${idx + 1}
                </div>
                <div>
                  <h4 class="text-xs font-black text-white leading-tight">${s.name_english || s.student_name}</h4>
                  ${s.student_name && s.name_english ? `<p class="text-[10px] text-slate-400 font-semibold">${s.student_name}</p>` : ''}
                </div>
              </div>
              <div class="flex flex-col items-end gap-1">
                <span class="px-2 py-0.5 rounded-md text-[10px] font-black ${isBoy ? 'bg-blue-900/40 text-blue-300' : 'bg-pink-900/40 text-pink-300'}">
                  ${isBoy ? '👦 ಬಾಲಕ' : '👧 ಬಾಲಕಿ'}
                </span>
                <span class="text-[10px] font-mono text-slate-400 font-semibold">STS: ${s.app_no || s.id}</span>
              </div>
            </div>

            <!-- Books Grid -->
            <div class="grid grid-cols-2 gap-1.5 pt-1">
              ${booksHtml}
            </div>

            <!-- Footer Save Status -->
            <div class="flex items-center justify-between pt-2 border-t border-white/10 text-xs">
              <span class="text-[10px] font-bold ${allReceived ? 'text-emerald-400' : (receivedCount > 0 ? 'text-amber-400' : 'text-slate-400')}">
                ಪುಸ್ತಕಗಳು: <strong>${receivedCount} / ${totalBooks}</strong> ${allReceived ? '(ಸಂಪೂರ್ಣ)' : ''}
              </span>
              <span id="card-tb-save-status-${s.id}" class="text-[10px] text-emerald-400 font-bold"><i class="fa-solid fa-circle-check"></i> Saved</span>
            </div>
          </div>
        `;
        container.innerHTML += cardHtml;
      });
    }

    function toggleTextbookItem(studentId, bookIdx) {
      const chk = document.getElementById(`book-${studentId}-${bookIdx}`);
      if (chk) {
        chk.checked = !chk.checked;
        const btn = document.getElementById(`card-tb-${studentId}-${bookIdx}`);
        if (btn) {
          if (chk.checked) {
            btn.className = "p-2 rounded-xl text-left transition cursor-pointer flex items-center justify-between gap-1.5 border-0 bg-emerald-600 text-white shadow-xs";
            const spanTitle = btn.querySelector('span');
            btn.innerHTML = `<span class="text-[10.5px] font-bold truncate max-w-[130px]">${spanTitle ? spanTitle.innerText : 'Book'}</span><span class="font-black text-xs">✓</span>`;
          } else {
            btn.className = "p-2 rounded-xl text-left transition cursor-pointer flex items-center justify-between gap-1.5 border-0 bg-black/50 text-slate-400 border border-white/10";
            const spanTitle = btn.querySelector('span');
            btn.innerHTML = `<span class="text-[10.5px] font-bold truncate max-w-[130px]">${spanTitle ? spanTitle.innerText : 'Book'}</span><span class="font-black text-xs">✗</span>`;
          }
        }
        autoSaveRecord(studentId);
      }
    }

    function renderTextbookTable(students, recordsMap) {
      const tbody = document.getElementById('distributionTableBody');
      if (students.length === 0) {
        tbody.innerHTML = `<tr><td colspan="15" class="p-8 text-center text-slate-500 font-semibold bg-slate-50/5"><i class="fa-solid fa-triangle-exclamation mr-1.5"></i> No records match these filters.</td></tr>`;
        return;
      }

      const activeClass = document.getElementById('entryClassFilter').value;
      const cleanClass = normalizeClass(activeClass === "ALL" ? "4" : activeClass);
      const books = defaultClassBooks[cleanClass] || [];

      let html = '';
      students.forEach((s, idx) => {
        const vals = recordsMap[s.id] || {};
        const isGirl = s.gender && (s.gender.toLowerCase().includes('girl') || s.gender.toLowerCase().includes('female') || s.gender.includes('ಹೆಣ್ಣು'));
        const displayGender = isGirl ? 'Girl / ಹೆಣ್ಣು' : 'Boy / ಗಂಡು';

        let bookCells = '';
        books.forEach((b, bIdx) => {
          const isDist = vals[`book_${bIdx}`] === true || vals[`book_${bIdx}`] === 'true';
          bookCells += `
            <td class="p-2 border-r border-white/5 text-center">
              <input type="checkbox" id="book-${s.id}-${bIdx}" onchange="autoSaveRecord('${s.id}')" ${isDist ? 'checked' : ''} class="w-4 h-4 rounded text-indigo-650 bg-black border-white/10 cursor-pointer">
            </td>
          `;
        });

        html += `
          <tr class="hover:bg-slate-50/5 border-b border-white/5 text-slate-300 font-medium">
            <td class="p-2.5 font-bold text-slate-500 text-center">${idx + 1}</td>
            <td class="p-2.5 font-mono text-center">${s.app_no || '-'}</td>
            <td class="p-2.5 text-left text-white">
              <div class="font-bold text-xs">${s.name_english || '-'}</div>
              <div class="text-[9px] text-slate-400">${s.student_name || '-'}</div>
            </td>
            <td class="p-2.5 text-center text-[10px]">${displayGender}</td>
            ${bookCells}
            <td class="p-2.5 no-print" id="status-container-${s.id}">
              <div id="save-indicator-${s.id}" class="text-[10px] text-emerald-400 font-bold flex items-center justify-center gap-1">
                <i class="fa-solid fa-circle-check"></i> Saved
              </div>
            </td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    async function autoSaveRecord(studentId)"""

tb_code = re.sub(render_target, render_replacement, tb_code)

with open('TextbookDistribution.html', 'w', encoding='utf-8') as f:
    f.write(tb_code)

print("Successfully integrated Mobile Card View into TextbookDistribution.html")
