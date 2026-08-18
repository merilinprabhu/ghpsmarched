
    let allTransactions = [];
    let defaultFeeReasons = [
      { id: 'FR1', name_en: 'Exam Fee', name_kn: 'ಪರೀಕ್ಷಾ ಶುಲ್ಕ', amount: 150, class: 'All', active: true },
      { id: 'FR2', name_en: 'ID Card & Badge', name_kn: 'ಐಡಿ ಕಾರ್ಡ್ ಮತ್ತು ಬ್ಯಾಡ್ಜ್', amount: 50, class: 'All', active: true },
      { id: 'FR3', name_en: 'Sports & Cultural Fund', name_kn: 'ಕ್ರೀಡಾ ಮತ್ತು ಸಾಂಸ್ಕೃತಿಕ ನಿಧಿ', amount: 50, class: 'All', active: true },
      { id: 'FR4', name_en: 'SDMC Development Fund', name_kn: 'SDMC ಶಾಲಾ ಅಭಿವೃದ್ಧಿ ನಿಧಿ', amount: 100, class: 'All', active: true },
      { id: 'FR5', name_en: 'Admission Fee', name_kn: 'ಪ್ರವೇಶ ಶುಲ್ಕ', amount: 200, class: 'LKG', active: true }
    ];

    let sampleStudents = [];

    let selectedModalStudent = null;
    let editingFeeReasonId = null;
    let categoryChartInstance = null;
    let html5QrcodeScannerInstance = null;

    document.addEventListener("DOMContentLoaded", async function() {
      // 1. Read URL query param to activate subpage tab
      const urlParams = new URLSearchParams(window.location.search);
      const tabParam = urlParams.get('tab') || 'dashboard';
      switchFinanceTab(tabParam);

      // 2. Load fee structure reasons from localStorage/DB
      loadFeeReasons();

      // 3. Set today date in collection modal
      const todayStr = new Date().toISOString().split('T')[0];
      document.getElementById('modal-date-input').value = todayStr;

      // 4. Load finance transaction data
      await loadFinanceData();

      // 5. Load student roster table
      loadStudents();
    });

    // Subpage Switcher Function
    function switchFinanceTab(tabId) {
      const tabs = ['dashboard', 'collection', 'settings'];
      tabs.forEach(t => {
        const btn = document.getElementById(`fin-tab-${t}`);
        const view = document.getElementById(`view-${t}`);
        if (btn && view) {
          if (t === tabId) {
            btn.classList.add('active');
            view.classList.remove('hidden');
          } else {
            btn.classList.remove('active');
            view.classList.add('hidden');
          }
        }
      });
    }

    // Fee Structure Settings Functions
    function loadFeeReasons() {
      const saved = localStorage.getItem('portal_fee_structures');
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          if (parsed && parsed.length > 0) defaultFeeReasons = parsed;
        } catch(e) {}
      } else {
        localStorage.setItem('portal_fee_structures', JSON.stringify(defaultFeeReasons));
      }

      renderSettingsReasonsTable();
    }

    function autoTranslateFeeReason(force = false) {
      const enInput = document.getElementById('set-reason-en');
      const knInput = document.getElementById('set-reason-kn');
      if (!enInput || !knInput) return;

      let text = enInput.value.trim();
      if (!text) return;
      if (knInput.value.trim() && !force) return;

      knInput.placeholder = "ಭಾಷಾಂತರಿಸಲಾಗುತ್ತಿದೆ... / Translating...";

      const dict = {
        "EXAM FEE": "ಪರೀಕ್ಷಾ ಶುಲ್ಕ",
        "EXAM": "ಪರೀಕ್ಷಾ ಶುಲ್ಕ",
        "ID CARD": "ಐಡಿ ಕಾರ್ಡ್ ಮತ್ತು ಬ್ಯಾಡ್ಜ್",
        "SPORTS": "ಕ್ರೀಡಾ ಮತ್ತು ಸಾಂಸ್ಕೃತಿಕ ನಿಧಿ",
        "SPORTS FEE": "ಕ್ರೀಡಾ ಶುಲ್ಕ",
        "SDMC": "SDMC ಶಾಲಾ ಅಭಿವೃದ್ಧಿ ನಿಧಿ",
        "SDMC FUND": "SDMC ಶಾಲಾ ಅಭಿವೃದ್ಧಿ ನಿಧಿ",
        "DEVELOPMENT": "ಶಾಲಾ ಅಭಿವೃದ್ಧಿ ನಿಧಿ",
        "ADMISSION": "ಪ್ರವೇಶ ಶುಲ್ಕ",
        "ADMISSION FEE": "ಪ್ರವೇಶ ಶುಲ್ಕ",
        "UNIFORM": "ಯೂನಿಫಾರ್ಮ್ ಶುಲ್ಕ",
        "PICNIC": "ಪ್ರವಾಸದ ಶುಲ್ಕ",
        "TOUR": "ಪ್ರವಾಸದ ಶುಲ್ಕ",
        "COMPUTER": "ಕಂಪ್ಯೂಟರ್ ಶಿಕ್ಷಣ ಶುಲ್ಕ",
        "CULTURAL": "ಸಾಂಸ್ಕೃತಿಕ ನಿಧಿ",
        "MAINTENANCE": "ನಿರ್ವಹಣಾ ವೆಚ್ಚ"
      };

      let upper = text.toUpperCase();
      if (dict[upper]) {
        knInput.value = dict[upper];
        return;
      }

      fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=kn&dt=t&q=${encodeURIComponent(text)}`)
        .then(res => res.json())
        .then(data => {
          if (data && data[0] && data[0][0]) {
            knInput.value = data[0].map(item => item[0]).join('').trim();
          } else {
            knInput.value = text;
          }
        })
        .catch(err => {
          knInput.value = text;
        });
    }

    function saveNewFeeReason(e) {
      if (e && e.preventDefault) e.preventDefault();
      
      const enInput = document.getElementById('set-reason-en');
      const knInput = document.getElementById('set-reason-kn');
      const amtInput = document.getElementById('set-amount');
      const clsSelect = document.getElementById('set-class');

      const nameEn = enInput ? enInput.value.trim() : '';
      let nameKn = knInput ? knInput.value.trim() : '';
      const amt = parseFloat(amtInput ? amtInput.value : 0);
      const cls = clsSelect ? clsSelect.value : 'All';

      if (!nameEn) {
        alert("ದಯವಿಟ್ಟು ಶುಲ್ಕದ ವಿವರವನ್ನು ನಮೂದಿಸಿ (ಉದಾ. Exam Fee, Sports Fee). / Please enter Fee Collection Reason.");
        if (enInput) enInput.focus();
        return false;
      }

      if (isNaN(amt) || amt <= 0) {
        alert("ದಯವಿಟ್ಟು ಸೂಕ್ತವಾದ ಶುಲ್ಕ ಮೊತ್ತವನ್ನು ನಮೂದಿಸಿ (ಉದಾ. 150). / Please enter a valid Fee Amount (₹).");
        if (amtInput) amtInput.focus();
        return false;
      }

      if (!nameKn) {
        const dict = {
          "EXAM FEE": "ಪರೀಕ್ಷಾ ಶುಲ್ಕ",
          "EXAM": "ಪರೀಕ್ಷಾ ಶುಲ್ಕ",
          "ID CARD": "ಐಡಿ ಕಾರ್ಡ್ ಮತ್ತು ಬ್ಯಾಡ್ಜ್",
          "SPORTS": "ಕ್ರೀಡಾ ಮತ್ತು ಸಾಂಸ್ಕೃತಿಕ ನಿಧಿ",
          "SDMC": "SDMC ಶಾಲಾ ಅಭಿವೃದ್ಧಿ ನಿಧಿ",
          "ADMISSION": "ಪ್ರವೇಶ ಶುಲ್ಕ",
          "UNIFORM": "ಯೂನಿಫಾರ್ಮ್ ಶುಲ್ಕ",
          "PICNIC": "ಪ್ರವಾಸದ ಶುಲ್ಕ",
          "COMPUTER": "ಕಂಪ್ಯೂಟರ್ ಶಿಕ್ಷಣ ಶುಲ್ಕ"
        };
        const upper = nameEn.toUpperCase();
        nameKn = dict[upper] || nameEn;
      }

      if (editingFeeReasonId) {
        // Edit Mode Update
        const targetIndex = defaultFeeReasons.findIndex(r => r.id === editingFeeReasonId);
        if (targetIndex !== -1) {
          defaultFeeReasons[targetIndex].name_en = nameEn;
          defaultFeeReasons[targetIndex].name_kn = nameKn;
          defaultFeeReasons[targetIndex].amount = amt;
          defaultFeeReasons[targetIndex].class = cls;
        }
        editingFeeReasonId = null;
        document.getElementById('form-heading-title').innerHTML = `<i class="fa-solid fa-plus-circle text-emerald-500"></i> ಹೊಸ ಶುಲ್ಕ ವಿಭಾಗ ಸೇರಿಸಿ / Add Fee Reason`;
        document.getElementById('save-reason-btn').innerHTML = `<i class="fa-solid fa-floppy-disk"></i> ಶುಲ್ಕ ವಿಭಾಗ ಸೇರಿಸಿ / Save Fee Reason`;
        document.getElementById('cancel-edit-btn').classList.add('hidden');
      } else {
        // Create New Mode
        const newReason = {
          id: 'FR' + Date.now(),
          name_en: nameEn,
          name_kn: nameKn,
          amount: amt,
          class: cls,
          active: true
        };
        defaultFeeReasons.push(newReason);
      }

      localStorage.setItem('portal_fee_structures', JSON.stringify(defaultFeeReasons));

      if (enInput) enInput.value = '';
      if (knInput) knInput.value = '';
      if (amtInput) amtInput.value = '';

      loadFeeReasons();

      alert(`ಶುಲ್ಕ ವಿಭಾಗ "${nameKn}" (₹${amt}) ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ! / Fee Reason Saved Successfully!`);
      return false;
    }

    function editFeeReason(id) {
      const reason = defaultFeeReasons.find(r => r.id === id);
      if (!reason) return;

      editingFeeReasonId = id;
      document.getElementById('set-reason-en').value = reason.name_en;
      document.getElementById('set-reason-kn').value = reason.name_kn;
      document.getElementById('set-amount').value = reason.amount;
      document.getElementById('set-class').value = reason.class || 'All';

      document.getElementById('form-heading-title').innerHTML = `<i class="fa-solid fa-pen-to-square text-amber-500"></i> ಶುಲ್ಕ ವಿಭಾಗ ತಿದ್ದುಪಡಿ ಮಾಡಿ / Edit Fee Reason`;
      document.getElementById('save-reason-btn').innerHTML = `<i class="fa-solid fa-check-double"></i> 💾 ನವೀಕರಿಸಿ / Update Fee Reason`;
      document.getElementById('cancel-edit-btn').classList.remove('hidden');

      document.getElementById('set-reason-en').focus();
    }

    function cancelFeeEdit() {
      editingFeeReasonId = null;
      document.getElementById('set-reason-en').value = '';
      document.getElementById('set-reason-kn').value = '';
      document.getElementById('set-amount').value = '';

      document.getElementById('form-heading-title').innerHTML = `<i class="fa-solid fa-plus-circle text-emerald-500"></i> ಹೊಸ ಶುಲ್ಕ ವಿಭಾಗ ಸೇರಿಸಿ / Add Fee Reason`;
      document.getElementById('save-reason-btn').innerHTML = `<i class="fa-solid fa-floppy-disk"></i> ಶುಲ್ಕ ವಿಭಾಗ ಸೇರಿಸಿ / Save Fee Reason`;
      document.getElementById('cancel-edit-btn').classList.add('hidden');
    }

    function deleteFeeReason(id) {
      if (!confirm("ಈ ಶುಲ್ಕ ವಿಭಾಗವನ್ನು ಅಳಿಸಲು ನೀವು ಖಚಿತವಾಗಿದ್ದೀರಾ? / Delete this fee reason?")) return;
      defaultFeeReasons = defaultFeeReasons.filter(r => r.id !== id);
      localStorage.setItem('portal_fee_structures', JSON.stringify(defaultFeeReasons));
      loadFeeReasons();
    }

    function renderSettingsReasonsTable() {
      const tbody = document.getElementById('settings-reasons-tbody');
      const badge = document.getElementById('fee-reasons-count-badge');
      if (!tbody) return;

      badge.textContent = defaultFeeReasons.length + ' Fee Reasons';

      let html = '';
      defaultFeeReasons.forEach((r, idx) => {
        html += `
          <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <td class="py-3 px-4 font-bold">
              <div class="text-slate-800 dark:text-white">${r.name_kn}</div>
              <div class="text-[10px] text-slate-400 font-medium">${r.name_en}</div>
            </td>
            <td class="py-3 px-4 text-center font-semibold"><span class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 rounded-lg text-[10px]">${r.class}</span></td>
            <td class="py-3 px-4 text-right font-mono font-black text-emerald-600 dark:text-emerald-400">₹ ${r.amount}</td>
            <td class="py-3 px-4 text-center">
              <div class="flex items-center justify-center gap-1.5">
                <button onclick="editFeeReason('${r.id}')" title="Edit Reason (ತಿದ್ದುಪಡಿ)" class="w-7 h-7 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-600 flex items-center justify-center border border-amber-200 cursor-pointer transition">
                  <i class="fa-solid fa-pen-to-square text-xs"></i>
                </button>
                <button onclick="deleteFeeReason('${r.id}')" title="Delete Reason" class="w-7 h-7 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-600 flex items-center justify-center border border-rose-200 cursor-pointer transition">
                  <i class="fa-solid fa-trash text-xs"></i>
                </button>
              </div>
            </td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    function normalizeFinanceStudent(s) {
      if (!s) return null;
      const stName = s.student_name || s.name_kannada || s.name_english || s.name || s.student_name_kn || s.fullName || '';
      const enName = s.name_english || s.student_name_en || s.student_name || s.name_en || s.name || stName;
      const knName = s.name_kannada || s.student_name_kn || s.name_kn || stName;
      const stsNum = s.app_no || s.sts_no || s.student_sts || s.sts || s.enrolment_no || s.admission_no || s.adminNo || s.id || '';
      const rawCls = s.enroll_class || s.enrollClass || s.standard || s.class || s.class_name || s.enrolment_class || s.admission_class || '1';
      const cleanCls = (rawCls || '').toString().trim().replace(/^class\s*/i, '');
      const father = s.father_name_az || s.father_name_kn || s.father_name || s.father_name_en || s.father || '';
      const gender = s.gender || s.sex || 'Boy';

      return {
        id: s.id || stsNum || `std_${Math.random()}`,
        sts: stsNum || 'N/A',
        name_en: enName || knName || stName,
        name_kn: knName || enName || stName,
        father: father,
        class: cleanCls || '1',
        gender: gender,
        status: s.status || 'ACTIVE'
      };
    }

    function fetchIndexedDBStudents() {
      return new Promise((resolve) => {
        try {
          const req = indexedDB.open('SchoolDB');
          req.onsuccess = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('students')) {
              resolve([]);
              return;
            }
            const tx = db.transaction('students', 'readonly');
            const store = tx.objectStore('students');
            const getReq = store.getAll();
            getReq.onsuccess = () => resolve(getReq.result || []);
            getReq.onerror = () => resolve([]);
          };
          req.onerror = () => resolve([]);
        } catch(err) {
          resolve([]);
        }
      });
    }

    async function loadStudents() {
      let rawStudents = [];

      // 1. Try Supabase admissions & student_admissions tables
      if (window.supabaseClient) {
        try {
          const schoolId = localStorage.getItem("school_id");
          let query = supabaseClient.from('admissions').select('*');
          if (schoolId) query = query.eq('school_id', schoolId);
          const { data: res1 } = await query;
          if (res1 && res1.length > 0) rawStudents.push(...res1);
        } catch (e) {}

        if (rawStudents.length === 0) {
          try {
            const { data: res1Fallback } = await supabaseClient.from('admissions').select('*');
            if (res1Fallback && res1Fallback.length > 0) rawStudents.push(...res1Fallback);
          } catch (e) {}
        }

        try {
          const { data: res2 } = await supabaseClient.from('student_admissions').select('*');
          if (res2 && res2.length > 0) rawStudents.push(...res2);
        } catch (e) {}
      }

      // 2. Fetch from IndexedDB SchoolDB -> students store
      try {
        const idbStudents = await fetchIndexedDBStudents();
        if (idbStudents && idbStudents.length > 0) {
          rawStudents.push(...idbStudents);
        }
      } catch (e) {}

      // 3. Check all localStorage student caches
      const localKeys = [
        'local_admissions', 'students_class_1', 'students_class_2', 'students_class_3', 'students_class_4', 'students_class_5',
        'students_class_6', 'students_class_7', 'students_class_8', 'students_class_9', 'students_class_10',
        'students', 'admissions', 'all_students', 'students_list', 'student_roster', 'cached_students', 'students_data',
        'portal_students_cache', 'admitted_students_cache', 'school_students_roster'
      ];

      localKeys.forEach(k => {
        try {
          const raw = localStorage.getItem(k);
          if (raw) {
            const parsed = JSON.parse(raw);
            if (Array.isArray(parsed)) rawStudents.push(...parsed);
          }
        } catch(e) {}
      });

      // 4. Strict Deduplicate and normalize
      const seen = new Set();
      let uniqueStudents = [];
      rawStudents.forEach(item => {
        if (item && item.status === 'TC_OUT' || item.status === 'DELETED' || item.status === 'REMOVED') return;
        const norm = normalizeFinanceStudent(item);
        if (norm && (norm.name_en || norm.name_kn || norm.sts !== 'N/A')) {
          const stsKey = (norm.sts && norm.sts !== 'N/A') ? String(norm.sts).trim().toLowerCase() : '';
          const nameKey = (String(norm.name_en || norm.name_kn).trim() + '_' + String(norm.class).trim()).toLowerCase();

          const isDuplicate = (stsKey && seen.has(stsKey)) || (nameKey && seen.has(nameKey));

          if (!isDuplicate) {
            if (stsKey) seen.add(stsKey);
            if (nameKey) seen.add(nameKey);
            uniqueStudents.push(norm);
          }
        }
      });

      sampleStudents = uniqueStudents;
      applyRosterFilters();
    }

    function applyRosterFilters() {
      const q = (document.getElementById('col-roster-search')?.value || '').trim().toLowerCase();
      const cls = document.getElementById('col-class-dd')?.value || '';
      const status = document.getElementById('col-status-dd')?.value || '';
      const gender = document.getElementById('col-gender-dd')?.value || '';

      const tbody = document.getElementById('roster-table-tbody');
      const badge = document.getElementById('roster-count-badge');
      if (!tbody) return;

      const filtered = sampleStudents.filter(s => {
        const nameEn = (s.name_en || '').toLowerCase();
        const nameKn = (s.name_kn || '').toLowerCase();
        const sts = (s.sts || '').toLowerCase();
        const studentGender = s.gender || '';

        const normStudentClass = (s.class || '').toString().trim().toLowerCase().replace(/^class\s*/i, '');
        const normFilterClass = cls.trim().toLowerCase().replace(/^class\s*/i, '').split('/')[0];
        
        const matchClass = !cls || normStudentClass === normFilterClass || (cls.includes('LKG') && normStudentClass.includes('lkg')) || (cls.includes('UKG') && normStudentClass.includes('ukg'));

        const studentTrans = allTransactions.filter(t => 
          (t.student_id && String(t.student_id) === String(s.id)) ||
          (t.sts && String(t.sts) === String(s.sts)) ||
          (t.student_name_en && t.student_name_en === s.name_en) ||
          (t.student_name_kn && t.student_name_kn === s.name_kn)
        );

        const isAnyPaid = studentTrans.length > 0;

        const matchQ = !q || nameEn.includes(q) || nameKn.includes(q) || sts.includes(q);
        const matchGender = !gender || studentGender.toLowerCase() === gender.toLowerCase();
        const matchStatus = !status || (status === 'PAID' && isAnyPaid) || (status === 'PENDING' && !isAnyPaid);

        return matchQ && matchClass && matchGender && matchStatus;
      });

      if (badge) badge.textContent = filtered.length;

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="p-8 text-center text-slate-400 font-semibold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ವಿವರಗಳು ಕಂಡುಬಂದಿಲ್ಲ. / No student records found matching filters.</td></tr>`;
        return;
      }

      let html = '';
      filtered.forEach((s, idx) => {
        const studentTrans = allTransactions.filter(t => 
          (t.student_id && String(t.student_id) === String(s.id)) ||
          (t.sts && String(t.sts) === String(s.sts)) ||
          (t.student_name_en && t.student_name_en === s.name_en) ||
          (t.student_name_kn && t.student_name_kn === s.name_kn)
        );

        const normStClass = (s.class || '').toString().trim().toLowerCase().replace(/^class\s*/i, '');
        const applicableReasons = defaultFeeReasons.filter(r => {
          if (!r.active) return false;
          if (r.class === 'All' || !r.class) return true;
          const normRClass = r.class.toString().trim().toLowerCase().replace(/^class\s*/i, '');
          return normRClass === normStClass || (normRClass.includes('lkg') && normStClass.includes('lkg')) || (normRClass.includes('ukg') && normStClass.includes('ukg'));
        });

        let paidReasonsSum = 0;
        let paidCount = 0;
        let reasonPillsHtml = '';

        applicableReasons.forEach(r => {
          const isPaid = studentTrans.some(t => 
            t.fee_reason_id === r.id ||
            (t.fee_category && (t.fee_category.includes(r.name_kn) || t.fee_category.includes(r.name_en)))
          );

          if (isPaid) {
            paidReasonsSum += parseFloat(r.amount || 0);
            paidCount++;
            reasonPillsHtml += `
              <button type="button" onclick="toggleStudentFeeReasonPaid('${s.id}', '${r.id}', false)" title="ಪಾವತಿಸಲಾಗಿದೆ - 1-ಕ್ಲಿಕ್‌ನಲ್ಲಿ ರದ್ದುಗೊಳಿಸಿ (Click to Mark Unpaid)" class="px-2 py-0.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-extrabold text-[10px] flex items-center gap-1 shadow-2xs border-0 cursor-pointer transition">
                <i class="fa-solid fa-circle-check text-white"></i> ${r.name_kn} ₹${r.amount}
              </button>
            `;
          } else {
            reasonPillsHtml += `
              <button type="button" onclick="toggleStudentFeeReasonPaid('${s.id}', '${r.id}', true)" title="1-ಕ್ಲಿಕ್‌ನಲ್ಲಿ ಪಾವತಿಸಿ (Tap to Select as Paid)" class="px-2 py-0.5 bg-amber-50 hover:bg-amber-100 text-amber-800 dark:bg-amber-950/40 dark:text-amber-300 dark:hover:bg-amber-900/60 border border-amber-300 dark:border-amber-800/80 rounded-lg font-bold text-[10px] flex items-center gap-1 shadow-2xs border-0 cursor-pointer transition">
                <i class="fa-solid fa-plus-circle text-amber-500"></i> ${r.name_kn} ₹${r.amount}
              </button>
            `;
          }
        });

        let tickBadge = '';
        if (paidCount === applicableReasons.length && applicableReasons.length > 0) {
          tickBadge = `<span class="px-2.5 py-1 bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 rounded-full font-extrabold text-[10px] flex items-center justify-center gap-1 shadow-2xs"><i class="fa-solid fa-circle-check text-emerald-600 text-xs"></i> Full Paid</span>`;
        } else if (paidCount > 0) {
          tickBadge = `<span class="px-2.5 py-1 bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 rounded-full font-extrabold text-[10px] flex items-center justify-center gap-1 shadow-2xs"><i class="fa-solid fa-clock-rotate-left text-amber-600 text-xs"></i> Partial (${paidCount}/${applicableReasons.length})</span>`;
        } else {
          tickBadge = `<span class="px-2.5 py-1 bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 rounded-full font-extrabold text-[10px] flex items-center justify-center gap-1 shadow-2xs"><i class="fa-solid fa-triangle-exclamation text-rose-600 text-xs"></i> Pending</span>`;
        }

        const latestTrans = studentTrans[0];
        const dateStr = latestTrans ? `${latestTrans.payment_date} (${latestTrans.payment_mode})` : '-';

        html += `
          <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <td class="py-3 px-4 text-center">${tickBadge}</td>
            <td class="py-3 px-4 text-center font-mono font-semibold text-slate-500">${idx + 1}</td>
            <td class="py-3 px-4 font-mono font-bold text-sky-600 dark:text-sky-400">${s.sts || 'N/A'}</td>
            <td class="py-3 px-4">
              <div class="font-bold text-slate-900 dark:text-white text-xs">${s.name_kn || s.name_en}</div>
              <div class="text-[10px] text-slate-400 font-medium">${s.name_en} • Father: ${s.father || 'N/A'}</div>
            </td>
            <td class="py-3 px-4 text-center font-bold">${s.class}</td>
            <td class="py-3 px-4">
              <div class="flex flex-wrap items-center gap-1.5">${reasonPillsHtml}</div>
            </td>
            <td class="py-3 px-4 text-right font-mono font-black text-emerald-600 dark:text-emerald-400 text-sm">₹ ${paidReasonsSum}</td>
            <td class="py-3 px-4 text-center font-mono text-xs text-slate-500">${dateStr}</td>
            <td class="py-3 px-4 text-center no-print">
              <div class="flex items-center justify-center gap-1.5">
                <button onclick="openCollectFeeModal('${s.sts}')" title="Collect Custom Fee / ಶುಲ್ಕ ಸ್ವೀಕರಿಸಿ" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-3 py-1.5 rounded-xl text-[11px] transition shadow-2xs border-0 cursor-pointer flex items-center gap-1">
                  <i class="fa-solid fa-receipt"></i> Modal Counter
                </button>
                ${latestTrans ? `
                  <button onclick="openReceiptModal('${latestTrans.id}')" title="View Receipt" class="w-7 h-7 rounded-xl bg-sky-50 hover:bg-sky-100 text-sky-600 flex items-center justify-center border border-sky-200 cursor-pointer">
                    <i class="fa-solid fa-eye text-xs"></i>
                  </button>
                ` : ''}
              </div>
            </td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    async function toggleStudentFeeReasonPaid(studentId, feeReasonId, markPaid) {
      const student = sampleStudents.find(s => String(s.id) === String(studentId));
      const reason = defaultFeeReasons.find(r => String(r.id) === String(feeReasonId));
      if (!student || !reason) return;

      if (markPaid) {
        const record = {
          id: 'FEE-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
          receipt_no: 'REC-2026-' + Math.floor(1000 + Math.random() * 9000),
          student_id: student.id,
          sts: student.sts,
          student_name_en: student.name_en,
          student_name_kn: student.name_kn,
          enroll_class: student.class,
          fee_reason_id: reason.id,
          fee_category: `${reason.name_kn} (${reason.name_en})`,
          amount: parseFloat(reason.amount || 0),
          payment_mode: 'Cash',
          payment_date: new Date().toISOString().split('T')[0],
          created_at: new Date().toISOString()
        };

        allTransactions.unshift(record);

        if (window.supabaseClient) {
          try {
            await supabaseClient.from('fee_collections').insert([record]);
          } catch(e) {
            console.warn("Supabase fee insert notice:", e);
          }
        }
      } else {
        allTransactions = allTransactions.filter(t => {
          const isSameStudent = (t.student_id && String(t.student_id) === String(student.id)) ||
                                (t.sts && String(t.sts) === String(student.sts)) ||
                                (t.student_name_en === student.name_en) ||
                                (t.student_name_kn === student.name_kn);
          const isSameReason = (t.fee_reason_id && String(t.fee_reason_id) === String(reason.id)) ||
                               (t.fee_category && (t.fee_category.includes(reason.name_kn) || t.fee_category.includes(reason.name_en)));
          return !(isSameStudent && isSameReason);
        });

        if (window.supabaseClient) {
          try {
            await supabaseClient.from('fee_collections').delete().eq('student_name_en', student.name_en);
          } catch(e) {}
        }
      }

      localStorage.setItem('portal_fee_transactions', JSON.stringify(allTransactions));
      applyRosterFilters();
      renderFinanceKPIs();
      renderCategoryChart();
      renderClasswiseProgress();
    }

    // Modal Fee Collection Functions (Inspired by NewAdmissionList.html)
    function openCollectFeeModal(sts) {
      selectedModalStudent = sampleStudents.find(s => s.sts === sts);
      if (!selectedModalStudent) return;

      document.getElementById('modal-sel-name').textContent = `${selectedModalStudent.name_kn || selectedModalStudent.name_en} (${selectedModalStudent.name_en})`;
      document.getElementById('modal-sel-sub').textContent = `Class: ${selectedModalStudent.class} • STS: ${selectedModalStudent.sts} • Father: ${selectedModalStudent.father || 'N/A'}`;

      // Render Modal Fee Reasons Checklist
      const tbody = document.getElementById('modal-fee-tbody');
      let html = '';
      defaultFeeReasons.forEach((r, idx) => {
        html += `
          <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <td class="py-2.5 px-3 text-center">
              <input type="checkbox" class="modal-fee-cb w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500 cursor-pointer" data-amount="${r.amount}" data-name="${r.name_kn} (${r.name_en})" ${idx < 2 ? 'checked' : ''} onchange="recalculateModalTotal()">
            </td>
            <td class="py-2.5 px-3 font-bold">
              <span class="text-slate-900 dark:text-white block">${r.name_kn}</span>
              <span class="text-[9px] text-slate-400 font-medium">${r.name_en}</span>
            </td>
            <td class="py-2.5 px-3 text-right font-mono font-black text-emerald-600 dark:text-emerald-400">₹ ${r.amount}</td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
      recalculateModalTotal();

      document.getElementById('collect-fee-modal').classList.remove('hidden');
    }

    function closeCollectFeeModal() {
      document.getElementById('collect-fee-modal').classList.add('hidden');
    }

    function recalculateModalTotal() {
      let sum = 0;
      document.querySelectorAll('.modal-fee-cb:checked').forEach(cb => {
        sum += parseFloat(cb.getAttribute('data-amount') || 0);
      });
      document.getElementById('modal-total-display').textContent = '₹ ' + sum;
      document.getElementById('modal-total-input').value = sum;
    }

    async function submitModalFeeCollection() {
      if (!selectedModalStudent) return;

      const totalAmt = parseFloat(document.getElementById('modal-total-input').value || 0);
      if (totalAmt <= 0) {
        alert("ದಯವಿಟ್ಟು ಕನಿಷ್ಠ ಒಂದು ಶುಲ್ಕ ವಿಭಾಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ. / Please select at least one fee category.");
        return;
      }

      const selectedReasons = Array.from(document.querySelectorAll('.modal-fee-cb:checked')).map(cb => cb.getAttribute('data-name')).join(', ');
      const mode = document.getElementById('modal-mode-select').value;
      const date = document.getElementById('modal-date-input').value;
      const receiptNo = 'REC-2026-' + Math.floor(1000 + Math.random() * 9000);

      const record = {
        id: 'FEE-' + Date.now(),
        receipt_no: receiptNo,
        student_name_en: selectedModalStudent.name_en,
        student_name_kn: selectedModalStudent.name_kn,
        enroll_class: selectedModalStudent.class,
        fee_category: selectedReasons,
        amount: totalAmt,
        payment_mode: mode,
        payment_date: date,
        created_at: new Date().toISOString()
      };

      try {
        if (window.supabaseClient) {
          await supabaseClient.from('fee_collections').insert([record]);
        }
      } catch (err) {}

      allTransactions.unshift(record);
      localStorage.setItem('portal_fee_transactions', JSON.stringify(allTransactions));

      closeCollectFeeModal();
      openReceiptModal(record.id);
      renderFinanceKPIs();
      applyRosterFilters();
      applyFinanceFilters();
    }

    // Finance Data Loading
    async function loadFinanceData() {
      try {
        let transactions = [];
        if (window.supabaseClient) {
          const { data, error } = await supabaseClient
            .from('fee_collections')
            .select('*')
            .order('created_at', { ascending: false });
          if (!error && data && data.length > 0) transactions = data;
        }

        const localData = JSON.parse(localStorage.getItem('portal_fee_transactions') || '[]');
        if (localData.length > 0) {
          const existingIds = transactions.map(t => t.id);
          localData.forEach(lt => {
            if (!existingIds.includes(lt.id)) transactions.push(lt);
          });
        }

        // Filter out any legacy dummy transactions (e.g. AADHYA/STS281626778)
        transactions = transactions.filter(t => t.student_name_en !== 'AADHYA' && t.sts !== 'STS281626778');

        allTransactions = transactions;
        renderFinanceKPIs();
        renderCategoryChart();
        renderClasswiseProgress();
        applyFinanceFilters();
      } catch (err) {
        console.error(err);
      }
    }

    function renderFinanceKPIs() {
      let totalAmt = 0, todayAmt = 0, todayCount = 0;
      const todayStr = new Date().toISOString().split('T')[0];

      allTransactions.forEach(t => {
        const amt = parseFloat(t.amount || 0);
        totalAmt += amt;
        if (t.payment_date === todayStr || (t.created_at && t.created_at.startsWith(todayStr))) {
          todayAmt += amt;
          todayCount++;
        }
      });

      document.getElementById('stat-total-collected').textContent = '₹ ' + totalAmt.toLocaleString('en-IN');
      document.getElementById('stat-collected-count').textContent = allTransactions.length;
      document.getElementById('stat-today-collected').textContent = '₹ ' + todayAmt.toLocaleString('en-IN');
      document.getElementById('stat-today-count').textContent = todayCount;

      const totalEnrolled = 505;
      const pendingCount = Math.max(0, totalEnrolled - allTransactions.length);
      const estimatedPending = pendingCount * 200;

      document.getElementById('stat-pending-dues').textContent = '₹ ' + estimatedPending.toLocaleString('en-IN');
      document.getElementById('stat-pending-count').textContent = pendingCount;
    }

    function renderCategoryChart() {
      const ctx = document.getElementById('categoryFeeChart')?.getContext('2d');
      if (!ctx) return;

      if (categoryChartInstance) categoryChartInstance.destroy();

      categoryChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Exam Fee', 'ID Card', 'Sports Fund', 'SDMC Fund', 'Admission Fee'],
          datasets: [{
            data: [4500, 1500, 1500, 3000, 2000],
            backgroundColor: ['#10b981', '#06b6d4', '#6366f1', '#f59e0b', '#ec4899']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }

    function renderClasswiseProgress() {
      const container = document.getElementById('classwise-progress-container');
      if (!container) return;

      const classes = ['LKG', 'UKG', '1', '2', '3', '4', '5', '6', '7'];
      let html = '';
      classes.forEach(cls => {
        html += `
          <div>
            <div class="flex justify-between text-xs font-bold mb-1">
              <span>Class ${cls}</span>
              <span>18 / 30 Collected (60%)</span>
            </div>
            <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
              <div class="bg-emerald-500 h-full rounded-full" style="width: 60%"></div>
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
    }

    function applyFinanceFilters() {
      const q = document.getElementById('finance-search').value.trim().toLowerCase();
      const cls = document.getElementById('finance-class-filter').value;
      const tbody = document.getElementById('finance-transactions-tbody');

      const filtered = allTransactions.filter(t => {
        const nameEn = (t.student_name_en || '').toLowerCase();
        const nameKn = (t.student_name_kn || '').toLowerCase();
        const recNo = (t.receipt_no || t.id || '').toLowerCase();
        const studentClass = (t.enroll_class || '').toString();

        const matchQ = !q || nameEn.includes(q) || nameKn.includes(q) || recNo.includes(q);
        const matchClass = !cls || studentClass === cls;

        return matchQ && matchClass;
      });

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="p-8 text-center text-slate-400">ಯಾವುದೇ ಶುಲ್ಕ ರಸೀದಿಗಳು ಕಂಡುಬಂದಿಲ್ಲ.</td></tr>`;
        return;
      }

      let html = '';
      filtered.forEach((t, idx) => {
        html += `
          <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <td class="py-3 px-4 text-center font-mono text-slate-500">${idx + 1}</td>
            <td class="py-3 px-4 font-mono font-bold text-emerald-600">${t.receipt_no || t.id}</td>
            <td class="py-3 px-4 font-bold">${t.student_name_kn || t.student_name_en}</td>
            <td class="py-3 px-4 text-center font-bold">${t.enroll_class || '-'}</td>
            <td class="py-3 px-4 font-medium text-slate-600">${t.fee_category}</td>
            <td class="py-3 px-4 text-center"><span class="px-2 py-0.5 bg-slate-100 rounded text-[10px] font-bold">${t.payment_mode}</span></td>
            <td class="py-3 px-4 text-right font-mono font-black text-sm">₹ ${t.amount}</td>
            <td class="py-3 px-4 text-center font-mono text-slate-500">${t.payment_date}</td>
            <td class="py-3 px-4 text-center no-print">
              <div class="flex items-center justify-center gap-1.5">
                <button onclick="openReceiptModal('${t.id}')" title="View Receipt" class="w-7 h-7 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center border border-sky-200 cursor-pointer">
                  <i class="fa-solid fa-eye text-xs"></i>
                </button>
                <button onclick="sendWhatsAppReceipt('${t.id}')" title="WhatsApp Receipt" class="w-7 h-7 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-200 cursor-pointer">
                  <i class="fa-brands fa-whatsapp text-xs"></i>
                </button>
              </div>
            </td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    function openReceiptModal(transId) {
      const trans = allTransactions.find(t => t.id === transId);
      if (!trans) return;

      const html = `
        <div class="border-2 border-slate-800 p-6 rounded-2xl bg-white text-slate-900 space-y-4">
          <div class="flex items-center gap-3 border-b-2 border-slate-800 pb-3">
            <div class="flex-1">
              <h2 class="text-xs font-black uppercase text-slate-900 tracking-wider">GHPS MARCHED</h2>
              <p class="text-[10px] font-bold text-slate-600">ಅಧಿಕೃತ ಶುಲ್ಕ ರಸೀದಿ / OFFICIAL FEE RECEIPT</p>
            </div>
            <div class="text-right font-mono">
              <span class="text-[9px] font-bold block text-slate-500">Receipt No:</span>
              <span class="text-xs font-black text-emerald-700">${trans.receipt_no || trans.id}</span>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-2 text-xs font-bold border-b border-slate-200 pb-3">
            <div><span class="text-slate-400 text-[10px] block">Student:</span><span>${trans.student_name_kn || trans.student_name_en}</span></div>
            <div><span class="text-slate-400 text-[10px] block">Class:</span><span>${trans.enroll_class}</span></div>
            <div><span class="text-slate-400 text-[10px] block">Date:</span><span>${trans.payment_date}</span></div>
            <div><span class="text-slate-400 text-[10px] block">Mode:</span><span>${trans.payment_mode}</span></div>
          </div>
          <div class="py-2 text-xs font-bold">
            <p>Reason: ${trans.fee_category}</p>
            <p class="text-right font-mono text-sm text-emerald-700 mt-2">Total Paid: ₹ ${trans.amount}</p>
          </div>
        </div>
      `;

      document.getElementById('receipt-printable-area').innerHTML = html;
      document.getElementById('receipt-modal').classList.remove('hidden');
    }

    function closeReceiptModal() {
      document.getElementById('receipt-modal').classList.add('hidden');
    }

    function printModalReceipt() {
      const content = document.getElementById('receipt-printable-area').innerHTML;
      const win = window.open('', '_blank');
      win.document.write(`<html><head><title>Fee Receipt</title><script src="https://cdn.tailwindcss.com"><\/script></head><body class="p-8">${content}<script>window.onload = function() { window.print(); window.close(); };<\/script></body></html>`);
      win.document.close();
    }

    function sendWhatsAppReceipt(transId) {
      const trans = allTransactions.find(t => t.id === transId);
      if (!trans) return;
      const msg = `ಆತ್ಮೀಯ ಪೋಷಕರೇ, GHPS ಮರ್ಚೆಡ್ ಶಾಲೆಯಲ್ಲಿ ನಿಮ್ಮ ಮಗ/ಮಗಳು ${trans.student_name_kn || trans.student_name_en} ಅವರ ${trans.fee_category} ₹${trans.amount} ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ರಸೀದಿ ನಂ: ${trans.receipt_no || trans.id}.`;
      window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, '_blank');
    }

    function exportFinanceExcel() {
      const data = allTransactions.map((t, i) => ({
        "Sl.No": i + 1,
        "Receipt No": t.receipt_no || t.id,
        "Student Name (EN)": t.student_name_en,
        "Student Name (KN)": t.student_name_kn,
        "Class": t.enroll_class,
        "Fee Category": t.fee_category,
        "Amount (INR)": t.amount,
        "Payment Date": t.payment_date
      }));
      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Finance");
      XLSX.writeFile(wb, "Finance_Report_2026-27.xlsx");
    }

    function openBarcodeScanner() {
      document.getElementById('barcode-modal').classList.remove('hidden');
      if (typeof Html5Qrcode !== 'undefined') {
        html5QrcodeScannerInstance = new Html5Qrcode("qr-reader");
        html5QrcodeScannerInstance.start(
          { facingMode: "environment" },
          { fps: 10, qrbox: { width: 200, height: 200 } },
          (decodedText) => {
            document.getElementById('col-roster-search').value = decodedText;
            applyRosterFilters();
            closeBarcodeScanner();
          },
          (errorMessage) => {}
        ).catch(err => {});
      }
    }

    function closeBarcodeScanner() {
      document.getElementById('barcode-modal').classList.add('hidden');
      if (html5QrcodeScannerInstance && html5QrcodeScannerInstance.isScanning) {
        html5QrcodeScannerInstance.stop().catch(err => {});
      }
    }
  