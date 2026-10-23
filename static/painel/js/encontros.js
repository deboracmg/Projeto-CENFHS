const modalEncontro = document.getElementById("modalPrimario");
const formEncontro = modalEncontro.querySelector("#formEncontro");
const camposEncontro = formEncontro.querySelectorAll("input, select");
const btnNovoEncontro = document.getElementById("btnNovoCadastro");

const tituloModalEncontro = modalEncontro.querySelector("#tituloModal");
const subtituloModalEncontro = modalEncontro.querySelector("#subtituloModal");
const qtdParticipantes = modalEncontro.querySelector("#qtd_participantes");
const idProfissional = modalEncontro.querySelector("#profissional_id");
const nomeProfissional = modalEncontro.querySelector("#resp_interno");
const idServico = modalEncontro.querySelector("#servico_id");
const tipoServico = modalEncontro.querySelector("#tipo_servico");
const nomeServico = modalEncontro.querySelector("#nome_servico");
const inputListaPresenca = document.getElementById("lista_presenca");
const labelArquivo = document.getElementById("labelArquivo");
const arquivoSelecionado = document.getElementById("arquivoSelecionado");
const linkVisualizar = document.getElementById("visualizarListaPresenca");

const btnEditarEncontro = modalEncontro.querySelector("#btnEditar");
const btnSalvarEncontro = modalEncontro.querySelector("#btnSalvar");
const btnFecharEncontro = modalEncontro.querySelector("#btnFechar");
const btnsDetalharEncontro = document.querySelectorAll(".btn-abrir-encontro");
const btnLimparProfissional = modalEncontro.querySelector(
    "#btnLimparProfissional",
);
const btnBuscarProfissional = modalEncontro.querySelector(
    "#btnBuscarProfissional",
);
const btnRemoverListaPresenca = document.getElementById("removerListaPresenca");
const btnBuscarServico = modalEncontro.querySelector("#btnBuscarServico");

btnsDetalharEncontro.forEach((button) => {
    button.addEventListener("click", async () => {
        const encontroId = button.dataset.encontroId;
        const response = await fetch(`/dashboard/encontros/${encontroId}`);

        if (!response.ok) {
            console.error("Erro ao buscar encontro.");
            return;
        }

        const encontro = await response.json();
        detalharEncontro(encontro);
    });
});

btnEditarEncontro.addEventListener("click", () => {
    btnLimparProfissional.disabled = false;
    btnRemoverListaPresenca.disabled = false;
    btnBuscarProfissional.disabled = false;
    btnBuscarServico.disabled = false;
    tituloModalEncontro.textContent = "Editando dados do encontro";
    habilitarEdicaoFormulario(modalEncontro);
});

btnNovoEncontro.addEventListener("click", () => {
    document.getElementById("remover_lista").value = "false";
    btnLimparProfissional.hidden = true;
    btnBuscarProfissional.disabled = false;
    btnBuscarServico.disabled = true;
    limparArquivo();
    formNovoCadastro(modalEncontro, "Cadastrar novo encontro");
});

btnFecharEncontro.addEventListener("click", () => modalEncontro.close());

btnLimparProfissional.addEventListener("click", () => {
    idProfissional.value = "";
    nomeProfissional.value = "";

    btnLimparProfissional.hidden = true;
});

function detalharEncontro(encontro) {
    preencherFormularioEncontro(encontro);
    tituloModalEncontro.textContent = "Dados do encontro";
    subtituloModalEncontro.textContent = "Código: " + encontro.encontro_id;
    formEncontro.classList.remove("com-erro");

    modalEncontro.showModal();
    btnLimparProfissional.disabled = true;
    btnRemoverListaPresenca.disabled = true;
    btnBuscarProfissional.disabled = true;
    desabilitarEdicaoFormulario(modalEncontro);
}

function preencherFormularioEncontro(encontro) {
    document.getElementById("encontro_id").value = encontro.encontro_id || "";
    document.getElementById("tipo_servico").value = encontro.tipo || "";
    document.getElementById("servico_id").value = encontro.servico_id || "";
    document.getElementById("nome_servico").value = encontro.nome || "";
    document.getElementById("local").value = encontro.local || "";

    const [data, hora] = converterDataHora(encontro.data_hora).split(", ");
    document.getElementById("data_encontro").value = data
        .split("/")
        .reverse()
        .join("-");
    document.getElementById("hora_encontro").value = hora;

    document.getElementById("profissional_id").value =
        encontro.profissional_id || "";
    document.getElementById("resp_interno").value = encontro.resp_interno || "";
    btnLimparProfissional.hidden = !idProfissional.value;

    document.getElementById("resp_externo").value = encontro.resp_externo || "";
    document.getElementById("qtd_participantes").value =
        encontro.qtd_participantes || "";

    exibirArquivo(encontro.lista_presenca);
}

/* =========================================================
   VALIDAÇÃO DE CAMPOS
   ========================================================= */
qtdParticipantes.addEventListener("input", (e) => {
    e.target.value = permitirApenasNumeros(e);
});

