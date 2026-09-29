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
    modalBody.scrollTo(0, 0);

    modalTitulo.textContent = "Cadastrar novo aluno";
    modalSubtitulo.textContent = "Preencha os dados abaixo";
    document.getElementById("data_cadastro").textContent = "-- / -- / ----";
    previewPhoto.innerHTML = `
        <i class="fa-solid fa-camera"></i>
        <span class="photo-label">Foto do aluno</span>
    `;

    btnEditar.disabled = true;
    btnSalvar.disabled = false;
    document.getElementById("remover_foto").value = "false";

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
    document.getElementById("data_nascimento").value =
        aluno.data_nascimento || "";
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

    preencherFamilia(aluno);
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

const inputFoto = document.getElementById("foto")
inputFoto.addEventListener("change", () => {
    if (!inputFoto.files[0]) return;

    const url = URL.createObjectURL(inputFoto.files[0]);
    preencherPreviewFoto(url);

    document.getElementById("remover_foto").value = "false";
});


function preencherFamilia(aluno) {
    document.getElementById("id_aluno_referencia").value = aluno.id || "";

    const familiaBody = document.getElementById("familiaBody");
    if (!aluno.familia.length) {
        familiaBody.innerHTML = `
        <tr>
            <td colspan="5" class="empty-message">
                Nenhum familiar cadastrado.
            </td>
        </tr>
        `
        return;
    }
    
    function checkOrSquare(condicao) {
        if (condicao) {
            return '<i class="fa-solid fa-square-check"></i>';
        }
        return '<i class="fa-regular fa-square"></i>';
    }

    let contentFamily = "";
    aluno.familia.forEach((f, index) => {
        contentFamily += `
            <tr>
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
    })

    familiaBody.innerHTML = contentFamily;

    document.querySelectorAll(".btn-abrir-parente").forEach((button) => {
        button.addEventListener("click", async () => {
            const index = button.dataset.index;
            const parente = aluno.familia[index];
            detalharFamiliar(parente);
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
   SALVAR CADASTRO
========================================================= */

alunoForm.addEventListener("submit", async (event) => {
    event.preventDefault();
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
        return;
    }

    console.log(dados.mensagem);
    alunoModal.close();
    window.location.reload();
});

/* =========================================================
   FECHAR
========================================================= */

function fecharModal() {
    alunoModal.close();
    alunoForm.reset();

    abrirAbaInicial();
}

btnFecharModal.addEventListener("click", fecharModal);
btnFecharModalFooter.addEventListener("click", fecharModal);
