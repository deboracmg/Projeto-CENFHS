const modalUsuario = document.getElementById("modalPrimario");
const formUsuario = modalUsuario.querySelector("#formUsuario");
const btnNovoUsuario = document.getElementById("btnNovoCadastro");

const tituloModalUsuario = modalUsuario.querySelector("#tituloModal");
const subtituloModalUsuario = modalUsuario.querySelector("#subtituloModal");
const secaoSenhaTemporaria = modalUsuario.querySelector(
    "#secaoSenhaTemporaria",
);
const campoSenha = modalUsuario.querySelector("#senha");
const btnCopiarSenha = modalUsuario.querySelector("#btnCopiarSenha");
const campoIsStaff = modalUsuario.querySelector("#is_staff");
const campoAtivo = modalUsuario.querySelector("#ativo");

const btnExcluirUsuario = modalUsuario.querySelector("#btnExcluir");
const btnRedefinirSenha = modalUsuario.querySelector("#btnRedefinirSenha");
const btnEditarUsuario = modalUsuario.querySelector("#btnEditar");
const btnSalvarUsuario = modalUsuario.querySelector("#btnSalvar");
const btnFecharUsuario = modalUsuario.querySelector("#btnFechar");
const btnsDetalharUsuario = document.querySelectorAll(".btn-abrir-usuario");

function gerarSenhaTemporaria(tamanho = 8) {
    const maiusculas = "ABCDEFGHJKLMNPQRSTUVWXYZ";
    const minusculas = "abcdefghijkmnopqrstuvwxyz";
    const numeros = "23456789";
    const simbolos = "!@#$%&*";
    const todos = maiusculas + minusculas + numeros + simbolos;

    const valoresAleatorios = new Uint32Array(tamanho);
    window.crypto.getRandomValues(valoresAleatorios);

    const caracteres = [
        maiusculas[valoresAleatorios[0] % maiusculas.length],
        maiusculas[valoresAleatorios[1] % maiusculas.length],
        minusculas[valoresAleatorios[2] % minusculas.length],
        minusculas[valoresAleatorios[3] % minusculas.length],
        numeros[valoresAleatorios[4] % numeros.length],
        numeros[valoresAleatorios[5] % numeros.length],
        simbolos[valoresAleatorios[6] % simbolos.length],
        simbolos[valoresAleatorios[7] % simbolos.length],
    ];

    for (let i = caracteres.length; i < tamanho; i++) {
        caracteres.push(todos[valoresAleatorios[i] % todos.length]);
    }

    // Embaralha os caracteres
    const indices = new Uint32Array(caracteres.length);
    window.crypto.getRandomValues(indices);
    for (let i = caracteres.length - 1; i > 0; i--) {
        const j = indices[i] % (i + 1);
        [caracteres[i], caracteres[j]] = [caracteres[j], caracteres[i]];
    }

    return caracteres.join("");
}

function exibirSenhaTemporariaGerada() {
    const novaSenha = gerarSenhaTemporaria(8);
    campoSenha.value = novaSenha;
    campoSenha.disabled = false;
    secaoSenhaTemporaria.hidden = false;
    btnCopiarSenha.disabled = false;
}

btnCopiarSenha.addEventListener("click", async () => {
    if (!campoSenha.value) return;

    try {
        await navigator.clipboard.writeText(campoSenha.value);
        const conteudoOriginal = btnCopiarSenha.innerHTML;
        btnCopiarSenha.innerHTML = '<i class="fa-solid fa-check"></i>';
        exibirNotificacao("Senha temporária copiada.", "sucesso");

        setTimeout(() => {
            btnCopiarSenha.innerHTML = conteudoOriginal;
        }, 2000);
    } catch {
        campoSenha.select();
        exibirNotificacao(
            "Selecione e copie a senha exibida no campo.",
            "info",
        );
    }
});

