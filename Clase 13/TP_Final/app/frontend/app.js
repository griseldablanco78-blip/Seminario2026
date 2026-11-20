const API_BASE_URL = (window.API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const form = document.querySelector("#prediction-form");
const predictButton = document.querySelector("#predict-button");
const formMessage = document.querySelector("#form-message");
const resultSection = document.querySelector("#result-section");
const apiStatus = document.querySelector("#api-status");
const sampleButton = document.querySelector("#sample-button");

const species = [
  { id: "setosa", name: "Iris setosa", className: "fill-setosa", note: "Pétalos habitualmente más cortos" },
  { id: "versicolor", name: "Iris versicolor", className: "fill-versicolor", note: "Medidas generalmente intermedias" },
  { id: "virginica", name: "Iris virginica", className: "fill-virginica", note: "Pétalos habitualmente más grandes" },
];
const colors = { setosa: "#8051bc", versicolor: "#e2748d", virginica: "#63a95e" };
let dataset = [];

function setApiStatus(state, message) {
  apiStatus.classList.toggle("is-online", state === "online");
  apiStatus.classList.toggle("is-offline", state === "offline");
  apiStatus.querySelector(".status-text").textContent = message;
}

async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    setApiStatus("online", "API conectada");
  } catch {
    setApiStatus("offline", "API sin conexión");
  }
}

function readMeasurements() {
  return Object.fromEntries([...new FormData(form).entries()].map(([key, value]) => [key, Number(value)]));
}

function showError(message) {
  formMessage.textContent = message;
  formMessage.hidden = false;
  resultSection.hidden = true;
}

function renderSpeciesCards(prediction) {
  const container = document.querySelector("#species-cards");
  container.replaceChildren(...species.map((item) => {
    const card = document.createElement("article");
    card.className = `species-result${prediction.especie === item.id ? " is-predicted" : ""}`;
    const heading = document.createElement("h3");
    heading.textContent = item.name;
    const text = document.createElement("p");
    text.textContent = prediction.especie === item.id ? "Es la especie estimada" : item.note;
    card.append(heading, text);
    return card;
  }));
}

function renderProbabilityChart(probabilities) {
  const chart = document.querySelector("#probability-chart");
  chart.replaceChildren(...species.map((item) => {
    const row = document.createElement("div");
    row.className = "probability-row";
    const label = document.createElement("span");
    label.className = "probability-label";
    label.textContent = item.name.replace("Iris ", "");
    const track = document.createElement("span");
    track.className = "probability-track";
    const fill = document.createElement("span");
    fill.className = `probability-fill ${item.className}`;
    const value = Math.max(0, Math.min(1, Number(probabilities[item.id] || 0)));
    fill.style.width = `${value * 100}%`;
    track.append(fill);
    const percent = document.createElement("span");
    percent.className = "probability-value";
    percent.textContent = `${(value * 100).toFixed(1)}%`;
    row.append(label, track, percent);
    return row;
  }));
}

