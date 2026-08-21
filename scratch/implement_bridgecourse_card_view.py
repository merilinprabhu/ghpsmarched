import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('BridgeCourse.html', 'r', encoding='utf-8') as f:
    bc_code = f.read()

# Replace renderRosterGrid and surrounding functions
target_pattern = r'function renderRosterGrid\(\)[\s\S]*?function onGradeChange\(studentId, compKey, val\)'

replacement_code = """function setBCViewMode(mode, triggerRender = true) {
      currentBCViewMode = mode || 'cards';
      localStorage.setItem('bc_view_mode', currentBCViewMode);

      const btnCards = document.getElementById('btn-bc-view-cards');
      const btnTable = document.getElementById('btn-bc-view-table');

      if (currentBCViewMode === 'cards') {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
      } else {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
      }

      if (triggerRender) {
        renderActiveBCView();
      }
    }

    function setBCGenderFilter(val) {
      bcGenderFilter = val || '';
      const btnAll = document.getElementById('bc-gen-all');
      const btnBoy = document.getElementById('bc-gen-boy');
      const btnGirl = document.getElementById('bc-gen-girl');

      const activeClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer';
      const inactiveClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer';

      if (btnAll) btnAll.className = bcGenderFilter === '' ? activeClass : inactiveClass;
      if (btnBoy) btnBoy.className = bcGenderFilter === 'Boy' ? activeClass : inactiveClass;
      if (btnGirl) btnGirl.className = bcGenderFilter === 'Girl' ? activeClass : inactiveClass;

      renderActiveBCView();
    }

    function applyBCFiltersAndRender() {
      const searchInput = document.getElementById('bc-search-input');
      bcSearchQuery = (searchInput ? searchInput.value : '').toLowerCase().trim();
      renderActiveBCView();
    }

    function getFilteredBCStudents() {
      return (selectedStudents || []).filter(s => {
        if (bcGenderFilter && s.gender !== bcGenderFilter) return false;
        if (bcSearchQuery) {
          const nameEn = (s.name_english || '').toLowerCase();
          const nameKn = (s.student_name_kn || s.student_name || '').toLowerCase();
          const sts = (s.adminNo || s.app_no || s.id || '').toLowerCase();
          const father = (s.father_name_az || s.father_name_kn || '').toLowerCase();
          return nameEn.includes(bcSearchQuery) || nameKn.includes(bcSearchQuery) || sts.includes(bcSearchQuery) || father.includes(bcSearchQuery);
        }
        return true;
      });
    }

    function renderActiveBCView() {
      const tableEl = document.getElementById('bc-table-wrapper');
      const cardsEl = document.getElementById('bc-cards-container');

      if (currentBCViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderBCCards();
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderRosterGrid();
        }
      }
      updateRowTotalsAndFooter();
    }

    function renderBCCards() {
      const container = document.getElementById('bc-cards-container');
      if (!container) return;
      container.innerHTML = '';

      const filtered = getFilteredBCStudents();
      if (filtered.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-300"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      filtered.forEach((student, index) => {
        const sId = student.id;
        if (!evaluations[sId]) {
          evaluations[sId] = { c1: 'B', c2: 'B', c3: 'B', c4: 'B', c5: 'B', c6: 'B', c7: 'B', c8: 'B', c9: 'B', c10: 'B' };
        }
        const evalData = evaluations[sId];
        const isBoy = student.gender === 'Boy';
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();

        let compItemsHtml = '';
        for (let i = 1; i <= 10; i++) {
          const cKey = `c${i}`;
          const val = evalData[cKey] || 'B';
          const isA = val === 'A';

          compItemsHtml += `
            <div class="p-2 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 flex items-center justify-between gap-2">
              <span class="text-[11px] font-bold text-slate-700 dark:text-slate-200 truncate max-w-[120px]" title="ಸಾಮರ್ಥ್ಯ C${i}">ಸಾಮರ್ಥ್ಯ C${i}</span>
              ${isEditing ? `
                <div class="flex items-center gap-1">
                  <button type="button" onclick="setCompetencyCardVal('${sId}', '${cKey}', 'A')" id="card-btn-${sId}-${cKey}-A" class="px-2.5 py-1 rounded-lg font-black text-xs transition cursor-pointer border-0 ${isA ? 'bg-emerald-600 text-white shadow-xs' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">A</button>
                  <button type="button" onclick="setCompetencyCardVal('${sId}', '${cKey}', 'B')" id="card-btn-${sId}-${cKey}-B" class="px-2.5 py-1 rounded-lg font-black text-xs transition cursor-pointer border-0 ${!isA ? 'bg-blue-600 text-white shadow-xs' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">B</button>
                </div>
              ` : `
                <span class="font-black text-xs px-2 py-0.5 rounded-full ${isA ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300'}">${val}</span>
              `}
            </div>
          `;
        }

        const cardHtml = `
          <div class="bg-white dark:bg-slate-850 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-3">
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
                <span class="text-[10px] font-mono text-slate-400 font-semibold">STS: ${student.adminNo || student.id}</span>
              </div>
            </div>

            <!-- Father -->
            <div class="text-[11px] text-slate-600 dark:text-slate-300 flex items-center gap-1.5 px-1">
              <i class="fa-solid fa-user-tie text-slate-400 text-xs"></i>
              <span>ತಂದೆ: <strong class="text-slate-800 dark:text-slate-200">${fatherEn || fatherKn || '-'}</strong></span>
            </div>

            <!-- Competencies 2-column grid -->
            <div class="grid grid-cols-2 gap-2 pt-1">
              ${compItemsHtml}
            </div>

            <!-- Footer -->
            <div class="flex items-center justify-between pt-2.5 border-t border-slate-100 dark:border-slate-800 text-xs">
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/30 px-2 py-0.5 rounded">A: <strong id="card-total-a-${sId}">0</strong></span>
                <span class="text-[10px] font-bold text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/30 px-2 py-0.5 rounded">B: <strong id="card-total-b-${sId}">0</strong></span>
              </div>
              ${!isEditing ? `
                <button type="button" onclick="enableEditing()" class="text-indigo-600 dark:text-indigo-400 hover:underline font-bold text-[11px] flex items-center gap-1 border-0 bg-transparent cursor-pointer">
                  <i class="fa-solid fa-pen-to-square"></i> ತಿದ್ದು / Edit
                </button>
              ` : ''}
            </div>
          </div>
        `;
        container.innerHTML += cardHtml;
      });
    }

    function setCompetencyCardVal(studentId, compKey, val) {
      onGradeChange(studentId, compKey, val);
      const btnA = document.getElementById(`card-btn-${studentId}-${compKey}-A`);
      const btnB = document.getElementById(`card-btn-${studentId}-${compKey}-B`);
      if (btnA && btnB) {
        if (val === 'A') {
          btnA.className = "px-2.5 py-1 rounded-lg font-black text-xs transition cursor-pointer border-0 bg-emerald-600 text-white shadow-xs";
          btnB.className = "px-2.5 py-1 rounded-lg font-black text-xs transition cursor-pointer border-0 bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300";
        } else {
          btnA.className = "px-2.5 py-1 rounded-lg font-black text-xs transition cursor-pointer border-0 bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300";
          btnB.className = "px-2.5 py-1 rounded-lg font-black text-xs transition cursor-pointer border-0 bg-blue-600 text-white shadow-xs";
        }
      }
    }

    function renderRosterGrid() {
      const tbody = document.getElementById('student-grid-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      const filtered = getFilteredBCStudents();
      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="16" class="p-8 text-center text-slate-400 font-semibold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</td></tr>`;
        return;
      }

      filtered.forEach((student, index) => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-50/80 transition text-center";
        tr.setAttribute('data-student-id', student.id);
        const sId = student.id;
        if (!evaluations[sId]) {
          evaluations[sId] = { c1: 'B', c2: 'B', c3: 'B', c4: 'B', c5: 'B', c6: 'B', c7: 'B', c8: 'B', c9: 'B', c10: 'B' };
        }
        
        const eval = evaluations[sId];
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || '').trim();
        let nameHtml = '';
        if (nameEn && nameKn) {
          nameHtml = `<div class="font-bold text-slate-800 text-[11px]">${nameEn}</div><div class="text-[10px] text-slate-550 font-medium">${nameKn}</div>`;
        } else {
          nameHtml = `<span class="font-bold text-slate-800 text-[11px]">${nameEn || nameKn || '-'}</span>`;
        }

        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();
        let fatherHtml = '';
        if (fatherEn && fatherKn) {
          fatherHtml = `<div class="font-bold text-slate-700 text-[11px]">${fatherEn}</div><div class="text-[10px] text-slate-500 font-medium">${fatherKn}</div>`;
        } else {
          fatherHtml = `<span class="font-semibold text-slate-700 text-[11px]">${fatherEn || fatherKn || '-'}</span>`;
        }

        let rowHtml = `
          <td class="p-3 text-center border-r border-slate-200 font-medium">${index + 1}</td>
          <td class="p-3 border-r border-slate-200 font-mono text-slate-500 font-bold">${student.adminNo || student.id}</td>
          <td class="p-3 border-r border-slate-200 text-left">${nameHtml}</td>
          <td class="p-3 border-r border-slate-200 text-left">${fatherHtml}</td>
        `;

        for (let i = 1; i <= 10; i++) {
          const val = eval[`c${i}`] || 'B';
          
          if (isEditing) {
            const selectClass = getGradeSelectClass(val);
            rowHtml += `
              <td class="p-1 border-r border-slate-200 text-center">
                <select onchange="this.className=getGradeSelectClass(this.value); onGradeChange('${sId}', 'c${i}', this.value)" class="${selectClass}">
                  <option value="A" ${val === 'A' ? 'selected' : ''}>A</option>
                  <option value="B" ${val === 'B' ? 'selected' : ''}>B</option>
                </select>
              </td>
            `;
          } else {
            let badgeClass = "text-slate-400 font-normal";
            if (val === 'A') badgeClass = "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 font-black rounded-full px-2.5 py-1 text-[11px] inline-block shadow-sm";
            if (val === 'B') badgeClass = "bg-blue-500/10 text-blue-700 dark:text-blue-400 border border-blue-500/20 font-black rounded-full px-2.5 py-1 text-[11px] inline-block shadow-sm";
            
            rowHtml += `
              <td class="p-2 border-r border-slate-200 text-center font-bold">
                <span class="${badgeClass}">${val || 'B'}</span>
              </td>
            `;
          }
        }

        rowHtml += `
          <td id="row-total-a-${sId}" class="p-3 border-r border-slate-200 text-center font-black bg-emerald-50/50 text-emerald-800 text-xs">0</td>
          <td id="row-total-b-${sId}" class="p-3 text-center font-black bg-blue-50/50 text-blue-800 text-xs">0</td>
        `;

        tr.innerHTML = rowHtml;
        tbody.appendChild(tr);
      });
    }

    function onGradeChange(studentId, compKey, val)"""

