(() => {
  "use strict";

  // Visible Grade → Subject groups replace confusing search/filter controls.
  const slots = new Map(
    [...document.querySelectorAll("[data-material-slot]")]
      .map(element => [element.dataset.materialSlot, element])
  );
  if (!slots.size) return;

  const clean = value => String(value ?? "").trim();
  const labels = Object.freeze({
    Textbook: "પાઠ્યપુસ્તક", Notes: "નોટ્સ",
    "Question Paper": "પ્રશ્નપત્ર", Worksheet: "વર્કશીટ",
    "Model Paper": "મોડેલ પેપર", Other: "અન્ય"
  });
  const hosts = Object.freeze({
    "drive.google.com": "Google Drive",
    "docs.google.com": "Google Drive",
    "mega.nz": "MEGA",
    "mega.io": "MEGA"
  });

  // Never show the owner's entire shared folder, even if mistakenly in JSON.
  function providerName(url) {
    try {
      const parsed = new URL(url);
      const host = parsed.hostname.toLowerCase().replace(/^www\./, "");
      const driveFile = host === "drive.google.com" &&
        /^\/file\/d\/[A-Za-z0-9_-]+(?:\/|$)/.test(parsed.pathname);
      const docsFile = host === "docs.google.com" &&
        /^\/(?:document|spreadsheets|presentation)\/d\/[A-Za-z0-9_-]+(?:\/|$)/.test(parsed.pathname);
      const megaFile = (host === "mega.nz" || host === "mega.io") &&
        /^\/file\/[A-Za-z0-9_-]+(?:\/|$)/.test(parsed.pathname);
      return parsed.protocol === "https:" && !parsed.username && !parsed.password &&
        (driveFile || docsFile || megaFile) ? hosts[host] : "";
    } catch {
      return "";
    }
  }

  function subjectId(value) {
    const subject = clean(value).toLocaleLowerCase("gu-IN");
    if (/ગણિત|math|mathematics/.test(subject)) return "math";
    if (/વિજ્ઞાન|ભૌતિક|રસાયણ|જીવવિજ્ઞાન|science|physics|chemistry|biology/.test(subject)) return "science";
    if (/અંગ્રેજી|english|grammar/.test(subject)) return "english";
    return "";
  }

  function normalize(row) {
    if (!row || row.status !== "Approved") return null;
    const url = clean(row.url), title = clean(row.title), grade = clean(row.standard);
    const subject = subjectId(row.subject), provider = providerName(url);
    if (!title || !["10", "12"].includes(grade) || !subject || !provider) return null;
    return {
      title: title.slice(0, 180), url, grade, subject, provider,
      category: Object.prototype.hasOwnProperty.call(labels, row.category) ? row.category : "Other",
      description: clean(row.description).slice(0, 450),
      date: clean(row.updated_at)
    };
  }

  // textContent prevents HTML from untrusted editorial entries being executed.
  function node(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function card(item) {
    const wrap = node("article", "material-item material-compact-item");
    const badges = node("div", "material-badges");
    badges.append(node("span", "material-badge", labels[item.category]));
    badges.append(node("span", "material-badge source", item.provider));
    wrap.append(badges, node("h4", "", item.title));
    if (item.description) wrap.append(node("p", "", item.description));
    if (/^\d{4}-\d{2}-\d{2}$/.test(item.date)) {
      wrap.append(node("p", "material-meta", "અપડેટ: " + item.date));
    }
    const link = node("a", "material-action", "PDF / ફાઇલ ખોલો ↗");
    link.href = item.url; link.target = "_blank";
    link.rel = "noopener noreferrer nofollow";
    link.setAttribute("aria-label", item.title + " — " + item.provider + " પર જુઓ");
    wrap.append(link);
    return wrap;
  }

  function showMessage(slot, message) {
    slot.replaceChildren(node("p", "material-inline-notice", message));
    slot.setAttribute("aria-busy", "false");
  }

  for (const slot of slots.values()) slot.setAttribute("aria-busy", "true");

  fetch("data/materials.json", {cache: "no-store"})
    .then(response => {
      if (!response.ok) throw new Error("Material list could not load");
      return response.json();
    })
    .then(rows => {
      if (!Array.isArray(rows)) throw new Error("Invalid material list");
      const groups = new Map([...slots.keys()].map(key => [key, []]));
      for (const item of rows.map(normalize).filter(Boolean)) {
        const key = item.grade + "-" + item.subject;
        if (groups.has(key)) groups.get(key).push(item);
      }
      for (const [key, slot] of slots) {
        const items = groups.get(key).sort((a, b) => b.date.localeCompare(a.date));
        if (items.length) {
          slot.replaceChildren(...items.map(card));
          slot.setAttribute("aria-busy", "false");
        } else {
          showMessage(slot, "આ વિષયની મંજૂર PDF / Notes હજી ઉપલબ્ધ નથી. નીચેની અભ્યાસ માર્ગદર્શિકા વાંચી શકો છો.");
        }
      }
    })
    .catch(() => {
      for (const slot of slots.values()) {
        showMessage(slot, "ફાઇલની યાદી હાલ લોડ થઈ શકી નથી. થોડા સમય પછી ફરી પ્રયાસ કરો.");
      }
    });
})();
