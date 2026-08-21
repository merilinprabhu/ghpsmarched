import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TextbookDistribution.html', 'r', encoding='utf-8') as f:
    tb_code = f.read()

target_pattern = r'function renderActiveTextbookView\(\)[\s\S]*?async function autoSaveRecord\(studentId\)'

replacement = """function renderActiveTextbookView() {
      const tableEl = document.getElementById('textbook-table-container');
      const cardsEl = document.getElementById('textbook-cards-container');

      // Always render both so that DOM elements exist for auto-saving and print drawers
      renderTextbookCards(currentTextbookStudents, currentTextbookRecordsMap);
      renderTextbookTable(currentTextbookStudents, currentTextbookRecordsMap);

      if (currentTextbookViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) cardsEl.classList.remove('hidden');
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) tableEl.classList.remove('hidden');
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
                  ${isBoy ? '👦 ಬಾಲಕ' : '👧扩大'}
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
              <span id="card-tb-count-${s.id}" class="text-[10px] font-bold ${allReceived ? 'text-emerald-400' : (receivedCount > 0 ? 'text-amber-400' : 'text-slate-400')}">
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
      let isChecked = false;
      if (chk) {
        chk.checked = !chk.checked;
        isChecked = chk.checked;
      }
      
      const btn = document.getElementById(`card-tb-${studentId}-${bookIdx}`);
      if (btn) {
        const spanTitle = btn.querySelector('span');
        const titleText = spanTitle ? spanTitle.innerText : 'Book';
        if (isChecked) {
          btn.className = "p-2 rounded-xl text-left transition cursor-pointer flex items-center justify-between gap-1.5 border-0 bg-emerald-600 text-white shadow-xs";
          btn.innerHTML = `<span class="text-[10.5px] font-bold truncate max-w-[130px]">${titleText}</span><span class="font-black text-xs">✓</span>`;
        } else {
          btn.className = "p-2 rounded-xl text-left transition cursor-pointer flex items-center justify-between gap-1.5 border-0 bg-black/50 text-slate-400 border border-white/10";
          btn.innerHTML = `<span class="text-[10.5px] font-bold truncate max-w-[130px]">${titleText}</span><span class="font-black text-xs">✗</span>`;
        }
      }
      autoSaveRecord(studentId);
    }

    function renderTextbookTable(students, recordsMap) {
      const tbody = document.getElementById('distributionTableBody');
      if (!tbody) return;
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
              <input type="checkbox" id="book-${s.id}-${bIdx}" onchange="handleTableBookChange('${s.id}', ${bIdx}, this.checked)" ${isDist ? 'checked' : ''} class="w-4 h-4 rounded text-indigo-650 bg-black border-white/10 cursor-pointer">
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

    function handleTableBookChange(studentId, bookIdx, isChecked) {
      const btn = document.getElementById(`card-tb-${studentId}-${bookIdx}`);
      if (btn) {
        const spanTitle = btn.querySelector('span');
        const titleText = spanTitle ? spanTitle.innerText : 'Book';
        if (isChecked) {
          btn.className = "p-2 rounded-xl text-left transition cursor-pointer flex items-center justify-between gap-1.5 border-0 bg-emerald-600 text-white shadow-xs";
          btn.innerHTML = `<span class="text-[10.5px] font-bold truncate max-w-[130px]">${titleText}</span><span class="font-black text-xs">✓</span>`;
        } else {
          btn.className = "p-2 rounded-xl text-left transition cursor-pointer flex items-center justify-between gap-1.5 border-0 bg-black/50 text-slate-400 border border-white/10";
          btn.innerHTML = `<span class="text-[10.5px] font-bold truncate max-w-[130px]">${titleText}</span><span class="font-black text-xs">✗</span>`;
        }
      }
      autoSaveRecord(studentId);
    }

    async function autoSaveRecord(studentId)"""

tb_code = re.sub(target_pattern, replacement, tb_code)

with open('TextbookDistribution.html', 'w', encoding='utf-8') as f:
    f.write(tb_code)

print("Synchronized and fixed TextbookDistribution.html card view")
