const modalPaciente = document.getElementById("modalPrimario");
const modalBodyPaciente = modalPaciente.querySelector(".modal-body");
const tratamentoBody = document.getElementById("tratamentoBody");

const formPaciente = document.getElementById("formPaciente");
const camposPaciente = formPaciente.querySelectorAll("input, select");

const tituloModalPaciente = modalPaciente.querySelector("#tituloModal");
const subtituloModalPaciente = modalPaciente.querySelector("#subtituloModal");

const campoCpf = modalPaciente.querySelector("#cpf");
const campoTelefone = modalPaciente.querySelector("#telefone");
const campoCep = modalPaciente.querySelector("#cep");
const campoRua = modalPaciente.querySelector("#rua");
const campoBairro = modalPaciente.querySelector("#bairro");
const campoNumero = modalPaciente.querySelector("#numero");
const campoCidade = modalPaciente.querySelector("#cidade");
const campoUf = modalPaciente.querySelector("#uf");

const btnNovoPaciente = document.getElementById("btnNovoCadastro");
const btnEditarPaciente = modalPaciente.querySelector("#btnEditar");
const btnSalvarPaciente = modalPaciente.querySelector("#btnSalvar");
const btnFecharPaciente = modalPaciente.querySelector("#btnFechar");
const btnsDetalharPaciente = document.querySelectorAll(".btn-abrir-paciente");

const tabButtons = document.querySelectorAll(".tab-button");

tabButtons.forEach((button) => {
    gerenciarAbas(modalPaciente, button)
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
    habilitarEdicaoFormulario(modalPaciente);
    tituloModalPaciente.textContent = "Editando dados do paciente";
});

btnNovoPaciente.addEventListener("click", () => {
    tratamentoBody.innerHTML = `
    <tr>
        <td colspan="5" class="empty-message">
            Nenhum tratamento cadastrado.
        </td>
    </tr>
    `;
    formNovoCadastro(modalPaciente, "Cadastrar novo paciente");
})
btnFecharPaciente.addEventListener("click", () => modalPaciente.close());

function detalharPaciente(paciente) {
    preencherFormularioPaciente(paciente);
    tituloModalPaciente.textContent = "Dados do paciente";
    subtituloModalPaciente.textContent = "Código: " + paciente.id;
    formPaciente.classList.remove("com-erro");

    modalPaciente.showModal();
    abrirAbaInicial(modalPaciente);
    desabilitarEdicaoFormulario(modalPaciente);
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

    const data = converterDataHora(paciente.data_cadastro);
    document.getElementById("data_cadastro").textContent = data.split(", ").join(" - ");

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
            const tratamento = tratamentos[index];
            detalharTratamento(tratamento);
        });
    });
}

/* =========================================================
   VALIDAÇÃO DE CAMPOS
========================================================= */

campoCpf.addEventListener("input", function (e) {
    e.target.value = formatarCampoCpf(e);
    campoCpf.setCustomValidity("");
});

campoTelefone.addEventListener("input", function (e) {
    e.target.value = formatarCampoTelefone(e);
});

campoCep.addEventListener("input", (e) => {
    e.target.value = formatarCampoCep(e);
    campoCep.setCustomValidity("");
});

campoCep.addEventListener("blur", async () => {
    preencherEnderecoAutomaticamente(campoCep.value, {
        cep: campoCep,
        rua: campoRua,
        bairro: campoBairro,
        numero: campoNumero,
        cidade: campoCidade,
        uf: campoUf,
    });
});

/* =========================================================
   SALVAR CADASTRO
========================================================= */

async function salvarPaciente() {
    try {
        campoCep.setCustomValidity("");
        campoCpf.setCustomValidity("");
        formPaciente.classList.remove("com-erro");
        
        checarFormulário(formPaciente);
        checarCpf(campoCpf, formPaciente);
        checarCep(campoCep, formPaciente);

        const url = "/dashboard/pacientes/salvar/";
        const formData = new FormData(formPaciente);
        const dados = await salvarCadastro(url, formData);

        document.getElementById("paciente_id").value = dados.id;
        return dados;
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
        return null;
    }
}

formPaciente.addEventListener("submit", async (event) => {
    event.preventDefault();
    const salvou = await salvarPaciente();
    if (salvou && salvou.sucesso) {
        exibirNotificacaoComReload(salvou.mensagem, "sucesso");
    }
});
