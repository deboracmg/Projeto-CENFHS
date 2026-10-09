const modalTratamento = document.getElementById("modalTratamento");
const modalBodyTratamento = document.querySelector(".modal-body.tratamento");
const formTratamento = document.getElementById("formTratamento");
const camposTratamento = formTratamento.querySelectorAll(
    "input, select, textarea",
);

const sectionAvaliacao = document.getElementById("avaliacao");
const camposAvaliacao = sectionAvaliacao.querySelectorAll(
    "input, select, textarea",
);

const tituloModalTratamento = document.getElementById("tituloModalTratamento");
const subtituloModalTratamento = document.getElementById(
    "subtituloModalTratamento",
);
const telefoneAcompanhante = document.getElementById("telefone_acompanhante");
const nSessoes = document.getElementById("n_sessoes");

const btnAdicionarTratamento = document.getElementById(
    "btnAdicionarTratamento",
);
const btnConcluirAvaliar = document.getElementById("btnConcluirAvaliar");
const btnEditarTratamento = document.getElementById("btnEditarTratamento");
const btnFecharTratamento = document.getElementById("btnFecharTratamento");
const btnSalvarTratamento = document.getElementById("btnSalvarTratamento");

function habilitarCamposTratamento() {
    camposTratamento.forEach((campo) => {
        campo.disabled = false;
    });

    btnSalvarTratamento.disabled = false;
}

function desabilitarCamposTratamento() {
    camposTratamento.forEach((campo) => {
        campo.disabled = true;
    });

    btnSalvarTratamento.disabled = true;
}

function exigirCamposAvaliacao() {
    camposAvaliacao.forEach((campo) => {
        campo.required = true;
    });
}

function dispensarCamposAvaliacao() {
    camposAvaliacao.forEach((campo) => {
        campo.required = false;
    });
}

btnEditarTratamento.addEventListener("click", () => {
    habilitarCamposTratamento();
    btnEditarTratamento.disabled = true;

    tituloModalTratamento.textContent = "Editando dados do tratamento";
});

btnConcluirAvaliar.addEventListener("click", () => {
    document.getElementById("data_saida").value = preencherDataAtual();
    exibirNotificacao("Salve o cadastro para efetuar a conclusão.", "info");
    document.getElementById("avaliacao").classList.add("active");
    document.getElementById("data_avaliacao").textContent = "-- / -- / ----";

    modalBodyTratamento.scrollTo({
        top: modalBodyTratamento.scrollHeight,
        behavior: "smooth",
    });
    exigirCamposAvaliacao();
    habilitarCamposTratamento();
});

async function formNovoTratamento() {
    const idPacienteReferencia = document.getElementById("paciente_id").value;
    let notificacao = "";
    if (!idPacienteReferencia) {
        const mensagem =
            "Para adicionar um tratamento, é necessário salvar o paciente primeiro. Deseja salvá-lo agora?";
        const confirmacao = await pedirConfirmacao(mensagem);
        if (!confirmacao) return;

        const salvou = await salvarPaciente();
        if (!salvou || !salvou.sucesso) return;

        tituloModalPaciente.textContent = "Editando dados do paciente";
        subtituloModalPaciente.textContent =
            "Código: " + document.getElementById("paciente_id").value;

        notificacao = salvou.mensagem;
    }

    modalTratamento.showModal();
    if (notificacao) exibirNotificacao(notificacao, "sucesso");
    
    formTratamento.reset();
    formTratamento.classList.remove("com-erro");
    document.getElementById("tratamento_id").value = "";
    document.getElementById("data_cadastro").textContent =
        formatarData(preencherDataAtual());
    document.getElementById("data_entrada").value = preencherDataAtual();

    tituloModalTratamento.textContent = "Cadastrar novo tratamento";
    subtituloModalTratamento.textContent = "Preencha os dados abaixo";

    btnConcluirAvaliar.disabled = true;
    btnEditarTratamento.disabled = true;

    dispensarCamposAvaliacao();
    habilitarCamposTratamento();
}

btnAdicionarTratamento.addEventListener("click", formNovoTratamento);