btnsDetalharUsuario.forEach((button) => {
    button.addEventListener("click", async () => {
        const usuarioId = button.dataset.usuarioId;
        const response = await fetch(`/dashboard/usuarios/${usuarioId}/`);

        if (response.redirected && response.url.includes("/entrar/")) {
            window.location.href = response.url;
            return;
        }

        const dados = await response.json();

        if (!response.ok) {
            exibirNotificacao(
                dados.mensagem ||
                    "Não foi possível carregar os dados do usuário.",
                "erro",
            );
            return;
        }

        detalharUsuario(dados);
    });
});

btnEditarUsuario.addEventListener("click", () => {
    habilitarEdicaoFormulario(modalUsuario);
    btnRedefinirSenha.disabled = false;
    tituloModalUsuario.textContent = "Editando dados do usuário";
});

btnRedefinirSenha.addEventListener("click", () => {
    habilitarEdicaoFormulario(modalUsuario);
    tituloModalUsuario.textContent = "Editando dados do usuário";
    exibirSenhaTemporariaGerada();
    exibirNotificacao("Senha temporária gerada, salve para confirmar.", "info");
});

btnNovoUsuario.addEventListener("click", () => {
    btnExcluirUsuario.disabled = true;
    btnExcluirUsuario.hidden = true;
    btnRedefinirSenha.hidden = true;
    formNovoCadastro(modalUsuario, "Cadastrar novo usuário");
    campoAtivo.checked = true;
    exibirSenhaTemporariaGerada();
});

btnFecharUsuario.addEventListener("click", () => modalUsuario.close());

function detalharUsuario(usuario) {
    preencherFormularioUsuario(usuario);
    tituloModalUsuario.textContent = "Dados do usuário";
    subtituloModalUsuario.textContent = "Código: " + usuario.usuario_id;
    formUsuario.classList.remove("com-erro");

    secaoSenhaTemporaria.hidden = true;
    campoSenha.value = "";
    btnRedefinirSenha.hidden = false;
    btnRedefinirSenha.disabled = false;

    desabilitarEdicaoFormulario(modalUsuario);
    btnRedefinirSenha.disabled = false;
    btnExcluirUsuario.hidden = false;
    btnExcluirUsuario.disabled = false;
    btnExcluirUsuario.dataset.usuarioId = usuario.usuario_id;

    modalUsuario.showModal();
}

function preencherFormularioUsuario(usuario) {
    document.getElementById("usuario_id").value = usuario.usuario_id || "";
    document.getElementById("nome").value = usuario.nome || "";
    document.getElementById("username").value = usuario.username || "";
    document.getElementById("email").value = usuario.email || "";
    campoIsStaff.checked = Boolean(usuario.is_staff);
    campoAtivo.checked = Boolean(usuario.ativo);
    campoSenha.value = "";

    const data = converterDataHora(usuario.data_cadastro);
    document.getElementById("data_cadastro").textContent = data
        .split(", ")
        .join(" - ");
}

btnExcluirUsuario.addEventListener("click", async () => {
    const usuarioId = btnExcluirUsuario.dataset.usuarioId;

    await excluirRegistro({
        modal: modalUsuario,
        mensagemConfirmacao: "Tem certeza que deseja excluir este usuário?",
        url: "/dashboard/usuarios/excluir/",
        dados: {
            usuario_id: usuarioId,
        },
        aoExcluir: (resultado) => {
            modalUsuario.close();
            exibirNotificacaoComReload(resultado.mensagem, "sucesso");
        },
    });
});

formUsuario.addEventListener("submit", async (event) => {
    event.preventDefault();
    const conteudoOriginalBotao = btnSalvarUsuario.innerHTML;

    try {
        formUsuario.classList.remove("com-erro");
        checarFormulario(formUsuario);

        btnSalvarUsuario.disabled = true;
        btnSalvarUsuario.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin"></i> Salvando...';

        const url = "/dashboard/usuarios/salvar/";
        const formData = new FormData(formUsuario);
        const dados = await salvarCadastro(url, formData);

        if (!dados) return;

        modalUsuario.close();
        exibirNotificacaoComReload(dados.mensagem, "sucesso");
    } catch (erro) {
        btnSalvarUsuario.disabled = false;
        exibirNotificacao(erro.message, "erro");
    } finally {
        btnSalvarUsuario.innerHTML = conteudoOriginalBotao;
    }
});