/* =========================================================
   SALVAR CADASTRO
========================================================= */

formEncontro.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();
        formEncontro.classList.remove("com-erro");
        checarFormulário(formEncontro);

        const url = "/dashboard/encontros/salvar/";
        const formData = new FormData(formEncontro);
        const dados = await salvarCadastro(url, formData);

        modalEncontro.close();
        exibirNotificacaoComReload(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});

/* =========================================================
   SELECIONAR ARQUIVO PDF
========================================================= */
const LIMITE_PDF = 1 * 1024 * 1024; // 1 MiB
let urlArquivo = null;

inputListaPresenca.addEventListener("change", async () => {
    const arquivo = inputListaPresenca.files[0];

    if (!arquivo) {
        limparArquivo();
        return;
    }

    // Verifica a extensão e o tipo informado pelo navegador.
    const extensaoValida = arquivo.name.toLowerCase().endsWith(".pdf");
    const tipoValido = arquivo.type === "application/pdf";

    if (!extensaoValida || !tipoValido) {
        exibirNotificacao("Selecione um arquivo PDF válido.", "aviso");

        limparArquivo();
        return;
    }

    // Verifica o limite de tamanho.
    if (arquivo.size > LIMITE_PDF) {
        exibirNotificacao("O arquivo não pode ultrapassar 1 MB.", "aviso");

        limparArquivo();
        return;
    }

    // Verifica a assinatura do arquivo, não apenas o nome.
    try {
        const inicioArquivo = await arquivo.slice(0, 1024).arrayBuffer();
        const cabecalho = new TextDecoder().decode(inicioArquivo);

        if (!cabecalho.includes("%PDF-")) {
            exibirNotificacao(
                "O arquivo selecionado não parece ser um PDF válido.",
                "aviso",
            );

            limparArquivo();
            return;
        }
    } catch (erro) {
        exibirNotificacao("Não foi possível validar o arquivo.", "aviso");

        limparArquivo();
        return;
    }

    // Libera a URL anterior, caso exista.
    if (urlArquivo) {
        URL.revokeObjectURL(urlArquivo);
    }

    // Cria uma URL temporária para abrir o PDF.
    urlArquivo = URL.createObjectURL(arquivo);
    exibirArquivo(urlArquivo);
});

function obterNomeArquivo(url) {
    const nome = url.split("/").pop().split("?")[0];

    try {
        return decodeURIComponent(nome);
    } catch {
        return nome;
    }
}

function exibirArquivo(urlArquivo) {
    if (urlArquivo) {
        arquivoSelecionado.hidden = false;
        labelArquivo.hidden = true;
        linkVisualizar.textContent =
            inputListaPresenca.files[0]?.name || obterNomeArquivo(urlArquivo);
        linkVisualizar.href = urlArquivo;
        document.getElementById("remover_lista").value = "false";
    } else {
        limparArquivo();
    }
}

function limparArquivo() {
    inputListaPresenca.value = "";
    arquivoSelecionado.hidden = true;
    labelArquivo.hidden = false;
    linkVisualizar.removeAttribute("href");
    linkVisualizar.textContent = "";

    if (urlArquivo) {
        URL.revokeObjectURL(urlArquivo);
        urlArquivo = null;
    }
}

btnRemoverListaPresenca.addEventListener("click", () => {
    document.getElementById("remover_lista").value = "true";
    limparArquivo();
});

/* =========================================================
   SELECIONAR SERVIÇO
========================================================= */

tipoServico.addEventListener("change", () => {
    nomeServico.value = "";
    idServico.value = "";
    btnBuscarServico.disabled = !tipoServico.value;
});

btnBuscarServico.addEventListener("click", () => {
    if (!tipoServico.value) {
        mostrarNotificacao("Selecione o tipo de serviço primeiro.", "aviso");
        return;
    }

    abrirModalBusca({
        titulo: `Buscar ${opcaoTiposServico[tipoServico.value]}`,
        placeholder: `Buscar ${opcaoTiposServico[tipoServico.value]} por nome`,
        url: "/dashboard/servicos/buscar/",
        parametros: {
            tipo: tipoServico.value,
        },
        rotulo: (servico) => servico.nome,
        aoConfirmar: (servico) => {
            nomeServico.value = servico.nome;
            idServico.value = servico.id;
        },
    });
});

/* =========================================================
   SELECIONAR PROFISSIONAL
========================================================= */

btnBuscarProfissional.addEventListener("click", () => {
    abrirModalBusca({
        titulo: "Buscar voluntário",
        placeholder: "Buscar voluntário por nome",
        url: "/dashboard/profissionais/buscar/",
        rotulo: (profissional) => profissional.nome,
        aoConfirmar: (profissional) => {
            idProfissional.value = profissional.id;
            nomeProfissional.value = profissional.nome;
            btnLimparProfissional.hidden = !idProfissional.value;
            btnLimparProfissional.disabled = !idProfissional.value;
        },
    });
});