/* =========================================================
   DETALHAR TRATAMENTO
========================================================= */
function detalharTratamento(tratamento) {
    preencherFormularioTratamento(tratamento);
    tituloModalTratamento.textContent = "Dados do tratamento";
    subtituloModalTratamento.textContent =
        "Código: " + tratamento.tratamento_id;

    if (tratamento.avaliacao_id) {
        document.getElementById("avaliacao").classList.add("active");
        btnConcluirAvaliar.disabled = true;
        exigirCamposAvaliacao();
    } else {
        document.getElementById("avaliacao").classList.remove("active");
        btnConcluirAvaliar.disabled = false;
        dispensarCamposAvaliacao();
    }

    desabilitarCamposTratamento();
    btnEditarTratamento.disabled = false;
    modalTratamento.showModal();
}

function preencherFormularioTratamento(tratamento) {
    document.getElementById("tratamento_id").value =
        tratamento.tratamento_id || "";
    document.getElementById("data_entrada").value =
        tratamento.data_entrada || "";
    document.getElementById("data_saida").value = tratamento.data_saida || "";
    document.getElementById("tipo_paciente").value =
        tratamento.tipo_paciente || "";
    document.getElementById("tratamento").value = tratamento.tratamento || "";
    document.getElementById("n_sessoes").value = tratamento.n_sessoes || "";
    document.getElementById("acompanhante").value =
        tratamento.acompanhante || "";
    document.getElementById("telefone_acompanhante").value =
        tratamento.telefone_acompanhante || "";
    document.getElementById("registrado_por").value =
        tratamento.registrado_por || "";
    document.getElementById("observacoes").value = tratamento.observacoes || "";

    // Avaliação
    document.getElementById("avaliacao_id").value =
        tratamento.avaliacao_id || "";
    document.getElementById("atendimento").value = tratamento.atendimento || "";
    document.getElementById("infraestrutura").value =
        tratamento.infraestrutura || "";
    document.getElementById("higiene").value = tratamento.higiene || "";
    document.getElementById("alimentacao").value = tratamento.alimentacao || "";
    document.getElementById("comunicacao").value = tratamento.comunicacao || "";
    document.getElementById("acolhimento").value = tratamento.acolhimento || "";
    document.getElementById("organizacao").value = tratamento.organizacao || "";
    document.getElementById("gestao").value = tratamento.gestao || "";
    document.getElementById("data_avaliacao").textContent =
        tratamento.data_avaliacao || "";
    document.getElementById("avaliacao_media").textContent = "---";

    if (tratamento.avaliacao_id) {
        const resultado = calcularMedia(tratamento);
        document.getElementById("avaliacao_media").textContent =
            `${resultado[0]} - ${resultado[1]}`;
    }
}

function calcularMedia(tratamento) {
    const notas = [
        tratamento.atendimento,
        tratamento.infraestrutura,
        tratamento.higiene,
        tratamento.alimentacao,
        tratamento.comunicacao,
        tratamento.acolhimento,
        tratamento.organizacao,
        tratamento.gestao,
    ];
    const media = notas.reduce((soma, num) => soma + num, 0) / notas.length;
    const mediaRound = Math.round(media);
    const opcoesAvaliacao = {
        5: "Ótimo",
        4: "Bom",
        3: "Regular",
        2: "Ruim",
        1: "Insatisfeito",
    };

    return [media.toFixed(2), opcoesAvaliacao[mediaRound]];
}

/* =========================================================
   VALIDAÇÃO DE CAMPOS
========================================================= */
telefoneAcompanhante.addEventListener("input", (e) => {
    e.target.value = formatarCampoTelefone(e);
});

nSessoes.addEventListener("input", (e) => {
    e.target.value = permitirApenasNumeros(e);
});

/* =========================================================
   SALVAR CADASTRO
========================================================= */
formTratamento.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();

        formTratamento.classList.remove("com-erro");
        checarFormulário(formTratamento);

        const url = "/dashboard/tratamentos/salvar/";
        const formData = new FormData(formTratamento);
        formData.append(
            "paciente_id",
            document.getElementById("paciente_id").value,
        );

        const dados = await salvarCadastro(url, formData);

        modalTratamento.close();
        exibirTratamentos(dados.paciente_id, dados.tratamentos);
        exibirNotificacao(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});

btnFecharTratamento.addEventListener("click", () => modalTratamento.close());