bc_code = re.sub(target_pattern, replacement_code, bc_code)

# In enableEditing, cancelEditing, onDataSaved -> call renderActiveBCView()
bc_code = bc_code.replace("renderRosterGrid();", "renderActiveBCView();")

# In updateRowTotalsAndFooter, also update card totals
totals_old = """      selectedStudents.forEach(student => {
        const sId = student.id;
        const eval = evaluations[sId] || {};
        let totalA = 0;
        let totalB = 0;
        for (let i = 1; i <= 10; i++) {
          if (eval[`c${i}`] === 'A') totalA++;
          else if (eval[`c${i}`] === 'B') totalB++;
        }
        const elA = document.getElementById(`row-total-a-${sId}`);
        const elB = document.getElementById(`row-total-b-${sId}`);
        if (elA) elA.innerText = totalA;
        if (elB) elB.innerText = totalB;
      });"""

totals_new = """      selectedStudents.forEach(student => {
        const sId = student.id;
        const eval = evaluations[sId] || {};
        let totalA = 0;
        let totalB = 0;
        for (let i = 1; i <= 10; i++) {
          if (eval[`c${i}`] === 'A') totalA++;
          else if (eval[`c${i}`] === 'B') totalB++;
        }
        const elA = document.getElementById(`row-total-a-${sId}`);
        const elB = document.getElementById(`row-total-b-${sId}`);
        if (elA) elA.innerText = totalA;
        if (elB) elB.innerText = totalB;

        const cardElA = document.getElementById(`card-total-a-${sId}`);
        const cardElB = document.getElementById(`card-total-b-${sId}`);
        if (cardElA) cardElA.innerText = totalA;
        if (cardElB) cardElB.innerText = totalB;
      });"""

bc_code = bc_code.replace(totals_old, totals_new)

with open('BridgeCourse.html', 'w', encoding='utf-8') as f:
    f.write(bc_code)

print("Successfully integrated Mobile Card View into BridgeCourse.html")
