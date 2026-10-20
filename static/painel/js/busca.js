const modalBusca = document.getElementById("modalBusca");
const tituloModal = modalBusca.querySelector("#tituloModal");
const subtituloModal = modalBusca.querySelector("#subtituloModal");
const pesquisaRegistro = modalBusca.querySelector("#pesquisaRegistro");
const labelPesquisa = modalBusca.querySelector("#labelPesquisa");
const mensagemBusca = modalBusca.querySelector("#mensagemBusca");
const resultadosBusca = modalBusca.querySelector("#resultados");
const btnBuscar = modalBusca.querySelector("#btnBuscar");
const btnConfirmar = modalBusca.querySelector("#btnConfirmar");

let configuracaoBusca = null;
let registroSelecionado = null;
let numeroBusca = 0;

// Fechar o modal
modalBusca.querySelector("#btnFechar").addEventListener("click", fecharModal);
modalBusca.querySelector("#btnCancelar").addEventListener("click", fecharModal);

function fecharModal() {
    modalBusca.close();
    registroSelecionado = null;
    configuracaoBusca = null;
}

// Abrir o modal para qualquer tipo de registro
function abrirModalBusca(configuracao) {
    configuracaoBusca = configuracao;
    registroSelecionado = null;

    tituloModal.textContent = configuracao.titulo;
    pesquisaRegistro.placeholder =
        configuracao.placeholder || "Digite para pesquisar";

    pesquisaRegistro.value = "";
    resultadosBusca.innerHTML = "";
    btnConfirmar.disabled = true;

    modalBusca.showModal();
    pesquisaRegistro.focus();

    buscarRegistros("");
}

// Buscar pelo botão
btnBuscar.addEventListener("click", () => {
    buscarRegistros(pesquisaRegistro.value.trim());
});

// Buscar também ao pressionar Enter
pesquisaRegistro.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        buscarRegistros(pesquisaRegistro.value.trim());
    }
});

async function buscarRegistros(termo = "") {
    if (!configuracaoBusca) return;

    const buscaAtual = ++numeroBusca;

    registroSelecionado = null;
    btnConfirmar.disabled = true;
    resultadosBusca.innerHTML = "";
    mensagemBusca.textContent = "Carregando resultados...";

    const parametros = new URLSearchParams({
        q: termo,
        ...(configuracaoBusca.parametros || {}),
    });

    try {
        const resposta = await fetch(`${configuracaoBusca.url}?${parametros}`);

        if (!resposta.ok) {
            throw new Error("Falha na consulta.");
        }

        const dados = await resposta.json();

        // Ignora uma resposta antiga, caso outra busca tenha sido feita.
        if (buscaAtual !== numeroBusca || !modalBusca.open) return;

        exibirResultados(dados.resultados || []);
    } catch (erro) {
        if (buscaAtual !== numeroBusca || !modalBusca.open) return;

        mensagemBusca.textContent =
            "Não foi possível carregar os resultados. Tente novamente.";
    }
}

function exibirResultados(registros) {
    resultadosBusca.innerHTML = "";

    if (registros.length === 0) {
        mensagemBusca.textContent = "Nenhum registro encontrado.";
        return;
    }

    mensagemBusca.textContent = `${registros.length} resultado(s) encontrado(s).`;

    registros.forEach((registro) => {
        const botao = document.createElement("button");

        botao.type = "button";
        botao.className = "item-resultado";
        botao.setAttribute("aria-pressed", "false");

        const titulo = document.createElement("span");
        titulo.className = "resultado-titulo";
        titulo.textContent = configuracaoBusca.rotulo(registro);

        botao.appendChild(titulo);

        if (configuracaoBusca.detalhe) {
            const detalheTexto = configuracaoBusca.detalhe(registro);

            if (detalheTexto) {
                const detalhe = document.createElement("span");
                detalhe.className = "resultado-detalhe";
                detalhe.textContent = detalheTexto;
                botao.appendChild(detalhe);
            }
        }

        // Selecionar com um clique
        botao.addEventListener("click", () => {
            registroSelecionado = registro;

            resultadosBusca
                .querySelectorAll(".item-resultado")
                .forEach((item) => {
                    item.classList.remove("selecionado");
                    item.setAttribute("aria-pressed", "false");
                });

            botao.classList.add("selecionado");
            botao.setAttribute("aria-pressed", "true");
            btnConfirmar.disabled = false;
        });

        // Confirmar com duplo clique
        botao.addEventListener("dblclick", confirmarSelecao);

        resultadosBusca.appendChild(botao);
    });
}

function confirmarSelecao() {
    if (!registroSelecionado || !configuracaoBusca) return;

    configuracaoBusca.aoConfirmar(registroSelecionado);
    fecharModal();
}

// Confirmar a seleção
btnConfirmar.addEventListener("click", confirmarSelecao);
