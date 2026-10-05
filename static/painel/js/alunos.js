const btnNovoAluno = document.getElementById("btnNovoCadastro");
const alunoModal = document.getElementById("alunoModal");
const modalBody = document.querySelector(".modal-body");

const btnFecharModal = document.getElementById("btnFecharModal");
const btnFecharModalFooter = document.getElementById("btnFecharModalFooter");

const btnEditar = document.getElementById("btnEditar");
const btnSalvar = document.getElementById("btnSalvar");
const btnsDetalharAluno = document.querySelectorAll(".btn-abrir-aluno");

const alunoForm = document.getElementById("alunoForm");
const formFields = alunoForm.querySelectorAll("input, select, textarea");

const modalTitulo = document.getElementById("modalTitulo");
const modalSubtitulo = document.getElementById("modalSubtitulo");
const previewPhoto = document.querySelector(".photo-preview");
const familiaBody = document.getElementById("familiaBody");
const campoCpf = document.getElementById("cpf");
const campoTelefone = document.getElementById("telefone");
const campoRendaFamiliar = document.getElementById("renda_familiar");
const campoQtdMoradores = document.getElementById("qtd_moradores");
const campoNBolsaFamilia = document.getElementById("n_bolsa_familia");
const campoNis = document.getElementById("nis");
const campoSus = document.getElementById("sus");

const campoCep = document.getElementById("cep");
const campoRua = document.getElementById("rua");
const campoBairro = document.getElementById("bairro");
const campoNumero = document.getElementById("numero");
const campoCidade = document.getElementById("cidade");
const campoUf = document.getElementById("uf");

const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");

btnsDetalharAluno.forEach((button) => {
    button.addEventListener("click", async () => {
        const alunoId = button.dataset.alunoId;
        const response = await fetch(`/dashboard/alunos/${alunoId}`);

        if (!response.ok) {
            console.error("Erro ao buscar aluno.");
            return;
        }

        const aluno = await response.json();
        detalharAluno(aluno);
    });
});

/* =========================================================
   ABAS
========================================================= */

tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const tabId = button.dataset.tab;

        tabButtons.forEach((item) => {
            item.classList.remove("active");
        });

        tabContents.forEach((content) => {
            content.classList.remove("active");
        });

        button.classList.add("active");
        document.getElementById(tabId).classList.add("active");
        modalBody.scrollTo(0, 0);
    });
});

/* =========================================================
   CAMPOS
========================================================= */

function habilitarCampos() {
    formFields.forEach((field) => {
        field.disabled = false;
    });

    btnSalvar.disabled = false;
    document.getElementById("btnAdicionarFamiliar").disabled = false;
    document.querySelectorAll(".btn-abrir-parente").forEach((button) => {
        button.disabled = false;
    });

    const btnRemoverFoto = document.getElementById("btnRemoverFoto");
    if (btnRemoverFoto) {
        btnRemoverFoto.disabled = false;
    }
}

function desabilitarCampos() {
    formFields.forEach((field) => {
        field.disabled = true;
    });

    btnSalvar.disabled = true;
    document.getElementById("btnAdicionarFamiliar").disabled = true;
    document.querySelectorAll(".btn-abrir-parente").forEach((button) => {
        button.disabled = true;
    });

    const btnRemoverFoto = document.getElementById("btnRemoverFoto");
    if (btnRemoverFoto) {
        btnRemoverFoto.disabled = true;
    }
}

/* =========================================================
   NOVO ALUNO
========================================================= */

function formNovoAluno() {
    alunoModal.showModal();
    alunoForm.reset();
    if (alunoForm.classList.contains("com-erro")) {
        alunoForm.classList.remove("com-erro");
    }
    modalBody.scrollTo(0, 0);

    modalTitulo.textContent = "Cadastrar novo aluno";
    modalSubtitulo.textContent = "Preencha os dados abaixo";
    document.getElementById("aluno_id").value = "";
    document.getElementById("data_cadastro").textContent = "-- / -- / ----";
    document.getElementById("remover_foto").value = "false";
    previewPhoto.innerHTML = `
        <i class="fa-solid fa-camera"></i>
        <span class="photo-label">Foto do aluno</span>
    `;
    familiaBody.innerHTML = `
    <tr>
        <td colspan="5" class="empty-message">
            Nenhum familiar cadastrado.
        </td>
    </tr>
    `;

    btnEditar.disabled = true;

    habilitarCampos();
    abrirAbaInicial();
}

btnNovoAluno.addEventListener("click", formNovoAluno);

/* =========================================================
   VISUALIZAR ALUNO
========================================================= */

