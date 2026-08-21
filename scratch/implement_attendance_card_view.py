import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance.html', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Replace loadStudentsForEntry and setRowStatus
target_pattern = r'async function loadStudentsForEntry\(\)[\s\S]*?function setRowStatus\(studentId, val\)[\s\S]*?function validateRowAttendance\(studentId\)'

replacement_code = """async function loadStudentsForEntry() {
      const entryClass = document.getElementById('entry-class-select').value;
      const type = document.getElementById('entry-type-select').value;
      
      const gridBody = document.getElementById('entry-grid-body');
      const loader = document.getElementById('entry-loading');
      const container = document.getElementById('entry-grid-container');
      const cardsContainer = document.getElementById('att-cards-container');
      const sfBar = document.getElementById('att-search-filter-bar');
      const actions = document.getElementById('entry-actions-container');

      loader.classList.remove('hidden');
      container.classList.add('hidden');
      if (cardsContainer) cardsContainer.classList.add('hidden');
      if (sfBar) sfBar.classList.add('hidden');
      actions.classList.add('hidden');

      // Filter students in active class & sort alphabetically (A to Z)
      const classStudents = allStudents
        .filter(s => normalizeClass(s.enroll_class) === entryClass)
        .sort((a, b) => {
          const nameA = (a.name_english || a.student_name || '').toString().trim();
          const nameB = (b.name_english || b.student_name || '').toString().trim();
          return nameA.localeCompare(nameB, undefined, { numeric: true, sensitivity: 'base' });
        });
      
      currentLoadedStudents = classStudents;

      if (classStudents.length === 0) {
        loader.classList.add('hidden');
        gridBody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-slate-500 font-bold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿಗಳು ಈ ತರಗತಿಯಲ್ಲಿ ಇಲ್ಲ / No students in this class</td></tr>`;
        container.classList.remove('hidden');
        return;
      }

      // Fetch existing records for active parameters
      let existingRecords = [];
      const dateVal = document.getElementById('entry-date-picker').value;
      const monthVal = document.getElementById('entry-month-picker').value;
      const yearVal = document.getElementById('entry-year-picker').value;

      if (isSupabaseAttendanceAvailable) {
        try {
          let query = supabaseClient.from('attendance')
            .select('student_id, present_days, working_days, remarks')
            .eq('class_name', entryClass)
            .eq('attendance_type', type);
          
          if (type === 'daily') query = query.eq('attendance_date', dateVal);
          else if (type === 'monthly') query = query.eq('attendance_month', monthVal);
          else if (type === 'yearly') query = query.eq('attendance_year', yearVal);

          const { data, error } = await query;
          if (!error) existingRecords = data || [];
        } catch (e) {
          console.error(e);
        }
      } else {
        const local = localStorage.getItem(`local_attendance_${currentSchoolId}`) || '[]';
        const parsed = JSON.parse(local);
        existingRecords = parsed.filter(r => 
          r.class_name === entryClass && 
          r.attendance_type === type &&
          (type === 'daily' ? r.attendance_date === dateVal :
           type === 'monthly' ? r.attendance_month === monthVal :
           r.attendance_year === yearVal)
        );
      }

      currentLoadedStudents.forEach(student => {
        const rec = existingRecords.find(r => r.student_id === student.id);
        student._attendanceRec = rec;
      });

      loader.classList.add('hidden');
      if (sfBar) sfBar.classList.remove('hidden');
      actions.classList.remove('hidden');

      // Adjust batch actions visibility
      const batchContainer = document.getElementById('daily-batch-actions');
      if (type === 'daily') batchContainer.classList.remove('hidden');
      else batchContainer.classList.add('hidden');

      setAttViewMode(currentAttViewMode, false);
      renderAttActiveView();
      validateAllWorkingDays();
    }

    function setAttViewMode(mode, triggerRender = true) {
      currentAttViewMode = mode || 'cards';
      localStorage.setItem('attendance_view_mode', currentAttViewMode);

      const btnCards = document.getElementById('btn-att-view-cards');
      const btnTable = document.getElementById('btn-att-view-table');

      if (currentAttViewMode === 'cards') {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
      } else {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
      }

      if (triggerRender) {
        renderAttActiveView();
      }
    }

    function setAttGenderFilter(val) {
      attGenderFilter = val || '';
      const btnAll = document.getElementById('att-gen-all');
      const btnBoy = document.getElementById('att-gen-boy');
      const btnGirl = document.getElementById('att-gen-girl');

      const activeClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer';
      const inactiveClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer';

      if (btnAll) btnAll.className = attGenderFilter === '' ? activeClass : inactiveClass;
      if (btnBoy) btnBoy.className = attGenderFilter === 'Boy' ? activeClass : inactiveClass;
      if (btnGirl) btnGirl.className = attGenderFilter === 'Girl' ? activeClass : inactiveClass;

      renderAttActiveView();
    }

    function applyAttFiltersAndRender() {
      const searchInput = document.getElementById('att-search-input');
      attSearchQuery = (searchInput ? searchInput.value : '').toLowerCase().trim();
      renderAttActiveView();
    }

    function getFilteredAttStudents() {
      return (currentLoadedStudents || []).filter(s => {
        if (attGenderFilter && s.gender !== attGenderFilter) return false;
        if (attSearchQuery) {
          const nameEn = (s.name_english || '').toLowerCase();
          const nameKn = (s.student_name || '').toLowerCase();
          const sts = (s.app_no || s.id || '').toLowerCase();
          const father = (s.father_name_az || s.father_name_kn || '').toLowerCase();
          return nameEn.includes(attSearchQuery) || nameKn.includes(attSearchQuery) || sts.includes(attSearchQuery) || father.includes(attSearchQuery);
        }
        return true;
      });
    }

    function renderAttActiveView() {
      const tableEl = document.getElementById('entry-grid-container');
      const cardsEl = document.getElementById('att-cards-container');

      if (currentAttViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderAttCards();
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderAttGrid();
        }
      }
    }

    function renderAttGrid() {
      const gridBody = document.getElementById('entry-grid-body');
      if (!gridBody) return;
      gridBody.innerHTML = '';
      const type = document.getElementById('entry-type-select').value;
      const filtered = getFilteredAttStudents();

      if (filtered.length === 0) {
        gridBody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-slate-400 font-semibold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</td></tr>`;
        return;
      }

      filtered.forEach((student, index) => {
        const record = student._attendanceRec;
        const nameDisplay = `${student.name_english || ''} <span class="block text-[10px] text-slate-450 dark:text-slate-500 font-medium mt-0.5">${student.student_name || ''}</span>`;
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition text-center border-b border-slate-100 dark:border-slate-850';
        
        let controlHtml = '';
        let badgeHtml = '';

        // Read current input value if already entered, or fallback to record/default
        const existingInput = document.getElementById(`input-present-${student.id}`);
        const currentVal = existingInput ? parseInt(existingInput.value) : (record ? record.present_days : (type === 'daily' ? 1 : (parseInt(document.getElementById('total-working-days').value) || 22)));

        if (type === 'daily') {
          const isPresent = currentVal === 1;
          controlHtml = `
            <div class="flex items-center justify-center gap-2">
              <button type="button" onclick="setRowStatus('${student.id}', 1)" id="btn-present-${student.id}" class="px-3 py-1.5 rounded-xl font-bold transition text-[10px] ${isPresent ? 'bg-emerald-500 text-white shadow-sm border border-emerald-500' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700'}">ಹಾಜರು / Present</button>
              <button type="button" onclick="setRowStatus('${student.id}', 0)" id="btn-absent-${student.id}" class="px-3 py-1.5 rounded-xl font-bold transition text-[10px] ${!isPresent ? 'bg-rose-500 text-white shadow-sm border border-rose-500' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700'}">ಗೈರು / Absent</button>
              <input type="hidden" id="input-present-${student.id}" value="${isPresent ? '1' : '0'}">
            </div>
          `;
          badgeHtml = `<span id="badge-${student.id}" class="px-2.5 py-1 rounded-full text-[9px] font-black uppercase ${isPresent ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-500 border border-rose-500/20'}">${isPresent ? 'Present' : 'Absent'}</span>`;
        } else {
          const maxDays = parseInt(document.getElementById('total-working-days').value) || 22;
          controlHtml = `
            <div class="flex items-center justify-center gap-2">
              <input type="number" id="input-present-${student.id}" value="${currentVal}" min="0" max="${maxDays}" oninput="validateRowAttendance('${student.id}')" class="w-24 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-center font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500 transition text-slate-800 dark:text-white">
              <span class="text-slate-400 text-xs">/ <span class="total-days-label font-bold">${maxDays}</span></span>
            </div>
          `;
          badgeHtml = `<span id="badge-${student.id}" class="px-2.5 py-1 rounded-full text-[9px] font-black uppercase bg-indigo-500/10 text-indigo-500 border border-indigo-500/20">Saved: ${currentVal} Days</span>`;
        }

        tr.innerHTML = `
          <td class="p-3 text-slate-450 dark:text-slate-500 font-bold text-left">${index + 1}</td>
          <td class="p-3 text-left font-mono font-bold text-slate-600 dark:text-slate-400">${student.app_no || '-'}</td>
          <td class="p-3 text-left font-bold text-slate-800 dark:text-white">${nameDisplay}</td>
          <td class="p-3 text-slate-500 dark:text-slate-400 font-bold">${student.gender}</td>
          <td class="p-3">${controlHtml}</td>
          <td class="p-3">${badgeHtml}</td>
        `;
        gridBody.appendChild(tr);
      });
    }

    function renderAttCards() {
      const container = document.getElementById('att-cards-container');
      if (!container) return;
      container.innerHTML = '';

      const type = document.getElementById('entry-type-select').value;
      const filtered = getFilteredAttStudents();

      if (filtered.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-300"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      filtered.forEach((student, index) => {
        const record = student._attendanceRec;
        const sId = student.id;
        const isBoy = student.gender === 'Boy';
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();

        const existingInput = document.getElementById(`input-present-${student.id}`);
        const currentVal = existingInput ? parseInt(existingInput.value) : (record ? record.present_days : (type === 'daily' ? 1 : (parseInt(document.getElementById('total-working-days').value) || 22)));

        let entryControlsHtml = '';
        if (type === 'daily') {
          const isPresent = currentVal === 1;
          entryControlsHtml = `
            <div class="grid grid-cols-2 gap-2 pt-1">
              <button type="button" onclick="setRowStatus('${sId}', 1)" id="card-btn-present-${sId}" class="py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 ${isPresent ? 'bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700'}">
                <i class="fa-solid fa-check text-sm"></i> <span>ಹಾಜರು (Present)</span>
              </button>
              <button type="button" onclick="setRowStatus('${sId}', 0)" id="card-btn-absent-${sId}" class="py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 ${!isPresent ? 'bg-rose-600 text-white shadow-md border-0 ring-2 ring-rose-500/30' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700'}">
                <i class="fa-solid fa-xmark text-sm"></i> <span>ಗೈರು (Absent)</span>
              </button>
            </div>
          `;
        } else {
          const maxDays = parseInt(document.getElementById('total-working-days').value) || 22;
          entryControlsHtml = `
            <div class="space-y-1.5 pt-1">
              <div class="flex items-center justify-between text-xs">
                <span class="text-slate-500">ಹಾಜರಾದ ದಿನಗಳು:</span>
                <span class="font-bold text-slate-700 dark:text-slate-300">ಗರಿಷ್ಠ: ${maxDays} ದಿನಗಳು</span>
              </div>
              <div class="flex items-center gap-2">
                <button type="button" onclick="stepAttDays('${sId}', -1)" class="w-9 h-9 rounded-xl bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-100 font-black text-base flex items-center justify-center border-0 cursor-pointer active:scale-95">-</button>
                <input type="number" id="card-input-present-${sId}" value="${currentVal}" min="0" max="${maxDays}" oninput="onCardAttDaysChange('${sId}', this.value)" class="flex-1 bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl py-1.5 text-center font-black text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <button type="button" onclick="stepAttDays('${sId}', 1)" class="w-9 h-9 rounded-xl bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-100 font-black text-base flex items-center justify-center border-0 cursor-pointer active:scale-95">+</button>
              </div>
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
                <span class="text-[10px] font-mono text-slate-400 font-semibold">STS: ${student.app_no || student.id}</span>
              </div>
            </div>

            <!-- Father -->
            <div class="text-[11px] text-slate-600 dark:text-slate-300 flex items-center gap-1.5 px-1">
              <i class="fa-solid fa-user-tie text-slate-400 text-xs"></i>
              <span>ತಂದೆ: <strong class="text-slate-800 dark:text-slate-200">${fatherEn || fatherKn || '-'}</strong></span>
            </div>

            <!-- Controls -->
            <div>
              ${entryControlsHtml}
            </div>
          </div>
        `;
        container.innerHTML += cardHtml;
      });
    }

    function stepAttDays(studentId, delta) {
      const maxDays = parseInt(document.getElementById('total-working-days').value) || 22;
      const input = document.getElementById(`input-present-${studentId}`);
      const cardInput = document.getElementById(`card-input-present-${studentId}`);
      let currentVal = input ? parseInt(input.value) : (cardInput ? parseInt(cardInput.value) : 0);
      let newVal = Math.max(0, Math.min(maxDays, currentVal + delta));
      if (input) input.value = newVal;
      if (cardInput) cardInput.value = newVal;
      validateRowAttendance(studentId);
    }

    function onCardAttDaysChange(studentId, val) {
      const input = document.getElementById(`input-present-${studentId}`);
      if (input) input.value = val;
      validateRowAttendance(studentId);
    }

    function setRowStatus(studentId, val) {
      const input = document.getElementById(`input-present-${studentId}`);
      if (input) input.value = val;

      // Table elements
      const pBtn = document.getElementById(`btn-present-${studentId}`);
      const aBtn = document.getElementById(`btn-absent-${studentId}`);
      const badge = document.getElementById(`badge-${studentId}`);

      if (pBtn && aBtn && badge) {
        if (val === 1) {
          pBtn.className = "px-3 py-1.5 rounded-xl font-bold transition text-[10px] bg-emerald-500 text-white shadow-sm border border-emerald-500";
          aBtn.className = "px-3 py-1.5 rounded-xl font-bold transition text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700";
          badge.className = "px-2.5 py-1 rounded-full text-[9px] font-black uppercase bg-emerald-500/10 text-emerald-500 border border-emerald-500/20";
          badge.innerText = "Present";
        } else {
          pBtn.className = "px-3 py-1.5 rounded-xl font-bold transition text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700";
          aBtn.className = "px-3 py-1.5 rounded-xl font-bold transition text-[10px] bg-rose-500 text-white shadow-sm border border-rose-500";
          badge.className = "px-2.5 py-1 rounded-full text-[9px] font-black uppercase bg-rose-500/10 text-rose-500 border border-rose-500/20";
          badge.innerText = "Absent";
        }
      }

      // Card elements
      const cardPBtn = document.getElementById(`card-btn-present-${studentId}`);
      const cardABtn = document.getElementById(`card-btn-absent-${studentId}`);
      if (cardPBtn && cardABtn) {
        if (val === 1) {
          cardPBtn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-emerald-600 text-white shadow-md border-0 ring-2 ring-emerald-500/30";
          cardABtn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700";
        } else {
          cardPBtn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700";
          cardABtn.className = "py-2.5 px-3 rounded-xl font-black text-xs transition cursor-pointer flex items-center justify-center gap-1.5 bg-rose-600 text-white shadow-md border-0 ring-2 ring-rose-500/30";
        }
      }
    }

    function validateRowAttendance(studentId)"""

js_code = re.sub(target_pattern, replacement_code, js_code)

with open('Attendance.html', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Successfully integrated Mobile Card View into Attendance.html")
