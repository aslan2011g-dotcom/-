const tg = window.Telegram?.WebApp;
tg?.ready(); 
tg?.expand();
tg?.setHeaderColor?.("#0a0f1f");

let WORDS = [];
let current = null;

const list = document.getElementById("list");
const detail = document.getElementById("detail");
const dTerm = document.getElementById("dTerm");
const dDef = document.getElementById("dDef");
const dAi = document.getElementById("dAi");
const btnExplain = document.getElementById("btnExplain");
const back = document.getElementById("back");

// Загружаем слова из JSON
fetch("words.json")
  .then(r => r.json())
  .then(data => {
    WORDS = data;
    render();
  })
  .catch(err => {
    list.innerHTML = "<div style='color:red; padding:20px'>Ошибка загрузки словаря. Проверь words.json</div>";
  });

function render() {
  list.innerHTML = "";
  WORDS.forEach((w, i) => {
    const el = document.createElement("div");
    el.className = "word-item";
    el.innerHTML = `
      <div>
        <div class="word-term">${escapeHtml(w.term)}</div>
        <div class="word-def">${escapeHtml(truncate(w.def, 60))}</div>
      </div>
      <div class="chev">›</div>`;
    el.addEventListener("click", () => open(i));
    list.appendChild(el);
  });
}

function open(i) {
  current = { ...WORDS[i], idx: i };
  dTerm.textContent = current.term;
  dDef.textContent = current.def;
  dAi.textContent = "Пояснение от ИИ появится после нажатия «Пояснить».";
  list.classList.add("hidden");
  detail.classList.remove("hidden");
  tg?.HapticFeedback?.impactOccurred("light");
}

back.addEventListener("click", () => {
  detail.classList.add("hidden");
  list.classList.remove("hidden");
  current = null;
});

btnExplain.addEventListener("click", () => {
  if (!current) return;
  // Отправляем данные боту
  tg.sendData(JSON.stringify({
    term: current.term,
    def: current.def,
    idx: current.idx
  }));
});

function truncate(s, n) { return s.length > n ? s.slice(0, n) + "…" : s; }
function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
  }[c]));
}