function detalharAluno(aluno) {
    preencherFormulario(aluno);
    modalTitulo.textContent = "Dados do aluno";
    modalSubtitulo.textContent = "Código: " + aluno.id;

    desabilitarCampos();
    btnEditar.disabled = false;
    abrirAbaInicial();

    alunoModal.showModal();
}

/* =========================================================
   PREENCHER FORMULÁRIO
========================================================= */

function preencherFormulario(aluno) {
    document.getElementById("aluno_id").value = aluno.id || "";
    document.getElementById("nome").value = aluno.nome || "";
    document.getElementById("cpf").value = aluno.cpf || "";
    document.getElementById("rg").value = aluno.rg || "";
    document.getElementById("data_nascimento").value =
        aluno.data_nascimento || "";
    document.getElementById("naturalidade").value = aluno.naturalidade || "";
    document.getElementById("genero").value = aluno.genero || "";
    document.getElementById("raca").value = aluno.raca || "";
    document.getElementById("n_certidao").value = aluno.n_certidao || "";
    document.getElementById("telefone").value = aluno.telefone || "";
    document.getElementById("email").value = aluno.email || "";
    document.getElementById("observacoes").value = aluno.observacoes || "";
    document.getElementById("autoriza_uso_imagem").checked =
        aluno.autoriza_uso_imagem || false;
    document.getElementById("data_cadastro").textContent =
        aluno.data_cadastro || "";

    preencherPreviewFoto(aluno.foto);

    /* Endereço */
    document.getElementById("cep").value = aluno.cep || "";
    document.getElementById("rua").value = aluno.rua || "";
    document.getElementById("numero").value = aluno.numero || "";
    document.getElementById("bairro").value = aluno.bairro || "";
    document.getElementById("cidade").value = aluno.cidade || "";
    document.getElementById("uf").value = aluno.uf || "";
    document.getElementById("zona").value = aluno.zona || "";

    /* Saúde */
    document.getElementById("sus").value = aluno.saude?.sus || "";
    document.getElementById("problema_saude").value =
        aluno.saude?.problema_saude || "";
    document.getElementById("tratamento").value = aluno.saude?.tratamento || "";
    document.getElementById("tipo_sanguineo").value =
        aluno.saude?.tipo_sanguineo || "";
    document.getElementById("alergia").value = aluno.saude?.alergia || "";
    document.getElementById("medicamento").value =
        aluno.saude?.medicamento || "";
    document.getElementById("vacinas").value = aluno.saude?.vacinas || "";

    /* Socioeconômico */
    document.getElementById("n_bolsa_familia").value =
        aluno.socioeconomico?.n_bolsa_familia || "";
    document.getElementById("nis").value = aluno.socioeconomico?.nis || "";
    document.getElementById("escola").value =
        aluno.socioeconomico?.escola || "";
    document.getElementById("transporte").value =
        aluno.socioeconomico?.transporte || "";
    document.getElementById("renda_familiar").value =
        aluno.socioeconomico?.renda_familiar || "";
    document.getElementById("situacao_moradia").value =
        aluno.socioeconomico?.situacao_moradia || "";
    document.getElementById("qtd_moradores").value =
        aluno.socioeconomico?.qtd_moradores || "";

    exibirFamilia(aluno.id, aluno.familia);
}

function preencherPreviewFoto(url) {
    if (!url) {
        previewPhoto.innerHTML = `
            <i class="fa-solid fa-camera"></i>
            <span class="photo-label">Foto do aluno</span>
        `;
        return;
    }

    previewPhoto.innerHTML = `
        <img src="${url}" alt="Foto do aluno">
        <button
            type="button"
            class="btn-remover-foto"
            id="btnRemoverFoto"
            title="Remover foto"
        >
            <i class="fa-regular fa-trash-can"></i>
        </button>
    `;

    document.getElementById("btnRemoverFoto").addEventListener("click", () => {
        document.getElementById("remover_foto").value = "true";
        document.getElementById("foto").value = "";

        preencherPreviewFoto(null);
    });
}

const inputFoto = document.getElementById("foto");
inputFoto.addEventListener("change", () => {
    if (!inputFoto.files[0]) return;

    const url = URL.createObjectURL(inputFoto.files[0]);
    preencherPreviewFoto(url);

    document.getElementById("remover_foto").value = "false";
});

