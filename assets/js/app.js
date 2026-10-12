(() => {
  "use strict";

  const navToggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".main-nav");

  function setNavState(open) {
    if (!nav || !navToggle) return;
    nav.classList.toggle("is-open", open);
    navToggle.setAttribute("aria-expanded", String(open));
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("nav-open", open);
  }

  function closeNav() {
    setNavState(false);
  }

  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      setNavState(!nav.classList.contains("is-open"));
    });

    nav.querySelectorAll("a").forEach(link => link.addEventListener("click", closeNav));

    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        closeNav();
        navToggle.focus();
      }
    });

    document.addEventListener("click", event => {
      if (nav.classList.contains("is-open") && !nav.contains(event.target) && !navToggle.contains(event.target)) {
        closeNav();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 1050) closeNav();
    });
  }

  window.addEventListener("pagehide", closeNav);

  const current = location.pathname.split("/").pop() || "index.html";
  const activePage = current.startsWith("blog-") ? "blog.html" : current;
  document.querySelectorAll(".main-nav a").forEach(a => {
    if (a.getAttribute("href") === activePage) a.setAttribute("aria-current", "page");
  });

  document.querySelectorAll("[data-year]").forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  const searchForm = document.querySelector("[data-site-search-form]");
  const searchInput = searchForm?.querySelector("input[type='search']");
  const searchResults = document.querySelector("[data-site-search-results]");

  const pages = [
    {title:"Study Material", desc:"Notes, papers and downloadable learning resources", url:"study-material.html", keys:"material textbook notes papers pdf drive mega download અભ્યાસ સામગ્રી પાઠ્યપુસ્તક પ્રશ્નપત્ર ડાઉનલોડ"},
    {title:"Board Exam", desc:"Std. 10 and Std. 12 board preparation", url:"board-exam.html", keys:"board exam gseb standard 10 12 std 10 std 12 બોર્ડ પરીક્ષા ધોરણ 10 12"},
    {title:"Online Quiz", desc:"Chapter-wise quiz and self-practice", url:"quiz.html", keys:"quiz mcq online test practice ક્વિઝ ટેસ્ટ પ્રશ્ન"},
    {title:"Learning Games", desc:"Math Sprint, Percentage and Algebra practice", url:"games.html", keys:"games learning math algebra percentage ગેમ્સ રમત ગણિત"},
    {title:"Study Plan", desc:"Daily, weekly and board-focused planning", url:"blog-study-plan.html", keys:"study plan timetable revision schedule અભ્યાસ આયોજન સમયપત્રક"},
    {title:"Study Guidance Blog", desc:"Original educational study guides", url:"blog.html", keys:"blog study revision guidance અભ્યાસ માર્ગદર્શન"},
    {title:"90-Day Board Study Plan", desc:"Three-phase board exam preparation guide", url:"blog-board-study-plan.html", keys:"90 day board study plan exam બોર્ડ અભ્યાસ આયોજન"},
    {title:"Smart Revision", desc:"Recall, weak-topic tracking and revision cycles", url:"blog-smart-revision.html", keys:"smart revision recall weak topic પુનરાવર્તન"},
    {title:"Self-Test Guide", desc:"Use quizzes to find learning gaps", url:"blog-self-test.html", keys:"self test quiz learning gaps practice સ્વમૂલ્યાંકન"},
    {title:"Answer Writing", desc:"Exam answer structure and time management", url:"blog-answer-writing.html", keys:"answer writing exam presentation time management જવાબ લેખન"},
    {title:"Maths Practice", desc:"Error logs, mixed sets and timed practice", url:"blog-math-practice.html", keys:"math maths practice error log ગણિત પ્રેક્ટિસ"},
    {title:"Exam Week", desc:"7-day exam revision routine", url:"blog-exam-week.html", keys:"exam week 7 day revision પરીક્ષા અઠવાડિયું"},
    {title:"News & Updates", desc:"Verified educational news and circulars", url:"updates.html", keys:"news updates circular gseb ssa udise education સમાચાર પરિપત્ર"},
    {title:"Education Jobs", desc:"School education recruitment notices", url:"jobs.html", keys:"jobs recruitment શિક્ષક ભરતી નોકરી"},
    {title:"FAQ", desc:"Common questions about Gyan Shiksha and Quiz Saathi", url:"faq.html", keys:"faq help quiz privacy official પ્રશ્ન મદદ"}
  ];

  function normalize(value) {
    return value.toLocaleLowerCase().trim();
  }

  function renderResults(query) {
    if (!searchResults || !searchInput) return [];
    const q = normalize(query);
    if (!q) {
      searchResults.hidden = true;
      searchResults.innerHTML = "";
      searchInput.setAttribute("aria-expanded", "false");
      return [];
    }

    const words = q.split(/\s+/).filter(Boolean);
    const matches = pages.filter(page => {
      const haystack = normalize(`${page.title} ${page.desc} ${page.keys}`);
      return words.every(word => haystack.includes(word));
    }).slice(0, 5);

    searchResults.innerHTML = "";
    if (matches.length === 0) {
      const empty = document.createElement("div");
      empty.className = "search-empty";
      empty.textContent = "મેળ ખાતું section મળ્યું નથી. Board, Quiz, Games, Study Plan અથવા Revision શોધો.";
      searchResults.appendChild(empty);
    } else {
      matches.forEach(page => {
        const link = document.createElement("a");
        link.href = page.url;
        const title = document.createElement("strong");
        title.textContent = page.title;
        const desc = document.createElement("span");
        desc.textContent = page.desc;
        link.append(title, desc);
        searchResults.appendChild(link);
      });
    }

    searchResults.hidden = false;
    searchInput.setAttribute("aria-expanded", "true");
    return matches;
  }

  if (searchForm && searchInput && searchResults) {
    searchInput.addEventListener("input", () => renderResults(searchInput.value));
    searchInput.addEventListener("focus", () => { if (searchInput.value.trim()) renderResults(searchInput.value); });
    searchInput.addEventListener("keydown", event => {
      if (event.key === "ArrowDown" && !searchResults.hidden) {
        const first = searchResults.querySelector("a");
        if (first) {
          event.preventDefault();
          first.focus();
        }
      } else if (event.key === "Escape") {
        searchResults.hidden = true;
        searchInput.setAttribute("aria-expanded", "false");
      }
    });

    searchResults.addEventListener("keydown", event => {
      const links = [...searchResults.querySelectorAll("a")];
      const index = links.indexOf(document.activeElement);
      if (event.key === "ArrowDown" && index >= 0) {
        event.preventDefault();
        (links[index + 1] || links[0])?.focus();
      } else if (event.key === "ArrowUp" && index >= 0) {
        event.preventDefault();
        (links[index - 1] || searchInput)?.focus();
      } else if (event.key === "Escape") {
        event.preventDefault();
        searchResults.hidden = true;
        searchInput.setAttribute("aria-expanded", "false");
        searchInput.focus();
      }
    });

    searchForm.addEventListener("submit", event => {
      event.preventDefault();
      const matches = renderResults(searchInput.value);
      if (matches.length === 1) {
        window.location.href = matches[0].url;
      } else if (matches.length > 1) {
        searchResults.querySelector("a")?.focus();
      } else {
        searchInput.focus();
      }
    });

    document.addEventListener("click", event => {
      if (!searchForm.contains(event.target) && !searchResults.contains(event.target)) {
        searchResults.hidden = true;
        searchInput.setAttribute("aria-expanded", "false");
      }
    });
  }
})();
