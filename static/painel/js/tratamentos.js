const modalTratamento = document.getElementById("modalTratamento");
const formTratamento = document.getElementById("formTratamento");
const camposTratamento = formTratamento.querySelectorAll("input, select, textarea");

const tituloModalTratamento = document.getElementById("tituloModalTratamento");
const subtituloModalTratamento = document.getElementById(
    "subtituloModalTratamento",
);
const telefoneAcompanhante = document.getElementById("telefone_acompanhante");

const btnAdicionarTratamento = document.getElementById("btnAdicionarTratamento");
const btnFinalizarTratamento = document.getElementById("btnFinalizarTratamento");
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

async function formNovoTratamento() {
    // const idPacienteReferencia = document.getElementById("paciente_id").value;
    // if (!idPacienteReferencia) {
    //     const mensagem =
    //         "Para adicionar um tratamento, é necessário salvar o paciente primeiro. Deseja salvá-lo agora?";
    //     const confirmacao = await pedirConfirmacao(mensagem);
    //     if (!confirmacao) return;

    //     const salvou = await salvarPaciente();
    //     if (!salvou || !salvou.sucesso) return;
    //     exibirNotificacao(salvou.mensagem, "sucesso");

    //     tituloModalPaciente.textContent = "Editando dados do paciente";
    //     subtituloModalPaciente.textContent =
    //         "Código: " + document.getElementById("paciente_id").value;
    // }

    modalTratamento.showModal();
    formTratamento.reset();
    formTratamento.classList.remove("com-erro");
    document.getElementById("tratamento_id").value = "";

    tituloModalTratamento.textContent = "Cadastrar novo tratamento";
    subtituloModalTratamento.textContent = "Preencha os dados abaixo";

    btnFinalizarTratamento.disabled = true;
    btnEditarTratamento.disabled = true;
    btnSalvarTratamento.disabled = false;

    habilitarCamposTratamento();
}

btnAdicionarTratamento.addEventListener("click", formNovoTratamento);
