
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
      if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        arrow.classList.add('rotate-90');
      } else {
        menu.classList.add('hidden');
        arrow.classList.remove('rotate-90');
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

    let mutableConfigs = {
      primary: {
        classes: ["1", "2", "3", "4", "5"],
        faMax: 15,
        saMax: 20, 
        saWrittenMax: 30,
        saOralMax: 20,
        subjects: ["ಕನ್ನಡ / Kannada", "English", "ಗಣಿತ / Maths", "ಪರಿಸರ ಅಧ್ಯಯನ / EVS"],
      },
      middleHigh: {
        classes: ["6", "7", "8", "9", "10"],
        faMax: 10,
        saMax: 30, 
        saWrittenMax: 40,
        saOralMax: 10,
        subjects: ["ಕನ್ನಡ / Kannada", "English", "ಹಿಂದಿ / Hindi", "ಗಣಿತ / Maths", "ವಿಜ್ಞಾನ / Science", "ಸಮಾಜ ವಿಜ್ಞಾನ / Social Sci", "दೈಹಿಕ ಶಿಕ್ಷಣ / PE"],
      }
    };

    let gradeScales = {
      10:  { 'A+': 9,  'A': 7,  'B+': 6,  'B': 3,  'C': 0 },
      15:  { 'A+': 14, 'A': 11, 'B+': 8,  'B': 5,  'C': 0 },
      20:  { 'A+': 18, 'A': 14, 'B+': 10, 'B': 6,  'C': 0 },
      25:  { 'A+': 23, 'A': 18, 'B+': 13, 'B': 8,  'C': 0 },
      30:  { 'A+': 27, 'A': 21, 'B+': 15, 'B': 9,  'C': 0 },
      50:  { 'A+': 45, 'A': 35, 'B+': 25, 'B': 15, 'C': 0 },
      100: { 'A+': 90, 'A': 70, 'B+': 50, 'B': 30, 'C': 0 }
    };

    let currentSubjects = [];
    let students = [];
    let evaluations = {};
    let isEditing = true;
    let autoSaveTimer = null;
    let originalEvaluations = {};
    let currentViewMode = localStorage.getItem('cce_view_mode') || 'cards';
    let genderFilter = '';
    let searchQuery = '';
    let currentSchoolId = localStorage.getItem("school_id") || null;

    const classFilter = document.getElementById('class-filter');
    const examTypeFilter = document.getElementById('exam-type-filter');
    const subjectFilter = document.getElementById('subject-filter');

    document.addEventListener("DOMContentLoaded", async function() {
      await initUserAndTheme();
      const { data: { session } } = await supabaseClient.auth.getSession();
      if (!session) {
        window.location.href = "index.html";
        return;
      }
      initSidebar();
      await loadSettingsFromBackend();
      fetchDashboardMetrics();

      // Check query parameters
      const urlParams = new URLSearchParams(window.location.search);
      const paramClass = urlParams.get('class');
      const paramExam = urlParams.get('exam');
      const paramSubject = urlParams.get('subject');
      
      if (paramClass && classFilter) classFilter.value = paramClass;
      if (paramExam && examTypeFilter) examTypeFilter.value = paramExam;
      if (paramSubject && subjectFilter) subjectFilter.value = paramSubject;
      
      if (paramClass || paramExam || paramSubject) {
        switchTab('grid');
        syncAllFilters();
        if (classFilter.value && examTypeFilter.value) {
          showDynamicRulesNote();
          loadSettingsIntoInputs();
          checkAndLoadGrid();
        }
      } else {
        switchTab('dashboard');
      }
    });

    async function fetchDashboardMetrics() {
      try {
        const { data: { session } } = await supabaseClient.auth.getSession();
        const rawSchoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id")) || null;
        const schoolId = (rawSchoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(rawSchoolId)) ? rawSchoolId : null;

        let totalCount = null;

        if (schoolId) {
          try {
            const { count, error } = await supabaseClient
              .from('admissions')
              .select('*', { count: 'exact', head: true })
              .or(`school_id.eq.${schoolId},school_id.is.null`);
            if (!error && count !== null) {
              totalCount = count;
            }
          } catch(e) {}
        }

        if (totalCount === null) {
          try {
            const { count, error } = await supabaseClient
              .from('admissions')
              .select('*', { count: 'exact', head: true });
            if (!error && count !== null) {
              totalCount = count;
            }
          } catch(e) {}
        }

        if (totalCount === null) {
          try {
            const localSt = JSON.parse(
              localStorage.getItem("all_students_cache") ||
              localStorage.getItem("students_data") ||
              localStorage.getItem("sts_master_list") ||
              localStorage.getItem("students") ||
              localStorage.getItem("admissions_data") ||
              "[]"
            );
            if (localSt && localSt.length > 0) {
              totalCount = localSt.filter(s => s.status !== 'TC_OUT' && s.status !== 'DELETED' && s.status !== 'REMOVED').length;
            }
          } catch(e) {}
        }

        const el = document.getElementById('dash-total-students');
        if (el) {
          el.innerText = totalCount !== null ? `${totalCount} Pupils` : "0 Pupils";
        }
      } catch(e) {
        const el = document.getElementById('dash-total-students');
        if (el) el.innerText = "0 Pupils";
      }
    }

    function syncAllFilters() {
      syncActiveGroupConfiguration();
    }

    [classFilter, examTypeFilter].forEach(filter => {
      filter.addEventListener('change', () => {
        syncAllFilters();
        if (classFilter.value && examTypeFilter.value) {
          showDynamicRulesNote();
          loadSettingsIntoInputs();
          checkAndLoadGrid();
        } else {
          resetToEmptyState();
        }
      });
    });

    subjectFilter.addEventListener('change', () => {
      if (students.length > 0) {
        buildTableHeader();
        renderActiveView();
      }
    });

    // Grid Sub Page Switcher System
    let currentGridSubPage = 'entermarks';
    function switchGridSubPage(pageKey) {
      currentGridSubPage = pageKey;
      const tabEnterMarks = document.getElementById('sub-tab-entermarks');
      const tabAssessSetting = document.getElementById('sub-tab-assesssetting');
      const pageEnterMarksDiv = document.getElementById('page-enter-marks');
      const pageAssessSettingDiv = document.getElementById('page-assessment-setting');

      const setInnerTabActive = (btn, isActive) => {
        if (!btn) return;
        if (isActive) {
          btn.className = "text-xs font-bold px-5 py-2.5 rounded-xl transition flex items-center gap-2 border-0 cursor-pointer bg-white text-slate-800 shadow";
        } else {
          btn.className = "text-xs font-bold px-5 py-2.5 rounded-xl transition flex items-center gap-2 border-0 cursor-pointer bg-transparent text-slate-600 hover:text-slate-800";
        }
      };

      setInnerTabActive(tabEnterMarks, pageKey === 'entermarks');
      setInnerTabActive(tabAssessSetting, pageKey === 'assesssetting');

      if (pageKey === 'entermarks') {
        pageEnterMarksDiv.classList.remove('hidden');
        pageAssessSettingDiv.classList.add('hidden');
        if (classFilter.value && examTypeFilter.value) renderActiveView();
      } else {
        pageEnterMarksDiv.classList.add('hidden');
        pageAssessSettingDiv.classList.remove('hidden');
        loadSettingsIntoInputs();
      }
    }

    // Tab view Router Engine
    function switchTab(tabId) {
      const tabDashboardBtn = document.getElementById('tab-dashboard');
      const tabGridBtn = document.getElementById('tab-grid');
      const tabSettingBtn = document.getElementById('tab-assesssetting');

      const viewDashboardMain = document.getElementById('main-dashboard-view');
      const viewGridMain = document.getElementById('main-grid-view');
      const pageAssessSettingDiv = document.getElementById('page-assessment-setting');

      const setTabActive = (btn, isActive, activeBg = 'bg-sky-600') => {
        if (!btn) return;
        if (isActive) {
          btn.className = `text-xs font-bold px-4 py-2.5 rounded-xl transition-all duration-300 flex items-center gap-2 border-0 cursor-pointer ${activeBg} text-white shadow-md active:scale-95`;
        } else {
          btn.className = "text-xs font-bold px-4 py-2.5 rounded-xl transition-all duration-300 flex items-center gap-2 border-0 cursor-pointer bg-transparent text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-800 dark:hover:text-slate-200 active:scale-95";
        }
      };

      setTabActive(tabDashboardBtn, tabId === 'dashboard', 'bg-sky-600');
      setTabActive(tabGridBtn, tabId === 'grid', 'bg-indigo-600');
      setTabActive(tabSettingBtn, tabId === 'assesssetting', 'bg-amber-600');

      if (tabId === 'dashboard') {
        viewDashboardMain?.classList.remove('hidden');
        viewGridMain?.classList.add('hidden');
        pageAssessSettingDiv?.classList.add('hidden');
      } else if (tabId === 'grid') {
        viewDashboardMain?.classList.add('hidden');
        viewGridMain?.classList.remove('hidden');
        pageAssessSettingDiv?.classList.add('hidden');
        if (!classFilter.value) classFilter.value = "1";
        if (!examTypeFilter.value) examTypeFilter.value = "FA1";
        syncAllFilters();
        showDynamicRulesNote();
        loadSettingsIntoInputs();
        checkAndLoadGrid();
      } else if (tabId === 'assesssetting') {
        viewDashboardMain?.classList.add('hidden');
        viewGridMain?.classList.add('hidden');
        pageAssessSettingDiv?.classList.remove('hidden');
        loadSettingsIntoInputs();
      }
    }

    async function loadSettingsFromBackend() {
      // First try to load from Supabase
      if (currentSchoolId) {
        try {
          const { data, error } = await supabaseClient
            .from('school_settings')
            .select('settings_value')
            .eq('school_id', currentSchoolId)
            .eq('settings_key', 'cce_saved_settings')
            .maybeSingle();

          if (!error && data && data.settings_value) {
            console.log("Loaded CCE settings from Supabase");
            const settingsStr = JSON.stringify(data.settings_value);
            onSettingsLoaded({ success: true, settings: settingsStr });
            // Cache locally
            localStorage.setItem(`cce_saved_settings_${currentSchoolId}`, settingsStr);
            return;
          }
        } catch (dbErr) {
          console.warn("Failed to load CCE settings from Supabase:", dbErr);
        }
      }

      // Fallback to localStorage
      const key = currentSchoolId ? `cce_saved_settings_${currentSchoolId}` : 'cce_saved_settings';
      const saved = localStorage.getItem(key);
      if (saved) {
        try { onSettingsLoaded({ success: true, settings: saved }); } catch(e) { loadSettingsIntoInputs(); }
      } else {
        // Fallback to legacy key
        const legacySaved = localStorage.getItem('cce_saved_settings');
        if (legacySaved) {
          try {
            onSettingsLoaded({ success: true, settings: legacySaved });
            if (currentSchoolId) {
              localStorage.setItem(key, legacySaved);
            }
            return;
          } catch(e) {}
        }
        loadSettingsIntoInputs();
      }
    }

    function onSettingsLoaded(response) {
      if (response && response.success && response.settings) {
        try {
          const parsed = JSON.parse(response.settings);
          if (parsed.mutableConfigs) mutableConfigs = parsed.mutableConfigs;
          if (parsed.gradeScales) gradeScales = parsed.gradeScales;
        } catch(e) { console.error("Error parsing settings: ", e); }
      }
      loadSettingsIntoInputs();
    }

    function loadSettingsIntoInputs() {
      document.getElementById('cfg-p-fa').value = mutableConfigs.primary.faMax;
      document.getElementById('cfg-p-sa').value = mutableConfigs.primary.saMax;
      document.getElementById('cfg-p-saw').value = mutableConfigs.primary.saWrittenMax;
      document.getElementById('cfg-p-sao').value = mutableConfigs.primary.saOralMax;
      document.getElementById('cfg-p-subs').value = mutableConfigs.primary.subjects.join(', ');

      document.getElementById('cfg-m-fa').value = mutableConfigs.middleHigh.faMax;
      document.getElementById('cfg-m-sa').value = mutableConfigs.middleHigh.saMax;
      document.getElementById('cfg-m-saw').value = mutableConfigs.middleHigh.saWrittenMax;
      document.getElementById('cfg-m-sao').value = mutableConfigs.middleHigh.saOralMax;
      document.getElementById('cfg-m-subs').value = mutableConfigs.middleHigh.subjects.join(', ');

      const targets = [10, 15, 20, 25, 30, 50, 100];
      targets.forEach(t => {
        if(gradeScales[t]) {
          document.getElementById(`sc-${t}-ap`).value = gradeScales[t]['A+'];
          document.getElementById(`sc-${t}-a`).value = gradeScales[t]['A'];
          document.getElementById(`sc-${t}-bp`).value = gradeScales[t]['B+'];
          document.getElementById(`sc-${t}-b`).value = gradeScales[t]['B'];
        }
      });
    }

    function applyCustomSettings() {
      mutableConfigs.primary.faMax = parseFloat(document.getElementById('cfg-p-fa').value) || 15;
      mutableConfigs.primary.saMax = parseFloat(document.getElementById('cfg-p-sa').value) || 20;
      mutableConfigs.primary.saWrittenMax = parseFloat(document.getElementById('cfg-p-saw').value) || 30;
      mutableConfigs.primary.saOralMax = parseFloat(document.getElementById('cfg-p-sao').value) || 20;
      mutableConfigs.primary.subjects = document.getElementById('cfg-p-subs').value.split(',').map(s => s.trim()).filter(Boolean);

      mutableConfigs.middleHigh.faMax = parseFloat(document.getElementById('cfg-m-fa').value) || 10;
      mutableConfigs.middleHigh.saMax = parseFloat(document.getElementById('cfg-m-sa').value) || 30;
      mutableConfigs.middleHigh.saWrittenMax = parseFloat(document.getElementById('cfg-m-saw').value) || 40;
      mutableConfigs.middleHigh.saOralMax = parseFloat(document.getElementById('cfg-m-sao').value) || 10;
      mutableConfigs.middleHigh.subjects = document.getElementById('cfg-m-subs').value.split(',').map(s => s.trim()).filter(Boolean);

      const targets = [10, 15, 20, 25, 30, 50, 100];
      targets.forEach(t => {
        gradeScales[t] = {
          'A+': parseFloat(document.getElementById(`sc-${t}-ap`).value) || 0,
          'A': parseFloat(document.getElementById(`sc-${t}-a`).value) || 0,
          'B+': parseFloat(document.getElementById(`sc-${t}-bp`).value) || 0,
          'B': parseFloat(document.getElementById(`sc-${t}-b`).value) || 0,
          'C': 0
        };
      });

      const settingsPayload = { mutableConfigs, gradeScales };
      const settingsPayloadStr = JSON.stringify(settingsPayload);
      const key = currentSchoolId ? `cce_saved_settings_${currentSchoolId}` : 'cce_saved_settings';
      localStorage.setItem(key, settingsPayloadStr);
      showToast("ನಿಯಮಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!", "success");

      if (currentSchoolId) {
        supabaseClient
          .from('school_settings')
          .upsert({
            school_id: currentSchoolId,
            settings_key: 'cce_saved_settings',
            settings_value: settingsPayload,
            updated_at: new Date().toISOString()
          }, { onConflict: 'school_id,settings_key' })
          .then(({ error }) => {
            if (error) {
              console.warn("Failed to persist CCE settings to Supabase:", error);
            } else {
              console.log("Successfully persisted CCE settings to Supabase");
            }
          });
      }

      if (classFilter.value && examTypeFilter.value) {
        syncActiveGroupConfiguration();
        showDynamicRulesNote();
        checkAndLoadGrid();
      }
    }

    function syncActiveGroupConfiguration() {
      const cls = classFilter.value;
      let subsList = mutableConfigs.primary.classes.includes(cls === "ALL" ? "1" : cls) ? mutableConfigs.primary.subjects : mutableConfigs.middleHigh.subjects;
      currentSubjects = subsList.map((subName, i) => ({ id: "sub_" + i, name: subName }));

      const previousSelection = subjectFilter.value;
      subjectFilter.innerHTML = '<option value="ALL">ಎಲ್ಲಾ ವಿಷಯಗಳು / All Subjects</option>';
      currentSubjects.forEach(sub => {
        subjectFilter.innerHTML += `<option value="${sub.id}">${sub.name}</option>`;
      });
      if([...subjectFilter.options].some(o => o.value === previousSelection)) subjectFilter.value = previousSelection;
    }

    function determineGradeByScale(marks, maxTarget) {
      if (marks === '' || marks === null || marks === undefined) return '-';
      const m = parseFloat(marks);
      if (isNaN(m)) return '-';
      
      const target = parseFloat(maxTarget) || 10;
      if (target <= 0) return '-';

      const userScale = gradeScales[target] || gradeScales[target.toString()];
      
      // If user configured direct mark threshold (e.g. A+ >= 9, A >= 7 out of 10)
      if (userScale && userScale['A+'] <= target && userScale['A+'] > 0) {
        if (m >= userScale['A+']) return 'A+';
        if (m >= userScale['A']) return 'A';
        if (m >= userScale['B+']) return 'B+';
        if (m >= userScale['B']) return 'B';
        return (userScale['C+'] !== undefined && m >= userScale['C+']) ? 'C+' : 'C';
      }
      
      // Official Karnataka DSEL CCE Percentage Standard (A+: 90-100%, A: 75-89%, B+: 60-74%, B: 50-59%, C+: 35-49%, C: <35%)
      const pct = (m / target) * 100;
      if (pct >= 90) return 'A+';
      if (pct >= 75) return 'A';
      if (pct >= 60) return 'B+';
      if (pct >= 50) return 'B';
      if (pct >= 35) return 'C+';
      return 'C';
    }

    function showDynamicRulesNote() {
      const cls = classFilter.value;
      const exam = examTypeFilter.value;
      const card = document.getElementById('rules-note-card');
      const content = document.getElementById('rules-content');
      if (!cls || !exam) { card.classList.add('hidden'); return; }

      const isPrimary = mutableConfigs.primary.classes.includes(cls === "ALL" ? "1" : cls);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      const isSA = exam.startsWith("SA");

      let rulesText = "";
      if (!isSA) {
        rulesText = `<b>ವಿಧಾನ / Type:</b> ${exam} &nbsp;|&nbsp; <b>FA ಗರಿಷ್ಠ ಅಂಕ:</b> ${cfg.faMax} (ಗ್ರೇಡ್ ಸಾಲು: ${cfg.faMax})`;
      } else {
        rulesText = `<b>ವಿಧಾನ / Type:</b> ${exam} &nbsp;|&nbsp; <b>SA ನೈಜ ಅಂಕ:</b> ಲಿಖಿತ (${cfg.saWrittenMax}) + ಮೌಖಿಕ (${cfg.saOralMax}) = ಒಟ್ಟು 50 &nbsp;|&nbsp; <b>ಗ್ರೇಡ್ ಲೆಕ್ಕಾಚಾರ:</b> ಒಟ್ಟು 50 ರ ಅಂಕದ ಪ್ಯಾಟರ್ನ್ ಮೇಲೆ &nbsp;|&nbsp; <b>ವರದಿ ಪರಿವರ್ತನೆ:</b> 50 ರ ಮೊತ್ತವನ್ನು <b>${cfg.saMax}</b> ಕ್ಕೆ ಬದಲಾಯಿಸಲಾಗುತ್ತದೆ.`;
      }
      content.innerHTML = rulesText;
      card.classList.remove('hidden');
    }

    function normalizeClass(classStr) {
      if (!classStr && classStr !== 0) return "";
      let clean = classStr.toString().trim().toLowerCase();
      
      if (clean.includes("lkg") || clean.includes("kg1") || clean.includes("kg 1") || clean.includes("pre-k")) return "LKG";
      if (clean.includes("ukg") || clean.includes("kg2") || clean.includes("kg 2")) return "UKG";
      
      const numMatch = clean.match(/\b(10|[1-9])(st|nd|rd|th)?\b/);
      if (numMatch) {
        return numMatch[1];
      }
      
      if (clean === "i" || clean.includes("class i ") || clean.endsWith("class i") || clean === "class i") return "1";
      if (clean === "ii" || clean.includes("class ii")) return "2";
      if (clean === "iii" || clean.includes("class iii")) return "3";
      if (clean === "iv" || clean.includes("class iv")) return "4";
      if (clean === "v" || clean.includes("class v")) return "5";
      if (clean === "vi" || clean.includes("class vi")) return "6";
      if (clean === "vii" || clean.includes("class vii")) return "7";
      if (clean === "viii" || clean.includes("class viii")) return "8";
      if (clean === "ix" || clean.includes("class ix")) return "9";
      if (clean === "x" || clean.includes("class x")) return "10";
      
      return classStr.toString().trim();
    }

    function hideActionButtons() {
      const btnEdit = document.getElementById('btn-edit');
      const btnSave = document.getElementById('btn-save');
      const btnCancel = document.getElementById('btn-cancel');
      if (btnEdit) btnEdit.classList.add('hidden');
      if (btnSave) btnSave.classList.add('hidden');
      if (btnCancel) btnCancel.classList.add('hidden');
    }

    async function checkAndLoadGrid() {
      const className = classFilter.value;
      const examType = examTypeFilter.value;
      if (!className || !examType) return;

      document.getElementById('loading-overlay').classList.remove('hidden');
      document.getElementById('empty-state').classList.add('hidden');
      document.getElementById('competency-table').classList.add('hidden');
      document.getElementById('stats-bar').classList.add('hidden');
      if (document.getElementById('btn-export-pdf')) document.getElementById('btn-export-pdf').classList.add('hidden');
      document.getElementById('btn-export-excel').classList.add('hidden');
      document.getElementById('btn-print').classList.add('hidden');
      if (document.getElementById('btn-export-csv')) document.getElementById('btn-export-csv').classList.add('hidden');
      if (document.getElementById('btn-import-csv')) document.getElementById('btn-import-csv').classList.add('hidden');
      if (document.getElementById('btn-add-student')) document.getElementById('btn-add-student').classList.add('hidden');
      hideActionButtons();

      try {
        const { data: { session } } = await supabaseClient.auth.getSession();
        const rawSchoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id")) || null;
        const schoolId = (rawSchoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(rawSchoolId)) ? rawSchoolId : null;

        let data = null;
        let fetchError = null;

        if (schoolId) {
          try {
            const res1 = await supabaseClient
              .from('admissions')
              .select('*')
              .or(`school_id.eq.${schoolId},school_id.is.null`)
              .range(0, 5000);
            if (!res1.error && res1.data && res1.data.length > 0) {
              data = res1.data;
            } else if (res1.error) {
              fetchError = res1.error;
            }
          } catch (e) {
            fetchError = e;
          }
        }

        if (!data || data.length === 0) {
          try {
            const res2 = await supabaseClient
              .from('admissions')
              .select('*')
              .range(0, 5000);
            if (!res2.error && res2.data) {
              data = res2.data;
            }
          } catch (e) {}
        }

        const localTrashed = JSON.parse(localStorage.getItem('trashed_students_list') || '[]');
        const trashedKeys = new Set(localTrashed.map(t => String(t.id || t.app_no || t.student_sts || '').replace(/\s+/g, '').toLowerCase()));

        let roster = (data || [])
          .filter(s => {
            const isNotOut = s.status !== 'TC_OUT' && s.status !== 'DELETED' && s.status !== 'REMOVED';
            const sKey1 = String(s.id || '').replace(/\s+/g, '').toLowerCase();
            const sKey2 = String(s.student_sts || s.app_no || '').replace(/\s+/g, '').toLowerCase();
            const isNotTrashed = (!sKey1 || !trashedKeys.has(sKey1)) && (!sKey2 || !trashedKeys.has(sKey2));
            const isClass = className === "ALL" || normalizeClass(s.enroll_class) === normalizeClass(className);
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
            adminNo: s.app_no || s.student_sts || s.id,
            app_no: s.app_no || '',
            enrollClass: s.enroll_class
          }));

        // Fallback to local students if database had no matches or errored
        if (roster.length === 0) {
          try {
            const localSt = JSON.parse(
              localStorage.getItem(`students_class_${className}`) ||
              localStorage.getItem("all_students_cache") ||
              localStorage.getItem("students_data") ||
              localStorage.getItem("sts_master_list") ||
              localStorage.getItem("students") ||
              localStorage.getItem("admissions_data") ||
              "[]"
            );
            const matchedLocal = localSt.filter(s => {
              const isClass = className === "ALL" || normalizeClass(s.enrollClass || s.enroll_class || s.standard || s.class || className) === normalizeClass(className);
              const sKey = String(s.id || s.adminNo || s.app_no || s.student_sts || '').replace(/\s+/g, '').toLowerCase();
              return isClass && (!sKey || !trashedKeys.has(sKey));
            });
            if (matchedLocal.length > 0) {
              roster = matchedLocal.map(s => ({
                id: s.id,
                student_name_kn: s.student_name_kn || s.student_name || s.name || '',
                student_name: s.student_name || s.name || '',
                name_english: s.name_english || s.name || '',
                father_name_kn: s.father_name_kn || s.father || '',
                father_name_az: s.father_name_az || s.father || '',
                mother_name_kn: s.mother_name_kn || s.mother || '',
                mother_name_az: s.mother_name_az || s.mother || '',
                gender: s.gender || s.sex || '',
                caste: s.caste || s.category || '',
                adminNo: s.adminNo || s.app_no || s.sts_no || s.student_sts || s.id,
                app_no: s.app_no || s.adminNo || s.id || '',
                enrollClass: s.enrollClass || s.enroll_class || s.class || className
              }));
            }
          } catch (localErr) {
            console.warn("Local storage student fallback error:", localErr);
          }
        }

        roster.sort((a, b) => {
          const nameA = (a.name_english || a.student_name_kn || '').trim().toUpperCase();
          const nameB = (b.name_english || b.student_name_kn || '').trim().toUpperCase();
          return nameA.localeCompare(nameB);
        });

        let allEvaluations = {};
        
        // Helper to load from localStorage
        const loadLocal = () => {
          let localData = {};
          if (className === "ALL") {
            const classes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];
            classes.forEach((cName) => {
              const mockKey = `cce_eval_${cName}_${examType}`;
              let saved = localStorage.getItem(mockKey);
              if (saved) {
                try {
                  Object.assign(localData, JSON.parse(saved));
                } catch (e) {
                  console.error("Failed to parse local CCE evaluations for " + cName, e);
                }
              }
            });
          } else {
            const mockKey = `cce_eval_${className}_${examType}`;
            let saved = localStorage.getItem(mockKey);
            if (saved) {
              try {
                localData = JSON.parse(saved) || {};
              } catch (e) {
                localData = {};
              }
            }
          }
          return localData;
        };

        try {
          let dbQuery = supabaseClient
            .from('cce_evaluations')
            .select('student_id, marks')
            .eq('exam_type', examType);

          const { data: dbRecords, error: dbError } = await dbQuery;

          if (dbError) {
            console.warn("Supabase fetch for CCE evaluations failed, falling back to local storage:", dbError);
            allEvaluations = loadLocal();
          } else if (dbRecords && dbRecords.length > 0) {
            dbRecords.forEach(r => {
              allEvaluations[r.student_id] = r.marks || {};
            });
            console.log("Loaded CCE evaluations from Supabase");
          } else {
            allEvaluations = loadLocal();
          }
        } catch (e) {
          console.warn("Exception loading CCE evaluations from Supabase, fallback to localStorage:", e);
          allEvaluations = loadLocal();
        }

        onDataLoaded({
          success: true,
          students: roster,
          evaluations: allEvaluations
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

      // Sanitize and re-evaluate grades from actual mark data
      const className = classFilter.value;
      const isSA = examTypeFilter.value.startsWith("SA");
      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      const wMax = isPrimary ? (mutableConfigs.primary.saWrittenMax || 30) : (mutableConfigs.middleHigh.saWrittenMax || 40);
      const oMax = isPrimary ? (mutableConfigs.primary.saOralMax || 20) : (mutableConfigs.middleHigh.saOralMax || 10);
      const saTotalMax = wMax + oMax;

      students.forEach(s => {
        const sId = s.id;
        if (!evaluations[sId]) evaluations[sId] = {};
        const eData = evaluations[sId];
        currentSubjects.forEach(sub => {
          const sKey = sub.id;
          if (isSA) {
            const wVal = eData[sKey + "_w"];
            const oVal = eData[sKey + "_o"];
            const hasW = (wVal !== '' && wVal !== undefined && wVal !== null);
            const hasO = (oVal !== '' && oVal !== undefined && oVal !== null);
            if (hasW || hasO) {
              const total = ((parseFloat(wVal) || 0) + (parseFloat(oVal) || 0)).toString();
              eData[sKey + "_mark"] = total;
              eData[sKey + "_grade"] = determineGradeByScale(total, saTotalMax);
            } else {
              eData[sKey + "_mark"] = '';
              eData[sKey + "_grade"] = '-';
            }
          } else {
            const m = eData[sKey + "_mark"];
            if (m !== '' && m !== undefined && m !== null) {
              eData[sKey + "_grade"] = determineGradeByScale(m, cfg.faMax);
            } else {
              eData[sKey + "_mark"] = '';
              eData[sKey + "_grade"] = '-';
            }
          }
        });
      });

      originalEvaluations = JSON.parse(JSON.stringify(evaluations));

      const gridSubtitle = document.getElementById('grid-subtitle');
      if (gridSubtitle) gridSubtitle.innerText = `${classFilter.value} | Exam: ${examTypeFilter.value}`;
      
      const statsBar = document.getElementById('stats-bar');
      if (statsBar) statsBar.classList.remove('hidden');

      const sfBar = document.getElementById('search-filter-bar');
      if (sfBar) sfBar.classList.remove('hidden');

      if (document.getElementById('btn-export-pdf')) document.getElementById('btn-export-pdf').classList.remove('hidden');
      if (document.getElementById('btn-export-excel')) document.getElementById('btn-export-excel').classList.remove('hidden');
      if (document.getElementById('btn-print')) document.getElementById('btn-print').classList.remove('hidden');
      if (document.getElementById('btn-export-csv')) document.getElementById('btn-export-csv').classList.remove('hidden');
      if (document.getElementById('btn-import-csv')) document.getElementById('btn-import-csv').classList.remove('hidden');
      if (document.getElementById('btn-add-student')) document.getElementById('btn-add-student').classList.remove('hidden');
      
      isEditing = true;
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
      localStorage.setItem('cce_view_mode', currentViewMode);

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
      const tableEl = document.getElementById('table-container');
      const cardsEl = document.getElementById('student-cards-container');
      const tableTag = document.getElementById('competency-table');
      const sfBar = document.getElementById('search-filter-bar');

      if (sfBar) sfBar.classList.remove('hidden');

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
          if (tableTag) tableTag.classList.remove('hidden');
          renderGrid();
        }
      }
      updateTotals();
    }

    function buildTableHeader() {
      const thead = document.getElementById('table-head');
      if (!thead) return;
      const selectedSub = subjectFilter.value;
      const isSA = examTypeFilter.value.startsWith("SA");
      
      let subHeadersHtml = ''; let subLabelsHtml = '';
      let numVisibleSubs = 0;
      currentSubjects.forEach(sub => { if (selectedSub === "ALL" || sub.id === selectedSub) numVisibleSubs++; });

      const colsPerSub = isSA ? 4 : 2;
      const totalSubCols = numVisibleSubs * colsPerSub;
      const pctPerSubCol = (100 - 54) / totalSubCols;

      currentSubjects.forEach(sub => {
        if (selectedSub !== "ALL" && sub.id !== selectedSub) return;
        if (isSA) {
          subHeadersHtml += `<th colspan="4" class="p-2 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: ${(pctPerSubCol * 4).toFixed(2)}%;">${sub.name}</th>`;
          subLabelsHtml += `
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 bg-amber-50/20 font-bold" style="width: ${pctPerSubCol.toFixed(2)}%;">W</th>
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 bg-amber-50/20 font-bold" style="width: ${pctPerSubCol.toFixed(2)}%;">O</th>
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 font-bold bg-amber-100/20" style="width: ${pctPerSubCol.toFixed(2)}%;">Tot</th>
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: ${pctPerSubCol.toFixed(2)}%;">G</th>
          `;
        } else {
          subHeadersHtml += `<th colspan="2" class="p-2 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: ${(pctPerSubCol * 2).toFixed(2)}%;">${sub.name}</th>`;
          subLabelsHtml += `
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: ${pctPerSubCol.toFixed(2)}%;">M</th>
            <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: ${pctPerSubCol.toFixed(2)}%;">G</th>
          `;
        }
      });

      thead.innerHTML = `
        <tr class="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border-b border-slate-200 dark:border-slate-700 font-bold">
          <th rowspan="2" class="p-3 text-center border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 4%;">ಕ್ರ.ಸಂ</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 10%;">STS ಸಂಖ್ಯೆ</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 16%;">ಹೆಸರು</th>
          <th rowspan="2" class="p-3 border-r border-slate-200 dark:border-slate-700 font-bold" style="width: 14%;">ತಂದೆಯ ಹೆಸರು</th>
          ${subHeadersHtml}
          <th colspan="2" class="p-2 text-center font-bold" style="width: 10%;">ಒಟ್ಟು ಕೌಂಟ್</th>
        </tr>
        <tr class="bg-slate-50 dark:bg-slate-850 text-[10px] text-slate-500 uppercase border-b border-slate-200 dark:border-slate-700">
          ${subLabelsHtml}
          <th class="p-1.5 text-center border-r border-slate-200 dark:border-slate-700 bg-emerald-50 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-300 font-bold" style="width: 5%;">A+,A</th>
          <th class="p-1.5 text-center bg-blue-50 dark:bg-blue-950/20 text-blue-800 dark:text-blue-300 font-bold" style="width: 5%;">Others</th>
        </tr>
      `;
    }

    function handleGridKeyNav(e, row, col) {
      if (['ArrowUp', 'ArrowDown', 'Enter'].includes(e.key)) {
        if (e.key === 'ArrowDown' || e.key === 'Enter') {
          e.preventDefault();
          const nextInput = document.querySelector(`input[data-nav-grid="true"][data-row="${row + 1}"][data-col="${col}"]`);
          if (nextInput) { nextInput.focus(); nextInput.select(); }
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          const prevInput = document.querySelector(`input[data-nav-grid="true"][data-row="${row - 1}"][data-col="${col}"]`);
          if (prevInput) { prevInput.focus(); prevInput.select(); }
        }
      } else if (e.key === 'ArrowRight') {
        const input = e.target;
        if (input.selectionEnd === input.value.length) {
          const nextCol = document.querySelector(`input[data-nav-grid="true"][data-row="${row}"][data-col="${col + 1}"]`);
          if (nextCol) { e.preventDefault(); nextCol.focus(); nextCol.select(); }
        }
      } else if (e.key === 'ArrowLeft') {
        const input = e.target;
        if (input.selectionStart === 0) {
          const prevCol = document.querySelector(`input[data-nav-grid="true"][data-row="${row}"][data-col="${col - 1}"]`);
          if (prevCol) { e.preventDefault(); prevCol.focus(); prevCol.select(); }
        }
      }
    }

    function handleCardKeyNav(e, row, col) {
      if (['ArrowUp', 'ArrowDown', 'Enter'].includes(e.key)) {
        if (e.key === 'ArrowDown' || e.key === 'Enter') {
          e.preventDefault();
          const nextInput = document.querySelector(`input[data-nav-card="true"][data-card-row="${row + 1}"][data-card-col="${col}"]`);
          if (nextInput) { nextInput.focus(); nextInput.select(); }
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          const prevInput = document.querySelector(`input[data-nav-card="true"][data-card-row="${row - 1}"][data-card-col="${col}"]`);
          if (prevInput) { prevInput.focus(); prevInput.select(); }
        }
      } else if (e.key === 'ArrowRight') {
        const input = e.target;
        if (input.selectionEnd === input.value.length) {
          const nextCol = document.querySelector(`input[data-nav-card="true"][data-card-row="${row}"][data-card-col="${col + 1}"]`);
          if (nextCol) { e.preventDefault(); nextCol.focus(); nextCol.select(); }
        }
      } else if (e.key === 'ArrowLeft') {
        const input = e.target;
        if (input.selectionStart === 0) {
          const prevCol = document.querySelector(`input[data-nav-card="true"][data-card-row="${row}"][data-card-col="${col - 1}"]`);
          if (prevCol) { e.preventDefault(); prevCol.focus(); prevCol.select(); }
        }
      }
    }

    function renderGrid() {
      const tbody = document.getElementById('student-grid-body');
      if (!tbody) return;
      tbody.innerHTML = '';
      const className = classFilter.value;
      const examType = examTypeFilter.value;
      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      
      const selectedSub = subjectFilter.value;
      const isSA = examType.startsWith("SA");
      const filtered = getFilteredStudents();

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="20" class="p-8 text-center text-slate-400 font-semibold">ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</td></tr>`;
        return;
      }

      filtered.forEach((student, index) => {
        const sId = student.id;
        if (!evaluations[sId]) evaluations[sId] = {};
        const evalData = evaluations[sId];
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || student.student_name || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();

        const tr = document.createElement('tr');
        tr.className = "hover:bg-indigo-50/20 dark:hover:bg-slate-800/40 transition";
        let rowHtml = `
          <td class="p-2 text-center border-r border-slate-200 dark:border-slate-700 font-bold">${index + 1}</td>
          <td class="p-2 border-r border-slate-200 dark:border-slate-700 font-mono text-slate-600 dark:text-slate-400 text-xs">${student.adminNo || student.id}</td>
          <td class="p-2 border-r border-slate-200 dark:border-slate-700 font-semibold">${nameEn || nameKn}${nameKn && nameEn ? `<br><span class="text-[10px] text-slate-400 font-normal">${nameKn}</span>` : ''}</td>
          <td class="p-2 border-r border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400">${fatherEn || fatherKn || '-'}</td>
        `;

        let colIdx = 0;
        currentSubjects.forEach(sub => {
          if (selectedSub !== "ALL" && sub.id !== selectedSub) return;
          const sKey = sub.id;

          if (isSA) {
            const wVal = evalData[sKey + "_w"] !== undefined ? evalData[sKey + "_w"] : '';
            const oVal = evalData[sKey + "_o"] !== undefined ? evalData[sKey + "_o"] : '';
            const wMax = isPrimary ? (mutableConfigs.primary.saWrittenMax || 30) : (mutableConfigs.middleHigh.saWrittenMax || 40);
            const oMax = isPrimary ? (mutableConfigs.primary.saOralMax || 20) : (mutableConfigs.middleHigh.saOralMax || 10);
            const saTotalMax = wMax + oMax;

            const hasW = (wVal !== '' && wVal !== undefined && wVal !== null);
            const hasO = (oVal !== '' && oVal !== undefined && oVal !== null);
            let totalVal = '';
            let g = '-';
            if (hasW || hasO) {
              const w = parseFloat(wVal) || 0;
              const o = parseFloat(oVal) || 0;
              totalVal = (w + o).toString();
              g = determineGradeByScale(w + o, saTotalMax);
            }
            evalData[sKey + "_mark"] = totalVal;
            evalData[sKey + "_grade"] = g;

            const c1 = colIdx++;
            const c2 = colIdx++;

            rowHtml += `
              <td class="p-1 border-r border-slate-200 dark:border-slate-700 text-center">
                <input type="number" min="0" max="${wMax}" value="${wVal}" data-nav-grid="true" data-row="${index}" data-col="${c1}" onkeydown="handleGridKeyNav(event, ${index}, ${c1})" onfocus="this.select()" oninput="onSAMarkChange('${sId}', '${sKey}', 'w', this.value, this)" class="w-10 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-0.5 text-center font-bold text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-900 dark:text-white transition">
              </td>
              <td class="p-1 border-r border-slate-200 dark:border-slate-700 text-center">
                <input type="number" min="0" max="${oMax}" value="${oVal}" data-nav-grid="true" data-row="${index}" data-col="${c2}" onkeydown="handleGridKeyNav(event, ${index}, ${c2})" onfocus="this.select()" oninput="onSAMarkChange('${sId}', '${sKey}', 'o', this.value, this)" class="w-10 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-0.5 text-center font-bold text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-900 dark:text-white transition">
              </td>
              <td id="total-${sId}-${sKey}" class="p-2 border-r border-slate-200 dark:border-slate-700 text-center font-black bg-slate-50/50 dark:bg-slate-850 text-xs">${totalVal !== '' ? totalVal : '-'}</td>
              <td class="p-1 border-r border-slate-200 dark:border-slate-700 text-center font-bold">
                <span id="grade-${sId}-${sKey}" class="${getCceGradeBadgeClass(g)}">${g}</span>
              </td>
            `;
          } else {
            const m = evalData[sKey + "_mark"] !== undefined ? evalData[sKey + "_mark"] : '';
            const g = (m !== '' && m !== null && m !== undefined) ? determineGradeByScale(m, cfg.faMax) : '-';
            evalData[sKey + "_grade"] = g;
            const c = colIdx++;

            rowHtml += `
              <td class="p-1.5 border-r border-slate-200 dark:border-slate-700 text-center">
                <input type="number" min="0" max="${cfg.faMax}" value="${m}" data-nav-grid="true" data-row="${index}" data-col="${c}" onkeydown="handleGridKeyNav(event, ${index}, ${c})" onfocus="this.select()" oninput="onFAMarkChange('${sId}', '${sKey}', this.value, this)" class="w-12 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-1 text-center font-bold focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-900 dark:text-white transition">
              </td>
              <td class="p-1.5 border-r border-slate-200 dark:border-slate-700 text-center font-bold bg-slate-50/50 dark:bg-slate-850">
                <span id="grade-${sId}-${sKey}" class="${getCceGradeBadgeClass(g)}">${g}</span>
              </td>
            `;
          }
        });

        rowHtml += `
          <td id="row-total-a-${sId}" class="p-3 border-r border-slate-200 dark:border-slate-700 text-center font-black bg-emerald-50 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-300 text-xs">0</td>
          <td id="row-total-b-${sId}" class="p-3 text-center font-black bg-blue-50 dark:bg-blue-950/20 text-blue-800 dark:text-blue-300 text-xs">0</td>
        `;

        tr.innerHTML = rowHtml;
        tbody.appendChild(tr);
      });
    }

    function getCceGradeBadgeClass(g) {
      if (g === 'A+') return 'inline-block bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/40 rounded-lg px-2 py-0.5 font-black text-xs shadow-xs';
      if (g === 'A') return 'inline-block bg-teal-500/15 text-teal-700 dark:text-teal-300 border border-teal-500/40 rounded-lg px-2 py-0.5 font-bold text-xs shadow-xs';
      if (g === 'B+') return 'inline-block bg-sky-500/15 text-sky-700 dark:text-sky-300 border border-sky-500/40 rounded-lg px-2 py-0.5 font-bold text-xs shadow-xs';
      if (g === 'B') return 'inline-block bg-indigo-500/15 text-indigo-700 dark:text-indigo-300 border border-indigo-500/40 rounded-lg px-2 py-0.5 font-bold text-xs shadow-xs';
      if (g === 'C+' || g === 'C') return 'inline-block bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/40 rounded-lg px-2 py-0.5 font-bold text-xs shadow-xs';
      if (g === 'D') return 'inline-block bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/40 rounded-lg px-2 py-0.5 font-bold text-xs shadow-xs';
      return 'inline-block bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400 border border-slate-200 dark:border-slate-700 rounded-lg px-2 py-0.5 font-bold text-xs';
    }

    function getStudentOverallGrade(studentId) {
      const evalData = evaluations[studentId] || {};
      const selectedSub = subjectFilter.value;
      if (selectedSub !== "ALL") {
        return evalData[selectedSub + "_grade"] || '-';
      }
      let totalEntered = 0;
      let gradeCounts = { 'A+': 0, 'A': 0, 'B+': 0, 'B': 0, 'C+': 0, 'C': 0, 'D': 0 };
      currentSubjects.forEach(sub => {
        const g = evalData[sub.id + "_grade"];
        if (g && g !== '-') {
          totalEntered++;
          if (gradeCounts[g] !== undefined) gradeCounts[g]++;
        }
      });
      if (totalEntered === 0) return '-';
      if (gradeCounts['A+'] > 0 && gradeCounts['A+'] >= (totalEntered / 2)) return 'A+';
      if ((gradeCounts['A+'] + gradeCounts['A']) >= (totalEntered / 2)) return 'A';
      if ((gradeCounts['A+'] + gradeCounts['A'] + gradeCounts['B+']) >= (totalEntered / 2)) return 'B+';
      if ((gradeCounts['A+'] + gradeCounts['A'] + gradeCounts['B+'] + gradeCounts['B']) >= (totalEntered / 2)) return 'B';
      return 'C+';
    }

    function getStudentCardClasses(grade) {
      if (grade === 'A+') {
        return 'bg-gradient-to-b from-emerald-50/90 via-white to-emerald-50/30 dark:from-emerald-950/40 dark:via-slate-850 dark:to-slate-850 border-2 border-emerald-400 dark:border-emerald-500/70 shadow-md shadow-emerald-500/10 ring-1 ring-emerald-400/30';
      } else if (grade === 'A') {
        return 'bg-gradient-to-b from-teal-50/90 via-white to-teal-50/30 dark:from-teal-950/40 dark:via-slate-850 dark:to-slate-850 border-2 border-teal-400 dark:border-teal-500/70 shadow-md shadow-teal-500/10 ring-1 ring-teal-400/30';
      } else if (grade === 'B+') {
        return 'bg-gradient-to-b from-sky-50/90 via-white to-sky-50/30 dark:from-sky-950/40 dark:via-slate-850 dark:to-slate-850 border-2 border-sky-400 dark:border-sky-500/70 shadow-md shadow-sky-500/10 ring-1 ring-sky-400/30';
      } else if (grade === 'B') {
        return 'bg-gradient-to-b from-indigo-50/90 via-white to-indigo-50/30 dark:from-indigo-950/40 dark:via-slate-850 dark:to-slate-850 border-2 border-indigo-400 dark:border-indigo-500/70 shadow-md shadow-indigo-500/10 ring-1 ring-indigo-400/30';
      } else if (grade === 'C+' || grade === 'C') {
        return 'bg-gradient-to-b from-amber-50/90 via-white to-amber-50/30 dark:from-amber-950/40 dark:via-slate-850 dark:to-slate-850 border-2 border-amber-400 dark:border-amber-500/70 shadow-md shadow-amber-500/10 ring-1 ring-amber-400/30';
      } else if (grade === 'D') {
        return 'bg-gradient-to-b from-rose-50/90 via-white to-rose-50/30 dark:from-rose-950/40 dark:via-slate-850 dark:to-slate-850 border-2 border-rose-400 dark:border-rose-500/70 shadow-md shadow-rose-500/10 ring-1 ring-rose-400/30';
      }
      return 'bg-white dark:bg-slate-850 border border-slate-200 dark:border-slate-800 shadow-sm';
    }

    function getSubjectCardBoxClasses(grade) {
      if (grade === 'A+') return 'p-2.5 rounded-xl bg-emerald-100/70 dark:bg-emerald-950/50 border border-emerald-300 dark:border-emerald-700/80 space-y-2 transition-colors duration-200';
      if (grade === 'A') return 'p-2.5 rounded-xl bg-teal-100/70 dark:bg-teal-950/50 border border-teal-300 dark:border-teal-700/80 space-y-2 transition-colors duration-200';
      if (grade === 'B+') return 'p-2.5 rounded-xl bg-sky-100/70 dark:bg-sky-950/50 border border-sky-300 dark:border-sky-700/80 space-y-2 transition-colors duration-200';
      if (grade === 'B') return 'p-2.5 rounded-xl bg-indigo-100/70 dark:bg-indigo-950/50 border border-indigo-300 dark:border-indigo-700/80 space-y-2 transition-colors duration-200';
      if (grade === 'C+' || grade === 'C') return 'p-2.5 rounded-xl bg-amber-100/70 dark:bg-amber-950/50 border border-amber-300 dark:border-amber-700/80 space-y-2 transition-colors duration-200';
      if (grade === 'D') return 'p-2.5 rounded-xl bg-rose-100/70 dark:bg-rose-950/50 border border-rose-300 dark:border-rose-700/80 space-y-2 transition-colors duration-200';
      return 'p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 space-y-2 transition-colors duration-200';
    }

    function updateCardVisualTheme(studentId, subKey, grade) {
      const cardEl = document.getElementById(`student-card-${studentId}`);
      if (cardEl) {
        const overallGrade = getStudentOverallGrade(studentId);
        cardEl.className = `student-card-item rounded-2xl p-4 transition-all duration-300 flex flex-col justify-between space-y-3.5 ${getStudentCardClasses(overallGrade)}`;
      }
      const subBox = document.getElementById(`subject-card-box-${studentId}-${subKey}`);
      if (subBox) {
        subBox.className = getSubjectCardBoxClasses(grade);
      }
    }

    function renderCards() {
      const container = document.getElementById('student-cards-container');
      if (!container) return;
      container.innerHTML = '';

      const className = classFilter.value;
      const examType = examTypeFilter.value;
      const selectedSub = subjectFilter.value;
      const isSA = examType.startsWith("SA");
      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      const filtered = getFilteredStudents();

      if (filtered.length === 0) {
        container.innerHTML = `<div class="col-span-full p-12 text-center text-slate-400 font-semibold bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800"><i class="fa-solid fa-user-slash text-3xl mb-2 text-slate-300"></i><p>ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿ ಕಂಡುಬಂದಿಲ್ಲ.</p></div>`;
        return;
      }

      const faMax = cfg.faMax;
      const wMax = isPrimary ? (mutableConfigs.primary.saWrittenMax || 30) : (mutableConfigs.middleHigh.saWrittenMax || 40);
      const oMax = isPrimary ? (mutableConfigs.primary.saOralMax || 20) : (mutableConfigs.middleHigh.saOralMax || 10);
      const presetChips = [faMax, Math.round(faMax * 0.9), Math.round(faMax * 0.75), Math.round(faMax * 0.5), Math.round(faMax * 0.25), 0].filter((v, i, arr) => arr.indexOf(v) === i);

      filtered.forEach((student, index) => {
        const sId = student.id;
        if (!evaluations[sId]) evaluations[sId] = {};
        const evalData = evaluations[sId];
        const nameEn = (student.name_english || '').trim().toUpperCase();
        const nameKn = (student.student_name_kn || student.student_name || '').trim();
        const fatherEn = (student.father_name_az || '').trim().toUpperCase();
        const fatherKn = (student.father_name_kn || '').trim();
        const isBoy = student.gender === 'Boy';
        const overallGrade = getStudentOverallGrade(sId);

        let subCardsHtml = '';
        let cardColIdx = 0;
        currentSubjects.forEach(sub => {
          if (selectedSub !== "ALL" && sub.id !== selectedSub) return;
          const sKey = sub.id;

          if (isSA) {
            const wVal = evalData[sKey + "_w"] !== undefined ? evalData[sKey + "_w"] : '';
            const oVal = evalData[sKey + "_o"] !== undefined ? evalData[sKey + "_o"] : '';
            const hasW = (wVal !== '' && wVal !== undefined && wVal !== null);
            const hasO = (oVal !== '' && oVal !== undefined && oVal !== null);
            let totalVal = '';
            let g = '-';
            if (hasW || hasO) {
              const w = parseFloat(wVal) || 0;
              const o = parseFloat(oVal) || 0;
              totalVal = (w + o).toString();
              g = determineGradeByScale(w + o, wMax + oMax);
            }
            evalData[sKey + "_mark"] = totalVal;
            evalData[sKey + "_grade"] = g;

            const cc1 = cardColIdx++;
            const cc2 = cardColIdx++;

            subCardsHtml += `
              <div id="subject-card-box-${sId}-${sKey}" class="${getSubjectCardBoxClasses(g)}">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black text-slate-800 dark:text-slate-200 truncate max-w-[160px]">${sub.name}</span>
                  <span id="card-grade-${sId}-${sKey}" class="${getCceGradeBadgeClass(g)}">${g}</span>
                </div>
                <div class="grid grid-cols-3 gap-1.5 items-center">
                  <div>
                    <span class="text-[9px] text-slate-400 font-bold block mb-0.5">ಬರಹ (W: 0-${wMax})</span>
                    <input type="number" min="0" max="${wMax}" value="${wVal}" data-nav-card="true" data-card-row="${index}" data-card-col="${cc1}" onkeydown="handleCardKeyNav(event, ${index}, ${cc1})" onfocus="this.select()" oninput="onSAMarkChange('${sId}', '${sKey}', 'w', this.value, this)" class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg py-1 text-center font-bold text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-900 dark:text-white transition" placeholder="0-${wMax}">
                  </div>
                  <div>
                    <span class="text-[9px] text-slate-400 font-bold block mb-0.5">ಮೌಖಿಕ (O: 0-${oMax})</span>
                    <input type="number" min="0" max="${oMax}" value="${oVal}" data-nav-card="true" data-card-row="${index}" data-card-col="${cc2}" onkeydown="handleCardKeyNav(event, ${index}, ${cc2})" onfocus="this.select()" oninput="onSAMarkChange('${sId}', '${sKey}', 'o', this.value, this)" class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg py-1 text-center font-bold text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-900 dark:text-white transition" placeholder="0-${oMax}">
                  </div>
                  <div>
                    <span class="text-[9px] text-indigo-500 font-black block mb-0.5">ಒಟ್ಟು (Total)</span>
                    <div id="card-total-${sId}-${sKey}" class="w-full bg-indigo-50 dark:bg-slate-950 border border-indigo-200 dark:border-indigo-900/50 rounded-lg py-1 text-center font-black text-xs text-indigo-700 dark:text-indigo-300">${totalVal !== '' ? totalVal : '-'}</div>
                  </div>
                </div>
              </div>
            `;
          } else {
            const m = evalData[sKey + "_mark"] !== undefined ? evalData[sKey + "_mark"] : '';
            const g = (m !== '' && m !== null && m !== undefined) ? determineGradeByScale(m, cfg.faMax) : '-';
            evalData[sKey + "_grade"] = g;
            const cc = cardColIdx++;

            subCardsHtml += `
              <div id="subject-card-box-${sId}-${sKey}" class="${getSubjectCardBoxClasses(g)}">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black text-slate-800 dark:text-slate-200 truncate max-w-[160px]">${sub.name}</span>
                  <span id="card-grade-${sId}-${sKey}" class="${getCceGradeBadgeClass(g)}">${g}</span>
                </div>
                <div class="flex items-center gap-1.5">
                  <button type="button" onclick="stepCceFAMark('${sId}', '${sKey}', -1)" class="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 font-black text-sm flex items-center justify-center border-0 cursor-pointer active:scale-95">-</button>
                  <input type="number" min="0" max="${faMax}" id="card-input-${sId}-${sKey}" value="${m}" data-nav-card="true" data-card-row="${index}" data-card-col="${cc}" onkeydown="handleCardKeyNav(event, ${index}, ${cc})" onfocus="this.select()" oninput="onFAMarkChange('${sId}', '${sKey}', this.value, this)" class="flex-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg py-1 text-center font-black text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-900 dark:text-white transition" placeholder="0-${faMax}">
                  <button type="button" onclick="stepCceFAMark('${sId}', '${sKey}', 1)" class="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 font-black text-sm flex items-center justify-center border-0 cursor-pointer active:scale-95">+</button>
                </div>
                <!-- Preset Chips -->
                <div class="flex items-center gap-1 justify-between pt-0.5">
                  ${presetChips.map(sc => `
                    <button type="button" onclick="quickSetCceFAMark('${sId}', '${sKey}', ${sc})" class="px-1.5 py-0.5 rounded bg-slate-200/60 dark:bg-slate-700/60 hover:bg-indigo-600 hover:text-white text-[10px] font-bold text-slate-600 dark:text-slate-300 transition cursor-pointer border-0">${sc}</button>
                  `).join('')}
                </div>
              </div>
            `;
          }
        });

        const cardHtml = `
          <div id="student-card-${sId}" class="student-card-item rounded-2xl p-4 transition-all duration-300 flex flex-col justify-between space-y-3.5 ${getStudentCardClasses(overallGrade)}">
            <!-- Header -->
            <div class="flex items-start justify-between gap-2 border-b border-slate-200/60 dark:border-slate-800 pb-2.5">
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

            <!-- Subject Grid -->
            <div class="space-y-2 pt-1 flex-1">
              ${subCardsHtml}
            </div>

            <!-- Footer -->
            <div class="flex items-center justify-between pt-2.5 border-t border-slate-200/60 dark:border-slate-800 text-xs">
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/30 px-2 py-0.5 rounded">A+,A: <strong id="card-total-a-${sId}">0</strong></span>
                <span class="text-[10px] font-bold text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/30 px-2 py-0.5 rounded">ಇತರ: <strong id="card-total-b-${sId}">0</strong></span>
              </div>
            </div>
          </div>
        `;

        container.innerHTML += cardHtml;
      });
    }

    function onFAMarkChange(studentId, subKey, val, inputEl) {
      if (!evaluations[studentId]) evaluations[studentId] = {};
      const className = classFilter.value;
      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      
      if (val !== '' && val !== null && val !== undefined) {
        let num = parseFloat(val);
        if (!isNaN(num)) {
          if (num > cfg.faMax) {
            num = cfg.faMax;
            val = cfg.faMax.toString();
            if (inputEl) inputEl.value = cfg.faMax;
            const cardInput = document.getElementById(`card-input-${studentId}-${subKey}`);
            if (cardInput) cardInput.value = cfg.faMax;
          } else if (num < 0) {
            num = 0;
            val = '0';
            if (inputEl) inputEl.value = '0';
            const cardInput = document.getElementById(`card-input-${studentId}-${subKey}`);
            if (cardInput) cardInput.value = '0';
          }
        }
      }

      evaluations[studentId][subKey + "_mark"] = val;
      const grade = (val !== '' && val !== null && val !== undefined) ? determineGradeByScale(val, cfg.faMax) : '-';
      evaluations[studentId][subKey + "_grade"] = grade;

      const tableGradeEl = document.getElementById(`grade-${studentId}-${subKey}`);
      if (tableGradeEl) {
        tableGradeEl.innerText = grade;
        tableGradeEl.className = `${getCceGradeBadgeClass(grade)} badge-print`;
      }

      const cardGradeEl = document.getElementById(`card-grade-${studentId}-${subKey}`);
      if (cardGradeEl) {
        cardGradeEl.innerText = grade;
        cardGradeEl.className = getCceGradeBadgeClass(grade);
      }

      // Dynamic Card & Box Colors
      updateCardVisualTheme(studentId, subKey, grade);

      updateTotals();
      triggerAutoSave();
    }

    function onSAMarkChange(studentId, subKey, type, val, inputEl) {
      if (!evaluations[studentId]) evaluations[studentId] = {};
      const className = classFilter.value;
      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const wMax = isPrimary ? (mutableConfigs.primary.saWrittenMax || 30) : (mutableConfigs.middleHigh.saWrittenMax || 40);
      const oMax = isPrimary ? (mutableConfigs.primary.saOralMax || 20) : (mutableConfigs.middleHigh.saOralMax || 10);

      if (type === 'w') {
        if (val !== '' && val !== null && val !== undefined) {
          let num = parseFloat(val);
          if (!isNaN(num)) {
            if (num > wMax) { num = wMax; val = wMax.toString(); if (inputEl) inputEl.value = wMax; }
            else if (num < 0) { num = 0; val = '0'; if (inputEl) inputEl.value = '0'; }
          }
        }
        evaluations[studentId][subKey + "_w"] = val;
      } else if (type === 'o') {
        if (val !== '' && val !== null && val !== undefined) {
          let num = parseFloat(val);
          if (!isNaN(num)) {
            if (num > oMax) { num = oMax; val = oMax.toString(); if (inputEl) inputEl.value = oMax; }
            else if (num < 0) { num = 0; val = '0'; if (inputEl) inputEl.value = '0'; }
          }
        }
        evaluations[studentId][subKey + "_o"] = val;
      }

      const wVal = evaluations[studentId][subKey + "_w"];
      const oVal = evaluations[studentId][subKey + "_o"];

      const hasW = (wVal !== '' && wVal !== undefined && wVal !== null);
      const hasO = (oVal !== '' && oVal !== undefined && oVal !== null);

      let total = '';
      let grade = '-';
      if (hasW || hasO) {
        const w = parseFloat(wVal) || 0;
        const o = parseFloat(oVal) || 0;
        total = w + o;
        const saTotalMax = wMax + oMax;
        grade = determineGradeByScale(total, saTotalMax);
      }

      evaluations[studentId][subKey + "_mark"] = total;
      evaluations[studentId][subKey + "_grade"] = grade;

      // Table DOM updates
      const tableTotalEl = document.getElementById(`total-${studentId}-${subKey}`);
      if (tableTotalEl) tableTotalEl.innerText = total !== '' ? total : '-';
      const tableGradeEl = document.getElementById(`grade-${studentId}-${subKey}`);
      if (tableGradeEl) {
        tableGradeEl.innerText = grade;
        tableGradeEl.className = `${getCceGradeBadgeClass(grade)} badge-print`;
      }

      // Card DOM updates
      const cardTotalEl = document.getElementById(`card-total-${studentId}-${subKey}`);
      if (cardTotalEl) cardTotalEl.innerText = total !== '' ? total : '-';
      const cardGradeEl = document.getElementById(`card-grade-${studentId}-${subKey}`);
      if (cardGradeEl) {
        cardGradeEl.innerText = grade;
        cardGradeEl.className = getCceGradeBadgeClass(grade);
      }

      // Dynamic Card & Box Colors
      updateCardVisualTheme(studentId, subKey, grade);

      updateTotals();
      triggerAutoSave();
    }

    function triggerAutoSave() {
      const indicator = document.getElementById('auto-save-indicator');
      if (indicator) {
        indicator.classList.remove('hidden');
        indicator.className = 'text-xs font-bold px-2.5 py-1 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 flex items-center gap-1.5 border border-amber-200/60 dark:border-amber-900/40';
        indicator.innerHTML = '<i class="fa-solid fa-arrows-rotate fa-spin text-amber-500 text-[11px]"></i> <span>ಉಳಿಸಲಾಗುತ್ತಿದೆ... / Saving...</span>';
      }

      if (autoSaveTimer) clearTimeout(autoSaveTimer);
      autoSaveTimer = setTimeout(() => {
        performSilentSave();
      }, 700);
    }

    function performSilentSave() {
      const className = classFilter.value;
      const examType = examTypeFilter.value;
      if (!className || !examType || students.length === 0) return;

      // Local backup immediately
      const mockKey = `cce_eval_${className}_${examType}`;
      localStorage.setItem(mockKey, JSON.stringify(evaluations));

      supabaseClient.auth.getSession().then(({ data: { session } }) => {
        const rawSchoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id")) || null;
        const schoolId = (rawSchoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(rawSchoolId)) ? rawSchoolId : null;

        const payload = students.map(student => {
          const sId = student.id;
          const marks = evaluations[sId] || {};
          return {
            school_id: schoolId,
            student_id: sId,
            class_name: className,
            exam_type: examType,
            marks: marks
          };
        });

        supabaseClient
          .from('cce_evaluations')
          .upsert(payload, { onConflict: 'student_id,exam_type' })
          .then(({ error }) => {
            const indicator = document.getElementById('auto-save-indicator');
            if (indicator) {
              indicator.className = 'text-xs font-bold px-2.5 py-1 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 flex items-center gap-1.5 border border-emerald-200/60 dark:border-emerald-900/40';
              if (error) {
                console.warn("Auto-save to Supabase failed, saved locally:", error);
                indicator.innerHTML = '<i class="fa-solid fa-circle-check text-teal-500 text-[11px]"></i> <span>ಆಫ್‌ಲೈನ್ ಉಳಿಸಲಾಗಿದೆ</span>';
              } else {
                indicator.innerHTML = '<i class="fa-solid fa-circle-check text-emerald-500 text-[11px]"></i> <span>ಸ್ವಯಂ ಉಳಿಸಲಾಗಿದೆ / Auto-saved</span>';
              }
              setTimeout(() => {
                if (indicator) indicator.classList.add('hidden');
              }, 2500);
            }
          });
      }).catch(() => {
        const indicator = document.getElementById('auto-save-indicator');
        if (indicator) {
          indicator.className = 'text-xs font-bold px-2.5 py-1 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 flex items-center gap-1.5 border border-emerald-200/60 dark:border-emerald-900/40';
          indicator.innerHTML = '<i class="fa-solid fa-circle-check text-teal-500 text-[11px]"></i> <span>ಸ್ಥಳೀಯವಾಗಿ ಉಳಿಸಲಾಗಿದೆ</span>';
          setTimeout(() => {
            if (indicator) indicator.classList.add('hidden');
          }, 2500);
        }
      });
    }

    function closeReportCardModal() {
      const modal = document.getElementById('report-card-modal');
      if (modal) modal.classList.add('hidden');
    }

    function downloadExcelTemplate() {
      downloadCSVTemplate();
    }

    function handleImportFile(input) {
      if (input && input.files && input.files[0]) {
        handleCSVUpload({ target: input });
      }
    }

    function exportIndividualReportCardToExcel() {
      exportToExcel();
    }

    function exportIndividualReportCardToPdf() {
      exportToPdf();
    }

    function printIndividualReportCard() {
      printPage();
    }

    function stepCceFAMark(studentId, subKey, delta) {
      const className = classFilter.value;
      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      const currentVal = evaluations[studentId] && evaluations[studentId][subKey + "_mark"] !== undefined && evaluations[studentId][subKey + "_mark"] !== '' ? parseFloat(evaluations[studentId][subKey + "_mark"]) : 0;
      let newVal = Math.min(cfg.faMax, Math.max(0, currentVal + delta));
      quickSetCceFAMark(studentId, subKey, newVal);
    }

    function quickSetCceFAMark(studentId, subKey, markVal) {
      const className = classFilter.value;
      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      let val = Math.min(cfg.faMax, Math.max(0, markVal));
      onFAMarkChange(studentId, subKey, val.toString());
      const cardInput = document.getElementById(`card-input-${studentId}-${subKey}`);
      if (cardInput) cardInput.value = val;
    }

    function updateTotals() {
      let grandTotalA = 0;
      let grandTotalOthers = 0;
      let apCount = 0, aCount = 0, bpCount = 0, bCount = 0, cCount = 0;

      students.forEach(student => {
        const sId = student.id;
        const evalData = evaluations[sId] || {};
        let rowA = 0;
        let rowOthers = 0;

        currentSubjects.forEach(sub => {
          const g = evalData[sub.id + "_grade"] || '-';
          if (g === '-') return;
          if (g === 'A+') { apCount++; rowA++; }
          else if (g === 'A') { aCount++; rowA++; }
          else if (g === 'B+') { bpCount++; rowOthers++; }
          else if (g === 'B') { bCount++; rowOthers++; }
          else if (['C+', 'C', 'D'].includes(g)) { cCount++; rowOthers++; }
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
      if (statTotalStudents) statTotalStudents.innerText = students.length;

      const statAP = document.getElementById('stat-grade-ap');
      const statA = document.getElementById('stat-grade-a');
      const statBP = document.getElementById('stat-grade-bp');
      const statB = document.getElementById('stat-grade-b');
      const statC = document.getElementById('stat-grade-others') || document.getElementById('stat-grade-c');
      if (statAP) statAP.innerText = apCount;
      if (statA) statA.innerText = aCount;
      if (statBP) statBP.innerText = bpCount;
      if (statB) statB.innerText = bCount;
      if (statC) statC.innerText = cCount;
    }

    function setMode(editing) {
      isEditing = true;
    }

    function resetToEmptyState() {
      const loadOverlay = document.getElementById('loading-overlay');
      if (loadOverlay) loadOverlay.classList.add('hidden');
      const tableContainer = document.getElementById('table-container');
      if (tableContainer) tableContainer.classList.remove('hidden');
      const emptyState = document.getElementById('empty-state');
      if (emptyState) emptyState.classList.remove('hidden');
      const compTable = document.getElementById('competency-table');
      if (compTable) compTable.classList.add('hidden');
      const cardsEl = document.getElementById('student-cards-container');
      if (cardsEl) cardsEl.classList.add('hidden');
      const sfBar = document.getElementById('search-filter-bar');
      if (sfBar) sfBar.classList.add('hidden');
      const statsBar = document.getElementById('stats-bar');
      if (statsBar) statsBar.classList.add('hidden');
    }

    function enableEditing() { isEditing = true; renderActiveView(); }
    function cancelEditing() { renderActiveView(); }

    function saveData() {
      performSilentSave();
    }

    function onDataSaved() {
      document.getElementById('loading-overlay').classList.add('hidden');
      showToast("ಮಾಹಿತಿ ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!", "success");
      originalEvaluations = JSON.parse(JSON.stringify(evaluations));
      setMode(false);
      renderActiveView();
    }

    async function syncAndOpenConsolidated() {
      const className = classFilter.value || "1";
      const examType = examTypeFilter.value || "FA1";
      showToast("ಕ್ರೋಢೀಕೃತ ವರದಿಯೊಂದಿಗೆ ಸಿಂಕ್ ಮಾಡಲಾಗುತ್ತಿದೆ...", "info");
      performSilentSave();
      setTimeout(() => {
        window.location.href = `CceConsolidatedReport.html?class=${className}`;
      }, 600);
    }

    function buildPrintArea() {
      const className = classFilter.value;
      const examType = examTypeFilter.value;
      const selectedSub = subjectFilter.value;
      const isAllSubjects = (selectedSub === "ALL");
      
      const schoolNameEn = localStorage.getItem('school_name_en') || "GOVERNMENT HIGHER PRIMARY SCHOOL, MARCHED";
      const schoolNameKn = localStorage.getItem('school_name_kn') || "ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ ಮರ್ಛೇಡ್";
      
      const defaultGovLogo = "https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg";
      const defaultSchoolLogo = "https://gsayvnnnfrrkwdfwocbu.supabase.co/storage/v1/object/public/school-logo/ghps-marched-logo.png";
      let govLogo = localStorage.getItem('school_gov_logo') || defaultGovLogo;
      if (govLogo.includes('e/e7/Emblem_of_Karnataka.svg')) govLogo = defaultGovLogo;
      const schoolLogo = localStorage.getItem('school_logo_url') || defaultSchoolLogo;

      const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
      const cfg = isPrimary ? mutableConfigs.primary : mutableConfigs.middleHigh;
      const maxMarks = examType.startsWith("SA") ? cfg.saMax : cfg.faMax;

      const printArea = document.getElementById('printArea');
      if (!printArea) return;
      printArea.innerHTML = '';

      // Header Block with Official Logos
      const headerDiv = document.createElement('div');
      headerDiv.className = 'text-center mb-3';
      headerDiv.innerHTML = `
        <div style="display: grid; grid-template-columns: 65px 1fr 65px; align-items: center; gap: 8px; margin-bottom: 6px;">
          <!-- Left: Karnataka Govt Emblem -->
          <div style="text-align: left;">
            <img src="${govLogo}" style="height: 55px; width: 55px; object-fit: contain;" alt="Govt Logo" crossorigin="anonymous">
          </div>
          <!-- Center: Title & School Name -->
          <div style="text-align: center;">
            <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #000; letter-spacing: 0.5px;">ಕರ್ನಾಟಕ ಸರ್ಕಾರ | GOVERNMENT OF KARNATAKA</div>
            <div style="font-size: 12px; font-weight: 800; text-transform: uppercase; color: #000; margin-top: 1px;">ಶಾಲಾ ಶಿಕ್ಷಣ ಮತ್ತು ಸಾಕ್ಷರತಾ ಇಲಾಖೆ | DEPARTMENT OF SCHOOL EDUCATION AND LITERACY</div>
            <div style="font-size: 17px; font-weight: 900; text-transform: uppercase; color: #000; margin-top: 2px; line-height: 1.2;">${schoolNameEn}</div>
            <div style="font-size: 14px; font-weight: 800; color: #000; margin-top: 1px; line-height: 1.2;">${schoolNameKn}</div>
          </div>
          <!-- Right: School Logo / Badge -->
          <div style="text-align: right;">
            <img src="${schoolLogo}" style="height: 55px; width: 55px; object-fit: contain;" alt="School Logo" crossorigin="anonymous">
          </div>
        </div>
        <div style="font-size: 12px; font-weight: 800; text-transform: uppercase; color: #000; margin-top: 4px; border-top: 1.5px solid #000; border-bottom: 1.5px solid #000; padding: 3px 0;">
          ಸಂಕಲನಾತ್ಮಕ ಮತ್ತು ರೂಪಣಾತ್ಮಕ ಮೌಲ್ಯಮಾಪನ ಪ್ರಗತಿ ಪಟ್ಟಿ 2026-27 (CCE ASSESSMENT REGISTER)
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 800; color: #000; margin-top: 6px; padding-bottom: 4px; border-bottom: 1px solid #000;">
          <span>ತರಗತಿ / Class: <strong>${className}</strong></span>
          <span>ಪರೀಕ್ಷೆ / Exam: <strong>${examType}</strong></span>
          ${!isAllSubjects ? `<span>ವಿಷಯ / Subject: <strong>${subjectFilter.options[subjectFilter.selectedIndex]?.text || ''}</strong></span>` : '<span>ವಿಷಯ: <strong>ಎಲ್ಲಾ ವಿಷಯಗಳು (All Subjects)</strong></span>'}
          <span>ಗರಿಷ್ಠ ಅಂಕ / Max: <strong>${maxMarks}</strong></span>
          <span>ದಿನಾಂಕ / Date: <strong>${new Date().toLocaleDateString('kn-IN')}</strong></span>
        </div>
      `;
      printArea.appendChild(headerDiv);

      // Ensure table rows are fully populated before cloning
      buildTableHeader();
      renderGrid();

      // Clone competency table
      const originalTable = document.getElementById('competency-table');
      if (originalTable) {
        const tableClone = originalTable.cloneNode(true);
        tableClone.removeAttribute('id');
        tableClone.classList.remove('hidden');

        // Replace inputs with plain text spans
        const inputs = tableClone.querySelectorAll('input');
        inputs.forEach(input => {
          const parent = input.parentNode;
          const span = document.createElement('span');
          span.innerText = input.value !== '' ? input.value : '-';
          span.style.fontWeight = 'bold';
          parent.replaceChild(span, input);
        });

        // Strip styling classes for crisp native print borders
        tableClone.removeAttribute('class');
        tableClone.querySelectorAll('*').forEach(el => {
          const isLeft = el.classList.contains('text-left');
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

        printArea.appendChild(tableClone);
      }

      // Grade Statistics Abstract Tally Box
      let totalStudents = students.length;
      let apCount = 0, aCount = 0, bpCount = 0, bCount = 0, cCount = 0;
      students.forEach(student => {
        const sId = student.id;
        const evalData = evaluations[sId] || {};
        currentSubjects.forEach(sub => {
          if (!isAllSubjects && sub.id !== selectedSub) return;
          const g = evalData[sub.id + "_grade"] || '-';
          if (g === 'A+') apCount++;
          else if (g === 'A') aCount++;
          else if (g === 'B+') bpCount++;
          else if (g === 'B') bCount++;
          else if (['C+', 'C', 'D'].includes(g)) cCount++;
        });
      });

      const abstractBox = document.createElement('div');
      abstractBox.style.marginTop = '12px';
      abstractBox.style.border = '1.5px solid #000';
      abstractBox.style.padding = '6px 10px';
      abstractBox.style.fontSize = '10px';
      abstractBox.style.fontWeight = 'bold';
      abstractBox.style.color = '#000';
      abstractBox.style.display = 'flex';
      abstractBox.style.justifyContent = 'space-between';
      abstractBox.style.alignItems = 'center';
      abstractBox.style.backgroundColor = '#fff';
      abstractBox.innerHTML = `
        <span>ಒಟ್ಟು ವಿದ್ಯಾರ್ಥಿಗಳು (Total Pupils): <strong>${totalStudents}</strong></span>
        <span>A+ ಶ್ರೇಣಿ: <strong>${apCount}</strong></span>
        <span>A ಶ್ರೇಣಿ: <strong>${aCount}</strong></span>
        <span>B+ ಶ್ರೇಣಿ: <strong>${bpCount}</strong></span>
        <span>B ಶ್ರೇಣಿ: <strong>${bCount}</strong></span>
        <span>C+ / ಇತರ ಶ್ರೇಣಿ: <strong>${cCount}</strong></span>
      `;
      printArea.appendChild(abstractBox);

      // Official 3-Signature Block
      const sigRow = document.createElement('div');
      sigRow.className = 'print-signatures-row';
      sigRow.style.marginTop = '35px';
      sigRow.style.display = 'flex';
      sigRow.style.justifyContent = 'space-between';
      sigRow.style.alignItems = 'flex-end';
      sigRow.style.fontSize = '11px';
      sigRow.style.fontWeight = 'bold';
      sigRow.style.color = '#000';
      sigRow.innerHTML = `
        <div style="text-align: center;">
          <div style="border-top: 1px solid #000; width: 160px; margin-bottom: 4px;"></div>
          <span>ತರಗತಿ ಶಿಕ್ಷಕರ ಸಹಿ<br>(Class Teacher Signature)</span>
        </div>
        ${!isAllSubjects ? `
          <div style="text-align: center;">
            <div style="border-top: 1px solid #000; width: 160px; margin-bottom: 4px;"></div>
            <span>ವಿಷಯ ಶಿಕ್ಷಕರ ಸಹಿ<br>(Subject Teacher Signature)</span>
          </div>
        ` : ''}
        <div style="text-align: center;">
          <div style="border-top: 1px solid #000; width: 180px; margin-bottom: 4px;"></div>
          <span>ಮುಖ್ಯೋಪಾಧ್ಯಾಯರ ಸಹಿ ಮತ್ತು ಮೊಹರು<br>(Head Master Signature & Seal)</span>
        </div>
      `;
      printArea.appendChild(sigRow);

      // Restore active view mode so Card View is not affected
      const currentMode = document.getElementById('btn-view-cards')?.classList.contains('bg-indigo-600') ? 'cards' : 'table';
      if (currentMode === 'cards') {
        const compTable = document.getElementById('competency-table');
        if (compTable) compTable.classList.add('hidden');
        const cardsEl = document.getElementById('student-cards-container');
        if (cardsEl) cardsEl.classList.remove('hidden');
      }
    }

    function printPage() {
      if (students.length === 0) {
        showToast("ಮುದ್ರಿಸಲು ಯಾವುದೇ ವಿದ್ಯಾರ್ಥಿಗಳ ಡೇಟಾ ಇಲ್ಲ", "warning");
        return;
      }
      window.customPrintGenerated = true;
      buildPrintArea();
      setTimeout(() => {
        window.print();
        window.addEventListener('afterprint', () => {
          window.customPrintGenerated = false;
        }, { once: true });
      }, 100);
    }

    function exportToPdf() {
      printPage();
    }

    function exportToExcel() {
      if (students.length === 0) { alert("ಯಾವುದೇ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ"); return; }
      const className = classFilter.value;
      const examType = examTypeFilter.value;
      const isSA = examType.startsWith("SA");

      const row1 = ["Sl. No", "STS Number", "Student Name", "Father Name"];
      const row2 = ["", "", "", ""];

      currentSubjects.forEach(sub => {
        if (subjectFilter.value !== "ALL" && sub.id !== subjectFilter.value) return;
        if (isSA) { row1.push(sub.name, "", "", ""); row2.push("Written", "Oral", "Total", "Grade"); } 
        else { row1.push(sub.name, ""); row2.push("Mark", "Grade"); }
      });
      row1.push("Total A+,A", "Others"); row2.push("", "");

      const aoa = [row1, row2];
      students.forEach((student, index) => {
        const sId = student.id; const evalData = evaluations[sId] || {};
        const stName = student.name_english || student.student_name_kn || student.student_name || student.name || '';
        const stFather = student.father_name_az || student.father_name_kn || student.father || '';
        const row = [index + 1, student.adminNo || student.app_no || student.id, stName, stFather];
        let rowA = 0; let rowOthers = 0;

        currentSubjects.forEach(sub => {
          if (subjectFilter.value !== "ALL" && sub.id !== subjectFilter.value) return;
          const m = evalData[sub.id + "_mark"] !== undefined ? evalData[sub.id + "_mark"] : '';
          const g = evalData[sub.id + "_grade"] || '-';
          if (isSA) {
            const parts = m.toString().split('+');
            const w = parts[0] || ''; const o = parts[1] || '';
            const tot = w !== '' || o !== '' ? (parseFloat(w)||0)+(parseFloat(o)||0) : '';
            row.push(w, o, tot, g);
          } else { row.push(m, g); }
          if (g !== '-') { if (['A+', 'A'].includes(g)) { rowA++; } else { rowOthers++; } }
        });
        row.push(rowA, rowOthers); aoa.push(row);
      });

      const sheet = XLSX.utils.aoa_to_sheet(aoa);
      const wb = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb, sheet, "CCE");
      XLSX.writeFile(wb, `CCE_${className}_${examType}.xlsx`);
    }

    function triggerImport() { document.getElementById('import-file-input').click(); }
    function getBackendSubjectKey(name) { return name.toLowerCase().includes("ಕನ್ನಡ") ? "kannada" : "english"; }
    function showToast(msg, type = "success") {
      const toast = document.getElementById('toast-notif');
      const msgEl = document.getElementById('toast-message');
      if (msgEl) msgEl.innerText = msg;
      if (toast) {
        toast.className = `fixed bottom-5 right-5 px-5 py-3 rounded-2xl shadow-xl transition transform z-[100] ${type === 'success' ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'}`;
        toast.classList.remove('translate-y-20', 'opacity-0');
        setTimeout(() => { toast.classList.add('translate-y-20', 'opacity-0'); }, 2500);
      } else {
        alert(msg);
      }
    }

    function changeTheme(themeName) {
      document.body.setAttribute('data-theme', themeName);
      localStorage.setItem('portal_theme', themeName);
    }

    function downloadCSVTemplate() {
      const className = classFilter.value || "1";
      const examType = examTypeFilter.value || "FA1";
      const isSA = examType.startsWith("SA");
      
      const headers = ["STS Number", "Student Name", "Father Name"];
      const sampleRow = ["STS2026001", "Chaitra G", "Girishappa"];
      
      const subs = currentSubjects && currentSubjects.length > 0 ? currentSubjects : [
        { id: "kannada", name: "KANNADA" },
        { id: "english", name: "ENGLISH" },
        { id: "maths", name: "MATHS" },
        { id: "science", name: "SCIENCE" },
        { id: "social_science", name: "SOCIAL SCIENCE" }
      ];

      subs.forEach(sub => {
        if (subjectFilter.value !== "ALL" && sub.id !== subjectFilter.value) return;
        if (isSA) {
          headers.push(`${sub.name} Written`, `${sub.name} Oral`);
          sampleRow.push("30", "10");
        } else {
          headers.push(`${sub.name} Mark`);
          sampleRow.push("15");
        }
      });
      
      let csvContent = "\uFEFF"; 
      csvContent += headers.map(h => `"${h.replace(/"/g, '""')}"`).join(",") + "\r\n";
      csvContent += sampleRow.map(r => `"${r.replace(/"/g, '""')}"`).join(",") + "\r\n";

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.setAttribute("href", url);
      link.setAttribute("download", `CCE_${examType}_Template.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    function exportToCSV() {
      if (students.length === 0) { alert("ಯಾವುದೇ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ"); return; }
      const className = classFilter.value;
      const examType = examTypeFilter.value;
      const isSA = examType.startsWith("SA");

      const row1 = ["Sl. No", "STS Number", "Student Name", "Father Name"];
      const row2 = ["", "", "", ""];

      currentSubjects.forEach(sub => {
        if (subjectFilter.value !== "ALL" && sub.id !== subjectFilter.value) return;
        if (isSA) { row1.push(sub.name, "", "", ""); row2.push("Written", "Oral", "Total", "Grade"); } 
        else { row1.push(sub.name, ""); row2.push("Mark", "Grade"); }
      });
      row1.push("Total A+,A", "Others"); row2.push("", "");

      const aoa = [row1, row2];
      students.forEach((student, index) => {
        const sId = student.id; const evalData = evaluations[sId] || {};
        const stName = student.name_english || student.student_name_kn || student.student_name || student.name || '';
        const stFather = student.father_name_az || student.father_name_kn || student.father || '';
        const row = [index + 1, student.adminNo || student.app_no || student.id, stName, stFather];
        let rowA = 0; let rowOthers = 0;

        currentSubjects.forEach(sub => {
          if (subjectFilter.value !== "ALL" && sub.id !== subjectFilter.value) return;
          const m = evalData[sub.id + "_mark"] !== undefined ? evalData[sub.id + "_mark"] : '';
          const g = evalData[sub.id + "_grade"] || '-';
          if (isSA) {
            const parts = m.toString().split('+');
            const w = parts[0] || ''; const o = parts[1] || '';
            const tot = w !== '' || o !== '' ? (parseFloat(w)||0)+(parseFloat(o)||0) : '';
            row.push(w, o, tot, g);
          } else { row.push(m, g); }
          if (g !== '-') { if (['A+', 'A'].includes(g)) { rowA++; } else { rowOthers++; } }
        });
        row.push(rowA, rowOthers); aoa.push(row);
      });

      const sheet = XLSX.utils.aoa_to_sheet(aoa);
      const wb = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb, sheet, "CCE");
      XLSX.writeFile(wb, `CCE_${className}_${examType}.csv`, { bookType: 'csv' });
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
          const examType = examTypeFilter.value;
          const isSA = examType.startsWith("SA");
          const isPrimary = mutableConfigs.primary.classes.includes(className === "ALL" ? "1" : className);
          const targetScale = isSA ? 
            (isPrimary ? mutableConfigs.primary.saMax : mutableConfigs.middleHigh.saMax) : 
            (isPrimary ? mutableConfigs.primary.faMax : mutableConfigs.middleHigh.faMax);
            
          const { data: { session } } = await supabaseClient.auth.getSession();
          const rawSchoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id")) || null;
        const schoolId = (rawSchoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(rawSchoolId)) ? rawSchoolId : null;
          
          let changedCount = 0;
          const upsertPayloads = [];
          
          json.forEach(row => {
            const stsVal = (row[stsKey] || '').toString().trim();
            if (!stsVal) return;
            
            const student = students.find(s => (s.adminNo || s.id) === stsVal);
            if (!student) return;
            
            if (!evaluations[student.id]) {
              evaluations[student.id] = {};
            }
            
            let studentChanged = false;
            
            currentSubjects.forEach(sub => {
              if (subjectFilter.value !== "ALL" && sub.id !== subjectFilter.value) return;
              
              if (isSA) {
                const wKey = headers.find(h => h.includes(sub.name) && (h.toLowerCase().includes('written') || h.includes('ಲಿಖಿತ')));
                const oKey = headers.find(h => h.includes(sub.name) && (h.toLowerCase().includes('oral') || h.includes('ಮೌಖಿಕ')));
                
                const wVal = wKey && row[wKey] !== undefined ? row[wKey].toString().trim() : '';
                const oVal = oKey && row[oKey] !== undefined ? row[oKey].toString().trim() : '';
                
                if (wVal !== '' || oVal !== '') {
                  const mVal = `${wVal}+${oVal}`;
                  const currentM = evaluations[student.id][sub.id + "_mark"] || '';
                  if (currentM !== mVal) {
                    evaluations[student.id][sub.id + "_mark"] = mVal;
                    const tot = (parseFloat(wVal)||0) + (parseFloat(oVal)||0);
                    evaluations[student.id][sub.id + "_grade"] = determineGradeByScale(tot, targetScale);
                    studentChanged = true;
                  }
                }
              } else {
                const mKey = headers.find(h => h.includes(sub.name) && (h.toLowerCase().includes('mark') || h.includes('ಅಂಕ') || !h.toLowerCase().includes('grade')));
                const mVal = mKey && row[mKey] !== undefined ? row[mKey].toString().trim() : '';
                
                if (mVal !== '') {
                  const currentM = evaluations[student.id][sub.id + "_mark"] || '';
                  if (currentM !== mVal) {
                    evaluations[student.id][sub.id + "_mark"] = mVal;
                    evaluations[student.id][sub.id + "_grade"] = determineGradeByScale(mVal, targetScale);
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
                exam_type: examType,
                marks: evaluations[student.id],
                updated_at: new Date().toISOString()
              });
            }
          });
          
          if (upsertPayloads.length > 0) {
            document.getElementById('loading-overlay').classList.remove('hidden');
            
            const { error } = await supabaseClient
              .from('cce_evaluations')
              .upsert(upsertPayloads, { onConflict: 'student_id,exam_type' });
              
            document.getElementById('loading-overlay').classList.add('hidden');
            
            if (error) {
              console.warn("Supabase upsert failed, saving to localStorage as fallback:", error);
              const mockKey = `cce_mock_cce_${className}_${examType}`;
              localStorage.setItem(mockKey, JSON.stringify(evaluations));
            } else {
              originalEvaluations = JSON.parse(JSON.stringify(evaluations));
            }
            
            renderActiveView();
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

    async function initUserAndTheme() {
      const savedTheme = localStorage.getItem('portal_theme') || 'light';
      document.body.setAttribute('data-theme', savedTheme);
      const selector = document.getElementById('themeSelector');
      if (selector) selector.value = savedTheme;

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
  