function exibirFamilia(aluno_id, familia) {
    if (!familia.length) {
        familiaBody.innerHTML = `
        <tr>
            <td colspan="5" class="empty-message">
                Nenhum familiar cadastrado.
            </td>
        </tr>
        `;
        return;
    }

    function checkOrSquare(condicao) {
        if (condicao) {
            return '<i class="fa-solid fa-square-check"></i>';
        }
        return '<i class="fa-regular fa-square"></i>';
    }

    let contentFamily = "";
    familia.forEach((f, index) => {
        contentFamily += `
            <tr data-parente-id="${f.id}">
                <td>${f.parentesco}</td>
                <td>${f.nome}</td>
                <td class="centralize-content">${checkOrSquare(f.responsavel)}</td>
                <td class="centralize-content">${checkOrSquare(f.contato_emergencia)}</td>
                <td class="centralize-button">    
                    <button
                        type="button"
                        class="action-button btn-abrir-parente"
                        data-index=${index}
                        title="Mais informações">

                        <i class="fa-solid fa-circle-info"></i>
                    </button>
                </td>
            </tr>
        `;
    });

    familiaBody.innerHTML = contentFamily;

    document.querySelectorAll(".btn-abrir-parente").forEach((button) => {
        button.addEventListener("click", async () => {
            const index = button.dataset.index;
            const parente = familia[index];
            detalharParente(aluno_id, parente);
        });
    });
}

/* =========================================================
   ABA INICIAL
========================================================= */

function abrirAbaInicial() {
    tabButtons.forEach((button) => {
        button.classList.remove("active");
    });

    tabContents.forEach((content) => {
        content.classList.remove("active");
    });

    document
        .querySelector('[data-tab="dados-pessoais"]')
        .classList.add("active");

    document.getElementById("dados-pessoais").classList.add("active");
}

/* =========================================================
   EDITAR
========================================================= */

btnEditar.addEventListener("click", () => {
    habilitarCampos();
    btnEditar.disabled = true;

    modalTitulo.textContent = "Editando dados do aluno";
});

/* =========================================================
   VALIDAÇÃO DE CAMPOS
   ========================================================= */
campoCep.addEventListener("input", function (e) {
    e.target.value = formatarCampoCep(e);
    campoCep.setCustomValidity("");
});

campoCep.addEventListener("blur", async () => {
    preencherEnderecoAutomaticamente(campoCep.value, {
        "cep": campoCep,
        "rua": campoRua,
        "bairro": campoBairro,
        "numero": campoNumero,
        "cidade": campoCidade,
        "uf": campoUf,
    })
});

campoRendaFamiliar.addEventListener("input", function (e) {
    e.target.value = permitirApenasNumeros(e);
});

campoQtdMoradores.addEventListener("input", function (e) {
    e.target.value = permitirApenasNumeros(e);
});

campoSus.addEventListener("input", function (e) {
    e.target.value = permitirApenasNumeros(e);
});

campoNBolsaFamilia.addEventListener("input", function (e) {
    e.target.value = permitirApenasNumeros(e);
});

campoNis.addEventListener("input", function (e) {
    e.target.value = permitirApenasNumeros(e);
});

campoTelefone.addEventListener("input", function (e) {
    e.target.value = formatarCampoTelefone(e);
});

campoCpf.addEventListener("input", function (e) {
    e.target.value = formatarCampoCpf(e);
    campoCpf.setCustomValidity("");
});

/* =========================================================
   SALVAR CADASTRO
========================================================= */

async function salvarAluno() {
    if (!alunoForm.checkValidity()) {
        alunoForm.classList.add("com-erro");
        exibirNotificacao("Preencha todos os campos obrigatórios", "info");
        return null;
    }

    if (!validarCPF(campoCpf.value)) {
        campoCpf.setCustomValidity("CPF inválido");
        exibirNotificacao("CPF inválido. Verifique o CPF informado.", "erro");
        return null;
    }

    if (campoCep.value.length != 9) {
        campoCep.setCustomValidity("CEP inválido");
        exibirNotificacao("O CEP deve conter exatamente 8 números.", "erro");
        return null;
    }

    const formData = new FormData(alunoForm);
    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]",
    ).value;

    const response = await fetch("/dashboard/alunos/salvar/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: formData,
    });

    const dados = await response.json();

    if (!response.ok) {
        console.error(dados);
        return dados;
    }

    document.getElementById("aluno_id").value = dados.id;
    return dados;
}

alunoForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const salvou = await salvarAluno();
    if (salvou && salvou.sucesso) {
        salvarNotificacaoERecarregar(salvou.mensagem, "sucesso");
    }
});

/* =========================================================
   FECHAR
========================================================= */

btnFecharModal.addEventListener("click", () => alunoModal.close());
