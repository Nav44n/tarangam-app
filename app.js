(function(){
  "use strict";

  var STORE_KEY = "tarangam_state_v1";
  var state = loadState();

  function loadState(){
    try{
      var raw = localStorage.getItem(STORE_KEY);
      if(raw) return JSON.parse(raw);
    }catch(e){}
    return { theme:"dark", size:"md", autoplay:false, reduceMotion:false, visited:{}, quizScores:{} };
  }
  function saveState(){
    try{ localStorage.setItem(STORE_KEY, JSON.stringify(state)); }catch(e){}
  }

  var SUBJECT = window.SUBJECTS.ml;
  var allTopics = [];
  SUBJECT.modules.forEach(function(mod){
    mod.topics.forEach(function(t){ allTopics.push({ mod:mod, topic:t }); });
  });

  var els = {
    sidebar: document.getElementById("sidebar"),
    moduleTree: document.getElementById("moduleTree"),
    subjectSwitch: document.getElementById("subjectSwitch"),
    content: document.getElementById("content"),
    pagefoot: document.getElementById("pagefoot"),
    crumb: document.getElementById("crumb"),
    progressFill: document.getElementById("progressFill"),
    progressLabel: document.getElementById("progressLabel"),
    settingsVeil: document.getElementById("settingsVeil"),
    sidebarToggle: document.getElementById("sidebarToggle"),
    settingsBtn: document.getElementById("settingsBtn"),
    closeSettings: document.getElementById("closeSettings"),
  };

  /* ---------------- Theme / settings ---------------- */
  function applyTheme(){
    document.body.setAttribute("data-theme", state.theme);
    document.body.setAttribute("data-size", state.size);
    document.body.setAttribute("data-reduce-motion", state.reduceMotion ? "1" : "0");
    document.querySelectorAll(".theme-opt").forEach(function(b){
      b.classList.toggle("active", b.dataset.theme === state.theme);
    });
    document.querySelectorAll(".size-btn").forEach(function(b){
      b.classList.toggle("active", b.dataset.size === state.size);
    });
    var autoplayEl = document.getElementById("autoplayToggle");
    var reduceEl = document.getElementById("reduceMotionToggle");
    if(autoplayEl) autoplayEl.checked = !!state.autoplay;
    if(reduceEl) reduceEl.checked = !!state.reduceMotion;
  }

  document.getElementById("themeRow").addEventListener("click", function(e){
    var btn = e.target.closest(".theme-opt");
    if(!btn) return;
    state.theme = btn.dataset.theme; saveState(); applyTheme();
  });
  document.querySelectorAll(".size-row .size-btn").forEach(function(b){
    b.addEventListener("click", function(){ state.size = b.dataset.size; saveState(); applyTheme(); });
  });
  document.getElementById("autoplayToggle").addEventListener("change", function(e){
    state.autoplay = e.target.checked; saveState();
  });
  document.getElementById("reduceMotionToggle").addEventListener("change", function(e){
    state.reduceMotion = e.target.checked; saveState(); applyTheme();
  });
  document.getElementById("resetProgress").addEventListener("click", function(){
    state.visited = {}; state.quizScores = {}; saveState(); renderSidebar(); updateProgress();
  });
  els.settingsBtn.addEventListener("click", function(){ els.settingsVeil.classList.add("open"); });
  els.closeSettings.addEventListener("click", function(){ els.settingsVeil.classList.remove("open"); });
  els.settingsVeil.addEventListener("click", function(e){ if(e.target === els.settingsVeil) els.settingsVeil.classList.remove("open"); });

  els.sidebarToggle.addEventListener("click", function(){
    if(window.innerWidth <= 860){ els.sidebar.classList.toggle("mobile-open"); }
    else{ els.sidebar.classList.toggle("collapsed"); }
  });

  /* ---------------- Sidebar ---------------- */
  function renderSidebar(){
    els.subjectSwitch.innerHTML =
      '<div class="subject-card"><span>' + SUBJECT.name + '</span><span class="tag">' + SUBJECT.code + '</span></div>';

    els.moduleTree.innerHTML = "";
    SUBJECT.modules.forEach(function(mod, idx){
      var block = document.createElement("div");
      block.className = "module-block" + (idx === 0 ? " open" : "");
      block.dataset.mod = mod.num;

      var head = document.createElement("button");
      head.className = "module-head";
      head.innerHTML =
        '<span class="module-num">M' + mod.num + '</span>' +
        '<span>' + mod.title + '</span>' +
        '<span class="module-hours">' + mod.hours + 'h</span>' +
        '<span class="chev">&#9656;</span>';
      head.addEventListener("click", function(){ block.classList.toggle("open"); });
      block.appendChild(head);

      var list = document.createElement("div");
      list.className = "topic-list";
      mod.topics.forEach(function(t){
        var link = document.createElement("button");
        link.className = "topic-link" + (state.visited[t.id] ? " visited" : "");
        link.dataset.id = t.id;
        link.innerHTML = '<span class="topic-dot"></span><span>' + t.title + '</span>';
        link.addEventListener("click", function(){ goTo(t.id); if(window.innerWidth<=860) els.sidebar.classList.remove("mobile-open"); });
        list.appendChild(link);
      });
      block.appendChild(list);
      els.moduleTree.appendChild(block);
    });
  }

  function markActive(id){
    document.querySelectorAll(".topic-link").forEach(function(l){
      l.classList.toggle("active", l.dataset.id === id);
    });
  }

  function updateProgress(){
    var visitedCount = Object.keys(state.visited).length;
    var total = allTopics.length;
    els.progressFill.style.width = (total ? (visitedCount/total*100) : 0) + "%";
    els.progressLabel.textContent = visitedCount + " of " + total + " topics visited";
  }

  /* ---------------- Rendering a topic ---------------- */
  function findTopicIndex(id){
    for(var i=0;i<allTopics.length;i++) if(allTopics[i].topic.id === id) return i;
    return -1;
  }

  function renderAccordion(items){
    if(!items || !items.length) return "";
    var html = '<div class="accordion">';
    items.forEach(function(it, i){
      html += '<div class="acc-item">' +
        '<button class="acc-trigger"><span>' + it.title + '</span><span class="plus">+</span></button>' +
        '<div class="acc-panel"><div class="acc-panel-inner"><p>' + it.body + '</p></div></div>' +
      '</div>';
    });
    html += '</div>';
    return html;
  }

  function renderWorked(w){
    if(!w) return "";
    var lis = w.steps.map(function(s){ return '<li>' + s + '</li>'; }).join("");
    return '<div class="worked"><span class="worked-title">WORKED EXAMPLE — ' + w.title.toUpperCase() + '</span><ol>' + lis + '</ol></div>';
  }

  function renderVideo(v){
    if(!v) return "";
    // src is optional: if assets/videos/<name>.mp4 exists (see README) it plays;
    // otherwise clicking just explains how to render it, without breaking layout.
    var name = v.script.split("/").pop().replace(".py", ".mp4");
    var src = "assets/videos/" + name;
    return '<div class="video-slot">' +
      '<div class="video-frame" data-src="' + src + '">' +
        '<div class="play-glyph">&#9654;</div>' +
        '<div class="video-caption">' + v.caption + '</div>' +
      '</div>' +
      '<div class="video-meta"><span class="manim-tag">MANIM</span><span>' + v.script + '</span></div>' +
    '</div>';
  }

  function renderQuiz(topicId, quiz){
    if(!quiz || !quiz.length) return "";
    var html = '<div class="quiz" data-topic="' + topicId + '">' +
      '<div class="quiz-head"><span class="quiz-label">SELF-CHECK</span><span class="quiz-score" data-role="score"></span></div>';
    quiz.forEach(function(q, qi){
      html += '<div class="quiz-item" data-qi="' + qi + '" style="' + (qi===0 ? "" : "display:none;") + '">' +
        '<p class="quiz-q">' + (qi+1) + '. ' + q.q + '</p>' +
        '<div class="quiz-opts">';
      q.options.forEach(function(opt, oi){
        html += '<button class="quiz-opt" data-oi="' + oi + '">' + opt + '</button>';
      });
      html += '</div><div class="quiz-explain"></div>' +
        '<div class="quiz-nav">' + (qi < quiz.length-1 ? '<button class="ghost-btn" data-role="next">Next question</button>' : '<button class="ghost-btn" data-role="finish">Done</button>') + '</div>' +
      '</div>';
    });
    html += '</div>';
    return html;
  }

  function renderTopic(id){
    var idx = findTopicIndex(id);
    if(idx === -1){ idx = 0; id = allTopics[0].topic.id; }
    var entry = allTopics[idx];
    var mod = entry.mod, t = entry.topic;

    state.visited[id] = true; saveState();

    var html = '';
    html += '<div class="topic-eyebrow">MODULE ' + mod.num + ' &middot; ' + mod.title + '</div>';
    html += '<h1 class="topic-title">' + t.title + '</h1>';
    if(t.dek) html += '<p class="topic-dek">' + t.dek + '</p>';
    html += '<div class="theory">' + t.theory + '</div>';
    if(t.formula) html += '<div class="formula-box">$$' + t.formula + '$$</div>';
    if(t.worked) html += renderWorked(t.worked);
    if(t.callout) html += '<div class="callout"><span class="callout-label">' + t.callout.label + '</span>' + t.callout.text + '</div>';
    if(t.video) html += renderVideo(t.video);
    if(t.extra) html += renderAccordion(t.extra);
    html += renderQuiz(id, t.quiz);

    els.content.innerHTML = html;
    els.crumb.textContent = SUBJECT.name + " / M" + mod.num + " / " + t.title;
    markActive(id);
    updateProgress();
    renderSidebar(); // refresh visited dot state
    markActive(id);
    wireContentEvents(id, t);
    renderFooterNav(idx);

    if(window.MathJax && window.MathJax.typesetPromise){
      window.MathJax.typesetPromise([els.content]).catch(function(){});
    }
    window.scrollTo({top:0, behavior: state.reduceMotion ? "auto" : "smooth"});
    if(location.hash !== "#" + id) history.replaceState(null, "", "#" + id);
  }

  function renderFooterNav(idx){
    var prev = idx > 0 ? allTopics[idx-1] : null;
    var next = idx < allTopics.length-1 ? allTopics[idx+1] : null;
    var html = "";
    if(prev){
      html += '<div class="nav-card prev" data-id="' + prev.topic.id + '"><span class="dir">&larr; PREVIOUS</span><div class="ttl">' + prev.topic.title + '</div></div>';
    } else { html += '<div></div>'; }
    if(next){
      html += '<div class="nav-card next" data-id="' + next.topic.id + '"><span class="dir">NEXT &rarr;</span><div class="ttl">' + next.topic.title + '</div></div>';
    } else { html += '<div></div>'; }
    els.pagefoot.innerHTML = html;
    els.pagefoot.querySelectorAll(".nav-card[data-id]").forEach(function(c){
      c.addEventListener("click", function(){ goTo(c.dataset.id); });
    });
  }

  function wireContentEvents(topicId, t){
    // accordion
    els.content.querySelectorAll(".acc-item").forEach(function(item){
      item.querySelector(".acc-trigger").addEventListener("click", function(){
        item.classList.toggle("open");
      });
    });

    // video click-to-play: if the rendered mp4 exists at data-src, play it;
    // otherwise show a one-line note instead of a broken player.
    els.content.querySelectorAll(".video-frame").forEach(function(frame){
      frame.addEventListener("click", function(){
        if(frame.dataset.checked) return;
        var src = frame.dataset.src;
        fetch(src, { method: "HEAD" }).then(function(res){
          frame.dataset.checked = "1";
          if(res.ok){
            var vid = document.createElement("video");
            vid.src = src; vid.controls = true; vid.autoplay = !!state.autoplay; vid.muted = !state.autoplay;
            vid.playsInline = true;
            frame.innerHTML = ""; frame.appendChild(vid); frame.classList.add("playing");
          } else {
            frame.querySelector(".video-caption").innerHTML =
              'Not rendered yet — run <code>manim -pqh ' + frame.closest(".video-slot").querySelector(".video-meta span:last-child").textContent + '</code> and drop the .mp4 into <code>assets/videos/</code>.';
          }
        }).catch(function(){
          frame.dataset.checked = "1";
          frame.querySelector(".video-caption").innerHTML = "Video not available in this environment.";
        });
      });
    });

    // quiz
    var quizEl = els.content.querySelector(".quiz");
    if(quizEl){
      var qData = t.quiz;
      var correctCount = 0;
      var scoreEl = quizEl.querySelector('[data-role="score"]');
      function updateScore(){ scoreEl.textContent = correctCount + " / " + qData.length + " correct"; }
      updateScore();

      quizEl.querySelectorAll(".quiz-item").forEach(function(itemEl){
        var qi = parseInt(itemEl.dataset.qi, 10);
        var q = qData[qi];
        var opts = itemEl.querySelectorAll(".quiz-opt");
        var explainEl = itemEl.querySelector(".quiz-explain");
        opts.forEach(function(optBtn){
          optBtn.addEventListener("click", function(){
            if(optBtn.dataset.answered) return;
            var oi = parseInt(optBtn.dataset.oi, 10);
            opts.forEach(function(b){ b.dataset.answered = "1"; b.setAttribute("disabled","disabled"); });
            opts[q.answer].classList.add("correct");
            if(oi !== q.answer) optBtn.classList.add("wrong");
            else { correctCount++; updateScore(); }
            explainEl.textContent = q.explain;
            explainEl.classList.add("show");
          });
        });
        var nextBtn = itemEl.querySelector('[data-role="next"]');
        if(nextBtn){
          nextBtn.addEventListener("click", function(){
            itemEl.style.display = "none";
            var nextEl = quizEl.querySelector('.quiz-item[data-qi="' + (qi+1) + '"]');
            if(nextEl) nextEl.style.display = "";
          });
        }
        var finishBtn = itemEl.querySelector('[data-role="finish"]');
        if(finishBtn){
          finishBtn.addEventListener("click", function(){
            state.quizScores[topicId] = correctCount + "/" + qData.length;
            saveState();
            itemEl.querySelector(".quiz-nav").innerHTML = '<span class="quiz-score">Score saved: ' + correctCount + '/' + qData.length + '</span>';
          });
        }
      });
    }
  }

  function goTo(id){ renderTopic(id); }

  /* ---------------- Init ---------------- */
  applyTheme();
  renderSidebar();
  var startId = (location.hash || "").replace("#","") || allTopics[0].topic.id;
  renderTopic(startId);

  window.addEventListener("hashchange", function(){
    var id = (location.hash || "").replace("#","");
    if(id) renderTopic(id);
  });
})();
