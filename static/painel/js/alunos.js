const modalAluno = document.getElementById("modalPrimario");
const familiaBody = modalAluno.querySelector("#familiaBody");

const btnNovoAluno = document.getElementById("btnNovoCadastro");
const btnFecharAluno = modalAluno.querySelector("#btnFechar");
const btnEditarAluno = modalAluno.querySelector("#btnEditar");
const btnSalvarAluno = modalAluno.querySelector("#btnSalvar");
const btnsDetalharAluno = document.querySelectorAll(".btn-abrir-aluno");

const formAluno = document.getElementById("formAluno");
const camposAluno = formAluno.querySelectorAll("input, select, textarea");

const tituloModalAluno = modalAluno.querySelector("#tituloModal");
const subtituloModalAluno = modalAluno.querySelector("#subtituloModal");
const previewPhoto = modalAluno.querySelector(".photo-preview");
const campoCpf = modalAluno.querySelector("#cpf");
const campoTelefone = modalAluno.querySelector("#telefone");
const campoRendaFamiliar = modalAluno.querySelector("#renda_familiar");
const campoQtdMoradores = modalAluno.querySelector("#qtd_moradores");
const campoNBolsaFamilia = modalAluno.querySelector("#n_bolsa_familia");
const campoNis = modalAluno.querySelector("#nis");
const campoSus = modalAluno.querySelector("#sus");

const campoCep = modalAluno.querySelector("#cep");
const campoRua = modalAluno.querySelector("#rua");
const campoBairro = modalAluno.querySelector("#bairro");
const campoNumero = modalAluno.querySelector("#numero");
const campoCidade = modalAluno.querySelector("#cidade");
const campoUf = modalAluno.querySelector("#uf");

const tabButtons = modalAluno.querySelectorAll(".tab-button");

tabButtons.forEach((button) => {
    gerenciarAbas(modalAluno, button);
});

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
   NOVO ALUNO
========================================================= */

btnNovoAluno.addEventListener("click", () => {
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
    
    formNovoCadastro(modalAluno, "Cadastrar novo aluno");
});

/* =========================================================
   VISUALIZAR ALUNO
========================================================= */

function detalharAluno(aluno) {
    preencherFormulario(aluno);
    tituloModalAluno.textContent = "Dados do aluno";
    subtituloModalAluno.textContent = "Código: " + aluno.id;
    formAluno.classList.remove("com-erro");

    modalAluno.showModal();
    abrirAbaInicial(modalAluno);
    desabilitarEdicaoFormulario(modalAluno);
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

    const data = converterDataHora(aluno.data_cadastro);
    document.getElementById("data_cadastro").textContent = data.split(", ").join(" - ");

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
            detalharFamiliar(aluno_id, parente);
        });
    });
}

/* =========================================================
   EDITAR
========================================================= */

btnEditarAluno.addEventListener("click", () => {
    habilitarEdicaoFormulario(modalAluno);
    tituloModalAluno.textContent = "Editando dados do aluno";
});

/* =========================================================
   VALIDAÇÃO DE CAMPOS
   ========================================================= */
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

campoRendaFamiliar.addEventListener("input", (e) => {
    e.target.value = permitirApenasNumeros(e);
});

campoQtdMoradores.addEventListener("input", (e) => {
    e.target.value = permitirApenasNumeros(e);
});

campoSus.addEventListener("input", (e) => {
    e.target.value = permitirApenasNumeros(e);
});

campoNBolsaFamilia.addEventListener("input", (e) => {
    e.target.value = permitirApenasNumeros(e);
});

campoNis.addEventListener("input", (e) => {
    e.target.value = permitirApenasNumeros(e);
});

campoTelefone.addEventListener("input", (e) => {
    e.target.value = formatarCampoTelefone(e);
});

campoCpf.addEventListener("input", (e) => {
    e.target.value = formatarCampoCpf(e);
    campoCpf.setCustomValidity("");
});

/* =========================================================
   SALVAR CADASTRO
========================================================= */

async function salvarAluno() {
    try {
        campoCpf.setCustomValidity("");
        campoCep.setCustomValidity("");
        formAluno.classList.remove("com-erro");

        checarFormulário(formAluno);
        checarCpf(campoCpf, formAluno);
        checarCep(campoCep, formAluno);

        const dados = await salvarCadastro(
            "/dashboard/alunos/salvar/",
            new FormData(formAluno),
        );

        document.getElementById("aluno_id").value = dados.id;
        return dados;
    } catch (erro) {
        exibirNotificacao(erro.message, "erro");
        return null;
    }
}

formAluno.addEventListener("submit", async (event) => {
    event.preventDefault();
    const salvou = await salvarAluno();
    if (salvou && salvou.sucesso) {
        exibirNotificacaoComReload(salvou.mensagem, "sucesso");
    }
});

/* =========================================================
   FECHAR
========================================================= */

btnFecharAluno.addEventListener("click", () => modalAluno.close());
