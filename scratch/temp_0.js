
    const supabaseUrl = "https://gsayvnnnfrrkwdfwocbu.supabase.co";
    const supabaseKey = "sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS";
    const supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);
    window.supabaseClient = supabaseClient;

    function updateClock() {
      const now = new Date();
      let h = now.getHours(), m = now.getMinutes(), s = now.getSeconds();
      const ampm = h >= 12 ? 'PM' : 'AM';
      h = h % 12; h = h ? h : 12;
      m = m < 10 ? '0'+m : m; s = s < 10 ? '0'+s : s;
      const clockEl = document.getElementById('liveClock');
      if (clockEl) clockEl.innerText = h + ':' + m + ':' + s + ' ' + ampm;
      const dateEl = document.getElementById('liveDate');
      if (dateEl) dateEl.innerText = now.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', weekday: 'short' });
    }
    setInterval(updateClock, 1000); updateClock();

    function toggleAccordion(menuId) {
      const menu = document.getElementById(menuId);
      const arrow = document.getElementById(menuId + '-arrow');
      if (menu) {
        if (menu.classList.contains('hidden')) {
          menu.classList.remove('hidden');
          if (arrow) arrow.classList.add('rotate-90');
        } else {
          menu.classList.add('hidden');
          if (arrow) arrow.classList.remove('rotate-90');
        }
      }
    }

    function initSidebar() {
      const path = window.location.pathname.split('/').pop();
      if (path === 'dashboard.html' || path === '') {
        const dashLink = document.getElementById('nav-Dashboard');
        if (dashLink) dashLink.classList.add('bg-indigo-50', 'text-indigo-800');
      } else if (path === 'teachers.html') {
        expandMenu('menu-teachers');
        highlightSubItem('menu-teachers', 'teachers.html');
      } else if (path === 'NewAdmission.html') {
        expandMenu('menu-students');
        highlightSubItem('menu-students', 'NewAdmission.html');
      } else if (path === 'NewAdmissionList.html') {
        expandMenu('menu-students');
        highlightSubItem('menu-students', 'NewAdmissionList.html');
      } else if (path === 'StudentList.html') {
        expandMenu('menu-students');
        highlightSubItem('menu-students', 'StudentList.html');
      } else if (path === 'StudentUpdate.html') {
        expandMenu('menu-students');
        highlightSubItem('menu-students', 'StudentUpdate.html');
      } else if (path === 'ApaarModule.html') {
        expandMenu('menu-students');
        highlightSubItem('menu-students', 'ApaarModule.html');
      } else if (path === 'BridgeCourse.html') {
        expandMenu('menu-academic');
        highlightSubItem('menu-academic', 'BridgeCourse.html');
      } else if (path === 'CceAssessmet.html') {
        expandMenu('menu-academic');
        highlightSubItem('menu-academic', 'CceAssessmet.html');
      } else if (path === 'LbaAssessment.html') {
        expandMenu('menu-academic');
        highlightSubItem('menu-academic', 'LbaAssessment.html');
      } else if (path === 'FlnAssessment.html') {
        expandMenu('menu-academic');
        highlightSubItem('menu-academic', 'FlnAssessment.html');
      }
    }

    function expandMenu(menuId) {
      const menu = document.getElementById(menuId);
      const arrow = document.getElementById(menuId + '-arrow');
      if (menu) menu.classList.remove('hidden');
      if (arrow) arrow.classList.add('rotate-90');
    }

    function highlightSubItem(menuId, href) {
      const menu = document.getElementById(menuId);
      if (!menu) return;
      const links = menu.getElementsByTagName('a');
      for (let link of links) {
        if (link.getAttribute('href') === href) {
          link.classList.remove('text-slate-500');
          link.classList.add('text-indigo-600', 'font-bold');
        }
      }
    }

    async function handleLogout() {
      await supabaseClient.auth.signOut();
      window.location.href = "index.html";
    }

    const prePrimarySubjects = ["ಕನ್ನಡ / Kannada", "English", "ಗಣಿತ / Maths", "ಸಾಮಾನ್ಯ ಜ್ಞಾನ / General Knowledge", "ರೇಖಾಚಿತ್ರ & ಚಟುವಟಿಕೆಗಳು / Drawing & Activities"];
    const primarySubjects = ["ಕನ್ನಡ / Kannada", "English", "ಗಣಿತ / Maths", "ಪರಿಸರ ಅಧ್ಯಯನ / Environment"];
    const middleSubjects = ["ಕನ್ನಡ / Kannada", "English", "ಹಿಂದಿ / Hindi", "ಸಮಾಜ ವಿಜ್ಞಾನ / Social Science", "ವಿಜ್ಞಾನ / Science", "ಗಣಿತ / Math"];

    let lessonConfigData = {
      "1": { "ಕನ್ನಡ / Kannada": ["ಪಾಠ 1", "ಪಾಠ 2"], "English": ["Lesson 1"] },
      "6": { "ಕನ್ನಡ / Kannada": ["ಪಾಠ 1: ಶ್ರಮದಾನ", "ಪಾಠ 2: ಮಳೆಗಾಲ"], "ವಿಜ್ಞಾನ / Science": ["Chapter 1", "Chapter 2"] }
    };
    let currentSchoolId = localStorage.getItem("school_id") || null;

    const gradeScale10 = { 'A+': 9, 'A': 7, 'B+': 5, 'B': 3, 'C': 0 };

    let currentLessons = [];
    let students = [];
    let evaluations = {};
    let isEditing = false;
    let originalEvaluations = {};
    let currentViewMode = localStorage.getItem('lba_view_mode') || 'cards';
    let genderFilter = '';
    let searchQuery = '';

    const classFilter = document.getElementById('class-filter');
    const subjectFilter = document.getElementById('subject-filter');

    if (classFilter) {
      classFilter.addEventListener('change', () => {
        const cls = classFilter.value;
        if (subjectFilter) {
          subjectFilter.innerHTML = '<option value="">-- ವಿಷಯ ಆಯ್ಕೆಮಾಡಿ --</option>';
          if (cls) {
            let subjects = primarySubjects;
            if (['LKG', 'UKG'].includes(cls)) {
              subjects = prePrimarySubjects;
            } else if (['6', '7', '8', '9', '10'].includes(cls)) {
              subjects = middleSubjects;
            }
            subjects.forEach(sub => {
              subjectFilter.innerHTML += `<option value="${sub}">${sub}</option>`;
            });
          }
        }
        resetToEmptyState();
      });
    }

    if (subjectFilter) {
      subjectFilter.addEventListener('change', () => {
        if (classFilter && classFilter.value && subjectFilter.value) {
          document.getElementById('rules-note-card').classList.remove('hidden');
          checkAndLoadGrid();
        } else {
          resetToEmptyState();
        }
      });
    }

    document.addEventListener("DOMContentLoaded", async function() {
      await initUserAndTheme();
      const { data: { session } } = await supabaseClient.auth.getSession();
      if (!session) {
        window.location.href = "index.html";
        return;
      }
      initSidebar();

      // Load config data from Supabase if currentSchoolId is available
      let loadedFromDb = false;
      if (currentSchoolId) {
        try {
          const { data, error } = await supabaseClient
            .from('school_settings')
            .select('settings_value')
            .eq('school_id', currentSchoolId)
            .eq('settings_key', 'lba_lesson_config')
            .maybeSingle();

          if (!error && data && data.settings_value) {
            lessonConfigData = data.settings_value;
            console.log("Loaded LBA lesson config from Supabase");
            localStorage.setItem(`lba_lesson_config_${currentSchoolId}`, JSON.stringify(lessonConfigData));
            loadedFromDb = true;
          }
        } catch (dbErr) {
          console.warn("Failed to load LBA configs from Supabase:", dbErr);
        }
      }

      if (!loadedFromDb) {
        // Fallback to localStorage safely per school
        const key = currentSchoolId ? `lba_lesson_config_${currentSchoolId}` : 'lba_lesson_config';
        if (localStorage.getItem(key)) {
          try {
            lessonConfigData = JSON.parse(localStorage.getItem(key));
          } catch (e) {
            console.error("Failed to parse lba_lesson_config from localStorage:", e);
          }
        } else {
          // Fallback to legacy key
          const legacyConfig = localStorage.getItem('lba_lesson_config');
          if (legacyConfig) {
            try {
              lessonConfigData = JSON.parse(legacyConfig);
              if (currentSchoolId) {
                localStorage.setItem(key, legacyConfig);
              }
            } catch(e){}
          }
        }
      }

      updateCfgSubjectDropdown();
      loadLessonsIntoConfigTextarea();

      // Check query parameters
      const urlParams = new URLSearchParams(window.location.search);
      const paramClass = urlParams.get('class');
      const paramSubject = urlParams.get('subject');
      
      if (paramClass && classFilter) {
        classFilter.value = paramClass;
        classFilter.dispatchEvent(new Event('change'));
        if (paramSubject && subjectFilter) {
          subjectFilter.value = paramSubject;
          subjectFilter.dispatchEvent(new Event('change'));
        }
      }
    });

    function toggleSettingsPanel() {
      const panel = document.getElementById('settings-panel');
      if (panel) {
        const isOpening = panel.classList.contains('hidden');
        panel.classList.toggle('hidden');
        if (isOpening) {
          const mainClass = document.getElementById('class-filter') ? document.getElementById('class-filter').value : '';
          const mainSub = document.getElementById('subject-filter') ? document.getElementById('subject-filter').value : '';
          if (mainClass) {
            const cfgClassSel = document.getElementById('cfg-class-select');
            if (cfgClassSel) {
              cfgClassSel.value = mainClass;
              updateCfgSubjectDropdown();
              const cfgSubSel = document.getElementById('cfg-subject-select');
              if (mainSub && cfgSubSel) {
                const options = Array.from(cfgSubSel.options);
                if (options.some(o => o.value === mainSub)) {
                  cfgSubSel.value = mainSub;
                  loadLessonsIntoConfigTextarea();
                }
              }
            }
          }
        }
      }
    }

    function updateCfgSubjectDropdown() {
      const clsEl = document.getElementById('cfg-class-select');
      const subSelect = document.getElementById('cfg-subject-select');
      if (!clsEl || !subSelect) return;
      
      const cls = clsEl.value;
      let subjects = primarySubjects;
      if (['LKG', 'UKG'].includes(cls)) {
        subjects = prePrimarySubjects;
      } else if (['6', '7', '8', '9', '10'].includes(cls)) {
        subjects = middleSubjects;
      }
      
      subSelect.innerHTML = '';
      subjects.forEach(sub => {
        subSelect.innerHTML += `<option value="${sub}">${sub}</option>`;
      });
      loadLessonsIntoConfigTextarea();
    }

    function loadLessonsIntoConfigTextarea() {
      const clsEl = document.getElementById('cfg-class-select');
      const subSelect = document.getElementById('cfg-subject-select');
      const input = document.getElementById('cfg-lessons-input');
      if (!clsEl || !subSelect || !input) return;
      
      const cls = clsEl.value;
      const sub = subSelect.value;
      
      if (lessonConfigData[cls] && lessonConfigData[cls][sub]) {
        input.value = lessonConfigData[cls][sub].join(', ');
      } else {
        input.value = "ಪಾಠ 1, ...";
      }
    }

    function applyLessonSettings() {
      const cls = document.getElementById('cfg-class-select').value;
      const sub = document.getElementById('cfg-subject-select').value;
      const inputVal = document.getElementById('cfg-lessons-input').value;

      const lessonsArray = inputVal.split(',').map(s => s.trim()).filter(Boolean);

      if (!lessonConfigData[cls]) lessonConfigData[cls] = {};
      lessonConfigData[cls][sub] = lessonsArray;

      const key = currentSchoolId ? `lba_lesson_config_${currentSchoolId}` : 'lba_lesson_config';
      localStorage.setItem(key, JSON.stringify(lessonConfigData));

      if (currentSchoolId) {
        supabaseClient
          .from('school_settings')
          .upsert({
            school_id: currentSchoolId,
            settings_key: 'lba_lesson_config',
            settings_value: lessonConfigData,
            updated_at: new Date().toISOString()
          }, { onConflict: 'school_id,settings_key' })
          .then(({ error }) => {
            if (error) {
              console.warn("Failed to persist LBA configs to Supabase:", error);
            } else {
              console.log("Successfully persisted LBA configs to Supabase");
            }
          });
      }

      showToast("ಪಾಠಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!", "success");
      toggleSettingsPanel();
      if (classFilter && subjectFilter && classFilter.value === cls && subjectFilter.value === sub) { checkAndLoadGrid(); }
    }

    function determineGrade(marks) {
      if (marks === '' || marks === null || undefined === marks) return '-';
      const m = parseFloat(marks);
      if (m >= gradeScale10['A+']) return 'A+';
      if (m >= gradeScale10['A']) return 'A';
      if (m >= gradeScale10['B+']) return 'B+';
      if (m >= gradeScale10['B']) return 'B';
      return 'C';
    }

    function normalizeClass(classStr) {
      if (!classStr) return "";
      let clean = classStr.toString().trim().toLowerCase();
      
      if (!clean.includes("lkg")) {
        clean = clean.replace(/class/g, "###").replace(/l/g, "i").replace(/###/g, "class");
      }
      
      if (clean.includes("lkg") || clean.includes("kg1") || clean.includes("kg 1")) return "LKG";
      if (clean.includes("ukg") || clean.includes("kg2") || clean.includes("kg 2")) return "UKG";
      
      if (clean === "1" || clean === "1st" || clean === "class 1" || clean === "class i" || clean === "i") return "1";
      if (clean === "2" || clean === "2nd" || clean === "class 2" || clean === "class ii" || clean === "ii") return "2";
      if (clean === "3" || clean === "3rd" || clean === "class 3" || clean === "class iii" || clean === "iii") return "3";
      if (clean === "4" || clean === "4th" || clean === "class 4" || clean === "class iv" || clean === "iv") return "4";
      if (clean === "5" || clean === "5th" || clean === "class 5" || clean === "class v" || clean === "v") return "5";
      if (clean === "6" || clean === "6th" || clean === "class 6" || clean === "class vi" || clean === "vi") return "6";
      if (clean === "7" || clean === "7th" || clean === "class 7" || clean === "class vii" || clean === "vii") return "7";
      if (clean === "8" || clean === "8th" || clean === "class 8" || clean === "class viii" || clean === "viii") return "8";
      if (clean === "9" || clean === "9th" || clean === "class 9" || clean === "class ix" || clean === "ix") return "9";
      if (clean === "10" || clean === "10th" || clean === "class 10" || clean === "class x" || clean === "x") return "10";
      
      return classStr.toString().trim();
    }

    async function checkAndLoadGrid() {
      const className = classFilter.value;
      const subjectName = subjectFilter.value;
      if (!className || !subjectName) return;

      document.getElementById('loading-overlay').classList.remove('hidden');
      document.getElementById('empty-state').classList.add('hidden');
      document.getElementById('competency-table').classList.add('hidden');
      document.getElementById('stats-bar').classList.add('hidden');
      if (document.getElementById('btn-save-pdf')) document.getElementById('btn-save-pdf').classList.add('hidden');
      document.getElementById('btn-print-report').classList.add('hidden');
      document.getElementById('btn-export-excel').classList.add('hidden');
      if (document.getElementById('btn-export-csv')) document.getElementById('btn-export-csv').classList.add('hidden');
      if (document.getElementById('btn-import-csv')) document.getElementById('btn-import-csv').classList.add('hidden');
      if (document.getElementById('btn-add-student')) document.getElementById('btn-add-student').classList.add('hidden');
      hideActionButtons();

      if (lessonConfigData[className] && lessonConfigData[className][subjectName]) {
        currentLessons = lessonConfigData[className][subjectName];
      } else {
        currentLessons = ["ಪಾಠ 1", "ಪಾಠ 2", "ಪಾಠ 3"];
      }

      try {
        // Retrieve all student admissions to filter in-memory via normalizeClass to handle database discrepancies
        const { data: { session } } = await supabaseClient.auth.getSession();
        const schoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id"));

        let query = supabaseClient.from('admissions').select('id, student_name, name_english, father_name_kn, father_name_az, mother_name_kn, mother_name_az, app_no, student_sts, enroll_class, gender, caste, status').neq('is_admitted', false);
        if (schoolId) {
          query = query.or(`school_id.eq.${schoolId},school_id.is.null`);
        }

        const { data, error } = await query;

        if (error) throw error;

        const localTrashed = JSON.parse(localStorage.getItem('trashed_students_list') || '[]');
        const trashedKeys = new Set(localTrashed.map(t => String(t.id || t.app_no || t.student_sts || '').replace(/\s+/g, '').toLowerCase()));

        const roster = (data || [])
          .filter(s => {
            const isNotOut = s.status !== 'TC_OUT' && s.status !== 'DELETED' && s.status !== 'REMOVED';
            const sKey1 = String(s.id || '').replace(/\s+/g, '').toLowerCase();
            const sKey2 = String(s.student_sts || s.app_no || '').replace(/\s+/g, '').toLowerCase();
            const isNotTrashed = (!sKey1 || !trashedKeys.has(sKey1)) && (!sKey2 || !trashedKeys.has(sKey2));
            const isClass = normalizeClass(s.enroll_class) === normalizeClass(className);
            return isNotOut && isNotTrashed && isClass;
          })
          .map(s => ({
            id: s.id,
            student_name_kn: s.student_name || '',
            student_name: s.student_name || '',
            name_english: s.name_english || '',
            father_name_kn: s.father_name_kn || '',
            father_name_az: s.father_name_az || '',
            mother_name_kn: s.mother_name_kn || '',
            mother_name_az: s.mother_name_az || '',
            gender: s.gender || '',
            caste: s.caste || '',
            adminNo: s.app_no,
            app_no: s.app_no || ''
          }))
          .sort((a, b) => {
            const nameA = (a.name_english || a.student_name_kn || '').trim().toUpperCase();
            const nameB = (b.name_english || b.student_name_kn || '').trim().toUpperCase();
            return nameA.localeCompare(nameB);
          });

        let parsedEval = {};
        const loadLocal = () => {
          const mockKey = `lba_mock_${className}_${subjectName.replace(/[^a-zA-Z0-9]/g, '_')}`;
          let saved = localStorage.getItem(mockKey);
          if (saved) {
            try { return JSON.parse(saved); } catch (e) { return {}; }
          }
          return {};
        };

        try {
          const { data: dbRecords, error: dbError } = await supabaseClient
            .from('lba_evaluations')
            .select('student_id, lessons')
            .eq('class_name', className)
            .eq('subject_name', subjectName);
          
          if (dbError) {
            console.warn("Supabase fetch for LBA evaluations failed, using local storage:", dbError);
            parsedEval = loadLocal();
          } else if (dbRecords && dbRecords.length > 0) {
            dbRecords.forEach(r => {
              parsedEval[r.student_id] = r.lessons || {};
            });
            console.log("Loaded LBA evaluations from Supabase");
          } else {
            parsedEval = loadLocal();
          }
        } catch (e) {
          console.warn("Exception loading LBA evaluations from Supabase, using local storage:", e);
          parsedEval = loadLocal();
        }

        onDataLoaded({
          success: true,
          students: roster,
          evaluations: parsedEval
        });
      } catch (err) {
        onDataLoadFailed(err);
      }
    }

    function onDataLoaded(response) {
      document.getElementById('loading-overlay').classList.add('hidden');
      if (!response.success) { resetToEmptyState(); return; }

      students = response.students || [];
      evaluations = response.evaluations || {};
      originalEvaluations = JSON.parse(JSON.stringify(evaluations));

      if (students.length === 0) { resetToEmptyState(); return; }

      document.getElementById('grid-subtitle').innerText = `${classFilter.value} | ವಿಷಯ: ${subjectFilter.value}`;
      document.getElementById('stats-bar').classList.remove('hidden');
      const sfBar = document.getElementById('search-filter-bar');
      if (sfBar) sfBar.classList.remove('hidden');
      
      if (document.getElementById('btn-save-pdf')) document.getElementById('btn-save-pdf').classList.remove('hidden');
      document.getElementById('btn-print-report').classList.remove('hidden');
      document.getElementById('btn-export-excel').classList.remove('hidden');
      if (document.getElementById('btn-export-csv')) document.getElementById('btn-export-csv').classList.remove('hidden');
      if (document.getElementById('btn-import-csv')) document.getElementById('btn-import-csv').classList.remove('hidden');
      if (document.getElementById('btn-add-student')) document.getElementById('btn-add-student').classList.remove('hidden');
      
      const hasSavedData = Object.keys(evaluations).length > 0;
      setMode(!hasSavedData);
      buildTableHeader();
      setViewMode(currentViewMode, false);
      renderActiveView();
    }

    function onDataLoadFailed(err) {
      document.getElementById('loading-overlay').classList.add('hidden');
      showToast("ಡೇಟಾ ಲೋಡ್ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ: " + (err.message || err), "error");
      resetToEmptyState();
    }

    function setViewMode(mode, triggerRender = true) {
      currentViewMode = mode || 'cards';
      localStorage.setItem('lba_view_mode', currentViewMode);

      const btnCards = document.getElementById('btn-view-cards');
      const btnTable = document.getElementById('btn-view-table');

      if (currentViewMode === 'cards') {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
      } else {
        if (btnCards) btnCards.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 text-slate-600 dark:text-slate-300 hover:text-slate-900 border-0 bg-transparent';
        if (btnTable) btnTable.className = 'px-3 py-1.5 rounded-lg text-xs font-black transition cursor-pointer flex items-center gap-1.5 bg-indigo-600 text-white shadow-xs border-0';
      }

      if (triggerRender) {
        renderActiveView();
      }
    }

    function setGenderFilter(val) {
      genderFilter = val || '';
      const btnAll = document.getElementById('gen-btn-all');
      const btnBoy = document.getElementById('gen-btn-boy');
      const btnGirl = document.getElementById('gen-btn-girl');

      const activeClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-indigo-600 text-white shadow-xs border-0 cursor-pointer';
      const inactiveClass = 'px-3 py-1.5 rounded-xl text-xs font-bold transition bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 cursor-pointer';

      if (btnAll) btnAll.className = genderFilter === '' ? activeClass : inactiveClass;
      if (btnBoy) btnBoy.className = genderFilter === 'Boy' ? activeClass : inactiveClass;
      if (btnGirl) btnGirl.className = genderFilter === 'Girl' ? activeClass : inactiveClass;

      renderActiveView();
    }

    function applyFiltersAndRender() {
      const searchInput = document.getElementById('search-student-input');
      searchQuery = (searchInput ? searchInput.value : '').toLowerCase().trim();
      renderActiveView();
    }

    function getFilteredStudents() {
      return students.filter(s => {
        if (genderFilter && s.gender !== genderFilter) return false;
        if (searchQuery) {
          const nameEn = (s.name_english || '').toLowerCase();
          const nameKn = (s.student_name_kn || s.student_name || '').toLowerCase();
          const sts = (s.adminNo || s.app_no || s.id || '').toLowerCase();
          const father = (s.father_name_az || s.father_name_kn || '').toLowerCase();
          return nameEn.includes(searchQuery) || nameKn.includes(searchQuery) || sts.includes(searchQuery) || father.includes(searchQuery);
        }
        return true;
      });
    }

    function renderActiveView() {
      const tableEl = document.getElementById('competency-table');
      const cardsEl = document.getElementById('student-cards-container');

      if (currentViewMode === 'cards') {
        if (tableEl) tableEl.classList.add('hidden');
        if (cardsEl) {
          cardsEl.classList.remove('hidden');
          renderCards();
        }
      } else {
        if (cardsEl) cardsEl.classList.add('hidden');
        if (tableEl) {
          tableEl.classList.remove('hidden');
          renderGrid();
        }
      }
      updateTotals();
    }

    function buildTableHeader() {
      const thead = document.getElementById('table-head');
      if (!thead) return;
      let lessonHeadersHtml = '';
      let subLabelsHtml = '';

      const numLessons = currentLessons.length || 1;
      const totalLessonCols = numLessons * 2;
      const pctPerLessonCol = (100 - 58) / totalLessonCols;

      currentLessons.forEach((lesson, index) => {
        lessonHeadersHtml += `<th colspan="2" class="p-2 text-center border-r border-slate-200 font-bold max-w-[120px] truncate" title="${lesson}" style="width: ${(pctPerLessonCol * 2).toFixed(2)}%;">${lesson}</th>`;
        subLabelsHtml += `
          <th class="p-1.5 text-center border-r border-slate-200" style="width: ${pctPerLessonCol.toFixed(2)}%;">Mark</th>
          <th class="p-1.5 text-center border-r border-slate-200" style="width: ${pctPerLessonCol.toFixed(2)}%;">Grade</th>
        `;
      });

      thead.innerHTML = `
        <tr class="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border-b border-slate-200 dark:border-slate-700 font-bold">
          <th rowspan="2" class="p-3 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 4%;">ಕ್ರ.ಸಂ</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 10%;">STS ಸಂಖ್ಯೆ</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 18%;">ಹೆಸರು</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 16%;">ತಂದೆಯ ಹೆಸರು</th>
          ${lessonHeadersHtml}
          <th colspan="2" class="p-2 text-center font-bold" style="width: 10%;">ಒಟ್ಟು ಶ್ರೇಣಿ ಕೌಂಟ್</th>
        </tr>
        <tr class="bg-slate-50 dark:bg-slate-850 text-[10px] text-slate-500 uppercase border-b border-slate-200 dark:border-slate-700 font-bold">
          ${subLabelsHtml}
          <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-400 font-bold" style="width: 5%;">Total A+,A</th>
          <th class="p-1.5 text-center bg-blue-50 dark:bg-blue-950/30 text-blue-800 dark:text-blue-400 font-bold" style="width: 5%;">Others</th>
        </tr>
      `;
    }

    function renderGrid() {
      const tbody = document.getElementById('student-grid-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      const filtered = getFilteredStudents();
      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${4 + (currentLessons.length * 2) + 2}" class="p-8 text-center text-slate-400 font-semibold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</td></tr>`;
        return;
      }

      filtered.forEach((student, index) => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-50 dark:hover:bg-slate-800/50 transition border-b border-slate-200 dark:border-slate-800 text-xs";
        const sId = student.id;
        tr.setAttribute('data-student-id', sId);

        if (!evaluations[sId]) {
          evaluations[sId] = {};
          currentLessons.forEach((_, i) => {
            evaluations[sId]["les_" + i + "_mark"] = "";
            evaluations[sId]["les_" + i + "_grade"] = "-";
          });
        }
        
        const evalData = evaluations[sId];
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || '').trim();
        let nameHtml = '';
        if (nameEn && nameKn) {
          nameHtml = `<div class="font-bold text-slate-800 dark:text-slate-100 text-[11px]">${nameEn}</div><div class="text-[10px] text-slate-500 font-medium">${nameKn}</div>`;
        } else {
          nameHtml = `<span class="font-bold text-slate-800 dark:text-slate-100 text-[11px]">${nameEn || nameKn || '-'}</span>`;
        }

        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();
        let fatherHtml = '';
        if (fatherEn && fatherKn) {
          fatherHtml = `<div class="font-bold text-slate-700 dark:text-slate-300 text-[11px]">${fatherEn}</div><div class="text-[10px] text-slate-500 font-medium">${fatherKn}</div>`;
        } else {
          fatherHtml = `<span class="font-semibold text-slate-700 dark:text-slate-300 text-[11px]">${fatherEn || fatherKn || '-'}</span>`;
        }

        let rowHtml = `
          <td class="p-3 text-center border-r border-slate-200 dark:border-slate-700 font-bold">${index + 1}</td>
          <td class="p-3 border-r border-slate-200 dark:border-slate-700 font-mono text-slate-500 dark:text-slate-400 font-bold">${student.adminNo || student.id}</td>
          <td class="p-3 border-r border-slate-200 dark:border-slate-700">${nameHtml}</td>
          <td class="p-3 border-r border-slate-200 dark:border-slate-700">${fatherHtml}</td>
        `;

        currentLessons.forEach((_, i) => {
          const m = evalData["les_" + i + "_mark"] !== undefined ? evalData["les_" + i + "_mark"] : '';
          const g = evalData["les_" + i + "_grade"] || '-';

          if (isEditing) {
            rowHtml += `
              <td class="p-1.5 border-r border-slate-200 dark:border-slate-700 text-center">
                <input type="number" min="0" max="10" step="0.5" value="${m}" oninput="onMarkChange('${sId}', ${i}, this.value, this)" class="w-12 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-1 text-center font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-900 dark:text-white">
              </td>
              <td class="p-1.5 border-r border-slate-200 dark:border-slate-700 text-center font-bold bg-slate-50/50 dark:bg-slate-900/50">
                <span id="grade-${sId}-${i}" class="text-xs ${getGradeBadgeClass(g)}">${g}</span>
              </td>
            `;
          } else {
            rowHtml += `
              <td class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-bold text-slate-800 dark:text-slate-200">${m !== '' ? m : '-'}</td>
              <td class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-bold">
                <span class="${getGradeBadgeClass(g)} badge-print">${g}</span>
              </td>
            `;
          }
        });

        rowHtml += `
          <td id="row-total-a-${sId}" class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-black bg-emerald-50 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-400 text-xs">0</td>
          <td id="row-total-b-${sId}" class="p-3 text-center font-black bg-blue-50 dark:bg-blue-950/20 text-blue-800 dark:text-blue-400 text-xs">0</td>
        `;

        tr.innerHTML = rowHtml;
        tbody.appendChild(tr);
      });
    }

    function getGradeBadgeClass(g) {
      if (g === 'A+') return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300 rounded px-2 py-0.5 font-black';
      if (g === 'A') return 'bg-teal-100 text-teal-800 dark:bg-teal-900/50 dark:text-teal-300 rounded px-2 py-0.5 font-bold';
      if (g === 'B+') return 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300 rounded px-2 py-0.5 font-bold';
      if (g === 'B') return 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300 rounded px-2 py-0.5 font-bold';
      if (g === 'C') return 'bg-rose-100 text-rose-800 dark:bg-rose-900/50 dark:text-rose-300 rounded px-2 py-0.5 font-bold';
      return 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400 rounded px-2 py-0.5 font-bold';
    }

    function renderCards() {
      const container = document.getElementById('student-cards-container');
      if (!container) return;
      container.innerHTML = '';

      const filtered = getFilteredStudents();
      if (filtered.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-300"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      filtered.forEach((student, index) => {
        const sId = student.id;
        if (!evaluations[sId]) {
          evaluations[sId] = {};
          currentLessons.forEach((_, i) => {
            evaluations[sId]["les_" + i + "_mark"] = "";
            evaluations[sId]["les_" + i + "_grade"] = "-";
          });
        }
        const evalData = evaluations[sId];
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();
        const isBoy = student.gender === 'Boy';

        let lessonsCardsHtml = '';
        currentLessons.forEach((lesson, i) => {
          const m = evalData["les_" + i + "_mark"] !== undefined ? evalData["les_" + i + "_mark"] : '';
          const g = evalData["les_" + i + "_grade"] || '-';

          lessonsCardsHtml += `
            <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-800 dark:text-slate-200 truncate max-w-[170px]" title="${lesson}">${lesson}</span>
                <span id="card-grade-${sId}-${i}" class="text-[11px] ${getGradeBadgeClass(g)}">${g}</span>
              </div>
              ${isEditing ? `
                <div class="flex items-center gap-1.5">
                  <button type="button" onclick="stepMark('${sId}', ${i}, -0.5)" class="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 font-black text-sm flex items-center justify-center border-0 cursor-pointer transition active:scale-95">-</button>
                  <input type="number" min="0" max="10" step="0.5" id="card-input-${sId}-${i}" value="${m}" oninput="onMarkChange('${sId}', ${i}, this.value, this)" class="flex-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg py-1 text-center font-black text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-900 dark:text-white" placeholder="0-10">
                  <button type="button" onclick="stepMark('${sId}', ${i}, 0.5)" class="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 font-black text-sm flex items-center justify-center border-0 cursor-pointer transition active:scale-95">+</button>
                </div>
                <!-- Quick Preset Chips -->
                <div class="flex items-center gap-1 justify-between pt-0.5">
                  ${[10, 9, 8, 7, 5, 0].map(sc => `
                    <button type="button" onclick="quickSetMark('${sId}', ${i}, ${sc})" class="px-1.5 py-0.5 rounded bg-slate-200/60 dark:bg-slate-700/60 hover:bg-indigo-600 hover:text-white text-[10px] font-bold text-slate-600 dark:text-slate-300 transition cursor-pointer border-0">${sc}</button>
                  `).join('')}
                </div>
              ` : `
                <div class="flex items-center justify-between pt-1">
                  <span class="text-xs text-slate-500">ಅಂಕ:</span>
                  <span class="text-sm font-black text-slate-800 dark:text-slate-100">${m !== '' ? m : '-'} / 10</span>
                </div>
              `}
            </div>
          `;
        });

        const cardHtml = `
          <div class="bg-white dark:bg-slate-850 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-3.5" data-card-student-id="${sId}">
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

            <!-- Father Details -->
            <div class="text-[11px] text-slate-600 dark:text-slate-300 flex items-center gap-1.5 px-1">
              <i class="fa-solid fa-user-tie text-slate-400 text-xs"></i>
              <span>ತಂದೆ: <strong class="text-slate-800 dark:text-slate-200">${fatherEn || fatherKn || '-'}</strong></span>
            </div>

            <!-- Lessons Grid -->
            <div class="space-y-2 pt-1 flex-1">
              ${lessonsCardsHtml}
            </div>

            <!-- Card Footer -->
            <div class="flex items-center justify-between pt-2.5 border-t border-slate-100 dark:border-slate-800 text-xs">
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/30 px-2 py-0.5 rounded">A+,A: <strong id="card-total-a-${sId}">0</strong></span>
                <span class="text-[10px] font-bold text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/30 px-2 py-0.5 rounded">ಇತರ: <strong id="card-total-b-${sId}">0</strong></span>
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

    function stepMark(studentId, lessonIdx, delta) {
      const currentVal = evaluations[studentId] && evaluations[studentId]["les_" + lessonIdx + "_mark"] !== undefined && evaluations[studentId]["les_" + lessonIdx + "_mark"] !== '' ? parseFloat(evaluations[studentId]["les_" + lessonIdx + "_mark"]) : 0;
      let newVal = Math.max(0, Math.min(10, currentVal + delta));
      quickSetMark(studentId, lessonIdx, newVal);
    }

    function quickSetMark(studentId, lessonIdx, markVal) {
      if (!evaluations[studentId]) evaluations[studentId] = {};
      evaluations[studentId]["les_" + lessonIdx + "_mark"] = markVal;
      const gradeVal = determineGrade(markVal);
      evaluations[studentId]["les_" + lessonIdx + "_grade"] = gradeVal;

      // Update Card input and grade badge
      const cardInput = document.getElementById(`card-input-${studentId}-${lessonIdx}`);
      if (cardInput) cardInput.value = markVal;
      const cardGrade = document.getElementById(`card-grade-${studentId}-${lessonIdx}`);
      if (cardGrade) {
        cardGrade.innerText = gradeVal;
        cardGrade.className = `text-[11px] ${getGradeBadgeClass(gradeVal)}`;
      }

      // Update Table grade badge
      const tableGrade = document.getElementById(`grade-${studentId}-${lessonIdx}`);
      if (tableGrade) {
        tableGrade.innerText = gradeVal;
        tableGrade.className = `text-xs ${getGradeBadgeClass(gradeVal)}`;
      }

      updateTotals();
    }

    function onMarkChange(studentId, lessonIdx, val, inputEl) {
      let markVal = val.trim() === '' ? '' : parseFloat(val);
      if (markVal > 10) {
        markVal = 10;
        if (inputEl) inputEl.value = 10;
      } else if (markVal < 0) {
        markVal = 0;
        if (inputEl) inputEl.value = 0;
      }

      quickSetMark(studentId, lessonIdx, markVal);
    }

    function updateTotals() {
      let grandTotalA = 0;
      let grandTotalOthers = 0;

      students.forEach(student => {
        const sId = student.id;
        const evalData = evaluations[sId] || {};
        let rowA = 0;
        let rowOthers = 0;

        currentLessons.forEach((_, i) => {
          const g = evalData["les_" + i + "_grade"] || '-';
          if (g === '-') return;
          if (['A+', 'A'].includes(g)) { rowA++; } else { rowOthers++; }
        });

        // Table totals
        const rowTotalAEl = document.getElementById(`row-total-a-${sId}`);
        const rowTotalBEl = document.getElementById(`row-total-b-${sId}`);
        if (rowTotalAEl) rowTotalAEl.innerText = rowA;
        if (rowTotalBEl) rowTotalBEl.innerText = rowOthers;

        // Card totals
        const cardTotalAEl = document.getElementById(`card-total-a-${sId}`);
        const cardTotalBEl = document.getElementById(`card-total-b-${sId}`);
        if (cardTotalAEl) cardTotalAEl.innerText = rowA;
        if (cardTotalBEl) cardTotalBEl.innerText = rowOthers;

        grandTotalA += rowA;
        grandTotalOthers += rowOthers;
      });

      const statTotalStudents = document.getElementById('stat-total-students');
      const statTotalA = document.getElementById('stat-total-a');
      const statTotalB = document.getElementById('stat-total-b');
      if (statTotalStudents) statTotalStudents.innerText = students.length;
      if (statTotalA) statTotalA.innerText = grandTotalA;
      if (statTotalB) statTotalB.innerText = grandTotalOthers;
    }

    function setMode(editing) {
      isEditing = editing;
      const modeTag = document.getElementById('grid-mode-tag');
      if (editing) {
        if (modeTag) {
          modeTag.innerText = "Edit Mode";
          modeTag.className = "px-2.5 py-1 rounded-full bg-amber-100 text-amber-800 font-bold uppercase tracking-wider text-[10px]";
          modeTag.classList.remove('hidden');
        }
        const btnEdit = document.getElementById('btn-edit');
        const btnSave = document.getElementById('btn-save');
        const btnCancel = document.getElementById('btn-cancel');
        if (btnEdit) btnEdit.classList.add('hidden');
        if (btnSave) btnSave.classList.remove('hidden');
        if (btnCancel) btnCancel.classList.remove('hidden');
      } else {
        if (modeTag) {
          modeTag.innerText = "View Mode";
          modeTag.className = "px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 font-bold uppercase tracking-wider text-[10px]";
          modeTag.classList.remove('hidden');
        }
        const btnEdit = document.getElementById('btn-edit');
        const btnSave = document.getElementById('btn-save');
        const btnCancel = document.getElementById('btn-cancel');
        if (btnEdit) btnEdit.classList.remove('hidden');
        if (btnSave) btnSave.classList.add('hidden');
        if (btnCancel) btnCancel.classList.add('hidden');
      }
    }

    function hideActionButtons() {
      const modeTag = document.getElementById('grid-mode-tag');
      if (modeTag) modeTag.classList.add('hidden');
      const btnEdit = document.getElementById('btn-edit');
      const btnSave = document.getElementById('btn-save');
      const btnCancel = document.getElementById('btn-cancel');
      if (btnEdit) btnEdit.classList.add('hidden');
      if (btnSave) btnSave.classList.add('hidden');
      if (btnCancel) btnCancel.classList.add('hidden');
    }

    function resetToEmptyState() {
      document.getElementById('empty-state').classList.remove('hidden');
      document.getElementById('competency-table').classList.add('hidden');
      const cardsEl = document.getElementById('student-cards-container');
      if (cardsEl) cardsEl.classList.add('hidden');
      const sfBar = document.getElementById('search-filter-bar');
      if (sfBar) sfBar.classList.add('hidden');

      document.getElementById('grid-subtitle').innerText = "ಯಾವುದೇ ತರಗತಿ ಅಥವಾ ವಿಷಯವನ್ನು ಆರಿಸಲಾಗಿಲ್ಲ";
      hideActionButtons();
      document.getElementById('stats-bar').classList.add('hidden');
      if (document.getElementById('btn-save-pdf')) document.getElementById('btn-save-pdf').classList.add('hidden');
      document.getElementById('btn-print-report').classList.add('hidden');
      document.getElementById('btn-export-excel').classList.add('hidden');
      if (document.getElementById('btn-export-csv')) document.getElementById('btn-export-csv').classList.add('hidden');
      if (document.getElementById('btn-import-csv')) document.getElementById('btn-import-csv').classList.add('hidden');
      if (document.getElementById('btn-add-student')) document.getElementById('btn-add-student').classList.add('hidden');
      document.getElementById('rules-note-card').classList.add('hidden');
    }

    function enableEditing() { setMode(true); renderActiveView(); }
    
    function cancelEditing() {
      evaluations = JSON.parse(JSON.stringify(originalEvaluations));
      setMode(Object.keys(originalEvaluations).length === 0);
      renderActiveView();
    }

    function saveData() {
      const className = classFilter.value;
      const subjectName = subjectFilter.value;
      if (!className || !subjectName) return;
      document.getElementById('loading-overlay').classList.remove('hidden');

      supabaseClient.auth.getSession().then(({ data: { session } }) => {
        const schoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id")) || null;

        const payload = students.map(student => {
          const sId = student.id;
          const marks = evaluations[sId] || {};
          return {
            school_id: schoolId,
            student_id: sId,
            class_name: className,
            subject_name: subjectName,
            lessons: marks
          };
        });

        supabaseClient
          .from('lba_evaluations')
          .upsert(payload, { onConflict: 'student_id,subject_name' })
          .then(({ error }) => {
            if (error) {
              console.warn("Supabase upsert for LBA evaluations failed, saving to localStorage as fallback:", error);
            } else {
              console.log("Supabase LBA evaluations upsert successful");
            }
            
            // Replicate/backup to localStorage
            const mockKey = `lba_mock_${className}_${subjectName.replace(/[^a-zA-Z0-9]/g, '_')}`;
            try {
              localStorage.setItem(mockKey, JSON.stringify(evaluations));
            } catch (e) {
              console.error("Failed to write to localStorage:", e);
            }

            onDataSaved();
          });
      });
    }

    function onDataSaved() {
      document.getElementById('loading-overlay').classList.add('hidden');
      showToast("ಮಾಹಿತಿ ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!", "success");
      originalEvaluations = JSON.parse(JSON.stringify(evaluations));
      setMode(false);
      renderActiveView();
    }

    function onDataSaveFailed() {
      document.getElementById('loading-overlay').classList.add('hidden');
      showToast("ದೋಷ: ಡೇಟಾ ಉಳಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.", "error");
    }

    function loadLocalMockData(className, subjectName) {
      const mockKey = `lba_mock_${className}_${subjectName.replace(/[^a-zA-Z0-9]/g, '_')}`;
      let saved = localStorage.getItem(mockKey);
      const roster = [
        { id: "GHPS001", student_name_kn: "ಅಭಿಷೇಕ್ ಎಂ", name_english: "Abhishek M", father_name_kn: "ಮಹಾದೇವಪ್ಪ", father_name_az: "Mahadevappa", adminNo: "STS202601" },
        { id: "GHPS002", student_name_kn: "ಚೈತ್ರಾ ಕೆ", name_english: "Chaitra K", father_name_kn: "ಕೃಷ್ಣಪ್ಪ", father_name_az: "Krishnappa", adminNo: "STS202602" },
        { id: "GHPS003", student_name_kn: "ದರ್ಶನ್ ಎಲ್", name_english: "Darshan L", father_name_kn: "ಲಕ್ಷ್ಮಣ್", father_name_az: "Lakshman", adminNo: "STS202603" }
      ];
      onDataLoaded({ success: true, students: roster, evaluations: saved ? JSON.parse(saved) : {} });
    }

    function buildPrintArea() {
      const className = classFilter.value;
      const subjectName = subjectFilter.value;
      
      const schoolNameEn = localStorage.getItem('school_name_en') || "GOVERNMENT HIGHER PRIMARY SCHOOL, MARCHED";
      const schoolNameKn = localStorage.getItem('school_name_kn') || "ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ ಮರ್ಛೇಡ್";
      
      document.getElementById('print-school-name').innerHTML = `
        <div style="font-size: 20px; font-weight: 800; text-transform: uppercase; color: #000000; line-height: 1.2;">${schoolNameEn}</div>
        <div style="font-size: 16px; font-weight: 700; color: #000000; margin-top: 4px; line-height: 1.2;">${schoolNameKn}</div>
      `;
      
      document.getElementById('print-class-meta').innerText = "ತರಗತಿ / Class: " + className;
      document.getElementById('print-subject-meta').innerText = "ವಿಷಯ / Subject: " + subjectName;
      document.getElementById('print-date-meta').innerText = "ದಿನಾಂಕ / Date: " + new Date().toLocaleDateString('kn-IN');
      
      // Clean up previous print content
      const existingTable = document.getElementById('printArea').querySelector('table');
      if (existingTable) existingTable.remove();
      const existingSigs = document.getElementById('printArea').querySelector('.print-signatures-row');
      if (existingSigs) existingSigs.remove();
      
      // Clone competency table
      const originalTable = document.getElementById('competency-table');
      const tableClone = originalTable.cloneNode(true);
      tableClone.removeAttribute('id');
      tableClone.classList.remove('hidden');
      
      // Sync input values to cloned table and replace them with spans
      const originalInputs = originalTable.querySelectorAll('input');
      const clonedInputs = tableClone.querySelectorAll('input');
      originalInputs.forEach((origInput, index) => {
        if (clonedInputs[index]) {
          const parent = clonedInputs[index].parentNode;
          const val = origInput.value !== '' ? origInput.value : '-';
          const span = document.createElement('span');
          span.innerText = val;
          span.style.fontWeight = 'bold';
          parent.replaceChild(span, clonedInputs[index]);
        }
      });
      
      // Clean classes from tableClone and its children to allow native print CSS to apply solid black borders and backgrounds
      tableClone.removeAttribute('class');
      tableClone.querySelectorAll('*').forEach(el => {
        const isLeft = el.classList.contains('text-left') || el.classList.contains('sticky-c3') || el.classList.contains('sticky-c4');
        const isRight = el.classList.contains('text-right');
        el.removeAttribute('class');
        if (isLeft) {
          el.style.textAlign = 'left';
          el.style.paddingLeft = '6px';
        } else if (isRight) {
          el.style.textAlign = 'right';
          el.style.paddingRight = '6px';
        } else {
          el.style.textAlign = 'center';
        }
      });
      
      // Append cloned table
      document.getElementById('printArea').appendChild(tableClone);
      
      // Add signature block
      const sigRow = document.createElement('div');
      sigRow.className = 'print-signatures-row';
      const isSingleClass = className && className !== "ALL";
      sigRow.innerHTML = `
        <span>ತರಗತಿ ಶಿಕ್ಷಕರ ಸಹಿ / Class Teacher Signature</span>
        ${isSingleClass ? '<span>ವಿಷಯ ಶಿಕ್ಷಕರ ಸಹಿ / Subject Teacher Signature</span>' : ''}
        <span>ಮುಖ್ಯೋಪಾಧ್ಯಾಯರ ಸಹಿ / Head Master Signature</span>
      `;
      document.getElementById('printArea').appendChild(sigRow);
    }

    function triggerPrint() {
      window.openPrintDrawer({
        tableId: 'competency-table',
        title: 'LBA Assessment Report / ಎಲ್.ಬಿ.ಎ ಮೌಲ್ಯಮಾಪನ ವರದಿ',
        class: classFilter.value,
        exam: '',
        subject: subjectFilter.value,
        students: students
      });
    }

    function exportToPdf() {
      triggerPrint();
    }

    function downloadCSVTemplate() {
      const headers = ["STS Number", "Student Name"];
      const sampleRow = ["STS2026001", "Chaitra G"];
      
      const lessons = currentLessons && currentLessons.length > 0 ? currentLessons : [
        "Lesson 1", "Lesson 2", "Lesson 3", "Lesson 4", "Lesson 5"
      ];
      
      lessons.forEach((lesson, index) => {
        headers.push(`Lesson ${index + 1} (${lesson})`);
        sampleRow.push("8.5");
      });
      
      let csvContent = "\uFEFF"; 
      csvContent += headers.map(h => `"${h.replace(/"/g, '""')}"`).join(",") + "\r\n";
      csvContent += sampleRow.map(r => `"${r.replace(/"/g, '""')}"`).join(",") + "\r\n";

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.setAttribute("href", url);
      link.setAttribute("download", `LBA_Template.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    function exportToExcel() {
      const table = document.getElementById('competency-table');
      const wb = XLSX.utils.table_to_book(table, { sheet: "LBA Report" });
      XLSX.writeFile(wb, `LBA_Report_${classFilter.value.replace(' ', '_')}_${subjectFilter.value.split('/')[0].trim()}.xlsx`);
    }

    function exportToCSV() {
      const table = document.getElementById('competency-table');
      const ws = XLSX.utils.table_to_sheet(table);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "LBA Report");
      XLSX.writeFile(wb, `LBA_Report_${classFilter.value.replace(' ', '_')}_${subjectFilter.value.split('/')[0].trim()}.csv`, { bookType: 'csv' });
    }

    async function handleCSVUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = async function(e) {
        try {
          const data = e.target.result;
          const workbook = XLSX.read(data, { type: 'binary' });
          const firstSheet = workbook.SheetNames[0];
          const sheet = workbook.Sheets[firstSheet];
          const json = XLSX.utils.sheet_to_json(sheet);
          
          if (json.length === 0) {
            alert('CSV file is empty.');
            return;
          }
          
          const headers = Object.keys(json[0] || {});
          const stsKey = headers.find(h => {
            const norm = h.trim().toLowerCase().replace(/[^a-z0-9]/g, '');
            return norm === 'stsno' || norm === 'sts' || norm === 'appno' || norm === 'studentno' || norm === 'stsnumber' || norm === 'ಎಸ್ಟಿಎಸ್ಸಂಖ್ಯೆ';
          }) || 'STS Number';
          
          const className = classFilter.value;
          const subjectName = subjectFilter.value;
          
          const { data: { session } } = await supabaseClient.auth.getSession();
          const schoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id"));
          
          let changedCount = 0;
          const upsertPayloads = [];
          
          json.forEach(row => {
            const stsVal = (row[stsKey] || '').toString().trim();
            if (!stsVal) return;
            
            const student = students.find(s => s.adminNo === stsVal);
            if (!student) return;
            
            if (!evaluations[student.id]) {
              evaluations[student.id] = {};
            }
            
            let studentChanged = false;
            
            currentLessons.forEach((lesson, index) => {
              const lIdx = index + 1;
              const csvKey = headers.find(h => h.includes(lesson) || h.toLowerCase().includes(`lesson ${lIdx}`) || h.includes(`ಪಾಠ ${lIdx}`));
              
              if (csvKey && row[csvKey] !== undefined) {
                const markStr = row[csvKey].toString().trim();
                let markVal = markStr === '' ? '' : parseFloat(markStr);
                if (markVal !== '') {
                  if (markVal > 10) markVal = 10;
                  
                  const currentM = evaluations[student.id][`les_${lIdx}_mark`] !== undefined ? parseFloat(evaluations[student.id][`les_${lIdx}_mark`]) : '';
                  if (currentM !== markVal) {
                    evaluations[student.id][`les_${lIdx}_mark`] = markVal;
                    evaluations[student.id][`les_${lIdx}_grade`] = determineGrade(markVal);
                    studentChanged = true;
                  }
                }
              }
            });
            
            if (studentChanged) {
              changedCount++;
              upsertPayloads.push({
                school_id: schoolId,
                student_id: student.id,
                class_name: className,
                subject_name: subjectName,
                lessons: evaluations[student.id],
                updated_at: new Date().toISOString()
              });
            }
          });
          
          if (upsertPayloads.length > 0) {
            document.getElementById('loading-overlay').classList.remove('hidden');
            
            const { error } = await supabaseClient
              .from('lba_evaluations')
              .upsert(upsertPayloads, { onConflict: 'student_id,subject_name' });
              
            document.getElementById('loading-overlay').classList.add('hidden');
            
            if (error) {
              console.warn("Supabase upsert failed, saving to localStorage as fallback:", error);
              const mockKey = `lba_mock_${className}_${subjectName.replace(/[^a-zA-Z0-9]/g, '_')}`;
              localStorage.setItem(mockKey, JSON.stringify(evaluations));
            } else {
              originalEvaluations = JSON.parse(JSON.stringify(evaluations));
            }
            
            renderGrid();
            alert(`ಯಶಸ್ವಿಯಾಗಿ ${changedCount} ವಿದ್ಯಾರ್ಥಿಗಳ ವಿವರಗಳನ್ನು ಅಪ್‌ಡೇಟ್ ಮಾಡಲಾಗಿದೆ!\nSuccessfully updated data for ${changedCount} students.`);
          } else {
            alert("ಯಾವುದೇ ಬದಲಾವಣೆ ಕಂಡುಬಂದಿಲ್ಲ.\nNo changes detected.");
          }
        } catch (err) {
          console.error(err);
          alert("CSV ಅಪ್‌ಲೋಡ್ ವಿಫಲವಾಗಿದೆ: " + err.message);
        }
      };
      reader.readAsBinaryString(file);
      event.target.value = '';
    }

    function showToast(msg, type = "success") {
      const toast = document.getElementById('toast-notif');
      const msgEl = document.getElementById('toast-message');
      msgEl.innerText = msg;
      toast.className = `fixed bottom-5 right-5 px-5 py-3 rounded-2xl shadow-xl transition transform z-[100] ${type === 'success' ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'}`;
      toast.classList.remove('translate-y-20', 'opacity-0');
      setTimeout(() => { toast.classList.add('translate-y-20', 'opacity-0'); }, 2500);
    }

    function goToDashboard() {
      window.location.href = "dashboard.html";
    }
  
    // Sidebar & Theme helpers
    

    function changeTheme(themeName) {
      document.body.setAttribute('data-theme', themeName);
      localStorage.setItem('portal_theme', themeName);
    }

    async function initUserAndTheme() {
      // 1. Theme
      const savedTheme = localStorage.getItem('portal_theme') || 'light';
      document.body.setAttribute('data-theme', savedTheme);
      const selector = document.getElementById('themeSelector');
      if (selector) selector.value = savedTheme;



      // 3. User info
      try {
        const { data: { session } } = await supabaseClient.auth.getSession();
        if (session) {
          const user = session.user;
          const headerUser = document.getElementById('headerUser');

          // Fetch user profile from database to check for name, developer role and school_id
          const { data: profile } = await supabaseClient
            .from('profiles')
            .select('name, role, school_id')
            .eq('id', user.id)
            .maybeSingle();

          const name = profile?.name || user.user_metadata?.name || user.email;
          if (headerUser) headerUser.innerText = name;

          if (profile) {
            currentSchoolId = profile.school_id || (user.user_metadata?.school_id || localStorage.getItem("school_id"));
          } else {
            currentSchoolId = (user.user_metadata?.school_id || localStorage.getItem("school_id"));
          }

          if (profile && profile.role === 'developer') {
            if (headerUser) headerUser.innerHTML = `<span class="bg-indigo-600/30 text-indigo-400 border border-indigo-500/30 px-2 py-0.5 rounded text-[10px] font-bold mr-1.5 uppercase">Dev</span>${name}`;
            
            const sidebarNav = document.getElementById('sidebarNav');
            if (sidebarNav && !document.getElementById('nav-DeveloperConsole')) {
              const devLink = document.createElement('a');
              devLink.href = "developer.html";
              devLink.id = "nav-DeveloperConsole";
              devLink.className = "flex items-center gap-2 px-3 py-2.5 rounded-xl font-bold text-indigo-600 hover:bg-indigo-50 transition border border-indigo-200/50 bg-indigo-50/30";
              devLink.innerHTML = `<i class="fa-solid fa-screwdriver-wrench text-indigo-600 text-sm w-5 text-center"></i> <span class="sidebar-text">Developer Console</span>`;
              sidebarNav.insertBefore(devLink, sidebarNav.firstChild);
            }
          }

          // Fetch school details and apply dynamically to DOM
          let schoolNameEn = localStorage.getItem('school_name_en');
          let schoolNameKn = localStorage.getItem('school_name_kn');
          
          if (!schoolNameEn && (user.user_metadata?.school_id || localStorage.getItem("school_id"))) {
            try {
              const { data: school } = await supabaseClient
                .from('schools')
                .select('school_name_en, school_name_kn')
                .eq('id', user.user_metadata.school_id)
                .single();
              if (school) {
                schoolNameEn = school.school_name_en || '';
                schoolNameKn = school.school_name_kn || '';
                localStorage.setItem('school_name_en', schoolNameEn);
                localStorage.setItem('school_name_kn', schoolNameKn);
              }
            } catch (schErr) {
              console.error("Failed to load school details inside initUserAndTheme:", schErr);
            }
          }

          if (schoolNameEn) {
            // Replace hardcoded English school name in text nodes
            const walkerEn = document.createTreeWalker(
              document.body,
              NodeFilter.SHOW_TEXT,
              null,
              false
            );
            let nodeEn;
            while (nodeEn = walkerEn.nextNode()) {
              const val = nodeEn.nodeValue;
              if (val.includes("Government Higher Primary School, Marched")) {
                nodeEn.nodeValue = val.replace(/Government Higher Primary School, Marched/g, schoolNameEn);
              } else if (val.includes("GOVERNMENT HIGHER PRIMARY SCHOOL, MARCHED")) {
                nodeEn.nodeValue = val.replace(/GOVERNMENT HIGHER PRIMARY SCHOOL, MARCHED/g, schoolNameEn.toUpperCase());
              } else if (val.includes("GHPS MARCHED")) {
                nodeEn.nodeValue = val.replace(/GHPS MARCHED/g, schoolNameEn.toUpperCase());
              } else if (val.includes("GHPS Marched")) {
                nodeEn.nodeValue = val.replace(/GHPS Marched/g, schoolNameEn);
              }
            }

            if (schoolNameKn) {
              // Replace hardcoded Kannada school name in text nodes
              const walkerKn = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null,
                false
              );
              let nodeKn;
              while (nodeKn = walkerKn.nextNode()) {
                const val = nodeKn.nodeValue;
                if (val.includes("ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ, ಮರ್ಚೆಡ್")) {
                  nodeKn.nodeValue = val.replace(/ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ, ಮರ್ಚೆಡ್/g, schoolNameKn);
                } else if (val.includes("ಜಿ.ಹೆಚ್.ಪಿ.ಎಸ್. ಮರ್ಚೆಡ್")) {
                  nodeKn.nodeValue = val.replace(/ಜಿ.ಹೆಚ್.ಪಿ.ಎಸ್. ಮರ್ಚೆಡ್/g, schoolNameKn);
                }
              }
            }
          }
        }
      } catch (e) {
        console.error("Error loading user session for header:", e);
      }
    }
