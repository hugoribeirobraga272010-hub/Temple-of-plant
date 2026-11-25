
const formulario = document.getElementById("formulario");
const resultado = document.getElementById("resultado");

formulario.addEventListener("submit", async function(evento) {
  evento.preventDefault();

  const luz = document.getElementById("luz").value;
  const pets = document.querySelector('input[name="pets"]:checked').value === "yes";
  const experiencia = document.getElementById("experiencia").value;
  const umidade = document.getElementById("umidade").value;
  const rega = document.getElementById("rega").value;
  const espaco = document.getElementById("espaco").value;
  const temperatura = document.getElementById("temperatura").value;

  resultado.innerHTML = "<p>Finding your plant...</p>";

  try {
    const resposta = await fetch("/recomendar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        luz,
        pets,
        experiencia,
        umidade,
        rega,
        espaco,
        temperatura
      })
    });

    const planta = await resposta.json();

    if (!resposta.ok) {
      resultado.innerHTML = `<p class="aviso">${planta.erro}</p>`;
      return;
    }

    resultado.innerHTML = `
      <p class="sobretitulo">THE FOREST HAS MADE ITS CHOICE</p>
      <article class="cartao-planta">
        <img src="${planta.imagem}" alt="${planta.nome}" onerror="this.style.display='none'">
        <div>
          <span class="tag">${planta.cuidado} care</span>
          <h3>${planta.nome}</h3>
          <p>${planta.descricao}</p>
          <p><strong>Why this plant?</strong> ${planta.motivo}</p>
          <p class="detalhes">Watering guide: about ${planta.rega} time(s) per week · Mature height: ${planta.altura} cm</p>
          ${pets ? '<p class="aviso">Pet safety information is based on our catalog. Verify it with a reliable source before purchasing.</p>' : ""}
        </div>
      </article>
    `;

    resultado.scrollIntoView({ behavior: "smooth" });

  } catch (erro) {
    resultado.innerHTML = '<p class="aviso">Could not connect to the plant server. Please try again.</p>';
    console.error(erro);
  }
});
