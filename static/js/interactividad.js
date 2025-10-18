// 🧠 Retroalimentación emocional
function mostrarMensaje(texto) {
  const mensaje = document.getElementById("mensaje-emocional");
  mensaje.innerText = texto;
  mensaje.style.opacity = 1;
  setTimeout(() => mensaje.style.opacity = 0, 2000);
}

// 🔁 Nivel 1: Bucles
function iniciarBucles() {
  let saltos = 0;
  const ticu = document.getElementById("ticu-clima");
  const intervalo = setInterval(() => {
    ticu.style.transform = "translateY(-20px)";
    setTimeout(() => ticu.style.transform = "translateY(0)", 200);
    saltos++;
    if (saltos >= 5) {
      clearInterval(intervalo);
      mostrarMensaje("¡Bucles dominados! 🌀");
      desbloquearMedalla("medalla-bucles");
    }
  }, 500);
}

// 🌦️ Nivel 2: Condicionales
function clima(tipo) {
  const ticu = document.getElementById("ticu-clima");
  if (tipo === "sol") {
    ticu.src = "/static/img/ticu-gafas.png";
    mostrarMensaje("¡TICU se protege del sol! 😎");
  } else {
    ticu.src = "/static/img/ticu-paraguas.png";
    mostrarMensaje("¡TICU se protege de la lluvia! ☔");
  }
  desbloquearMedalla("medalla-condicionales");
}

// 📦 Nivel 3: Variables
let puntos = 0;
function sumarPuntos() {
  puntos++;
  document.getElementById("contador").innerText = "Puntos: " + puntos;
  if (puntos === 10) {
    mostrarMensaje("¡Has alcanzado 10 puntos! 🎉");
    desbloquearMedalla("medalla-variables");
  }
}

// 🏅 Sistema de medallas
function desbloquearMedalla(id) {
  const medalla = document.getElementById(id);
  medalla.classList.remove("bloqueada");
  medalla.classList.add("desbloqueada");
  localStorage.setItem(id, "desbloqueada");
}

// ❓ Quiz TIC con vidas
let vidas = 3;
let preguntaActual = 0;

const preguntas = [
  { pregunta: "¿Qué hace un bucle?", opciones: ["Repite acciones", "Detiene el programa", "Cambia colores", "Borra datos"], correcta: 0 },
  { pregunta: "¿Qué es una variable?", opciones: ["Un número fijo", "Un contenedor de datos", "Un error", "Una imagen"], correcta: 1 },
  { pregunta: "¿Qué hace un condicional?", opciones: ["Repite acciones", "Toma decisiones", "Cambia colores", "Termina el programa"], correcta: 1 },
  { pregunta: "¿Qué hace un botón?", opciones: ["Inicia acciones", "Repite acciones", "Borra datos", "Cambia colores"], correcta: 0 },
  { pregunta: "¿Qué significa 'if' en programación?", opciones: ["Mientras", "Entonces", "Si", "Repetir"], correcta: 2 },
  { pregunta: "¿Qué tipo de dato es 'true'?", opciones: ["Texto", "Número", "Booleano", "Condicional"], correcta: 2 },
  { pregunta: "¿Qué hace un bucle 'for'?", opciones: ["Ejecuta una vez", "Repite con condición", "Detiene el programa", "Cambia colores"], correcta: 1 },
  { pregunta: "¿Qué es una función?", opciones: ["Una imagen", "Un bloque de código reutilizable", "Un error", "Un botón"], correcta: 1 },
  { pregunta: "¿Qué hace 'console.log'?", opciones: ["Muestra en pantalla", "Repite acciones", "Cambia colores", "Detiene el programa"], correcta: 0 },
  { pregunta: "¿Qué es un evento?", opciones: ["Una fiesta", "Una acción que activa código", "Un error", "Una variable"], correcta: 1 }
];

function mostrarSiguientePregunta() {
  const quiz = document.getElementById("quiz-container");
  if (preguntaActual >= preguntas.length || vidas === 0) {
    quiz.innerHTML = "<p>¡Quiz terminado!</p>";
    return;
  }

  const p = preguntas[preguntaActual];
  quiz.innerHTML = `<p>${p.pregunta}</p>` + p.opciones.map((op, i) =>
    `<button onclick="responder(${i === p.correcta})">${op}</button>`).join("");
}

function responder(correcta) {
  if (!correcta) {
    vidas--;
    document.getElementById("vidas").innerText = "Vidas: " + "❤️".repeat(vidas);
    mostrarMensaje(`¡Ups! Te queda${vidas === 1 ? '' : 'n'} ${vidas} vida${vidas === 1 ? '' : 's'} 😟`);
  } else {
    mostrarMensaje("¡Correcto! 🎉");
  }
  preguntaActual++;
  mostrarSiguientePregunta();
}

// 🚀 Inicialización al cargar la página
window.onload = function () {
  mostrarSiguientePregunta();
  ["medalla-bucles", "medalla-condicionales", "medalla-variables"].forEach(id => {
    if (localStorage.getItem(id) === "desbloqueada") {
      const medalla = document.getElementById(id);
      medalla.classList.remove("bloqueada");
      medalla.classList.add("desbloqueada");
    }
  });
};