function renderProfileChart() {
  const host = document.querySelector("#profile-chart");
  if (dataset.length === 0) {
    host.textContent = "No se pudo cargar la comparación de medidas.";
    return;
  }
  const width = 780, height = 340;
  const margin = { left: 50, right: 22, top: 22, bottom: 55 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const features = [
    { key: "sepal_length_cm", label: "Sépalo largo" },
    { key: "sepal_width_cm", label: "Sépalo ancho" },
    { key: "petal_length_cm", label: "Pétalo largo" },
    { key: "petal_width_cm", label: "Pétalo ancho" },
  ];
  const x = (index) => margin.left + index * (plotWidth / (features.length - 1));
  const y = (value) => margin.top + plotHeight - (value / 8) * plotHeight;
  const NS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(NS, "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Comparación de los promedios de las cuatro medidas para las tres especies de Iris");
  const add = (name, attrs, textValue = "") => {
    const element = document.createElementNS(NS, name);
    for (const [key, value] of Object.entries(attrs)) element.setAttribute(key, value);
    if (textValue) element.textContent = textValue;
    svg.append(element);
    return element;
  };

  for (let tick = 0; tick <= 8; tick += 2) {
    const yy = y(tick);
    add("line", { x1: margin.left, x2: width - margin.right, y1: yy, y2: yy, class: "grid-line" });
    add("text", { x: margin.left - 12, y: yy + 4, "text-anchor": "end", class: "axis-text" }, String(tick));
  }
  features.forEach((feature, index) => {
    add("text", { x: x(index), y: height - 23, "text-anchor": "middle", class: "axis-text category-text" }, feature.label);
  });
  add("text", { x: 14, y: margin.top + plotHeight / 2, transform: `rotate(-90 14 ${margin.top + plotHeight / 2})`, "text-anchor": "middle", class: "axis-text" }, "Centímetros");

  const series = species.map((item) => {
    const rows = dataset.filter((row) => row.especie === item.id);
    return { id: item.id, values: features.map((feature) => rows.reduce((total, row) => total + row[feature.key], 0) / rows.length) };
  });
  const seriesColors = colors;
  for (const line of series) {
    const points = line.values.map((value, index) => `${x(index)},${y(value)}`).join(" ");
    add("polyline", { points, class: `profile-line line-${line.id}`, fill: "none", stroke: seriesColors[line.id], "stroke-width": 3, "stroke-linecap": "round", "stroke-linejoin": "round" });
    line.values.forEach((value, index) => {
      const dot = add("circle", { cx: x(index), cy: y(value), r: 4.5, fill: seriesColors[line.id], class: "profile-point" });
      const title = document.createElementNS(NS, "title");
      title.textContent = `Iris ${line.id}: ${features[index].label.toLowerCase()}, ${value.toFixed(2)} cm`;
      dot.append(title);
    });
  }
  host.replaceChildren(svg);
}

function loadDataset() {
  dataset = Array.isArray(window.IRIS_DATA) ? window.IRIS_DATA : [];
  if (dataset.length === 0) {
    const host = document.querySelector("#profile-chart");
    host.textContent = "No se pudo cargar la comparación de medidas.";
    host.classList.add("chart-caption");
  }
}

sampleButton.addEventListener("click", () => {
  form.elements.sepal_length_cm.value = "6.3";
  form.elements.sepal_width_cm.value = "3.3";
  form.elements.petal_length_cm.value = "6.0";
  form.elements.petal_width_cm.value = "2.5";
  formMessage.hidden = true;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formMessage.hidden = true;
  if (!form.reportValidity()) return;
  const measurements = readMeasurements();
  predictButton.disabled = true;
  predictButton.querySelector("span:first-child").textContent = "Consultando el modelo…";
  try {
    const response = await fetch(`${API_BASE_URL}/predecir`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(measurements),
    });
    const result = await response.json();
    if (!response.ok) {
      if (response.status === 422) {
        const details = Array.isArray(result.detail)
          ? result.detail.map((item) => `${item.loc?.at(-1) || "Dato"}: ${item.msg}`).join("; ")
          : "Revisá los cuatro valores ingresados.";
        throw new Error(`La API rechazó la entrada (422). ${details}`);
      }
      throw new Error(`La API respondió con un error ${response.status}. Probá de nuevo más tarde.`);
    }
    renderSpeciesCards(result);
    renderProbabilityChart(result.probabilidades);
    renderProfileChart();
    resultSection.hidden = false;
    resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    showError(error instanceof TypeError
      ? "No pude conectar con la API. Comprobá que esté encendida y que la URL configurada sea correcta."
      : error.message);
  } finally {
    predictButton.disabled = false;
    predictButton.querySelector("span:first-child").textContent = "Descubrir la especie";
  }
});

loadDataset();
checkHealth();
