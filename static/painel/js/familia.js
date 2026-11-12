const modalFamiliar = document.getElementById("modalSecundario");
const formFamiliar = modalFamiliar.querySelector("#formFamiliar");
const camposFamiliar = formFamiliar.querySelectorAll("input, select");

const tituloModalFamiliar = modalFamiliar.querySelector("#tituloModal");
const subtituloModalFamiliar = modalFamiliar.querySelector("#subtituloModal");
const cpfFamiliar = modalFamiliar.querySelector("#cpf_familiar");
const telefoneFamiliar = modalFamiliar.querySelector("#telefone_familiar");

const btnAdicionarFamiliar = document.getElementById("btnAdicionarFamiliar");
const btnExcluirFamiliar = modalFamiliar.querySelector("#btnExcluir");
const btnEditarFamiliar = modalFamiliar.querySelector("#btnEditar");
const btnFecharFamiliar = modalFamiliar.querySelector("#btnFechar");
const btnSalvarFamiliar = modalFamiliar.querySelector("#btnSalvar");

btnEditarFamiliar.addEventListener("click", () => {
    habilitarEdicaoFormulario(modalFamiliar);
    tituloModalFamiliar.textContent = "Editando dados do familiar";
});

btnAdicionarFamiliar.addEventListener("click", async () => {
    const dados = await verificarESalvarCadastroRelacionado(
        "familiar",
        "aluno",
        salvarAluno,
        modalAluno,
    );

    if (!dados) return;

    btnExcluirFamiliar.disabled = true;
    formNovoCadastro(modalFamiliar, "Cadastrar novo familiar");
    
    if (dados.mensagem) exibirNotificacao(dados.mensagem, "sucesso");
});

/* =========================================================
   DETALHAR CADASTRO
========================================================= */

function detalharFamiliar(aluno_id, familiar) {
    preencherFormularioFamiliar(familiar);
    tituloModalFamiliar.textContent = "Dados do familiar";
    subtituloModalFamiliar.textContent = "Código: " + familiar.familiar_id;

    desabilitarEdicaoFormulario(modalFamiliar);
    btnExcluirFamiliar.disabled = false;
    btnExcluirFamiliar.dataset.familiarId = familiar.familiar_id;
    btnExcluirFamiliar.dataset.alunoId = aluno_id;

    modalFamiliar.showModal();
}

function preencherFormularioFamiliar(familiar) {
    document.getElementById("familiar_id").value = familiar.familiar_id || "";
    document.getElementById("cpf_familiar").value = familiar.cpf || "";
    document.getElementById("nome_familiar").value = familiar.nome || "";
    document.getElementById("telefone_familiar").value =
        familiar.telefone || "";
    document.getElementById("profissao_familiar").value =
        familiar.profissao || "";
    document.getElementById("local_trabalho").value =
        familiar.local_trabalho || "";
    document.getElementById("escolaridade_familiar").value =
        familiar.escolaridade || "";
    document.getElementById("parentesco_id").value =
        familiar.parentesco_id || "";
    document.getElementById("parentesco").value = familiar.parentesco || "";
    document.getElementById("familiar_vivo").checked = familiar.vivo || false;
    document.getElementById("familiar_responsavel").checked =
        familiar.responsavel || false;
    document.getElementById("familiar_emergencia").checked =
        familiar.contato_emergencia || false;
}

async function buscarFamiliarPorCpf() {
    const cpf = cpfFamiliar.value;
    if (!cpf) return;

    const params = new URLSearchParams({ cpf: cpf });
    const resposta = await fetch(
        `/dashboard/familiar/buscar-por-cpf/?${params}`,
    );

    const dados = await resposta.json();
    if (dados.encontrado) {
        preencherFormularioFamiliar(dados.familiar);
    }
}

/* =========================================================
   VALIDAÇÃO DE CAMPOS
========================================================= */

cpfFamiliar.addEventListener("input", function (e) {
    e.target.value = formatarCampoCpf(e, cpfFamiliar);
});

cpfFamiliar.addEventListener("blur", buscarFamiliarPorCpf);

telefoneFamiliar.addEventListener("input", function (e) {
    e.target.value = formatarCampoTelefone(e);
});

/* =========================================================
   EXCLUIR CADASTRO
========================================================= */
btnExcluirFamiliar.addEventListener("click", async () => {
    const familiarId = btnExcluirFamiliar.dataset.familiarId;
    const alunoId = btnExcluirFamiliar.dataset.alunoId;

    await excluirRegistro({
        modal: modalFamiliar,
        mensagemConfirmacao: "Tem certeza que deseja excluir este familiar?",
        url: "/dashboard/familiar/excluir/",
        dados: {
            aluno_id: alunoId,
            familiar_id: familiarId,
        },
        aoExcluir: (dados) => {
            modalFamiliar.close();
            exibirFamilia(alunoId, dados.familia);
        },
    });
});

/* =========================================================
   SALVAR CADASTRO
========================================================= */

formFamiliar.addEventListener("submit", async (event) => {
    try {
        event.preventDefault();

        formFamiliar.classList.remove("com-erro");
        cpfFamiliar.setCustomValidity("");

        checarFormulario(formFamiliar);
        checarCpf(cpfFamiliar, formFamiliar);

        const url = "/dashboard/familiar/salvar/";
        const formData = new FormData(formFamiliar);
        formData.append("aluno_id", document.getElementById("aluno_id").value);

        const dados = await salvarCadastro(url, formData);

        modalFamiliar.close();
        exibirFamilia(dados.aluno_id, dados.familia);
        exibirNotificacao(dados.mensagem, "sucesso");
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
    }
});

btnFecharFamiliar.addEventListener("click", () => modalFamiliar.close());
