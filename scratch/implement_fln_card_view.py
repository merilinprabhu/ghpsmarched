import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('FlnAssessment.html', 'r', encoding='utf-8') as f:
    fln_code = f.read()

# Replace renderGrid through updateCellGrade
target_pattern = r'function renderGrid\(\)[\s\S]*?function updateTotalsFooter\(\)'

replacement_code = """function setFlnViewMode(mode, triggerRender = true) {
      currentFlnViewMode = mode || 'cards';
      localStorage.setItem('fln_view_mode', currentFlnViewMode);

      const btnCards = document.getElementById('btn-fln-view-cards');
      const btnTable = document.getElementById('btn-fln-view-table');

      if (currentFlnViewMode === 'cards') {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
      } else {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
      }

      if (triggerRender) {
        renderActiveFlnView();
      }
    }

    function setFlnGenderFilter(val) {
      flnGenderFilter = val || '';
      const btnAll = document.getElementById('fln-gen-all');
      const btnBoy = document.getElementById('fln-gen-boy');
      const btnGirl = document.getElementById('fln-gen-girl');

      const activeClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer';
      const inactiveClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer';

      if (btnAll) btnAll.className = flnGenderFilter === '' ? activeClass : inactiveClass;
      if (btnBoy) btnBoy.className = flnGenderFilter === 'Boy' ? activeClass : inactiveClass;
      if (btnGirl) btnGirl.className = flnGenderFilter === 'Girl' ? activeClass : inactiveClass;

      renderActiveFlnView();
    }

    function applyFlnFiltersAndRender() {
      const searchInput = document.getElementById('fln-search-input');
      flnSearchQuery = (searchInput ? searchInput.value : '').toLowerCase().trim();
      renderActiveFlnView();
    }

    function getFilteredFlnStudents() {
      return (students || []).filter(s => {
        if (flnGenderFilter && s.gender !== flnGenderFilter) return false;
        if (flnSearchQuery) {
          const nameEn = (s.name_english || '').toLowerCase();
          const nameKn = (s.student_name || '').toLowerCase();
          const sts = (s.app_no || s.id || '').toLowerCase();
          const father = (s.father_name_az || s.father_name_kn || '').toLowerCase();
          return nameEn.includes(flnSearchQuery) || nameKn.includes(flnSearchQuery) || sts.includes(flnSearchQuery) || father.includes(flnSearchQuery);
        }
        return true;
      });
    }

    function renderActiveFlnView() {
      const tableEl = document.getElementById('grid-table-container');
      const cardsEl = document.getElementById('fln-cards-container');
      const sfBar = document.getElementById('fln-search-filter-bar');

      if (sfBar) sfBar.classList.remove('hidden');

      if (currentFlnViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderFlnCards();
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderGrid();
        }
      }
      updateFlnMetaCounts();
    }

    function updateFlnMetaCounts() {
      let achievedCount = 0;
      let notAchievedCount = 0;

      students.forEach(student => {
        const outcomes = evaluations[student.id] || {};
        let gradedCount = 0;
        let aCount = 0;
        for (let i = 1; i <= TOTAL_COLS_COUNT; i++) {
          const val = outcomes[`col_${i}`] || '';
          if (val) {
            gradedCount++;
            if (val === 'A') aCount++;
          }
        }
        if (gradedCount > 0 && aCount >= (gradedCount * 0.65)) {
          achievedCount++;
        } else {
          notAchievedCount++;
        }
      });

      const className = classFilter.value;
      const dateVal = dateFilter.value;
      const classKn = className === "7" ? "7ನೇ" : (className + "ನೇ");
      const schoolNameKn = localStorage.getItem('school_name_kn') || "ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ ಮರ್ಛೇಡ್";

      const achievedPct = students.length > 0 ? Math.round((achievedCount / students.length) * 100) : 0;
      const notAchievedPct = students.length > 0 ? Math.round((notAchievedCount / students.length) * 100) : 0;

      const wsEl = document.getElementById('web-school-name');
      const wcEl = document.getElementById('web-class-meta');
      const weEl = document.getElementById('web-enrolled-meta');
      const waEl = document.getElementById('web-achieved-meta');
      const wnEl = document.getElementById('web-notachieved-meta');

      if (wsEl) wsEl.innerText = schoolNameKn;
      if (wcEl) wcEl.innerText = classKn;
      if (weEl) weEl.innerText = students.length;
      if (waEl) waEl.innerText = `${achievedCount} (${achievedPct}%)`;
      if (wnEl) wnEl.innerText = `${notAchievedCount} (${notAchievedPct}%)`;

      updateTotalsFooter();
    }

    function renderFlnCards() {
      const container = document.getElementById('fln-cards-container');
      if (!container) return;
      container.innerHTML = '';

      const filtered = getFilteredFlnStudents();
      if (filtered.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-300"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      const allCols = [...KANNADA_COLS.map((c, i) => ({ key: `col_${i+1}`, label: `ಕನ್ನಡ ${c.sub}`, full: `ಕನ್ನಡ - ${c.desc}` })),
                       ...MATH_COLS.map((c, i) => ({ key: `col_${i+10}`, label: `ಗಣಿತ ${c.sub}`, full: `ಗಣಿತ - ${c.desc}` }))];

      filtered.forEach((student, index) => {
        const sId = student.id;
        if (!evaluations[sId]) evaluations[sId] = {};
        const outcomes = evaluations[sId];
        const isBoy = student.gender === 'Boy';
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();

        let colsHtml = '';
        allCols.forEach(col => {
          const val = outcomes[col.key] || '';
          colsHtml += `
            <div class="p-2 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 space-y-1.5">
              <div class="flex items-center justify-between text-[11px] font-bold text-slate-700 dark:text-slate-200">
                <span class="truncate max-w-[130px]" title="${col.full}">${col.label}</span>
                <span id="fln-card-badge-${sId}-${col.key}" class="font-mono font-black text-xs ${getFlnBadgeColor(val)}">${val || '-'}</span>
              </div>
              <div class="grid grid-cols-4 gap-1">
                ${['BB', 'B', 'P', 'A'].map(lvl => `
                  <button type="button" onclick="setFlnCardLevel('${sId}', '${col.key}', '${lvl}')" id="fln-btn-${sId}-${col.key}-${lvl}" class="py-1 rounded-lg text-[10px] font-black transition cursor-pointer border-0 ${val === lvl ? getFlnActiveBtnColor(lvl) : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">${lvl}</button>
                `).join('')}
              </div>
            </div>
          `;
        });

        // Achieved calculation for card
        let gradedCount = 0;
        let aCount = 0;
        for (let i = 1; i <= TOTAL_COLS_COUNT; i++) {
          const val = outcomes[`col_${i}`] || '';
          if (val) { gradedCount++; if (val === 'A') aCount++; }
        }
        const isAchieved = gradedCount > 0 && aCount >= (gradedCount * 0.65);

        const cardHtml = `
          <div class="bg-white dark:bg-slate-850 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition flex flex-col justify-between space-y-3">
            <!-- Header -->
            <div class="flex items-start justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-2.5">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center font-black text-xs ${isBoy ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' : 'bg-pink-100 text-pink-700 dark:bg-pink-900/50 dark:text-pink-300'} shadow-xs">
                  ${index + 1}
                </div>
                <div>
                  <h4 class="text-xs font-black text-slate-900 dark:text-white leading-tight">${nameEn || nameKn}</h4>
                  ${nameKn && nameEn ? `<p class="text-[10px] text-slate-500 font-semibold">${nameKn}</p>` : ''}
                </div>
              </div>
              <div class="flex flex-col items-end gap-1">
                <span class="px-2 py-0.5 rounded-md text-[10px] font-black ${isBoy ? 'bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-400' : 'bg-pink-50 text-pink-700 dark:bg-pink-950/40 dark:text-pink-400'}">
                  ${isBoy ? '👦 ಬಾಲಕ' : '👧 ಬಾಲಕಿ'}
                </span>
                <span class="text-[10px] font-mono text-slate-400 font-semibold">STS: ${student.app_no || student.id}</span>
              </div>
            </div>

            <!-- Father -->
            <div class="text-[11px] text-slate-600 dark:text-slate-300 flex items-center gap-1.5 px-1">
              <i class="fa-solid fa-user-tie text-slate-400 text-xs"></i>
              <span>ತಂದೆ: <strong class="text-slate-800 dark:text-slate-200">${fatherEn || fatherKn || '-'}</strong></span>
            </div>

            <!-- FLN Competencies Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
              ${colsHtml}
            </div>

            <!-- Footer Status -->
            <div class="flex items-center justify-between pt-2.5 border-t border-slate-100 dark:border-slate-800 text-xs">
              <span id="fln-card-status-${sId}" class="px-2.5 py-1 rounded-full text-[10px] font-black ${isAchieved ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300' : 'bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-300'}">
                ${isAchieved ? '✓ FLN ಸಾಧಿಸಿದ್ದಾರೆ' : '✗ FLN ಸಾಧಿಸಿಲ್ಲ'}
              </span>
              <span class="text-[10px] text-slate-400 font-bold">A ಮಟ್ಟ: <strong class="text-slate-700 dark:text-slate-200">${aCount}/${gradedCount}</strong></span>
            </div>
          </div>
        `;
        container.innerHTML += cardHtml;
      });
    }

    function getFlnBadgeColor(val) {
      if (val === 'BB') return 'text-rose-600 bg-rose-50 px-2 py-0.5 rounded';
      if (val === 'B') return 'text-amber-600 bg-amber-50 px-2 py-0.5 rounded';
      if (val === 'P') return 'text-sky-600 bg-sky-50 px-2 py-0.5 rounded';
      if (val === 'A') return 'text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded';
      return 'text-slate-400';
    }

    function getFlnActiveBtnColor(lvl) {
      if (lvl === 'BB') return 'bg-rose-600 text-white shadow-xs';
      if (lvl === 'B') return 'bg-amber-600 text-white shadow-xs';
      if (lvl === 'P') return 'bg-sky-600 text-white shadow-xs';
      if (lvl === 'A') return 'bg-emerald-600 text-white shadow-xs';
      return 'bg-slate-700 text-white';
    }

    function setFlnCardLevel(studentId, colKey, lvl) {
      if (!evaluations[studentId]) evaluations[studentId] = {};
      evaluations[studentId][colKey] = lvl;

      // Update Card buttons
      ['BB', 'B', 'P', 'A'].forEach(l => {
        const btn = document.getElementById(`fln-btn-${studentId}-${colKey}-${l}`);
        if (btn) {
          btn.className = `py-1 rounded-lg text-[10px] font-black transition cursor-pointer border-0 ${lvl === l ? getFlnActiveBtnColor(l) : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}`;
        }
      });

      const cardBadge = document.getElementById(`fln-card-badge-${studentId}-${colKey}`);
      if (cardBadge) {
        cardBadge.innerText = lvl;
        cardBadge.className = `font-mono font-black text-xs ${getFlnBadgeColor(lvl)}`;
      }

      // Update Table cell if present
      const tableRow = document.querySelector(`tr[data-student-id="${studentId}"]`);
      if (tableRow) {
        const select = tableRow.querySelector(`select[onchange*="${colKey}"]`);
        if (select) {
          select.value = lvl;
          updateCellGrade(studentId, colKey, select);
        }
      }

      updateFlnMetaCounts();
    }

    function renderGrid() {
      const tbody = document.getElementById('student-grid-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      const filtered = getFilteredFlnStudents();
      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${4 + TOTAL_COLS_COUNT}" class="p-8 text-center text-slate-400 font-semibold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</td></tr>`;
        return;
      }

      filtered.forEach((student, index) => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-50 transition border-b border-slate-200";
        const sId = student.id;
        tr.setAttribute('data-student-id', sId);

        if (!evaluations[sId]) {
          evaluations[sId] = {};
        }

        const outcomes = evaluations[sId];
        let nameEn = (student.name_english || '').trim().toUpperCase();
        let nameKn = (student.student_name || '').trim();
        let nameHtml = `<div class="font-bold text-slate-800 text-xs">${nameEn}</div>`;
        if (nameKn) {
          nameHtml += `<div class="text-[10px] text-slate-400 font-bold">${nameKn}</div>`;
        }

        let fatherEn = (student.father_name_az || '').trim().toUpperCase();
        let fatherKn = (student.father_name_kn || '').trim();
        let fatherHtml = `<div class="font-bold text-slate-700 text-xs">${fatherEn}</div>`;
        if (fatherKn) {
          fatherHtml += `<div class="text-[10px] text-slate-400 font-bold">${fatherKn}</div>`;
        }

        let stsNo = student.app_no || '-';

        // Build cells (17 outcome columns)
        let cellsHtml = '';
        for (let i = 1; i <= KANNADA_COLS.length; i++) {
          cellsHtml += buildGridCell(sId, `col_${i}`, outcomes[`col_${i}`] || '');
        }
        for (let i = 10; i <= TOTAL_COLS_COUNT; i++) {
          cellsHtml += buildGridCell(sId, `col_${i}`, outcomes[`col_${i}`] || '');
        }

        tr.innerHTML = `
          <td class="p-2.5 text-center font-bold border-r border-slate-200 sticky-c1">${index + 1}</td>
          <td class="p-2.5 text-center border-r border-slate-200 font-bold text-slate-800 sticky-c2">${stsNo}</td>
          <td class="p-2.5 border-r border-slate-200 sticky-c3">${nameHtml}</td>
          <td class="p-2.5 border-r border-slate-200 sticky-c4">${fatherHtml}</td>
          ${cellsHtml}
        `;
        tbody.appendChild(tr);
      });
    }

    function buildGridCell(studentId, colKey, val) {
      let bgClass = "bg-transparent";
      let textClass = "text-slate-600";
      
      if (val === 'BB') { bgClass = "bg-rose-50"; textClass = "text-rose-700 font-bold"; }
      else if (val === 'B') { bgClass = "bg-amber-50"; textClass = "text-amber-700 font-bold"; }
      else if (val === 'P') { bgClass = "bg-sky-50"; textClass = "text-sky-700 font-bold"; }
      else if (val === 'A') { bgClass = "bg-emerald-50"; textClass = "text-emerald-700 font-bold"; }

      return `
        <td class="p-1 border-r border-slate-200 text-center ${bgClass}">
          <select 
            onchange="updateCellGrade('${studentId}', '${colKey}', this)"
            class="bg-transparent text-center outline-none cursor-pointer text-xs w-full h-full py-1 ${textClass}"
          >
            <option value="" class="text-slate-400 font-normal">-</option>
            <option value="BB" ${val === 'BB' ? 'selected' : ''} class="text-rose-600 font-bold">BB</option>
            <option value="B" ${val === 'B' ? 'selected' : ''} class="text-amber-600 font-bold">B</option>
            <option value="P" ${val === 'P' ? 'selected' : ''} class="text-sky-600 font-bold">P</option>
            <option value="A" ${val === 'A' ? 'selected' : ''} class="text-emerald-600 font-bold">A</option>
          </select>
        </td>
      `;
    }

    function updateCellGrade(studentId, colKey, selectEl) {
      const val = selectEl.value;
      evaluations[studentId][colKey] = val;

      const parentTd = selectEl.parentNode;
      parentTd.className = "p-1 border-r border-slate-200 text-center";
      selectEl.className = "bg-transparent text-center outline-none cursor-pointer text-xs w-full h-full py-1";

      if (val === 'BB') {
        parentTd.classList.add("bg-rose-50");
        selectEl.classList.add("text-rose-700", "font-bold");
      } else if (val === 'B') {
        parentTd.classList.add("bg-amber-50");
        selectEl.classList.add("text-amber-700", "font-bold");
      } else if (val === 'P') {
        parentTd.classList.add("bg-sky-50");
        selectEl.classList.add("text-sky-700", "font-bold");
      } else if (val === 'A') {
        parentTd.classList.add("bg-emerald-50");
        selectEl.classList.add("text-emerald-700", "font-bold");
      }

      updateTotalsFooter();
    }

    function updateTotalsFooter()"""

fln_code = re.sub(target_pattern, replacement_code, fln_code)

# In onDataLoaded, call setFlnViewMode & renderActiveFlnView()
fln_code = fln_code.replace("buildTableHeader();\n      renderGrid();", "buildTableHeader();\n      setFlnViewMode(currentFlnViewMode, false);\n      renderActiveFlnView();")

with open('FlnAssessment.html', 'w', encoding='utf-8') as f:
    f.write(fln_code)

print("Successfully integrated Mobile Card View into FlnAssessment.html")
