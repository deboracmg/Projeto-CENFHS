const btnNovoPaciente = document.getElementById("btnNovoCadastro");
const modalPaciente = document.getElementById("pacienteModal");
const modalBodyPaciente = document.querySelector(".modal-body");
const tratamentoBody = document.getElementById("tratamentoBody");

const formPaciente = document.getElementById("formPaciente");
const camposPaciente = formPaciente.querySelectorAll("input, select");

const tituloModalPaciente = document.getElementById("tituloModal");
const subtituloModalPaciente = document.getElementById("subtituloModal");
const cpfPaciente = document.getElementById("cpf");
const telefonePaciente = document.getElementById("telefone");

const btnEditarPaciente = document.getElementById("btnEditar");
const btnSalvarPaciente = document.getElementById("btnSalvar");
const btnFecharPaciente = document.getElementById("btnFechar");
const btnsDetalharPaciente = document.querySelectorAll(".btn-abrir-paciente");

const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");

tabButtons.forEach((button) => {
    gerenciarAbas(button, tabButtons, tabContents, modalBodyPaciente)
});

btnsDetalharPaciente.forEach((button) => {
    button.addEventListener("click", async () => {
        const pacienteId = button.dataset.pacienteId;
        const response = await fetch(`/dashboard/pacientes/${pacienteId}`);

        if (!response.ok) {
            console.error("Erro ao buscar paciente.");
            return;
        }

        const paciente = await response.json();
        detalharPaciente(paciente);
    });
});

btnEditarPaciente.addEventListener("click", () => {
    habilitarCamposPaciente();
    btnEditarPaciente.disabled = true;

    tituloModalPaciente.textContent = "Editando dados do paciente";
});

function desabilitarCamposPaciente() {
    camposPaciente.forEach(campo => {
        campo.disabled = true;
    });

    btnSalvarPaciente.disabled = true;
    document.getElementById("btnAdicionarTratamento").disabled = true;
    document.querySelectorAll(".btn-abrir-tratamento").forEach((button) => {
        button.disabled = true;
    });
}

function habilitarCamposPaciente() {
    camposPaciente.forEach((campo) => {
        campo.disabled = false;
    });

    btnSalvarPaciente.disabled = false;
    document.getElementById("btnAdicionarTratamento").disabled = false;
    document.querySelectorAll(".btn-abrir-tratamento").forEach((button) => {
        button.disabled = false;
    });
}

function formNovoPaciente() {
    modalPaciente.showModal();
    formPaciente.reset();
    formPaciente.classList.remove("com-erro");
    modalBodyPaciente.scrollTo(0, 0);

    tituloModalPaciente.textContent = "Cadastrar novo paciente";
    subtituloModalPaciente.textContent = "Preencha os dados abaixo";
    document.getElementById("paciente_id").value = "";
    document.getElementById("data_cadastro").textContent = "-- / -- / ----";

    btnEditarPaciente.disabled = true;

    habilitarCamposPaciente();
    abrirAbaInicial(tabButtons, tabContents);
}

btnNovoPaciente.addEventListener("click", formNovoPaciente)
btnFecharPaciente.addEventListener("click", () => modalPaciente.close());

function detalharPaciente(paciente) {
    preencherFormularioPaciente(paciente);
    tituloModalPaciente.textContent = "Dados do paciente";
    subtituloModalPaciente.textContent = "Código: " + paciente.id;
    formPaciente.classList.remove("com-erro");

    desabilitarCamposPaciente();
    btnEditarPaciente.disabled = false;
    abrirAbaInicial(tabButtons, tabContents);

    modalPaciente.showModal();
}

function preencherFormularioPaciente(paciente) {
    document.getElementById("paciente_id").value = paciente.id || "";
    document.getElementById("cpf").value = paciente.cpf || "";
    document.getElementById("rg").value = paciente.rg || "";
    document.getElementById("nome").value = paciente.nome || "";
    document.getElementById("data_nascimento").value = paciente.data_nascimento || "";
    document.getElementById("naturalidade").value = paciente.naturalidade || "";
    document.getElementById("genero").value = paciente.genero || "";
    document.getElementById("telefone").value = paciente.telefone || "";
    document.getElementById("email").value = paciente.email || "";
    document.getElementById("nome_mae").value = paciente.nome_mae || "";
    document.getElementById("nome_pai").value = paciente.nome_pai || "";
    document.getElementById("profissao").value = paciente.profissao || "";
    document.getElementById("data_cadastro").textContent = paciente.data_cadastro || "";

    /* Endereço */
    document.getElementById("cep").value = paciente.cep || "";
    document.getElementById("rua").value = paciente.rua || "";
    document.getElementById("numero").value = paciente.numero || "";
    document.getElementById("bairro").value = paciente.bairro || "";
    document.getElementById("cidade").value = paciente.cidade || "";
    document.getElementById("uf").value = paciente.uf || "";

    exibirTratamentos(paciente.id, paciente.tratamentos)
}

function exibirTratamentos(paciente_id, tratamentos) {
    if (!tratamentos.length) {
        tratamentoBody.innerHTML = `
        <tr>
            <td colspan="5" class="empty-message">
                Nenhum tratamento cadastrado.
            </td>
        </tr>
        `;
        return;
    }

    function formatarData(data) {
        if (!data) return "-";
        const [ano, mes, dia] = data.split("-");
        return `${dia}/${mes}/${ano}`;
    }

    let contentTratament = "";
    tratamentos.forEach((t, index) => {
        contentTratament += `
            <tr data-tratamento-id="${t.id}">
                <td>${formatarData(t.data_entrada)}</td>
                <td>${formatarData(t.data_saida)}</td>
                <td>${t.tratamento}</td>
                <td>${t.n_sessoes}</td>
                <td class="centralize-button">    
                    <button
                        type="button"
                        class="action-button btn-abrir-tratamento"
                        data-index=${index}
                        title="Mais informações">

                        <i class="fa-solid fa-circle-info"></i>
                    </button>
                </td>
            </tr>
        `;
    });

    tratamentoBody.innerHTML = contentTratament;

    document.querySelectorAll(".btn-abrir-tratamento").forEach((button) => {
        button.addEventListener("click", async () => {
            const index = button.dataset.index;
            const paciente = tratamentos[index];
            // detalharTratamento(paciente_id, paciente);
        });
    });
}

/* =========================================================
   VALIDAÇÃO DE CAMPOS
========================================================= */

cpfPaciente.addEventListener("input", function (e) {
    e.target.value = formatarCampoCpf(e);
    cpfPaciente.setCustomValidity("");
});

telefonePaciente.addEventListener("input", function (e) {
    e.target.value = formatarCampoTelefone(e);
}); 

/* =========================================================
   SALVAR CADASTRO
========================================================= */

formPaciente.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();

        cpfPaciente.setCustomValidity("");
        formPaciente.classList.remove("com-erro");
        
        checarFormulário(formPaciente);
        checarCpf(cpfPaciente, formPaciente);

        const url = "/dashboard/pacientes/salvar/";
        const formData = new FormData(formPaciente);
        const dados = await salvarCadastro(url, formData);

        modalPaciente.close();
        exibirNotificacaoComReload(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});
